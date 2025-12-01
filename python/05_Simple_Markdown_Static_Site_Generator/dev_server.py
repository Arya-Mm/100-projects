"""
DEV SERVER WITH LIVE RELOAD
---------------------------
This script does three things:

1) Watches your project folders (content/, templates/, assets/)
2) Rebuilds the static site whenever something changes
3) Serves the built site at http://localhost:8000 with auto-refresh

This gives you the same workflow as frameworks like Jekyll, Hugo, Astro, Vite, etc.
"""

import http.server
import socketserver
import threading
import time
from pathlib import Path
import subprocess
import sys
import io

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

BUILD_SCRIPT = "build.py"                # The script that generates your HTML files
SITE_DIR = Path("site")                  # Output folder containing the generated website
WATCH_DIRS = ["content", "templates", "assets"]
PORT = 8000                              # Local server port
RELOAD_FILE = SITE_DIR / ".reload"       # Timestamp file used for browser auto-reload


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def ensure_site_directory():
    """Make sure the site/ folder always exists."""
    SITE_DIR.mkdir(parents=True, exist_ok=True)


def update_reload_timestamp():
    """Touch or update .reload to trigger browser refresh."""
    ensure_site_directory()
    RELOAD_FILE.write_text(str(time.time()))


# ---------------------------------------------------------
# BUILD PROCESS (called every time files change)
# ---------------------------------------------------------

def rebuild_site():
    """Rebuild the static site using build.py (or fallback import)."""
    print("\n[BUILD] Rebuilding your site…")

    ensure_site_directory()

    # Try running "python build.py --force"
    if Path(BUILD_SCRIPT).exists():
        try:
            result = subprocess.run(
                [sys.executable, BUILD_SCRIPT, "--force"],
                capture_output=True,
                text=True
            )
            print(result.stdout or "[BUILD] Finished.")
            if result.returncode != 0:
                print("[BUILD] Error in build.py:")
                print(result.stderr)
        except Exception as error:
            print(f"[BUILD] Failed to run build.py: {error}")

    else:
        print("[BUILD] No build.py found — skipping site generation.")

    # Always update reload file
    update_reload_timestamp()
    print("[BUILD] Done.\n")


# ---------------------------------------------------------
# FILE WATCHER (triggers rebuild on any file change)
# ---------------------------------------------------------

class ChangeHandler(FileSystemEventHandler):
    """Watchdog event handler — rebuild site whenever any file is edited."""
    def on_any_event(self, event):
        print(f"[WATCH] Detected change: {event.src_path}")
        rebuild_site()


def start_file_watcher():
    """Start watching project folders for changes."""
    observer = Observer()

    for folder in WATCH_DIRS:
        path = Path(folder)
        if path.exists():
            print(f"[WATCH] Watching → {folder}/")
            observer.schedule(ChangeHandler(), folder, recursive=True)
        else:
            print(f"[WATCH] Skipping missing folder → {folder}/")

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[WATCH] Stopping watcher.")
        observer.stop()

    observer.join()


# ---------------------------------------------------------
# LIVE-RELOAD SERVER
# ---------------------------------------------------------

LIVE_RELOAD_JS = """
<script>
async function checkReload() {
    let last = localStorage.getItem("reload_time") || "0";
    try {
        let res = await fetch("/.reload");
        let text = await res.text();
        if (text !== last) {
            localStorage.setItem("reload_time", text);
            location.reload();
        }
    } catch (err) {}
}
setInterval(checkReload, 1000);
</script>
"""


class LiveReloadHandler(http.server.SimpleHTTPRequestHandler):
    """Serve files from site/ and inject auto-reload JS into HTML pages."""

    def translate_path(self, path):
        # Serve everything out of site/
        clean = path.lstrip("/")
        if clean == "":
            clean = "index.html"
        return str(SITE_DIR / clean)

    def send_head(self):
        """Inject reload script into HTML pages."""
        path = Path(self.translate_path(self.path))

        if path.is_file() and path.suffix == ".html":
            try:
                content = path.read_text(encoding="utf-8")
                if "</body>" in content:
                    content = content.replace("</body>", LIVE_RELOAD_JS + "</body>")
                else:
                    content += LIVE_RELOAD_JS

                encoded = content.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.send_header("Content-Length", len(encoded))
                self.end_headers()

                return io.BytesIO(encoded)

            except Exception as e:
                print("[SERVER] Failed to serve HTML:", e)

        return super().send_head()


def start_server():
    """Start the local development server."""
    with socketserver.TCPServer(("", PORT), LiveReloadHandler) as httpd:
        print(f"[SERVER] Live server → http://localhost:{PORT}")
        httpd.serve_forever()


# ---------------------------------------------------------
# MAIN ENTRY POINT
# ---------------------------------------------------------

if __name__ == "__main__":
    print("[START] Developer server with live reload is starting…")

    # Do an initial build before starting the server
    rebuild_site()

    # Start server in background thread
    threading.Thread(target=start_server, daemon=True).start()

    # Start watching files (blocking loop)
    start_file_watcher()
