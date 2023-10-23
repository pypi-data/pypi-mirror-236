# Netix ASGI Server

Netix is a high-performance ASGI (Asynchronous Server Gateway Interface) server designed for efficiently serving ASGI web applications and APIs. It offers a robust, customizable, and easy-to-use platform for deploying your ASGI applications.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
  - [Available Commands and Options](#available-commands-and-options)
- [Middleware Support](#middleware-support)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Support and Feedback](#support-and-feedback)

## Features

- **Concurrency Control**: Easily set the number of worker processes to manage concurrent requests efficiently.
- **Socket Options**: Support for both Unix sockets and network sockets with customizable socket options.
- **Middleware Support**: Implement request and response middlewares to customize the behavior of your ASGI application.
- **Daemon Mode**: Run Netix as a daemon to keep it running in the background, detached from the terminal.
- **Status Monitoring**: Schedule status checks to monitor the health of your ASGI server.

## Installation

You can install Netix via `pip`, making it a breeze to get started:

```bash
pip install netix
```

## Configuration

### Available Commands and Options

You can control and configure Netix using various command-line options when starting the server:

- `--host`: Listen host. Defaults to "127.0.0.1".
- `--daemon`: Start the daemon mode to run the server in the background. Use `--daemon main:app` or `@app module` to daemonize.
- `--port`: Listen port. Defaults to 8000.
- `--bind`: Address to bind. You can use this option instead of `--host` and `--port`. For example, "127.0.0.1:8000" or "/tmp/file.sock".
- `--reuse-port`: Use `SO_REUSEPORT` when available.
- `--worker-num`: Number of worker processes. Defaults to 1.
- `--backlog`: Maximum number of pending connections. Defaults to 100.
- `--ssl-cert`: SSL certificate location. For example, "/path/to/fullchain.pem".
- `--ssl-key`: SSL private key location. For example, "/path/to/privkey.pem".
- `--debug`: Enable debug mode. Intended for development.
- `--no-ws`: Disable built-in WebSocket support.
- `--log-level`: Defaults to "DEBUG". For available log levels, see [Python Logging Levels](https://docs.python.org/3/library/logging.html#levels).
- `--download-rate`: Limits the sending speed to the client. Defaults to 1048576, which means 1 MiB/s.
- `--upload-rate`: Limits the upload / POST speed. Defaults to 1048576, which means 1 MiB/s.
- `--buffer-size`: Defaults to 16384, or 16 KiB.
- `--client-max-body-size`: Defaults to 2 * 1048576, or 2 MiB.
- `--request-timeout`: Defaults to 30 seconds.
- `--keepalive-timeout`: Defaults to 30 seconds.
- `--keepalive-connections`: Maximum number of keep-alive connections per worker. Defaults to 512 connections per worker.
- `--root-path`: Set the ASGI root_path. Defaults to an empty string.

For example, you can run Netix with these options:

```bash
python3 -m netix --debug --port 8080 example:app
python3 -m netix --daemon example:app

or 

netix --debug --port 8080 example:app
netix --daemon example:app
```

## Example

- Run the Lexan ASGI Framework App using Netix Server.
```bash
$ netix --bind 127.0.0.1:8000 example:app
```
- Output:

```bash
Starting Netix v1.11 (cpython 3.11.4, linux)
------------------------------------------------------------------------
Settings: [
  host=127.0.0.1, port=8000, reuse_port=True, worker_num=1, ssl={}, app=test:app, log_level=DEBUG 
]
------------------------------------------------------------------------
[2023-10-21 23:02:39] Starting Netix ASGI server for /\ Lexan Framework
[2023-10-21 23:02:39,890] INFO: lifespan: startup
[2023-10-21 23:02:40] Netix (ASGI) (pid 69334) is started at 127.0.0.1:8000 (Press CTRL+C to quit)
```

