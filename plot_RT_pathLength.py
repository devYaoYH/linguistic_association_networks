import os
import sys

# Filter out incorrect responses
# Take mean of all subjects responses
# Compare to network path lengths
def parseColumns(rt_data, path_length):
	columns = dict()
	with open(rt_data, "r") as fin:
		word_pairs = dict()
		for line in fin:
			prompt, target, correct, time = line.split(',')
			correct = True if correct == "1" else False
			time = int(time)
			if (not correct):
				continue
			pair = (prompt.lower(), target.lower())
			try:
				word_pairs[pair][0] += 1
				word_pairs[pair][1] += time
			except KeyError:
				word_pairs[pair] = [1, time]
	fin.close()

	with open(path_length, "r") as fin:
		paths = dict()
		for line in fin:
			items = line.split()
			paths[(items[1], items[-1])] = int(items[0])
	fin.close()

	# Process Mean RT for all subjects
	output_fname = input("Output .csv name: ")
	with open(output_fname, "w+") as fout:
		for key, value in word_pairs.items():
			word_pairs[key] = float(value[1]/value[0])
			if (key in paths):
				fout.write("{},{},{},{}\n".format(key[0], key[1], word_pairs[key], paths[key]))
	fout.close()

parseColumns("RT_pairs.csv", "demasking_path_length.txt")