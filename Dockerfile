# --- BUILD STAGE ---
FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim AS builder

WORKDIR /app

# Cloud Run must listen on $PORT, defaulting to 8080.
ENV PORT=8080
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1

# Install essential build tools, Git, and Node.js dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libssl-dev \
    && curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

ADD . /app

# Run Tailwind build
RUN uv run manage.py tailwind install && \
    uv run manage.py tailwind build

# Final preparations (e.g., collect static files for Django)
RUN uv run manage.py collectstatic --noinput

# --- FINAL STAGE ---
# Use the smallest possible image for the final runtime
FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim AS final

WORKDIR /app

# Set critical environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1

# Copy only the necessary files from the build stage:
# 1. Application code (including static/compiled files)
# 2. Installed Python virtual environment
COPY --from=builder /app /app

# Ensure the virtual environment's binaries are in the PATH
ENV PATH="/app/.venv/bin:$PATH"


EXPOSE 8080

# The entrypoint script will handle starting both Celery and Gunicorn.
ENTRYPOINT ["/app/entrypoint.sh"]
