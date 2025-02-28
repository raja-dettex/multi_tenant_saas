# Use an official Python runtime as a base image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements file to install dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the FastAPI application port
EXPOSE 8000

# Run the FastAPI application with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
