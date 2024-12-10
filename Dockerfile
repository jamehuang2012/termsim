# Use an official Python image as a base
FROM python:3.9-slim

# Install system dependencies including tmux, tini, apt-utils, and build tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    python3-dev \
    libffi-dev \
    tmux \
    bash \
    tini \
    apt-utils && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir \
    aiofile==3.9.0 \
    flask==3.0.3 \
    markdown-it-py==3.0.0 \
    MarkupSafe==2.1.5 \
    numpy==1.24.4 \
    pillow==10.4.0 \
    posix-ipc==1.1.1 \
    requests==2.22.0 \
    rich==13.9.4 \
    textual==0.87.1 \
    python-dateutil==2.8.2

# Make the start_ui.sh script executable
RUN chmod +x start-ui.sh

# Set tini as the entrypoint and start the script
ENTRYPOINT ["/usr/bin/tini", "--"]
#CMD ["/bin/bash", "./start_ui.sh"]

