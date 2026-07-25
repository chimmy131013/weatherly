# Use Python official image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Tell Docker that the app uses port 5000
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]