# Chatbot UI Project

## Project Overview

This project sets up a **FastAPI backend** and a **React frontend** to create a chatbot interface. Follow the instructions below to get your development environment running smoothly.

## Prerequisites

- **Python 3.7+**
- **Node.js and npm**

---

## Getting Started

### **Server Setup (FastAPI)**

1. **Create a Virtual Environment**:

   ```bash
   python3 -m venv venv
   ```

2. **Activate the Virtual Environment**:

   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```
   - **Windows**:
     ```bash
     .\venv\Scripts\activate
     ```

3. **Install Required Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   Alternatively, you can manually install the necessary packages:

   ```bash
   pip install fastapi uvicorn pydantic sqlalchemy
   ```

4. **Start the FastAPI Server**:
   ```bash
   uvicorn app.main:app --reload
   ```
   The server will run at: `http://127.0.0.1:8000`

### **Client Setup (React)**

1. **Install Required Packages**:
   Navigate to Client

   ```bash
   npm install
   ```

2. **Start the React Development Server**:
   ```bash
   npm run dev
   ```
   The frontend will run at: `http://localhost:3175`

---
