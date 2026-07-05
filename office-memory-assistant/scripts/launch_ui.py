#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import os
import socket
import subprocess
import sys
import time
import urllib.request
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UI_DIR = ROOT / "assets" / "ui"
DEFAULT_API_PORT = 4177
DEFAULT_WEB_PORT = 5173


def port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.25)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def read_url(url):
    try:
        with urllib.request.urlopen(url, timeout=1.0) as response:
            body = response.read(200000).decode("utf-8", errors="ignore")
            return response.status, body
    except Exception:
        return None, ""


def http_ok(url):
    status, _ = read_url(url)
    return status is not None and 200 <= status < 500


def web_is_office_memory(url):
    status, body = read_url(url)
    return status is not None and "办公室记忆助手" in body


def api_is_office_memory(url, expected_data_dir=None):
    status, body = read_url(url)
    if status is None:
        return False
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return False
    if not ("dataDir" in data and "validation" in data):
        return False
    if expected_data_dir is None:
        return True
    try:
        return Path(data["dataDir"]).resolve() == Path(expected_data_dir).resolve()
    except Exception:
        return False


def next_available_or_matching(start_port, matcher, url_builder, limit=20):
    for port in range(start_port, start_port + limit):
        url = url_builder(port)
        if not port_open(port):
            return port
        if matcher(url):
            return port
    raise RuntimeError(f"No usable local port found from {start_port} to {start_port + limit - 1}")


def main():
    parser = argparse.ArgumentParser(description="Start or reuse the Office Memory Assistant UI.")
    parser.add_argument("--data-dir", default="OL-Memory", help="Path to OL-Memory.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--web-port", type=int, default=DEFAULT_WEB_PORT)
    parser.add_argument("--api-port", type=int, default=DEFAULT_API_PORT)
    parser.add_argument("--open", action="store_true", help="Open the browser after starting.")
    args = parser.parse_args()

    data_dir = Path(args.data_dir).expanduser().resolve()
    api_port = next_available_or_matching(
        args.api_port,
        lambda url: api_is_office_memory(url, data_dir),
        lambda port: f"http://{args.host}:{port}/api/state",
    )
    web_port = None
    for candidate in range(args.web_port, args.web_port + 20):
        url = f"http://{args.host}:{candidate}/"
        if not port_open(candidate):
            web_port = candidate
            break
        if candidate == args.web_port and api_is_office_memory(f"http://{args.host}:{api_port}/api/state", data_dir) and web_is_office_memory(url):
            web_port = candidate
            break
    if web_port is None:
        raise RuntimeError(f"No usable local web port found from {args.web_port} to {args.web_port + 19}")
    web_url = f"http://{args.host}:{web_port}/"
    api_url = f"http://{args.host}:{api_port}/api/state"

    if web_is_office_memory(web_url) and api_is_office_memory(api_url, data_dir):
        print(f"UI already running: {web_url}")
        print(f"Data dir: {data_dir}")
        return

    if not (UI_DIR / "node_modules").exists():
        print("Installing UI dependencies. This only needs to happen once...")
        install = subprocess.run(["npm", "install"], cwd=UI_DIR)
        if install.returncode != 0:
            sys.exit(install.returncode)

    env = os.environ.copy()
    env["OFFICE_MEMORY_DATA"] = str(data_dir)
    env["OFFICE_MEMORY_API_PORT"] = str(api_port)
    env["OFFICE_MEMORY_WEB_PORT"] = str(web_port)
    env["VITE_OFFICE_MEMORY_API"] = f"http://{args.host}:{api_port}/api"
    env["VITE_DEV_SERVER_URL"] = web_url

    log_path = UI_DIR / "office-memory-ui.log"
    log = log_path.open("a", encoding="utf-8")
    subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=UI_DIR,
        env=env,
        stdout=log,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )

    for _ in range(60):
        if http_ok(api_url) and http_ok(web_url):
            print(f"Started Office Memory Assistant UI: {web_url}")
            print(f"Data dir: {data_dir}")
            print(f"Log: {log_path}")
            if args.open:
                subprocess.run(["open", web_url], check=False)
            return
        time.sleep(0.5)

    print(f"UI did not become ready in time. Check log: {log_path}")
    sys.exit(1)


if __name__ == "__main__":
    main()
