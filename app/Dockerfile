# ---- Builder Stage ----
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0

RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# ---- Final Stage ----
FROM python:3.12-slim-bookworm

# Create app user
RUN useradd --create-home --shell /bin/bash app

# Set home and app paths


WORKDIR /app
RUN mkdir -p /app/staticfiles/
RUN chown -R app:app /app/staticfiles/

# Install required dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Copy application files from the builder stage
COPY --from=builder --chown=app:app /app /app


# Set permissions on copied files
RUN chown -R app:app /app

# Copy the entrypoint script
COPY --from=builder /app/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && chown app:app /entrypoint.sh

# Update the PATH to include virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Switch to app user for container runtime
USER app

# Define the entrypoint to run your app
ENTRYPOINT ["/entrypoint.sh"]
