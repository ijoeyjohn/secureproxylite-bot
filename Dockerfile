# ********************** Config to Create Docker Image ******************

# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies (executes on Build time)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files to container
COPY . .

# Run the bot (executes on Docker Run/Restart)
CMD ["python", "bot.py"]

# ********************** Config to Create Docker Image ******************
