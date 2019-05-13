import numpy as np
from utils import parseArgs
from utils import file_concat
from gensim.models.keyedvectors import KeyedVectors

# Help message for script
def printHelp():
	print("Utility script to load up a gensim model from binary data")
	sys.stdout.flush()

def load_gensim(sysargs):
	# Parse arguments for script
	# argc (argument count) | argv (argument list) | args (argument dictionary with flags)
	argc, argv, args = parseArgs(sysargs, "h");

	if ('h' in args):
		printHelp()
		return

	# Load Model from pre-trained vectors
	model = KeyedVectors.load_word2vec_format('data/GoogleNews-vectors-negative300.bin', binary=True)
	return model