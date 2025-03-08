 
# Use official Python image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the FastAPI app files into the container
COPY . /app

# Install required dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install -r requirements.txt

# Expose port 8000 for FastAPI
EXPOSE 8000

# Run FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
