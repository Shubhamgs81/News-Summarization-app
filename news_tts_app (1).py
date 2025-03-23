import os

import streamlit as st
import requests


if __name__ == "__main__":
    # Define API base URL (Update for Hugging Face deployment)
    API_URL = "http://localhost:8000/"

    # Streamlit UI Title
    st.title("News Summarization & Sentiment Analysis")

    # User input field for company name
    company = st.text_input("Enter Company Name")

    # Initialize button state
    if "fetch_disabled" not in st.session_state:
        st.session_state["fetch_disabled"] = False

    # Fetch News button
    fetch_button = st.button("Fetch News", disabled=st.session_state["fetch_disabled"])

    if fetch_button and company:
        st.session_state["fetch_disabled"] = True  # Disable button while processing
        with st.spinner("Fetching and processing news..."):
            try:
                # Request news data from FastAPI backend
                response = requests.get(f"{API_URL}news", params={"company": company})
                if response.status_code == 200:
                    news_data = response.json()
                    hindi_summary = news_data.pop("Audio", "")  # Extract Hindi summary
                    st.json(news_data)  # Display structured JSON output

                    # Request Text-to-Speech conversion
                    if hindi_summary:
                        tts_response = requests.get(
                            f"{API_URL}tts", params={"summary": hindi_summary}
                        )
                        if tts_response.status_code == 200:
                            st.audio(tts_response.content, format="audio/mp3")
                        else:
                            st.error("Failed to generate Hindi summary audio.")
                else:
                    st.error(f"API request failed: {response.status_code}")

            except requests.exceptions.RequestException as e:
                st.error(f"API connection error: {e}")

            finally:
                st.session_state["fetch_disabled"] = False  # Re-enable button

