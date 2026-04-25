# ============================================================
# main.py - The Brain of our Chatbot
# This is the backend server that handles all the logic.
# It receives questions from the user and sends back answers.
# ============================================================

# --- Import the tools we need ---

# FastAPI: a modern, easy-to-use web framework for Python
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# wikipedia: a Python library to search and get Wikipedia articles
import wikipedia

# transformers: from Hugging Face, lets us use AI models
from transformers import pipeline

# uvicorn: the server that runs our FastAPI app
import uvicorn

# re: a standard Python library for cleaning text using patterns
import re

# ============================================================
# Step 1: Create the FastAPI app
# ============================================================
app = FastAPI()

# Tell FastAPI where our CSS files live (the "static" folder)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Tell FastAPI where our HTML files live (the "templates" folder)
templates = Jinja2Templates(directory="templates")

# ============================================================
# Step 2: Load the Hugging Face Summarization Model
# We use "facebook/bart-large-cnn" - a popular summarization model.
# It is loaded ONCE when the server starts so it is faster later.
# ============================================================
print("⏳ Loading Hugging Face model... (this may take a moment the first time)")

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

print("✅ Model loaded and ready!")


# ============================================================
# Step 3: Helper Functions
# These are small tools our main code will use.
# ============================================================

def clean_text(text):
    """
    Cleans up messy text by removing extra spaces and newlines.
    'text' is the raw string we want to clean.
    Returns a clean, neat string.
    """
    # Replace multiple whitespace/newlines with a single space
    text = re.sub(r'\s+', ' ', text)
    # Remove leading and trailing spaces
    text = text.strip()
    return text


def search_wikipedia(query):
    """
    Searches Wikipedia for the given query.
    Returns: (summary_text, page_url) if found, or (None, None) if not found.
    """
    try:
        # Set the Wikipedia language to English
        wikipedia.set_lang("en")

        # Search Wikipedia and get a list of possible article titles
        search_results = wikipedia.search(query, results=3)

        # If no results were found, return nothing
        if not search_results:
            return None, None

        # Try the first search result (the most relevant one)
        page = wikipedia.page(search_results[0], auto_suggest=False)

        # Get the first 1500 characters of the article content
        # (We limit it so the AI model doesn't get overwhelmed)
        content = clean_text(page.content[:1500])

        # Return the content and the Wikipedia page URL
        return content, page.url

    except wikipedia.exceptions.DisambiguationError as e:
        # This happens when a query matches many topics (e.g., "Mercury")
        # Try the first option from the disambiguation list
        try:
            page = wikipedia.page(e.options[0], auto_suggest=False)
            content = clean_text(page.content[:1500])
            return content, page.url
        except:
            return None, None

    except wikipedia.exceptions.PageError:
        # This happens when the exact page is not found
        return None, None

    except Exception:
        # Catch any other unexpected errors
        return None, None


def summarize_with_huggingface(text):
    """
    Uses the Hugging Face BART model to summarize a long piece of text.
    'text' should be at least a few sentences long for good results.
    Returns a shorter, clear summary string.
    """
    try:
        # The model needs text that is not too short
        # min_length and max_length control the size of the summary
        result = summarizer(
            text,
            max_length=150,   # Maximum number of words in the summary
            min_length=40,    # Minimum number of words in the summary
            do_sample=False   # Use greedy decoding (more predictable output)
        )

        # The result is a list with one item; we get the summary text from it
        summary = result[0]['summary_text']
        return clean_text(summary)

    except Exception as e:
        # If summarization fails, return a simple error message
        return f"Could not generate a summary. Error: {str(e)}"


def generate_simple_answer(question):
    """
    When Wikipedia has no result, we try to give a helpful fallback answer.
    This uses a simple rule-based approach (no AI) for common question types.
    Returns a string with a simple answer.
    """
    question_lower = question.lower()

    # Greetings
    if any(word in question_lower for word in ["hello", "hi", "hey", "good morning", "good evening"]):
        return "Hello! 👋 I'm your study assistant. Ask me anything about any topic, and I'll do my best to help you!"

    # How are you
    if "how are you" in question_lower:
        return "I'm doing great and ready to help you learn! What topic would you like to explore today?"

    # What is the chatbot
    if any(phrase in question_lower for phrase in ["who are you", "what are you", "your name"]):
        return "I'm StudyBot 🤖, a simple AI chatbot built to help students like you explore topics and get clear answers!"

    # Thank you
    if any(word in question_lower for word in ["thank", "thanks", "thank you"]):
        return "You're welcome! 😊 Feel free to ask me anything else!"

    # Fallback message when nothing matches
    return (
        "Hmm, I couldn't find specific information on that. "
        "Try rephrasing your question, or ask me about a specific topic like "
        "'What is photosynthesis?' or 'Explain gravity'."
    )


# ============================================================
# Step 4: Define the Web Routes (Pages and API Endpoints)
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    This is the HOME route. When a user visits the website,
    this function sends back the main HTML page (index.html).
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat")
async def chat(request: Request):
    """
    This is the CHAT route. It receives the user's question,
    finds an answer, and sends it back as a JSON response.

    The frontend sends: { "question": "What is gravity?" }
    We send back:       { "answer": "...", "source": "...", "source_url": "..." }
    """

    # --- Read the JSON data sent by the user ---
    data = await request.json()
    question = data.get("question", "").strip()

    # If the question is empty, send back an error
    if not question:
        return JSONResponse({
            "answer": "Please type a question first! 😊",
            "source": "System",
            "source_url": ""
        })

    # -------------------------------------------------------
    # LOGIC FLOW:
    # 1. Search Wikipedia for the question
    # 2. If Wikipedia has content → summarize it with Hugging Face
    # 3. If not → use simple fallback answer
    # -------------------------------------------------------

    # Step A: Try Wikipedia first
    wiki_content, wiki_url = search_wikipedia(question)

    if wiki_content:
        # Step B: Summarize the Wikipedia content using Hugging Face BART
        summary = summarize_with_huggingface(wiki_content)

        return JSONResponse({
            "answer": summary,
            "source": "Wikipedia + Hugging Face Summary",
            "source_url": wiki_url
        })

    else:
        # Step C: Wikipedia had no result — use fallback
        fallback_answer = generate_simple_answer(question)

        return JSONResponse({
            "answer": fallback_answer,
            "source": "StudyBot Response",
            "source_url": ""
        })


# ============================================================
# Step 5: Run the Server
# This block runs only when you execute: python main.py
# ============================================================
if __name__ == "__main__":
    print("🚀 Starting StudyBot server...")
    print("📖 Open your browser and go to: http://127.0.0.1:8000")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
