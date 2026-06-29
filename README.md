# 📄 AI Resume Builder

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Gemini](https://img.shields.io/badge/Gemini%20API-4285F4?style=for-the-badge&logo=google&logoColor=white)

**A full-stack AI-powered resume builder — because your resume should be as impressive as you are.**

</div>

---

## 🎯 What is This?

A full-stack web app that helps you build professional resumes with AI assistance. The **Flask backend** handles AI generation via Google's Gemini API, while the **React frontend** delivers a smooth, interactive editing experience. Enter your experience, skills, and goals — Gemini does the writing.

## ✨ Features

- 🤖 **AI-powered content** — Gemini API generates bullet points, summaries, and descriptions
- ⚛️ **React frontend** — responsive, clean UI with real-time editing
- 🐍 **Flask backend** — lightweight REST API
- 📋 **Structured output** — properly formatted resume sections
- 🎨 **Multiple templates** — choose your style

## 🏗️ Architecture

```
React Frontend (apps/)
      │  HTTP requests
      ▼
Flask Backend (app/)
      │
      ▼
Gemini API ──► AI-generated content
```

## 🚀 Run Locally

```bash
git clone https://github.com/bhavnaa22/resume-builder
cd resume-builder

# Backend
pip install -r requirements.txt
python run.py

# Frontend (in another terminal)
cd apps/Frontend_react
npm install && npm start
```

Set your Gemini API key:
```bash
export GEMINI_API_KEY=your_key_here
```

## 📁 Project Structure

```
resume-builder/
├── app/
│   ├── __init__.py
│   └── config.py           # Flask config & Gemini setup
├── apps/
│   └── Frontend_react/     # React frontend
├── run.py                  # Flask entry point
├── test_gemini.py          # API integration tests
├── requirements.txt
└── README.md
```

## 🔧 Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | React |
| Backend | Flask |
| AI | Google Gemini API |
| Language | Python 3.10+, JavaScript |
