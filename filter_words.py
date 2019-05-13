import sys
import json
import numpy as np
from utils import parseArgs
from utils import file_concat
from gensim.models.keyedvectors import KeyedVectors

# Help message for script
def printHelp():
	print("Utility for filtering out words which do not exist inside a corpus")
	print("  -f: Input wordlist file name")
	print("  -o: Output wordlist file name")
	sys.stdout.flush()

def filter_words(sysargs, model=None):
	# Parse arguments for script
	# argc (argument count) | argv (argument list) | args (argument dictionary with flags)
	argc, argv, args = parseArgs(sysargs, "h");

	if ('h' in args):
		printHelp()
		return

	# Filter vectors for some subset of words
	fname = "google-10000-english.txt" if ('f' not in args) else args['f']
	output_fname = "google-10000.txt" if ('o' not in args) else args['o']
	unknown_fname = "unknown_google-10000-english.txt" if ('o' not in args) else file_concat("unknown", output_fname)
	vectors_fname = "common_subset/vectors_google-10000-english.txt" if ('o' not in args) else file_concat("vectors", "common_subset\\" + output_fname)
	dic_fname = "common_subset/google-10000.json" if ('o' not in args) else "common_subset\\" + output_fname.split('\\')[-1].split('.')[0] + ".json"

	cont = input("Parsing options...continue?(y/n)\nfname: {}\noutput: {}\nunknown: {}\nvectors: {}\njson: {}\n".format(fname, output_fname, unknown_fname, vectors_fname, dic_fname))
	while(cont != "y" and cont != "n"):
		cont = input("Parsing options...continue?(y/n)\nfname: {}\noutput: {}\nunknown: {}\nvectors: {}\njson: {}\n".format(fname, output_fname, unknown_fname, vectors_fname, dic_fname))
	if (cont == "n"):
		sys.exit()

	# Load Model from pre-trained vectors
	if (model is None):
		model = KeyedVectors.load_word2vec_format('data/GoogleNews-vectors-negative300.bin', binary=True)

	# Load text file
	unknown_words = []
	vectors = []
	dic = dict()
	with open(output_fname, "w+") as fout: 
		with open(fname) as fin:
			conut = 0
			for line in fin:
				word = line.split()[0]
				# Extract vector from model
				try:
					word_vec = model[word.lower()]
					vectors.append(word_vec)
					fout.write("{}\n".format(word.lower()))
					dic[word.lower()] = word_vec.tolist()
				except KeyError:
					try:
						word_vec = model[word.upper()]
						vectors.append(word_vec)
						fout.write("{}\n".format(word.upper()))
						dic[word.upper()] = word_vec.tolist()
					except KeyError:
						unknown_words.append(word)
						pass
				# Write to text file
				conut += 1
				if (conut%50 == 0):
					print("Parsed...{}".format(conut))
					sys.stdout.flush()
		fin.close()
	fout.close()
	with open(unknown_fname, "w+") as fout:
		for word in unknown_words:
			fout.write("{}\n".format(word))
	fout.close()
	np.savetxt(vectors_fname, np.vstack(vectors))

	with open(dic_fname, "w+") as fout:
		json.dump(dic, fout)
	fout.close()

# Dynamic keyword query
query = input("Query for word within word2vec loaded model ('quit' to end): ")
while(query != "quit"):
	try:
		print(model[query.lower()])
	except KeyError:
		print("Word {} NOT FOUND".format(query))
	query = input("Query for word within word2vec loaded model ('quit' to end): ")