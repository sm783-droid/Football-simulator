FROM --platform=linux/amd64 python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-tk \
        tk-dev \
        libx11-6 \
        git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /repo

COPY app.py db.py db_games.py db_managers.py simulation.py \
     styles.py ui_league.py ui_setup.py ui_week.py \
     task_config.json requirements.txt ./

COPY tests/ ./tests/

RUN python -m venv /repo/venv
ENV VIRTUAL_ENV=/repo/venv
ENV PATH="/repo/venv/bin:$PATH"

RUN pip install --upgrade pip --quiet \
    && pip install -r requirements.txt --quiet

RUN git init \
    && git config --system --add safe.directory /repo \
    && chmod -R 777 /repo

ENV DISPLAY=:0

CMD ["python", "app.py"]