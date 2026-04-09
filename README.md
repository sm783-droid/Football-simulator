# Football Tournament Simulator

A tkinter-based football tournament simulation app. This guide covers how to run it using Docker.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed and running
- An X11 display server:
  - **Linux**: X11 is available by default
  - **macOS**: XQuartz is required — see [macOS (XQuartz)](#macos-xquartz) below
  - **Windows (WSL2)**: Use an X server like [VcXsrv](https://sourceforge.net/projects/vcxsrv/) or [WSLg](https://github.com/microsoft/wslg)

## Build the Image

```bash
docker build -t football-sim .
```

## Run the App

### Linux / WSL2

```bash
xhost +local:docker
docker run --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix football-sim
```

### macOS (XQuartz)

1. Install XQuartz:

   ```bash
   brew install --cask xquartz
   ```

2. **Log out and log back in** so XQuartz registers correctly.
3. Open XQuartz, go to **Settings > Security**, and check **"Allow connections from network clients"**. Restart XQuartz after saving.
4. Grant display access and run the container:

   ```bash
   xhost + 127.0.0.1
   docker run --rm -e DISPLAY=host.docker.internal:0 football-sim
   ```

## Persisting the Database

By default the SQLite database (`football.db`) lives inside the container and is lost when it stops. To persist it across runs, mount a local directory:

```bash
# Linux / WSL2
docker run --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v "$PWD/data":/app/data \
  -e DB_DIR=/app/data \
  football-sim

# macOS
docker run --rm \
  -e DISPLAY=host.docker.internal:0 \
  -v "$PWD/data":/app/data \
  -e DB_DIR=/app/data \
  football-sim
```

The `data/` directory will be created in your current working directory on first run.

## Running Tests

```bash
docker run --rm --entrypoint pytest football-sim
```
"# Football-simulator" 
"# Football-simulator" 
