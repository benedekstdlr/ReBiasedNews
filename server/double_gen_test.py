from http.server import BaseHTTPRequestHandler
from socketserver import TCPServer
import gpt_2_simple as gpt2
import json
import ssl

CP_DIR_1 = '../../models/breitbart/checkpoint'
CP_DIR_2 = '../../models/cnn/checkpoint'

sess = gpt2.start_tf_sess(threads=7)
gpt2.load_gpt2(sess1, checkpoint_dir=CP_DIR_1)
gpt2.generate(sess)

sess = gpt2.reset_session(sess, threads=7)
gpt2.load_gpt2(sess, checkpoint_dir=CP_DIR_2)
gpt2.generate(sess)
