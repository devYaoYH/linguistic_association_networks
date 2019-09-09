import os
import sys
import numpy as np

def parseColumns(rt_data):
	columns = dict()
	with open(rt_data, "r") as fin:
		network_lengths = dict()
		for line in fin:
			prompt, target, time, length = line.split(',')
			time = float(time)
			length = int(length)
			try:
				network_lengths[length].append(time)
			except KeyError:
				network_lengths[length] = [time]
	fin.close()

	# Compute Numpy std/mean for each length
	output_fname = input("Output .csv name: ")
	with open(output_fname, "w+") as fout:
		for key, li in network_lengths.items():
			data = np.array(li)
			fout.write("{},{},{}\n".format(key, np.mean(data), np.std(data)))
	fout.close()

parseColumns("RT_against_pathLength.csv")