import os
import sys
import json
import numpy
import inspect

# Add our own package directory
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "\\scripts")
import scripts

print(sys.path)

clsmembers = inspect.getmembers(sys.modules['scripts'], inspect.isfunction)
print(clsmembers)

# CONSTS
TOP = ""
ANALYSIS = "analysis"
__ENVIRONMENTS__ = [TOP, ANALYSIS]

# GLOBALS
__stack__ = []
__context__ = TOP			# Top-level entry context

#####################
# Context Variables #
#####################
_model = None				# Gensim VSM
_ANNTree = None				# Annoy Indexing Tree
_wordlist = None			# Currently loaded wordlis
t_graph = None				# Currently loaded graph

# Help Instructions
help_entries = {}

# Help Entry for 'default' context
help_entries[TOP] = []
help_entries[TOP].append(("help <cmd>:","prints help message for the given optional command | Defaults to top-level context"))
help_entries[TOP].append(("exit:", "exits shell"))

# Help Entry for 'analysis' context
help_entries[ANALYSIS] = []
help_entries[ANALYSIS].append(("<prime> <target>:","Type in word pairs to query network path length between them"))
help_entries[ANALYSIS].append(("<prime> <target> -d:", "Type in a word pair with the '-d' specifier to search based on edge weight"))
help_entries[ANALYSIS].append(("<word>:","Type a single word to list its edges"))
help_entries[ANALYSIS].append(("-help:","print this usage message"))
help_entries[ANALYSIS].append(("-list:","list all nodes (words) in graph"))
help_entries[ANALYSIS].append(("-quit:","exit program"))
help_entries[ANALYSIS].append(("-hub <num>:","list top <num> most connected nodes in graph"))
help_entries[ANALYSIS].append(("-avg <num>:","run <num> random searches through the graph to compute average path length"))
	
# Print init help msg
def print_init():
	print("")
	print("###################################")
	print("# Interactive Graph Query Console #")
	print("###################################")
	print("")

######################
# Built-in Functions #
######################
# Help Utility
def top_help(argv):
	entries = help_entries[TOP]
	if (len(argv) > 0):
		try:
			entries = help_entries[argv[0]]
		except KeyError:
			print("Environment '{}' Not Found".format(argv[0]))
			return
	print("Usage Instructions:")
	max_hint_len = max([len(e[0]) for e in entries])
	print_string = "{:>"+str(max_hint_len+4)+"} {}"
	for e in entries:
		print(print_string.format(e[0], e[1]))
	print("")

# Transition Functions
def start_env(argv):
	global __stack__
	global __context__
	if (len(argv) < 1 or argv[0] not in __ENVIRONMENTS__):
		print("Error, {} does not describe a valid Environment".format(argv[0]))
	else:
		__stack__.append(__context__)
		__context__ = argv[0]

def quit_env(argv):
	global __stack__
	global __context__
	if (len(__stack__) < 1):
		print("Error, we are at TOP, use 'exit' to quit shell")
	else:
		__context__ = __stack__.pop()

# Linking in graph formatting/creation process
def load_model(argv):
	global _model
	_model = scripts.load_gensim(" ".join(argv))

def unload_model(argv):
	global _model
	if (_model is not None):
		del _model
		_model = None

def subset_model(argv):
	global _model
	global _wordlist

	if (_model is None):
		print("Error: Use 'model' to load word2vec VSM first")
		return

	_wordlist = filter_words(" ".join(argv), model=_model)

#####################
# Built in commands #
#####################
builtin_cmd = {
	TOP: {
		"help": top_help,
		"model": load_model,
		"unload": unload_model,
		"subset": subset_model
	},
	ANALYSIS: {
		#"load": analysis_load,
		#"save": analysis_save,
		#"list": analysis_list_nodes,
		"quit": quit_env
		#"hub": analysis_hubs,
		#"avg": analysis_avg
	}
}

# Run built-in command
def run(argv):
	cmd = argv[0]
	# Run built-in command
	if (cmd in builtin_cmd[__context__]):
		builtin_cmd[__context__][cmd](argv[1:])
	# Attempt to Execute external shell process
	else:
		print("Command {} NOT FOUND".format(cmd))

# Interactive Console
print_init()
query = input(">>> ")
while (query != "exit"):
	run(query.split())
	query = input(">>> ")