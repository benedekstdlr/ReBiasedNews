from http.server import BaseHTTPRequestHandler
from socketserver import TCPServer
import gpt_2_simple as gpt2
import json
import ssl

CP_DIR_1 = '../../models/breitbart/checkpoint'
CP_DIR_2 = '../../models/cnn/checkpoint'

sess1 = gpt2.start_tf_sess()
sess2 = gpt2.start_tf_sess()
gpt2.load_gpt2(sess1, checkpoint_dir=CP_DIR_1)
gpt2.load_gpt2(sess2, checkpoint_dir=CP_DIR_2)
gpt2.generate(sess1)
gpt2.generate(sess2)
