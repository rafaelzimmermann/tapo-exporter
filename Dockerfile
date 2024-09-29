FROM python:3.10-slim

WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY . .


# Expose the Prometheus metrics port
# (the default port for Prometheus is 9090, but many apps use 8000 or 9100 for metrics)
EXPOSE 9100

ENV FLASK_APP=src/main.py
ENV TAPO_USERNAME="tplink_username"
ENV TAPO_PASSWORD="tplink_password"
ENV TAPO_ADDRESS="192.168.1.0/24"

# Run the Flask application
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=9100"]