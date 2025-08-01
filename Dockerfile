# Use official Python image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Copy requirements file first to install dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install flask requests python-dotenv pymysql cryptography


# Copy the rest of the code
COPY apidata.py /app/apidata.py


# Expose the port Flask will run on
EXPOSE 5000

# Run Flask app
CMD ["python", "apidata.py"]
