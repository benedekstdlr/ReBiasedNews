from http.server import BaseHTTPRequestHandler
from socketserver import TCPServer
import gpt_2_simple as gpt2
import json

CP_DIR = '../../models/breitbart/checkpoint'

sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, checkpoint_dir=CP_DIR)

class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        print(self.headers)
        body = self.rfile.read(int(self.headers.get('content-length'))).decode('utf-8')
        print(body)
        vals = json.loads(body)
        prompt = vals['title'] + ' <START> ' + vals['body']
        text = gpt2.generate(sess, checkpoint_dir=CP_DIR, return_as_list=True, prefix=prompt)[0]
        text = str.encode(text)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", len(text))
        self.end_headers()
        self.wfile.write(text)

PORT = 80

Handler = MyHandler

httpd = TCPServer(("", PORT), Handler)

print("serving at port", PORT)
httpd.socket = ssl.wrap_socket (httpd.socket, certfile='./server.pem', server_side=True)
httpd.serve_forever()
