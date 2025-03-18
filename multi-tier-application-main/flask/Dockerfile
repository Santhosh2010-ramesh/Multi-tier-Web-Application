# Use official Python 3.8 image
FROM python:3.8

# Set working directory
WORKDIR /app

# Copy application files
COPY app.py .
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the Flask application
CMD ["python", "app.py"]
