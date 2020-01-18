from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
DUMMY_RESPONSE = """Content-type: text/html

<html>
<head>
<title>Python Test</title>
</head>

<body>
Test page...success.
</body>
</html>
"""

class MyHandler(SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        SimpleHTTPRequestHandler.__init__(self, request, client_address, server)


    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", len(DUMMY_RESPONSE))
        self.end_headers()
        self.wfile.write(str.encode(DUMMY_RESPONSE))

PORT = 80

Handler = MyHandler

httpd = TCPServer(("", PORT), Handler)

print("serving at port", PORT)
httpd.serve_forever()
