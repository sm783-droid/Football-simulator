FROM --platform=linux/amd64 python:3.11-slim

# Install git, tkinter + X11 client libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
        python3-tk \
        tk-dev \
        libx11-6 \
    && rm -rf /var/lib/apt/lists/*

# Clone repo at exact base commit (buggy state — no fixes applied)
WORKDIR /repo
RUN git clone https://github.com/sm783-droid/Football-simulator.git . && \
    git checkout 61547997bf27ab8eb989889e1c6902bb8e70f154

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Mark repo as safe for all users and ensure write access
RUN git config --system --add safe.directory /repo \
    && chmod -R 777 /repo

ENV DISPLAY=:0

CMD ["python", "app.py"]