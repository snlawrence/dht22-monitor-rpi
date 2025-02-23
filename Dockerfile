FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y gcc python3-dev curl libgpiod-dev libgpiod2 && \
    rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
ln -s /root/.local/bin/uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock ./
COPY src/ ./src/

# Install dependencies
RUN ~/.local/bin/uv sync

# Run the monitor
CMD ["uv", "run", "python", "src/monitor.py"]