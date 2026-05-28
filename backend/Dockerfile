# ============================================================
# FASTAPI DOCKERFILE (EDUCATIONAL VERSION)
# ============================================================
#
# This Dockerfile packages your FastAPI application into a
# portable container that can run anywhere (laptop, server,
# cloud) without worrying about Python setup differences.
#
# Think of it like:
#   "a boxed version of your backend app + its environment"
#
# ============================================================


# ------------------------------------------------------------
# 1. BASE IMAGE
# ------------------------------------------------------------
#
# We start from an official Python image.
# "slim" means:
# - smaller size
# - fewer unnecessary tools
# - faster builds
#
FROM python:3.11-slim


# ------------------------------------------------------------
# 2. ENVIRONMENT VARIABLES
# ------------------------------------------------------------
#
# These settings improve Python behavior inside Docker:
#
# - PYTHONDONTWRITEBYTECODE=1
#   → prevents Python from creating .pyc files
#
# - PYTHONUNBUFFERED=1
#   → ensures logs appear immediately (important for Docker logs)
#
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# ------------------------------------------------------------
# 3. WORKING DIRECTORY
# ------------------------------------------------------------
#
# This defines where your code will live inside the container.
# Every following command runs inside /app.
#
WORKDIR /app


# ------------------------------------------------------------
# 4. SYSTEM DEPENDENCIES
# ------------------------------------------------------------
#
# Some Python packages need system-level tools to compile.
# Example:
# - numpy
# - sentence-transformers
# - PDF processing libraries
#
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*
#
# IMPORTANT:
# We remove apt cache at the end to keep image size small.


# ------------------------------------------------------------
# 5. INSTALL PYTHON DEPENDENCIES FIRST (CACHE OPTIMIZATION)
# ------------------------------------------------------------
#
# Why copy requirements first?
# → Docker caches this layer
# → If requirements don't change, rebuilds are faster
#
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# ------------------------------------------------------------
# 6. COPY APPLICATION CODE
# ------------------------------------------------------------
#
# Now we copy your actual FastAPI project into the container.
#
COPY . .

# ---------------------------------------------------
# 4. Ensure Python can find "app" module
# ---------------------------------------------------
ENV PYTHONPATH=/app

# ------------------------------------------------------------
# 7. EXPOSE PORT
# ------------------------------------------------------------
#
# This tells Docker:
# "this container will listen on port 8000"
#
# NOTE:
# This does NOT publish the port to your computer.
# It is just documentation/metadata.
#
EXPOSE 8000


# ------------------------------------------------------------
# 8. START COMMAND (WHAT RUNS WHEN CONTAINER STARTS)
# ------------------------------------------------------------
#
# We use uvicorn, the ASGI server that runs FastAPI apps.
#
# Breakdown:
# - app.main:app → Python path to FastAPI instance
# - 0.0.0.0 → allows external access (important in Docker)
# - 8000 → port inside container
#
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]