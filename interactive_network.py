import sys
import json
import queue
import random

# Parse cmd Arguments
argv = []
opt_args = []
for arg in sys.argv:
	if ('-' in arg):
		opt_args.append(arg[1:])
	else:
		argv.append(arg)

directed_graph = 'd' in opt_args
if ('h' in opt_args):
	print("python interactive_network.py <graph_log.json>")
	print("Optional Configuration Flags:")
	print("    -d  :  Directed Graph (without flag -> default undirected)")
	exit()

argc = len(argv)
if (argc < 2):
	print("Error, please provide a _log.json file to load graph.")
	exit()

# Load graph
graph = dict()
try:
	with open(argv[1], "r") as fin:
		graph = json.load(fin)
	fin.close()
	print("")
	print("###################################")
	print("# Interactive Graph Query Console #")
	print("###################################")
	print("")
except:
	print("File I/O Error: {} cannot be opened".format(argv[1]))
	exit()

# Nodes
word_list = graph['nodes']
help_list = sorted(word_list)
word_to_idx = {w: i for i, w in enumerate(word_list)}
valid_words = set(word_list)

# Edges -> AdjList
adjList = dict()
for edge in graph['edges']:
	s, t, v = edge
	if (s not in adjList):
		adjList[s] = []
	if (t not in adjList):
		adjList[t] = []
	insert_s = True
	for tup in adjList[s]:
		if (tup[0] == t):
			insert_s = False
	if (insert_s):
		adjList[s].append((t, v))
	insert_t = True
	for tup in adjList[t]:
		if (tup[0] == s):
			insert_t = False
	if (insert_t):
		adjList[t].append((s, v))

# Sorts adjacency list by weight
for n in range(len(word_list)):
	adjList[n] = sorted(adjList[n], key=lambda x: x[1])

hubs = sorted(adjList.keys(), key=lambda x: len(adjList[x]), reverse=True)

# BFS Helper to measure path length
def bfs(s, t):
	v = set()
	q = queue.Queue()
	q.put((s, 0, [word_list[s]]))
	while(not q.empty()):
		n, dist, li = q.get()
		if (n == t):
			return (dist, li)
		v.add(n)
		for adj, weight in adjList[n]:
			if (adj in v):
				continue
			q.put((adj, dist+1, li[:]+[word_list[adj]]))
	return (None, [])

# Dijkstra measurement: Heuristic by path weight (not path length)
def dijkstra(s, t, decay=0):
	v = set()
	q = queue.PriorityQueue()
	q.put((0, s, 0, [word_list[s]]))
	while(not q.empty()):
		tot_dist, n, dist, li = q.get()
		if (n == t):
			return (tot_dist, li)
		v.add(n)
		for adj, weight in adjList[n]:
			if (adj in v):
				continue
			# Multiplicative
			# q.put(((tot_dist+weight)*(1+decay), adj, dist+1, li[:]+[word_list[adj]]))
			# Additive
			q.put((tot_dist+weight+decay, adj, dist+1, li[:]+[word_list[adj]]))
	return (None, [])

# Run a bunch of random bfs(source -> target) scans to determine average path length connectivity
#	k = 1000 | avg = 4.66500
def avg_path(k):
	size = len(word_list)
	p_len_tot = 0
	tot_num = k
	for i in range(k):
		if (i%10 == 0):
			print("...done {}/{}".format(i, k))
		s = random.randint(0, size-1)
		t = random.randint(0, size-1)
		cur_len = bfs(s, t)[0]
		if (cur_len is not None):
			p_len_tot += cur_len
		else:
			tot_num -= 1
	return p_len_tot/tot_num

# Help message for script
def run_help():
	print("Usage Instructions:")
	help_entries = []
	help_entries.append(("<prime> <target>:","Type in word pairs to query network path length between them"))
	help_entries.append(("<prime> <target> -d:", "Type in a word pair with the '-d' specifier to search based on edge weight"))
	help_entries.append(("<word>:","Type a single word to list its edges"))
	help_entries.append(("-help:","print this usage message"))
	help_entries.append(("-list:","list all nodes (words) in graph"))
	help_entries.append(("-quit:","exit program"))
	help_entries.append(("-hub <num>:","list top <num> most connected nodes in graph"))
	help_entries.append(("-avg <num>:","run <num> random searches through the graph to compute average path length"))
	max_hint_len = max([len(e[0]) for e in help_entries])
	print_string = "{:>"+str(max_hint_len+4)+"} {}"
	for e in help_entries:
		print(print_string.format(e[0], e[1]))
	print("")

# Interactive Script for us to query path lengths
def run():
	run_help()
	query = input(">>> ")
	while(query != "-quit"):
		if (query == "-list"):
			print(help_list)
			query = input(">>> ")
			continue
		if (query == "-help"):
			run_help()
			query = input(">>> ")
			continue
		try:
			source, target = query.split()[:2]
		except:
			source = query.split()[0]
			if (len(source) < 1):
				print("Query is empty")
				query = input(">>> ")
				continue
			else:
				try:
					for w, val in [(word_list[i], v) for i, v in adjList[word_to_idx[source]]]:
						print("   {:<15} {}".format(w, val))
				except KeyError:
					print("Word: {} NOT FOUND".format(source))
			query = input(">>> ")
			continue
		if (source == '-hub'):
			top = int(target)
			for idx in hubs[:top]:
				print("{} ({})".format(word_list[idx], len(adjList[idx])))
				for w, val in adjList[idx]:
					print("    {:<15} {}".format(word_list[w], val))
			query = input(">>> ")
			continue
		if (source == '-avg'):
			print("    Average path length: {:.5f}".format(avg_path(int(target))))
			query = input(">>> ")
			continue
		valid = True
		try:
			source_idx = word_to_idx[source]
		except KeyError:
			print("Word: {} NOT FOUND".format(source))
			valid = False
		try:
			target_idx = word_to_idx[target]
		except KeyError:
			print("Word: {} NOT FOUND".format(target))
			valid = False
		
		# If both are contained within our graph, we commence bfs lookup
		if (valid):
			terms = query.split()
			if (len(terms) > 2 and terms[2] == '-d'):
				dist, path = dijkstra(source_idx, target_idx, decay=float(terms[3]) if len(terms) > 3 else 0.0)
			else:
				dist, path = bfs(source_idx, target_idx)
			if (dist is not None):
				print("    Network distance: {}\n    Path: {}".format(dist, path))
			else:
				print("Path NOT FOUND. {} and {} are not connected in this graph".format(source, target))

		# Continue with next query
		query = input(">>> ")

run()