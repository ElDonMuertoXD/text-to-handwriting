FROM python:3.11-slim

# Install system dependencies including X11 for GUI support
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    libgl1-mesa-dev \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgstreamer1.0-0 \
    libgstreamer-plugins-base1.0-0 \
    xvfb \
    x11-utils \
    xauth \
    libx11-dev \
    libxrandr2 \
    libxss1 \
    libxcursor1 \
    libxcomposite1 \
    libasound2 \
    libxi6 \
    libxtst6 \
    python3-tk \
    python3-dev \
    vim-common \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files
COPY . .

# Install Python dependencies using uv
RUN uv venv && \
    . .venv/bin/activate && \
    uv add pywhatkit pillow pytesseract reportlab fpdf2

# Create output directory
RUN mkdir -p /app/output

# Set environment variables
ENV PYTHONPATH=/app
ENV PATH="/app/.venv/bin:$PATH"
ENV DISPLAY=:99

# Create a startup script with proper X11 auth
RUN echo '#!/bin/bash\n\
# Create Xauthority file with proper auth\n\
touch /root/.Xauthority\n\
xauth add :99 . $(xxd -l 16 -p /dev/urandom)\n\
# Start Xvfb\n\
Xvfb :99 -screen 0 1024x768x24 -auth /root/.Xauthority > /dev/null 2>&1 &\n\
sleep 2\n\
exec "$@"' > /entrypoint.sh && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

# Command to run the application
CMD ["python", "src/main.py"]