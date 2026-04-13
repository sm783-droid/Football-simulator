# Football Tournament Simulator — Dockerfile
#
# Requires X11 forwarding so the tkinter window can appear on your host.
#
# Build:
#   docker build -t football-sim .
#
# Run (Linux / WSL2):
#   xhost +local:docker
#   docker run --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix football-sim
#
# Run (macOS — needs XQuartz installed and "Allow connections from network clients" enabled):
#   xhost + 127.0.0.1
#   docker run --rm -e DISPLAY=host.docker.internal:0 football-sim
#
# The SQLite database (football.db) is stored inside the container by default.
# Mount a volume to persist it across runs:
#   docker run --rm -e DISPLAY=$DISPLAY \
#              -v /tmp/.X11-unix:/tmp/.X11-unix \
#              -v "$PWD/data":/app/data \
#              -e DB_DIR=/app/data \
#              football-sim

FROM python:3.11-slim

# Install tkinter + X11 client libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-tk \
        tk-dev \
        libx11-6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy source
COPY app.py db.py db_games.py db_managers.py simulation.py \
     styles.py ui_league.py ui_setup.py ui_week.py \
    requirements.txt ./

# Create and activate a virtual environment
RUN python -m venv /app/venv
ENV VIRTUAL_ENV=/app/venv
ENV PATH="/app/venv/bin:$PATH"

# No pip packages needed, but upgrade pip for good measure
RUN pip install --upgrade pip --quiet

# Default display (overridden at runtime via -e DISPLAY=...)
ENV DISPLAY=:0

CMD ["python", "app.py"]
