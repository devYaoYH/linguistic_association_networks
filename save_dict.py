import json
import numpy as np

# Load data from small file
dic = dict()

word_list = []
with open("common_subset/google-10000-filtered.txt") as fin:
	for line in fin:
		word_list.append(line.split()[0])
fin.close()
dataset = np.loadtxt("common_subset/top10000_vectors.txt")
for i, word in enumerate(word_list):
	dic[word] = dataset[i].tolist()

with open("common_subset/dic.json", "w+") as fout:
	json.dump(dic, fout)
fout.close()