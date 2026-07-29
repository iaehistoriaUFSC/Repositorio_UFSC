"""Inicializador Windows: Streamlit local em uma janela WebView2."""

from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
import urllib.request
import webbrowser
from pathlib import Path


ROOT = Path(__file__).resolve().parent
HOST = "127.0.0.1"


def available_port() -> int:
    """Reserva uma porta local livre para impedir reaproveitar um servidor antigo."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
        connection.bind((HOST, 0))
        return int(connection.getsockname()[1])


def wait_ready(url: str, timeout: float = 45) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2) as response:
                if response.status == 200:
                    return True
        except Exception:
            time.sleep(0.4)
    return False


def show_startup_error(message: str) -> None:
    """Exibe uma falha de inicialização mesmo quando o atalho usa pythonw.exe."""
    try:
        import ctypes

        ctypes.windll.user32.MessageBoxW(0, message, "WOKE — erro ao iniciar", 0x10)
    except Exception:
        pass


def main() -> int:
    log_dir = Path(os.environ.get("LOCALAPPDATA", ROOT)) / "Woke" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / "streamlit_server.log"
    port = available_port()
    url = f"http://{HOST}:{port}"
    with log_path.open("a", encoding="utf-8") as log:
        log.write(f"\n--- WOKE startup {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n")
        log.flush()
        server = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                str(ROOT / "woke_app.py"),
                "--server.headless=true",
                f"--server.address={HOST}",
                f"--server.port={port}",
                "--browser.gatherUsageStats=false",
                "--server.fileWatcherType=none",
            ],
            cwd=ROOT,
            stdout=log,
            stderr=subprocess.STDOUT,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        if not wait_ready(url):
            server.terminate()
            message = f"A interface não iniciou. Consulte o log em:\n{log_path}"
            show_startup_error(message)
            return 1

        try:
            import webview

            webview.create_window("WOKE — IA & História", url, width=1280, height=820, min_size=(980, 680))
            webview.start(private_mode=False)
        except Exception:
            webbrowser.open(url)
            try:
                return server.wait()
            except KeyboardInterrupt:
                pass
        finally:
            if server.poll() is None:
                server.terminate()
                try:
                    server.wait(timeout=8)
                except subprocess.TimeoutExpired:
                    server.kill()
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
