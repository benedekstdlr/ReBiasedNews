from http.server import BaseHTTPRequestHandler
from socketserver import TCPServer
import gpt_2_simple as gpt2
import json
import ssl
import hashlib
import random

BB_DIR = '../../models/breitbart/checkpoint'
CNN_DIR = '../../models/cnn/checkpoint'

last_model = None
sess = gpt2.start_tf_sess()


def model_dir(origin):
    if 'breitbart' in origin:
        return CNN_DIR
    else:
        return BB_DIR


class MyHandler(BaseHTTPRequestHandler):
    def generate_new(self, origin, vals):
        return 'stuff ' + random.randrange(10000)
        dir = source(origin)
        if dir != last_model:
            sess = gpt2.reset_session(sess, threads=7)
            gpt2.load_gpt2(sess, checkpoint_dir=dir)
            last_model = dir
        prompt = vals['title'] + ' <START> ' + vals['body']
        text = gpt2.generate(sess, checkpoint_dir=last_model, return_as_list=True, prefix=prompt)[0]
        text = str.encode(text)
        return text


    def do_POST(self):
        print(self.headers)
        body = self.rfile.read(int(self.headers.get('content-length'))).decode('utf-8')
        print(body)
        vals = json.loads(body)
        referer = self.headers.get('referer')
        hash = hashlib.md5(referer.encode('utf-8')).hexdigest()
        try:
            f = open('../../out/'+hash, 'r')
            text = f.read()
            f.close()
        except IOError:
            text = self.generate_new(referer, origin)
            f = open('../../out/'+hash, 'w')
            f.write(text)
            f.close()


        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", len(text))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(text)

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()


PORT = 443

httpd = TCPServer(("", PORT), MyHandler)

print("serving at port", PORT)
httpd.socket = ssl.wrap_socket (httpd.socket, certfile='/etc/letsencrypt/live/rebiasednews.ddns.net/fullchain.pem',
        keyfile='/etc/letsencrypt/live/rebiasednews.ddns.net/privkey.pem', server_side=True)
httpd.serve_forever()
