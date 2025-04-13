FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create templates directory if not exists
RUN mkdir -p templates

# Expose the port the app runs on
EXPOSE 5008

# Command to run the application
CMD ["python", "flask_app.py"] 