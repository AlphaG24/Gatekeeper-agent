# Use official Python image
FROM python:3.11-slim

# 1. Install system dependencies for Playwright (The heavy lifting)
RUN apt-get update && apt-get install -y     wget     gnupg     && rm -rf /var/lib/apt/lists/*

# 2. Set working directory
WORKDIR /app

# 3. Copy files
COPY requirements.txt .
COPY src/ src/
COPY deploy_server.py .
COPY .env . 
# NOTE: In real production, never copy .env. 
# But for this hackathon submission, it ensures your key works immediately without complex Secret Manager setup.

# 4. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt fastapi uvicorn

# 5. Install Playwright Browsers
RUN playwright install chromium
RUN playwright install-deps chromium

# 6. Run the server
CMD ["python", "deploy_server.py"]
