import http.server
import socketserver

# This port matched the port exposed in Dockerfile (usually 80)
PORT = 80

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # 1. Send a 200 OK success status
        self.send_response(200)
        # 2. Tell the browser we are sending HTML
        self.send_header("Content-type", "text/html")
        self.end_headers()
        # 3. The actual message verification
        message = """
        <html>
            <head><title>GridOps Verification</title></head>
            <body style="background-color: #e0f7fa; padding: 40px; font-family: sans-serif;">
                <h1 style="color: #006064;">Success!</h1>
                <p><b>Service:</b> Payment Service</p>
                <p><b>Version:</b> v2 (Updated via Jenkins + Argo CD)</p>
                <p>If you see this, your GitOps pipeline is fully operational.</p>
            </body>
        </html>
        """
        self.wfile.write(bytes(message, "utf8"))
        
# Start the server
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()
