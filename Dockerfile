FROM python:3.9-slim

# Install essential system utilities including tmux and bash
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    python3-dev \
    libffi-dev \
    tmux \
    bash \
    tini \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install Python dependencies (if any are needed)
# Uncomment and edit as required
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


# Make the main script executable
RUN chmod +x start-ui.sh

# Use tini as entrypoint for better container process management
ENTRYPOINT ["/usr/bin/tini", "--"]
#CMD ["/bin/bash", "/app/script.sh"]


