import sys
import json
from utils import parseArgs
from annoy import AnnoyIndex
import numpy as np

def printHelp():
	print("Indexing vectors for faster search")
	print("  -f: Indicate which subset to index")
	sys.stdout.flush()

# Load from small dataset
def index_tree(sysargs):
	vsm = dict()
	word_list = []
	word_to_idx = dict()
	stopwords_filter = set()

	# Parse Arguments
	argc, argv, args = parseArgs(sysargs, "h,strip")

	if ('h' in args):
		printHelp()
		return

	fname = "google-10000" if ('f' not in args) else args['f']

	print("Loading dataset: {}".format(fname))

	with open("common_subset\\" + fname + ".json", "r") as fin:
		vsm = json.load(fin)
	fin.close()

	if ('strip' in args):
		with open("nltk_stopwords.txt", "r") as fin:
			for line in fin:
				stopwords_filter.add(line.split()[0])
		fin.close()

	with open("common_subset/" + fname + ".txt", "r") as fin:
		conut = 0
		for line in fin:
			w = line.split()[0]
			if (w not in stopwords_filter and len(w) > 1):
				word_list.append(w)
				word_to_idx[w] = conut
				conut += 1
	fin.close()

	print("Loaded {} words".format(len(word_list)))

	# Load .ann file
	def load_tree(dims, fname):
	    model = AnnoyIndex(dims)
	    model.load(fname + ".ann")
	    print("Annoying Tree Loaded")
	    sys.stdout.flush()
	    return model

	# Interact with our loaded dictionary
	def interactive_test(dims, fname):
		model = load_tree(dims, fname)
		usr_input = input()
		while(usr_input != "quit"):
			try:
				#print(vsm[usr_input])
				print("Index: {}".format(word_to_idx[usr_input]))
				li = model.get_nns_by_item(word_to_idx[usr_input], 10)
				print([word_list[i] for i in li])
			except KeyError:
				print("ERROR: Word not in dictionary")
			usr_input = input()

	# Build .ann file
	def build_tree():
		dims = len(vsm[word_list[0]])
		t = AnnoyIndex(dims)
		for i in range(len(word_list)):
			t.add_item(i, vsm[word_list[i]])

		t.build(53) # 53 trees
		t.save(fname + ".ann")
		print("Successfully Generated Index Tree")

	#############
	# EXECUTION #
	#############
	build_tree()
	interactive_test(len(vsm[word_list[0]]), fname)