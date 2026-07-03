# QuensultingAI Dental Receptionist 🦷🎙️

An intelligent, ultra-low latency voice AI receptionist built for dental clinics. This agent handles incoming phone calls, answers FAQs using a RAG-based knowledge base, checks real-time slot availability, books appointments, and gracefully handles emergencies by transferring calls to human staff.

## 🌟 Features

- **Conversational Voice AI**: Powered by Retell AI for natural, human-like phone interactions with dynamic conversation flows.
- **Real-time Availability**: Checks existing bookings and dynamically suggests alternative time slots if a requested time is unavailable.
- **Automated Booking System**: Directly inserts confirmed appointments and patient details into a Google Sheet.
- **Instant Notifications**: Dispatches automated email confirmations to patients (and internal clinic staff) via the Resend API upon successful booking.
- **Emergency & Fallback Handling**: Automatically detects medical emergencies (pain, swelling, bleeding) and routes calls directly to human staff. Logs callback requests if the front desk is busy.
- **Robust Engineering**: Implements idempotency keys to prevent duplicate bookings during LLM self-corrections or network retries.

## 🏗️ Architecture Stack

- **Voice Engine**: Retell AI (Conversation Flow Nodes + Custom Functions Webhooks)
- **Backend Framework**: FastAPI (Python)
- **Database**: Google Sheets API (via `gspread`)
- **Email Service**: Resend API
- **Deployment**: Render (Infrastructure as Code via `render.yaml`)

## 🚀 Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/SanatanSinghVishen/DentalAI.git
cd DentalAI
```

### 2. Install dependencies
Ensure you have Python 3.10+ installed.
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory and configure the following secrets:
```env
# Retell AI Security
RETELL_API_KEY=your_retell_key

# Google Sheets Integration
GOOGLE_SERVICE_ACCOUNT_JSON={"type": "service_account", ...}
GOOGLE_SHEET_ID=your_google_sheet_id

# Email Notifications (Resend)
RESEND_API_KEY=your_resend_key
CLINIC_FROM_EMAIL=onboarding@resend.dev
CLINIC_NOTIFY_EMAIL=your_email@example.com
```

### 4. Run the server
```bash
uvicorn app.main:app --reload
```
Your backend webhook server will now be running locally on `http://localhost:8000`.

## 🌐 Deployment
This project is configured for one-click deployment on **Render**. The included `render.yaml` file automatically provisions the web service, installs dependencies, and runs the Uvicorn server in production mode.

## 📂 Project Structure
- `/app/routers/` - FastAPI endpoints acting as webhook targets for Retell AI Custom Functions.
- `/app/services/` - Core business logic (Google Sheets API, Email dispatching, Availability logic, Idempotency tracking).
- `/app/models/` - Pydantic schemas enforcing strict payload validation for the LLM.
- `/app/core/` - Request authentication, API security, and environment configuration.
