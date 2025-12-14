FROM python:3.12-slim

# Install FluidSynth for midi2audio
RUN apt-get update && apt-get install -y fluidsynth && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app
WORKDIR /app
