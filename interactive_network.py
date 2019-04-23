import sys
import json
import queue

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
with open(sys.argv[1], "r") as fin:
	graph = json.load(fin)
fin.close()

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

# Interactive Script for us to query path lengths
def run():
	print("Usage Instructions:")
	print("  <prime> <target>: Type in word pairs to query network path length between them")
	print("            <word>: Type a single word to list its edges")
	print("             -help: Type 'help' to list all nodes (words) in graph")
	print("             -quit: Type 'quit' to exit program")
	print("        -hub <num>: Type 'hub' to list top <num> most connected nodes in graph")
	query = input()
	while(query != "-quit"):
		if (query == "-help"):
			print(help_list)
			query = input()
			continue
		try:
			source, target = query.split()[:2]
		except:
			source = query.split()[0]
			if (len(source) < 1):
				print("Query is empty")
				query = input()
				continue
			else:
				try:
					for w, val in [(word_list[i], v) for i, v in adjList[word_to_idx[source]]]:
						print(w, val)
				except KeyError:
					print("Word: {} NOT FOUND".format(source))
			query = input()
			continue
		if (source == '-hub'):
			top = int(target)
			for idx in hubs[:top]:
				print("{} ({})".format(word_list[idx], len(adjList[idx])))
				for w, val in adjList[idx]:
					print("   ", word_list[w], val)
			query = input()
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
			dist, path = bfs(source_idx, target_idx)
			if (dist is not None):
				print("Network distance: {}\nPath: {}".format(dist, path))
			else:
				print("Path NOT FOUND. {} and {} are not connected in this graph".format(source, target))

		# Continue with next query
		query = input()

run()