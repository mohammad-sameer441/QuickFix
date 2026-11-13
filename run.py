#!/usr/bin/env python3
"""
QuickFix Turnkey Localhost Launcher
Starts the full QuickFix platform on http://127.0.0.1:8000
Serves the dark-mode dashboard UI and the Python AI API simultaneously.
"""

import os
import sys
import time
import threading
import webbrowser
import subprocess

PORT = 8000
HOST = "127.0.0.1"
URL = f"http://{HOST}:{PORT}"

def print_banner():
    print("=" * 72)
    print("⚡   QuickFix: AI Predictive Intelligence & Automated Program Repair")
    print("=" * 72)
    print(f"[*] Platform launching at: {URL}")
    print("[*] Dashboard & AI REST API running unified on port 8000")
    print("=" * 72)

def open_browser():
    time.sleep(1.2)
    print(f"[*] Opening browser at {URL} ...")
    webbrowser.open(URL)

def ensure_dependencies():
    """Checks for fastapi and uvicorn; auto-installs if missing."""
    try:
        import fastapi
        import uvicorn
        import pydantic
        return True
    except ImportError:
        print("[!] FastAPI/Uvicorn not detected in environment.")
        print("[*] Installing lightweight requirements from backend/requirements.txt...")
        req_path = os.path.join(os.path.dirname(__file__), "backend", "requirements.txt")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_path])
            print("[✔] Dependencies installed successfully!")
            return True
        except Exception as e:
            print(f"[!] Pip install encountered an error: {e}")
            print("[!] Falling back to Python standard library HTTP server...")
            return False

def start_fastapi_server():
    """Runs the full FastAPI backend + static UI app."""
    # Add backend directory to sys.path
    backend_dir = os.path.join(os.path.dirname(__file__), "backend")
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)

    import uvicorn
    from app import app

    uvicorn.run(app, host=HOST, port=PORT, log_level="info")

def start_fallback_http_server():
    """Fallback server using standard library http.server (0 dependencies needed)."""
    import http.server
    import socketserver

    web_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(web_dir)

    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer((HOST, PORT), Handler) as httpd:
        print(f"[✔] Standard HTTP Server active on {URL}")
        httpd.serve_forever()

if __name__ == "__main__":
    print_banner()

    # Launch browser in a background thread
    threading.Thread(target=open_browser, daemon=True).start()

    # Attempt FastAPI full server; fallback to standard http.server if necessary
    has_deps = ensure_dependencies()
    if has_deps:
        try:
            start_fastapi_server()
        except Exception as e:
            print(f"[!] FastAPI server stopped or failed: {e}")
            print("[*] Switching to standard HTTP server...")
            start_fallback_http_server()
    else:
        start_fallback_http_server()
