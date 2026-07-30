# Lightweight image of Python
FROM python:3.12-slim

# working directory inside the container
WORKDIR /app

# Copying and installation of dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY ./src/main ./src/main

# Port for exposing the API
EXPOSE 8000

# Command to execute the application
CMD ["uvicorn", "src.main.main:app", "--host", "0.0.0.0", "--port", "8000"]