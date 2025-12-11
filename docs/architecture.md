# AI Mock Interview Platform – System Architecture

## 1. Overview
Short description of what the system does.

## 2. Tech Stack
- Frontend: React (Vite)
- Backend: FastAPI
- Database: MongoDB
- AI: Gemini API
- Others: Web Speech API (for STT), Tailwind CSS (for UI)

## 3. High-Level Architecture

The system is divided into four main layers:

1. **Client (Frontend)**
   - Built with React.
   - Allows user to select role, attend mock interview, and view feedback.
   - Sends HTTP requests to backend to start interview, submit answers, and fetch results.

2. **Backend API (FastAPI)**
   - Exposes REST API endpoints:
     - `/start-interview`
     - `/submit-answer`
     - `/final-feedback`
   - Stores and retrieves data from MongoDB.
   - Orchestrates calls to the AI services.

3. **AI Services (Gemini API)**
   - Question Generator:
     - Generates role-specific interview questions.
   - Answer Evaluator:
     - Scores each answer on communication, technical correctness, and confidence.
   - Improvement Plan Generator:
     - Produces final feedback and learning recommendations.

4. **Database (MongoDB)**
   - Stores users, interview sessions, and individual question-answer records.


## 4. Data Flow (Interview Flow)
Step-by-step: user starts interview → questions → answers → evaluation → feedback.

## 5. API Design
List of core APIs: /start-interview, /submit-answer, /final-feedback.

## 6. AI Integration
Explain how you call the AI model for:
- Question generation
- Answer evaluation
- Final improvement plan

## 7. Deployment Plan (Optional)
How you'd deploy (Render, Vercel, etc.).
