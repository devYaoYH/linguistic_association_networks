import json
from annoy import AnnoyIndex
import numpy as np
import random

# Load from small dataset
vsm = dict()
word_list = []
word_to_idx = dict()
stopwords_filter = set()

print("Loading VSM .... ", end="")
with open("common_subset/dic.json", "r") as fin:
	vsm = json.load(fin)
fin.close()
print("done")

print("Loading nltk english stopwords ... ", end="")
with open("nltk_stopwords.txt", "r") as fin:
	for line in fin:
		stopwords_filter.add(line.split()[0])
fin.close()
print("done")

print("Loading top 10000 common english words ... ", end="")
with open("common_subset/google-10000-filtered.txt", "r") as fin:
	conut = 0
	for line in fin:
		w = line.split()[0]
		if (w not in stopwords_filter and len(w) > 1):
			word_list.append(w)
			word_to_idx[w] = conut
			conut += 1
fin.close()
print("done")

model = None

# Interact with our loaded dictionary
def interactive_test():
	global model
	if (model is None):
		load_tree()
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
	global model
	if (model is None):
		model = AnnoyIndex(len(vsm[word_list[0]]))
		model.load("top-10000.ann")
		print("Annoying Tree Loaded")

# Uniform Random build our smallworld network
def random_smallworld(m, k):	# m -> Number of edges formed per iteration | k -> Number of neighbors 'activated'
	global model
	if (model is None):
		load_tree()
	json_graph = dict()
	json_graph['nodes'] = [{'name': word} for word in word_list]
	json_graph['links'] = []	# 'source': 0, 'target': 0, 'value': 0
	for w in word_list[:100]:
		cur_idx = word_to_idx[w]
		li = model.get_nns_by_item(cur_idx, k)
		word_li = [word_list[i] for i in li]
		# We pick m nodes to connect with
		for i in range(m):
			source = cur_idx
			target = random.choice(li)
			value = model.get_distance(source, target)
			json_graph['links'].append({'source': source, 'target': target, 'value': value})
	with open("smallworld_network.json", "w+") as fout:
		json.dump(json_graph, fout)
	fout.close()

#############
# EXECUTION #
#############
#interactive_test()
random_smallworld(3, 10)