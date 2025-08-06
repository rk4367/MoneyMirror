# MoneyMirror – Household Income & Expense Tracker with Bank Matching

## 🎯 Project Overview
MoneyMirror is a comprehensive, full-stack, real-time, responsive web application for managing household finances. It allows users to log daily income/expenses, upload bank statements (CSV/PDF), automatically match records, receive alerts, and view insightful reports—all in one place.

## ✨ Features

### 🔐 Authentication & Security
- **Firebase Authentication**: Secure email/password login system
- **User-specific data**: Each user's data is isolated and secure
- **Environment-based configuration**: Secure API key management

### 📊 Dashboard & Analytics
- **Real-time dashboard**: Live balance, income, expenses, and summaries
- **Visual analytics**: Charts and graphs for financial insights
- **Period-based summaries**: Today, weekly, and monthly views

### 💰 Transaction Management
- **Income/Expense Entry**: Add, edit, delete, filter, and sort entries
- **Category management**: Organize transactions by categories
- **Transaction history**: Complete audit trail of all financial activities

### 🏦 Bank Statement Integration
- **Multi-format support**: Upload CSV and PDF bank statements
- **Automatic parsing**: Intelligent extraction of transaction data
- **Smart matching**: Compare bank records with manual entries
- **Status tracking**: Color-coded matching status (matched, duplicate, missing)

### 📈 Reports & Export
- **Financial reports**: Comprehensive spending analysis
- **Export functionality**: Download reports in CSV format
- **Visual charts**: Pie charts, bar charts, and trend analysis

### 🔔 Alerts & Notifications
- **Real-time alerts**: Notifications for mismatches, duplicates, and large entries
- **Smart recommendations**: Actionable insights for financial management

### 📱 Responsive Design
- **Mobile-first**: Optimized for all device sizes
- **Modern UI**: Clean, intuitive interface with Tailwind CSS
- **Accessibility**: WCAG compliant design patterns

---

## 🛠️ Tech Stack

### Frontend
- **React 18**: Modern React with hooks and functional components
- **Vite**: Fast build tool and development server
- **Tailwind CSS**: Utility-first CSS framework
- **React Router**: Client-side routing
- **React Query**: Server state management
- **Chart.js**: Data visualization
- **PapaParse**: CSV parsing library
- **Lucide React**: Modern icon library

### Backend
- **Python 3.8+**: Modern Python with type hints
- **Flask**: Lightweight web framework
- **Flask-CORS**: Cross-origin resource sharing
- **pdfplumber**: PDF text extraction library
- **python-dotenv**: Environment variable management

### Database & Authentication
- **Firebase Authentication**: Secure user authentication
- **Firestore**: NoSQL cloud database
- **Real-time listeners**: Live data synchronization

### Development Tools
- **ESLint**: Code linting and formatting
- **PostCSS**: CSS processing
- **Autoprefixer**: CSS vendor prefixing

---

## 🚀 Features
- **User Authentication:** Email/password login (Firebase Auth)
- **Real-Time Dashboard:** Live balance, income, expenses, summaries
- **Income/Expense Entry:** Add, edit, delete, filter, and sort entries
- **Bank Statement Upload:** Upload CSV/PDF, auto-parse and match with entries
- **Matching Logic:** Detect matched, duplicate, and missing records (color-coded)
- **Alerts:** Real-time notifications for mismatches, duplicates, large entries
- **Reports & Charts:** Visualize data (Chart.js), export to CSV/PDF
- **Responsive UI:** Mobile-first, color-coded, intuitive navigation

---

## ⚡ Quick Start

### Prerequisites
- **Node.js 18+** and **npm 8+**
- **Python 3.8+** and **pip**
- **Firebase account** for authentication and database

### 1. **Clone the Repository**
```bash
git clone <your-repo-url>
cd MoneyMirror
```

### 2. **Environment Setup**
```bash
# Copy environment template
cp env.example .env

# Edit .env with your Firebase configuration
# See Firebase Configuration section below
  ```

### 3. **Frontend Setup**
```bash
# Install dependencies
npm install

# Start development server
npm run dev
```
- Frontend runs at [http://localhost:5173](http://localhost:5173)

### 4. **Backend Setup**
```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Start Flask server
python app.py
```
- Backend API runs at [http://localhost:5000](http://localhost:5000)
- Health check: [http://localhost:5000/api/health](http://localhost:5000/api/health)

### 5. **Firebase Configuration**

#### Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or select existing one
3. Enable **Authentication** with Email/Password provider
4. Create **Firestore Database** in test mode

#### Configure Environment Variables
Edit your `.env` file with Firebase configuration:
```env
VITE_FIREBASE_API_KEY=your_api_key_here
VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your_project_id
VITE_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=123456789
VITE_FIREBASE_APP_ID=1:123456789:web:abcdef123456
```

#### Firestore Security Rules
Set up Firestore security rules:
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /entries/{document} {
      allow read, write: if request.auth != null && request.auth.uid == resource.data.uid;
    }
  }
}
```

---

## 🏦 **Bank Statement Upload & Matching**
- Upload `.csv` (parsed in browser) or `.pdf` (sent to backend for parsing)
- Matching logic compares date, amount, and description
- Color-coded results:
  - ✅ Matched (Green)
  - ⚠️ Duplicate (Yellow)
  - ❌ Missing (Red)

---

## 📊 **Reports & Charts**
- Pie, bar, and line charts (Chart.js)
- Export to CSV (PDF export coming soon)

---

## 🔔 **Alerts**
- Real-time alerts for mismatches, duplicates, and large entries

---

## 📱 **Responsive UI**
- Mobile-first, color-coded, sidebar/topbar navigation

---

## 🛡️ **Deployment**

### **Frontend (Vercel/Netlify):**
- Push to GitHub, connect repo to Vercel/Netlify, set build command: `npm run build`, output: `dist`
- Set environment variables for Firebase if needed

### **Backend (Render/Heroku):**
- Deploy `backend/` as a Python web service
- Set start command: `python app.py`
- Ensure CORS is enabled if frontend and backend are on different domains

---

## 📝 **Customization & Extending**
- Add advanced matching logic in `backend/app.py`
- Add email notifications (Flask + SMTP or 3rd party)
- Add more charts or export options

---

## 🤝 **Contributing**
Pull requests welcome! Please open issues for bugs/feature requests.
