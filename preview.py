#!/usr/bin/env python3
"""
preview.py - Local Live Preview for your GitHub Profile README
Starts a local web server and opens your rendered README.md with GitHub's exact
dark theme in your browser.

Usage:
    python3 preview.py
"""

import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8000

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GitHub Profile README - Local Preview</title>
  <!-- GitHub Markdown CSS -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.5.0/github-markdown-dark.min.css">
  <!-- Marked.js for real-time Markdown parsing -->
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    body {
      background-color: #0d1117;
      color: #c9d1d9;
      margin: 0;
      padding: 30px 16px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    }
    .container {
      max-width: 920px;
      margin: 0 auto;
      background: #0d1117;
      border: 1px solid #30363d;
      border-radius: 8px;
      padding: 32px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    }
    .preview-banner {
      max-width: 920px;
      margin: 0 auto 16px auto;
      padding: 10px 16px;
      background: #161b22;
      border: 1px solid #30363d;
      border-radius: 6px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 13px;
      color: #8b949e;
    }
    .status-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      color: #39d353;
      font-weight: 600;
    }
    .status-badge::before {
      content: "";
      width: 8px;
      height: 8px;
      background: #39d353;
      border-radius: 50%;
      display: inline-block;
    }
    .markdown-body {
      background-color: transparent !important;
    }
  </style>
</head>
<body>
  <div class="preview-banner">
    <span class="status-badge">Local Preview Server Active</span>
    <span>Viewing <code>README.md</code> • Press Ctrl+C in terminal to stop</span>
  </div>

  <div class="container">
    <article id="content" class="markdown-body">
      Loading README preview...
    </article>
  </div>

  <script>
    async function loadReadme() {
      try {
        const res = await fetch('/README.md?t=' + Date.now());
        const markdown = await res.text();
        marked.setOptions({
          gfm: true,
          breaks: true
        });
        document.getElementById('content').innerHTML = marked.parse(markdown);
      } catch (err) {
        document.getElementById('content').innerHTML = '<p style="color:#ff7b72;">Failed to load README.md: ' + err + '</p>';
      }
    }
    loadReadme();
  </script>
</body>
</html>
"""

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode("utf-8"))
        else:
            super().do_GET()

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        url = f"http://localhost:{PORT}"
        print(f"=======================================================")
        print(f"🚀 GitHub README Local Preview Server running at:")
        print(f"   {url}")
        print(f"=======================================================")
        print(f"Opening your browser now... (Press Ctrl+C to stop)")
        try:
            webbrowser.open(url)
        except Exception:
            pass
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nPreview server stopped.")

if __name__ == "__main__":
    main()

