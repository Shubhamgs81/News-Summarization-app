import os
import streamlit as st
import requests

API_URL = "http://localhost:8000/"

st.title("News Summarization & Sentiment Analysis")
company = st.text_input("Enter Company Name")

fetch_button = st.button("Fetch News")

if fetch_button and company:
    with st.spinner("Fetching and processing news..."):
        response = requests.get(f"{API_URL}news", params={"company": company})
        if response.status_code == 200:
            try:
                news_data = response.json()
            except requests.exceptions.JSONDecodeError:
                st.error("API returned invalid JSON. Check backend logs.")
            hindi_summary = news_data.pop("Audio", "")
            st.json(news_data)
            
            if hindi_summary:
                tts_response = requests.get(f"{API_URL}tts", params={"summary": hindi_summary})
                if tts_response.status_code == 200:
                    st.audio(tts_response.content, format="audio/mp3")  # Play the actual audio file
                else:
                    st.error("Failed to generate Hindi summary audio.")

        else:
            st.error(f"API request failed: {response.status_code}")
