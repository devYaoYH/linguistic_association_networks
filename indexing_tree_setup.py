import json
from annoy import AnnoyIndex
import numpy as np

# Load from small dataset
vsm = dict()
word_list = []
word_to_idx = dict()
stopwords_filter = set()

with open("common_subset/dic.json", "r") as fin:
	vsm = json.load(fin)
fin.close()

with open("nltk_stopwords.txt", "r") as fin:
	for line in fin:
		stopwords_filter.add(line.split()[0])
fin.close()

with open("common_subset/google-10000-filtered.txt", "r") as fin:
	conut = 0
	for line in fin:
		w = line.split()[0]
		if (w not in stopwords_filter and len(w) > 1):
			word_list.append(w)
			word_to_idx[w] = conut
			conut += 1
fin.close()

model = AnnoyIndex(len(vsm[word_list[0]]))

# Interact with our loaded dictionary
def interactive_test():
	usr_input = input()
	while(usr_input != "quit"):
		try:
			#print(vsm[usr_input])
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
	t.save("top-10000.ann")

# Load .ann file
def load_tree():
	model.load("top-10000.ann")
	print("Annoying Tree Loaded")

#############
# EXECUTION #
#############
build_tree()