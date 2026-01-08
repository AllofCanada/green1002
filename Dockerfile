# 1. Use the python slim image (good for production size)
FROM python:3.9-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy requirements and install
COPY /docker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the application code
COPY /docker .

# 5. Expose the port (we stick to 5000, the load balancer will handle port 80)
EXPOSE 5003

# 6. CMD - THE IMPORTANT CHANGE
# Syntax: gunicorn -b [IP]:[PORT] [filename]:[flask_variable_name]
CMD ["gunicorn", "-b", "0.0.0.0:5003", "server:app"]