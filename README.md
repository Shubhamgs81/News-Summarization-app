# News-Summarization-app
News Summarization and Text-to-Speech Application

### **Overview**
This project is a web-based application that extracts key details from multiple news articles related to a given company, performs sentiment analysis, conducts comparative analysis, and generates Hindi Text-to-Speech (TTS) output.

The application consists of:
- **FastAPI Backend** (`news_api.py`): Handles news extraction, sentiment analysis, topic extraction, and TTS generation.
- **Streamlit Frontend** (`news_tts_app.py`): Provides a user-friendly interface to interact with the API.
- **Google Gemini API**: Used for AI-powered text analysis.

---

## **⚙️ Features**
- Extract news articles from various sources using **NewsAPI**  
- Perform **sentiment analysis** (Positive, Negative, Neutral)  
- Conduct **comparative analysis** of multiple articles  
- Extract key **topics** using NLP  
- Generate **Hindi TTS audio** using `gTTS`  
- Provide a **Streamlit-based UI** for user interaction  
- Deployable on **Hugging Face Spaces**  

---

## **Installation & Setup**
### **1️. Clone the Repository**
```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/news-summarization-app
```

### **2. Clone the Repository**
Set environment variables:
- NEWSAPI_KEY=YOUR_NEWSAPI.ORG_KEY
- GEMINI_API_KEY=YOUR_GEMINI_API_KEY

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Run FastAPI Backend**
```bash
uvicorn news_api:app --host 127.0.0.1 --port 8000
```

### **5. Run Streamlit Frontend**
```bash
streamlit run news_tts_app.py --server.port 7860
```
---

## **API Endpoints** 
| **Method** | **Endpoint** | **Description** |
|------------|-------------|----------------|
| `GET` | `/news?company=Tesla` | Fetches news articles and performs sentiment analysis. |
| `GET` | `/tts?summary=Hindi Text` | Converts text to speech in Hindi and returns an MP3 file. |

---

## **Author** 
👤 Shubham Sontakke  
🔗 GitHub: https://github.com/Shubhamgs81  
🔗 Hugging https://huggingface.co/spaces/shubhamgs  
