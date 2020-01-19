from http.server import BaseHTTPRequestHandler
from socketserver import TCPServer
import gpt_2_simple as gpt2
import json
import ssl
import hashlib
import random
import threading
import queue
import time
import os.path

BB_DIR = '../../models/breitbart/checkpoint'
CNN_DIR = '../../models/cnn/checkpoint'


q = queue.Queue(10000)

def model_dir(origin):
    if 'breitbart' in origin:
        return CNN_DIR
    else:
        return BB_DIR


class GeneratorThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(GeneratorThread,self).__init__()
        self.target = target
        self.name = name
        self.last_model = ''
        self.sess = gpt2.start_tf_sess()
        return

    def generate_new(self, origin, vals):
        #return ('stuff ' + str(random.randrange(10000))).encode('utf-8')
        dir = model_dir(origin)
        if dir != self.last_model:
            self.sess = gpt2.reset_session(self.sess, threads=7)
            gpt2.load_gpt2(self.sess, checkpoint_dir=dir)
            self.last_model = dir
        if self.last_model == BB_DIR:
            prompt = vals['title'] + ' - Breitbart <START> ' + vals['body']
        else:
            if vals['body'][:6] == ' (CNN)':
                vals['body'] = vals['body'][6:]
            if vals['body'][:5] == '(CNN)':
                vals['body'] = vals['body'][5:]
            prompt = vals['title'] + ' <START> ' + vals['body']

        text = gpt2.generate(self.sess, checkpoint_dir=self.last_model, return_as_list=True, prefix=prompt)[0]
        if self.last_model == BB_DIR:
            text = text.replace('[', '</p> <p class="zn-body__paragraph">')
        text = text[len(prompt):]
        text = str.encode(text)
        return text

    def run(self):
        while True:
            if not q.empty():
                (hash, origin, vals) = q.get()
                print('Getting \"' + str(vals['title']) + '\" with hash ' + hash
                              + ' : ' + str(q.qsize()) + ' items in queue')
                out_path = '../../out/'+hash
                if not os.path.exists(out_path):
                    text = self.generate_new(origin, vals)
                    f = open(out_path, 'wb')
                    f.write(text)
                    f.close()
            time.sleep(1)
        return




class MyHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        print(self.headers)
        body = self.rfile.read(int(self.headers.get('content-length'))).decode('utf-8')
        print(body)
        vals = json.loads(body)
        referer = self.headers.get('referer')
        origin = self.headers.get('origin')
        hash = hashlib.md5(referer.encode('utf-8')).hexdigest()
        try:
            f = open('../../out/'+hash, 'rb')
            print('Accessing from cache')
            text = f.read()
            f.close()
        except IOError:
            print('Generating new')
            q.put((hash, origin, vals))
            text = b'... And then what? Check back later to find out!'


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

GeneratorThread(name='generator-thread').start()

PORT = 443
httpd = TCPServer(("", PORT), MyHandler)

print("serving at port", PORT)
httpd.socket = ssl.wrap_socket (httpd.socket, certfile='/etc/letsencrypt/live/rebiasednews.ddns.net/fullchain.pem',
        keyfile='/etc/letsencrypt/live/rebiasednews.ddns.net/privkey.pem', server_side=True)
httpd.serve_forever()
