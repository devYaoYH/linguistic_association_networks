import sys
import numpy as np
from gensim.models.keyedvectors import KeyedVectors

# Filter vectors for top 10000 subset

# Load Model from pre-trained vectors
model = KeyedVectors.load_word2vec_format('data/GoogleNews-vectors-negative300.bin', binary=True)

# Load text file
vectors = []
with open("common_subset/google-10000-filtered.txt", "w+") as fout: 
	with open("google-10000-english.txt") as fin:
		conut = 0
		for line in fin:
			word = line.split()[0]
			# Extract vector from model
			try:
				word_vec = model[word]
				vectors.append(word_vec)
				fout.write("{}\n".format(word))
			except KeyError:
				pass
			# Write to text file
			conut += 1
			if (conut%50 == 0):
				print("Status...{}/10000".format(conut))
	fin.close()
fout.close()
np.savetxt("common_subset/top10000_vectors.txt", np.vstack(vectors))