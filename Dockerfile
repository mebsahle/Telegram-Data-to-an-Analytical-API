FROM python:3.10-slim

# Install OpenCV dependency (required for YOLO)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0


# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

CMD ["bash"]
