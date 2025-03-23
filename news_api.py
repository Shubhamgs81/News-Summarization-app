import os
import json
import tempfile
import requests
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
from bs4 import BeautifulSoup
from gtts import gTTS
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Initialize FastAPI app
app = FastAPI()


def scrape_article(url: str) -> str:
    """Extracts text content from a given news article URL."""
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        content = " ".join([p.get_text() for p in paragraphs])
        return content[:1000]  # Limit content to 1000 characters
    except requests.RequestException:
        return "Content not available"


def gemini_analyze_articles(company: str, articles: list) -> dict:
    """
    Analyze news articles using Google Gemini AI.

    Extracts summary, sentiment analysis, key topics,
    comparative evaluation, and Hindi TTS summary.
    """
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = (
        f"Analyze the following news articles related to {company}. Extract:\n"
        "- Summary\n"
        "- Sentiment (Positive, Negative, Neutral)\n"
        "- Key Topics\n"
        "- Comparative Analysis\n"
        "- Final Sentiment Conclusion\n"
        "- Hindi Text-to-Speech summary\n\n"
        "Return the result in the following JSON format:\n"
        "{\n"
        f'    "Company": "{company}",\n'
        '    "Articles": [\n'
        '        {"Title": "Title 1", "Summary": "...", "Sentiment": "...", "Topics": ["..."]},\n'
        '        {"Title": "Title 2", "Summary": "...", "Sentiment": "...", "Topics": ["..."]}\n'
        "    ],\n"
        '    "Comparative Sentiment Score": {\n'
        '        "Sentiment Distribution": {"Positive": X, "Negative": Y, "Neutral": Z},\n'
        '        "Coverage Differences": [{"Comparison": "...", "Impact": "..."}],\n'
        '        "Topic Overlap": {"Common Topics": [...], "Unique Topics": [...]}'
        "    },\n"
        '    "Final Sentiment Analysis": "Overall sentiment summary",\n'
        '    "Audio": "Hindi summary in short 2-3 paragraphs"\n'
        "}\n\n"
        f"Articles:\n{json.dumps(articles, indent=2)}"
    )
    response = model.generate_content(prompt)

    try:
        return json.loads(response.text.strip("```json\n").strip("```"))
    except json.JSONDecodeError:
        return {"error": "Failed to parse Gemini response"}


@app.get("/news")
def fetch_news(company: str = Query(..., description="Company name for news extraction")):
    """
    Fetches news articles for a company, extracts content,
    and performs AI-based sentiment analysis.
    """
    url = f"https://newsapi.org/v2/everything?q={company}&apiKey={NEWSAPI_KEY}"
    response = requests.get(url)
    articles = response.json().get("articles", [])[:10]  # Limit to 10 articles

    if not articles:
        return JSONResponse(
            content={"error": "No articles found for this company."}, status_code=404
        )

    article_data = [
        {
            "Title": article.get("title", "No Title"),
            "URL": article.get("url", ""),
            "Content": scrape_article(article.get("url", ""))
        }
        for article in articles
    ]

    return gemini_analyze_articles(company, article_data)


@app.get("/tts")
def generate_tts(summary: str = Query(..., description="Hindi text summary")):
    """
    Converts a Hindi text summary to speech and returns an MP3 file.
    """
    try:
        tts = gTTS(text=summary, lang="hi")
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        audio_path = temp_audio.name
        tts.save(audio_path)
        return FileResponse(audio_path, media_type="audio/mpeg", filename="summary.mp3")
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# End of script
