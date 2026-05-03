# 🚀 AI Code Review Platform

Instant, actionable, AI-powered code reviews streamed token-by-token directly to your browser. This platform acts as a **24/7 Senior Software Engineer** that catches bugs, security holes, and performance bottlenecks before your code ever hits production.

## ✨ Why use this?
*   **Instant Feedback**: No more waiting hours or days for a PR review.
*   **Logical Understanding**: Unlike static linters, this understands *context* and *intent*.
*   **Live Streaming**: Watch the review appear word-by-word like a real person is typing it.
*   **Growth Tracking**: Monitor your code quality improvement over time with personal analytics.

---

## 🛠️ Tech Stack
*   **Backend**: FastAPI (Python 3.11), SQLAlchemy (Async)
*   **Frontend**: Vanilla HTML5, CSS3, JavaScript (ES6+)
*   **Database**: PostgreSQL 15 & Redis
*   **AI Engine**: Groq (Llama 3.3 70b Versatile)
*   **Authentication**: GitHub OAuth 2.0 & JWT

---

## 📋 Requirements
The project is fully containerized. You only need:
*   **Docker** and **Docker Compose** installed.
*   A **Groq API Key** (Get one for free at [console.groq.com](https://console.groq.com/)).
*   A **GitHub OAuth App** (Created in your [GitHub Developer Settings](https://github.com/settings/developers)).

---

## 🚀 Quick Start (First Time Setup)

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd ai-code-review
```

### 2. Configure Environment Variables
Copy the example file and fill in your keys:
```bash
cp .env.example .env
```
**Edit `.env` and provide:**
*   `GROQ_API_KEY`: Your gsk_... key.
*   `GITHUB_CLIENT_ID` & `GITHUB_CLIENT_SECRET`: From your GitHub OAuth App.
*   `GITHUB_REDIRECT_URI`: Should be `http://localhost:8000/auth/github/callback`.
*   `SECRET_KEY`: Any secure random string.

### 3. Start the Platform
Run the following command to build and start all services:
```bash
docker compose up --build
```

### 4. Access the App
*   **Frontend**: Open [http://localhost:3000](http://localhost:3000) in your browser.
*   **Backend API Docs**: Explore at [http://localhost:8000/docs](http://localhost:8000/docs).

---

## 🛤️ User Journey
1.  **Landing**: Visit the homepage and click "Sign in with GitHub".
2.  **Authorize**: Login via GitHub (Single Sign-On).
3.  **Dashboard**: View your past reviews and code quality trends.
4.  **New Review**: Paste any code snippet and select the language.
5.  **Review My Code**: Watch as the AI expert identifies [CRITICAL] bugs and [INFO] suggestions in real-time.
6.  **Score**: Get a 0-100 quality score and save it to your history.

---

## 🔒 Security & Performance
*   **Stateless Auth**: Uses JWT (JSON Web Tokens) for secure, scalable session management.
*   **Async Processing**: Built on Python's `asyncio` for non-blocking WebSocket streaming.
*   **CORS Protected**: Restrictive cross-origin policies to prevent unauthorized access.
*   **Zero-Knowledge**: Your GitHub password is never seen or stored by this application.

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
