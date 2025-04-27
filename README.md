
# 🧠 Quiz Creator Web App

A full-stack quiz platform that allows users to **create**, **select**, and **take quizzes** in a seamless experience.  
Built with **React + Vite** on the frontend and **FastAPI** on the backend, this app supports real-time quiz creation, 
multiple-choice questions, and result tracking — all in a clean, responsive interface.

🔗 **Live Demo**: [quiz-creator-v2.netlify.app](https://quiz-creator-v2.netlify.app/)

![React](https://img.shields.io/badge/Frontend-React-blue)
![Vite](https://img.shields.io/badge/Build-Vite-purple)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green)
![MongoDB](https://img.shields.io/badge/Database-MongoDB-lightgreen)
![Deployed-Netlify](https://img.shields.io/badge/Deployed%20on-Netlify-brightgreen)


## 🚀 Features

- 📋 Create custom quizzes with multiple questions
- ✅ Each question supports multiple choices (A–D) and a correct answer
- 🎯 Take quizzes interactively with real-time feedback
- 📊 View results after each quiz
- 💡 Loading, error, and empty states for a polished UX
- 🌀 Now with SHUFFLE feature for questions and choices!


## 🛠 Tech Stack

**Frontend:**
- React + Vite
- TailwindCSS
- Deployed via **Netlify**

**Backend:**
- FastAPI
- MongoDB
- Deployed via **Render**


## 🛠️ Local Development Setup

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 10000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```
- Ensure MongoDB is running (locally or on Atlas).
- Update the API URL in the frontend if necessary (e.g., via `.env` file).


## 🚧 Known Issues / Future Improvements

- Add user authentication (login/signup)
- Add quiz timer / countdown feature
- Create leaderboard for top scorers
- Enhance mobile responsiveness
- Improve error messages and handling for a better user experience


## 📷 Screenshots

![image](https://github.com/user-attachments/assets/78c2e74a-631f-49b6-8e9c-143f05bb0a5e)
![image](https://github.com/user-attachments/assets/63bfd273-e089-4c66-a532-04fb594873ab)

> [Originally built for a school assignment]
