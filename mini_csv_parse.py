import os
import sys

def parseColumns(fname):
	columns = dict()
	with open(fname, "r") as fin:
		headers = fin.readline().split()
		columns = {title: [] for title in headers}
		for line in fin:
			for i, data in enumerate(line.split()):
				columns[headers[i]].append(data)
	fin.close()
	print("Columns: {}".format(columns.keys()))
	if (len(headers) < 1):
		print("Error: No Columns found")
		return
	filter_cols = [int(i) for i in input("Index columns to preserve (0-idx): ").split()]
	output_fname = input("Output .csv name: ")
	with open(output_fname, "w+") as fout:
		for i in range(len(columns[headers[0]])):
			data_row = []
			for col in filter_cols:
				data_row.append(columns[headers[col]][i])
			print(data_row)
			fout.write(" ".join(data_row))
			fout.write("\n")
	fout.close()

parseColumns("data/demasking_errors.dat")