# Use an official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app code
COPY . /app

# Expose port 8000 for FastAPI
EXPOSE 8000

# Run the FastAPI app using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
