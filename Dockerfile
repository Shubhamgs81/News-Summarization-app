# Use a lightweight Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy all files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose correct ports
EXPOSE 8000 7860

# Start FastAPI first and keep it running, then launch Streamlit
CMD uvicorn news_api:app --host 0.0.0.0 --port 8000 & streamlit run news_tts_app.py --server.port 7860 --server.address 0.0.0.0
