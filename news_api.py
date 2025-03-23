from fastapi import FastAPI, Query
import requests
import json
import os
from bs4 import BeautifulSoup
from gtts import gTTS
import tempfile
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi.responses import JSONResponse, FileResponse

# Load environment variables
load_dotenv()
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI()

def fetch_news(company):
    url = f'https://newsapi.org/v2/everything?q={company}&apiKey={NEWSAPI_KEY}'
    response = requests.get(url)
    articles = response.json().get('articles', [])[:10]
    
    if not articles:
        return {"error": "No articles found for this company."}
    
    article_data = [
        {
            "Title": article.get('title', 'No Title'),
            "URL": article.get('url', ''),
            "Content": scrape_article(article.get('url', ''))
        }
        for article in articles
    ]
    
    return gemini_analyze_articles(company, article_data)

def scrape_article(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        content = ' '.join([p.get_text() for p in paragraphs])
        return content[:1000]  # Limit to 1000 characters
    except:
        return "Content not available"

def gemini_analyze_articles(company, articles):
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    prompt = f"""
    Analyze the following news articles related to {company}. Extract:
    - Summary
    - Sentiment (Positive, Negative, Neutral)
    - Key Topics
    - Comparative Analysis
    - Final Sentiment Conclusion
    - Hindi Text-to-Speech summary
    
    Return the result in the following JSON format:
    {{
        "Company": "{company}",
        "Articles": [
            {{"Title": "Title 1", "Summary": "...", "Sentiment": "...", "Topics": ["..."]}},
            {{"Title": "Title 2", "Summary": "...", "Sentiment": "...", "Topics": ["..."]}}
        ],
        "Comparative Sentiment Score": {{
            "Sentiment Distribution": {{"Positive": X, "Negative": Y, "Neutral": Z}},
            "Coverage Differences": [{{"Comparison": "...", "Impact": "..."}}],
            "Topic Overlap": {{"Common Topics": [...], "Unique Topics": [...]}}
        }},
        "Final Sentiment Analysis": "Overall sentiment summary",
        "Audio": "Hindi summary in short 2-3 paragraphs"
    }}
    
    Articles:
    {json.dumps(articles, indent=2)}
    """
    
    response = model.generate_content(prompt)
    response_text = response.text.strip("```json\n").strip("```")
    
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        return {"error": "Failed to parse Gemini response"}

@app.get("/")
def read_root():
    return {"message": "FastAPI is running"}
    
@app.get("/news")
def get_news(company: str = Query(..., description="Company name")):
    news_data = fetch_news(company)
    return JSONResponse(content=news_data)

@app.get("/tts")
def generate_tts(summary: str = Query(..., description="Hindi text summary")):
    try:
        tts = gTTS(text=summary, lang='hi')
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        audio_path = temp_audio.name
        tts.save(audio_path)

        return FileResponse(audio_path, media_type="audio/mpeg", filename="summary.mp3")
    except Exception as e:
        return JSONResponse(content={"error": str(e)})

