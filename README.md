# Football Tournament Simulator

A tkinter-based football tournament simulation app. This guide covers how to run it using Docker.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed and running
- An X11 display server:
  - **Linux**: X11 is available by default
  - **macOS**: XQuartz is required — see [macOS (XQuartz)](#macos-xquartz) below
  - **Windows**: An X server is required — see [Windows](#windows) below

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

### Windows

Docker Desktop on Windows can forward GUI apps via an X server. There are two options:

#### Option A — WSLg (Windows 11 / Docker Desktop with WSL2 backend, recommended)

WSLg ships a built-in Wayland/X11 server. No extra software needed.

1. Open a **WSL2 terminal** (e.g. Ubuntu from the Start menu).
2. Build the image from within WSL2:

   ```bash
   docker build -t football-sim .
   ```

3. Run the container:

   ```bash
   xhost +local:docker
   docker run --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix football-sim
   ```

#### Option B — VcXsrv (Windows 10 or without WSLg)

1. Download and install [VcXsrv](https://sourceforge.net/projects/vcxsrv/).
2. Launch **XLaunch**, choose *Multiple windows*, display number `0`, and on the extra settings page check **"Disable access control"**.
3. Find your Windows host IP (shown in `ipconfig` as the Ethernet/Wi-Fi adapter address, or use `host.docker.internal`).
4. Open **PowerShell** or **Command Prompt** and run:

   ```powershell
   docker run --rm -e DISPLAY=host.docker.internal:0 football-sim
   ```

> **Firewall note:** Windows Firewall may block the connection. Allow VcXsrv through the firewall when prompted, or add a manual inbound rule for TCP port 6000.

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
