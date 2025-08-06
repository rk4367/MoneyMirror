from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import pdfplumber
import tempfile
import os
import logging
from datetime import datetime
from werkzeug.exceptions import HTTPException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

@app.route('/api/parse-pdf', methods=['POST'])
def parse_pdf():
    """Parse PDF bank statements and extract transaction data"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename or not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Only PDF files are supported'}), 400

        logger.info(f"Processing PDF file: {file.filename}")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            file.save(tmp)
            tmp_path = tmp.name

        entries = []
        try:
            with pdfplumber.open(tmp_path) as pdf:
                logger.info(f"PDF has {len(pdf.pages)} pages")
                
                for page_num, page in enumerate(pdf.pages):
                    table = page.extract_table()
                    if not table or len(table) < 2:
                        logger.info(f"No table found on page {page_num + 1}, trying to extract text lines.")
                        # Try to extract lines of text and parse heuristically
                        lines = page.extract_text().split('\n') if page.extract_text() else []
                        for line in lines:
                            # Heuristic: look for lines with date, description, amount, type
                            # (very basic, can be improved for specific bank formats)
                            parts = [p.strip() for p in line.split('  ') if p.strip()]
                            if len(parts) >= 4:
                                date, description, amount, type_ = parts[:4]
                                try:
                                    amount_val = float(amount.replace(',', ''))
                                except Exception:
                                    continue
                                if date and description and amount:
                                    entries.append({
                                        'date': date,
                                        'description': description,
                                        'amount': amount_val,
                                        'type': type_
                                    })
                        continue  # Move to next page
                    headers = [h.strip().lower() if h else "" for h in table[0]]
                    logger.info(f"Headers found: {headers}")
                    
                    for row in table[1:]:
                        if not row or len(row) != len(headers):
                            continue
                        row_dict = dict(zip(headers, row))
                        date = (row_dict.get('date') or '').strip()
                        description = (row_dict.get('narration') or row_dict.get('description') or '').strip()
                        withdrawal = (row_dict.get('withdrawal (dr)') or row_dict.get('withdrawal') or '0')
                        deposit = (row_dict.get('deposit (cr)') or row_dict.get('deposit') or '0')
                        try:
                            if withdrawal and withdrawal.strip() and float(withdrawal.replace(',', '')) > 0:
                                amount = float(withdrawal.replace(',', ''))
                                type_ = 'Debit'
                            elif deposit and deposit.strip() and float(deposit.replace(',', '')) > 0:
                                amount = float(deposit.replace(',', ''))
                                type_ = 'Credit'
                            else:
                                amount = 0
                                type_ = ''
                            if date and description and amount:
                                entries.append({
                                    'date': date,
                                    'description': description,
                                    'amount': amount,
                                    'type': type_
                                })
                        except (ValueError, TypeError) as e:
                            logger.warning(f'Error parsing row on page {page_num+1}: {e}')
                            continue
            if not entries:
                return jsonify({'error': 'No valid entries found in PDF. Please check the format. The PDF may not contain a recognizable table or text-based data.'}), 400
            logger.info(f"Successfully extracted {len(entries)} entries")
            return jsonify({'entries': entries, 'count': len(entries)})
            
        except Exception as e:
            logger.error(f'PDF parsing error: {e}')
            return jsonify({'error': f'PDF parsing error: {str(e)}'}), 500
        finally:
            os.remove(tmp_path)
            
    except Exception as e:
        logger.error(f'Unexpected error: {e}')
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.errorhandler(Exception)
def handle_exception(e):
    # Pass through HTTP errors
    if isinstance(e, HTTPException):
        return make_response(jsonify({'error': str(e)}), e.code)
    # Non-HTTP exceptions
    logger.error(f'Unhandled exception: {e}')
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('BACKEND_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'true').lower() == 'true'
    app.run(debug=debug, host='0.0.0.0', port=port)