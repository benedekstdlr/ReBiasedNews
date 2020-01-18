import gpt_2_simple as gpt2

CP_DIR = '../../models/breitbart/checkpoint'

sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, checkpoint_dir=CP_DIR)

gpt2.generate(sess, checkpoint_dir=CP_DIR)
