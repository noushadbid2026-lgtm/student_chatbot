# 📚 StudyBot — Mini ChatGPT-Style Chatbot for Students

A beginner-friendly AI chatbot web app built with Python, FastAPI, HTML, and CSS.
It answers questions using **Wikipedia** and **Hugging Face BART summarization**.

---

## 📁 Project Folder Structure

```
student_chatbot/
│
├── main.py                  ← Backend server (Python + FastAPI)
│
├── requirements.txt         ← List of Python packages to install
│
├── templates/
│   └── index.html           ← The chatbot web page (HTML)
│
└── static/
    └── css/
        └── style.css        ← Visual design (CSS)
```

---

## 🗂️ File Explanations

| File | Purpose |
|------|---------|
| `main.py` | The Python backend. Handles all logic: receiving questions, searching Wikipedia, summarizing with Hugging Face, sending back answers. |
| `templates/index.html` | The web page the user sees. Contains the chat layout, input box, and JavaScript for sending messages without page reload. |
| `static/css/style.css` | Makes the chatbot look good. Dark "warm academic" theme with amber highlights. |
| `requirements.txt` | Lists all Python packages needed. Install them all with one command. |

---

## ⚙️ How the Project Works — Step by Step

```
User types question
        ↓
JavaScript sends it to Python backend (/chat)
        ↓
Python searches Wikipedia for the topic
        ↓
    [Wikipedia found?]
       /         \
     YES          NO
      ↓            ↓
  Hugging Face   Simple fallback
  BART model     rule-based answer
  summarizes it
      ↓
Answer + source sent back to browser
        ↓
JavaScript shows the answer as a chat bubble
```

---

## 🛠️ Installation Steps

### 1. Make sure Python is installed
```bash
python --version
# Should show Python 3.9 or higher
```

### 2. Create a virtual environment (recommended)
```bash
# Create it
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (Mac/Linux)
source venv/bin/activate
```

### 3. Install all required packages
```bash
pip install -r requirements.txt
```
> ⚠️ Note: The first time you run the app, Hugging Face will download the BART model (~1.6 GB). This only happens once.

### 4. Run the server
```bash
python main.py
```

### 5. Open your browser
Go to: **http://127.0.0.1:8000**

---

## ▶️ How to Run (Quick Reference)

```bash
# 1. Activate your environment
source venv/bin/activate   # or venv\Scripts\activate on Windows

# 2. Start the server
python main.py

# 3. Visit in browser
# http://127.0.0.1:8000
```

---

## 🖥️ Sample Output

**User asks:** *What is photosynthesis?*

**Bot replies:**
> Photosynthesis is the process by which green plants and some other organisms use sunlight to synthesize nutrients from carbon dioxide and water. It is essential for life on Earth, producing oxygen as a byproduct.
>
> 📌 Source: [Wikipedia + Hugging Face Summary](https://en.wikipedia.org/wiki/Photosynthesis)

---

**User asks:** *Hello!*

**Bot replies:**
> Hello! 👋 I'm your study assistant. Ask me anything about any topic, and I'll do my best to help you!
>
> 📌 StudyBot Response

---

## 🖼️ Screenshot Layout Description

```
┌──────────────────────────────────────────────────┐
│  🤖 StudyBot    Your AI-powered learning...   [Clear Chat] │
├──────────────────────────────────────────────────┤
│                                                  │
│   ┌──────────────────────────────────────┐       │
│   │  📚 Hello, Student! 👋               │       │
│   │  Ask me anything...                  │       │
│   │  [Photosynthesis] [Gravity] [DNA]... │       │
│   └──────────────────────────────────────┘       │
│                                                  │
│                    What is gravity? ◀─ [USER]    │
│                                                  │
│  [BOT] ▶─ Gravity is the force that attracts    │
│            objects with mass toward each other.  │
│            📌 Source: Wikipedia + HuggingFace    │
│                                                  │
├──────────────────────────────────────────────────┤
│  [  Ask me anything, e.g. What is DNA?  ] [Send] │
│         Powered by Wikipedia + Hugging Face      │
└──────────────────────────────────────────────────┘
```

---

## 🧪 10 Example Questions to Test the Chatbot

1. `What is photosynthesis?`
2. `Explain the water cycle`
3. `What is the French Revolution?`
4. `Tell me about the solar system`
5. `What is DNA?`
6. `Explain gravity`
7. `What is machine learning?`
8. `Who was Albert Einstein?`
9. `What is the theory of evolution?`
10. `Tell me about climate change`

---

## 🚀 Suggestions for Future Improvements

| Feature | Idea |
|---------|------|
| **Memory** | Store chat history in a database (SQLite) so it persists after refresh |
| **Better AI** | Use GPT-2 or Llama 2 for open-ended question answering |
| **Voice Input** | Add browser speech recognition so users can speak questions |
| **Subject Filter** | Let users pick a subject (Science, History, Math) |
| **Dark/Light Toggle** | Add a theme toggle button |
| **Typing animation** | Show bot answer word by word like real ChatGPT |
| **Export chat** | Let users download their chat as a .txt file |
| **User login** | Add accounts so each student has a personal history |
| **Quiz mode** | After explaining a topic, ask the student 3 questions |
| **Multilingual** | Add Wikipedia language support for regional languages |

---

## 🐛 Common Errors and Fixes

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| Model download stuck | Check internet connection; first download is ~1.6 GB |
| Port 8000 in use | Change `port=8000` to `port=8001` in `main.py` |
| Wikipedia rate limit | Add `time.sleep(1)` between requests if querying many times |
| Empty answer | Try rephrasing the question more specifically |

---

## 📌 Why JavaScript Was Used (Minimal)

JavaScript was kept to the **absolute minimum**. It is used for only two reasons:
1. **Async fetch**: HTML forms cannot send JSON to a backend and receive a response without reloading the page. `fetch()` handles this smoothly.
2. **Dynamic DOM**: Adding new message bubbles to the chat without a full page reload.

No external JS libraries or frameworks were used. Everything is plain browser JavaScript (~90 lines with comments).

---

Built with ❤️ for students, by students.
