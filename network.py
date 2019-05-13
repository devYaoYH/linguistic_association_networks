import sys
import json
from annoy import AnnoyIndex
import numpy as np
import random

# Implemented Graphing Types
networks = ["complete", "smallworld"]
COMPLETE = networks[0]
SMALLWORLD = networks[1]

DATASET = "nelson_5018"

# Parse Command Line Arguments
args = []
opt = COMPLETE
type_args = [3, 10]
limit = 5013
optional_args = dict()
i = 1
while(i < len(sys.argv)):
    arg = sys.argv[i]
    if (arg[0] == '-'):
        if (arg[1:] == 'h'):
            print("[Usage] python network.py -t <extension> -f <filename> <opt> <nodes> <args>")
            print("Flags (Optional):")
            print("        -t    <gexf,json>")
            print("        -f    <filename_without_extension>")
            print("Compulsory Arguments:")
            print("     <opt>    type of network [complete/smallworld]")
            print("   <nodes>    max(1000)")
            print("    <args>    network-specific parameters")
            print("<args>:")
            print("smallworld    m(num edges per turn), k(k-nearest)")
            print("  complete    k(min edges per node), k2(max edges per node)")
            sys.exit()
        optional_args[arg[1:]] = sys.argv[i+1]
        i += 1
    else:
        args.append(arg)
    i += 1

if (len(args) > 0):
    opt = args[0]
if (len(args) > 1):
    limit = min(limit, int(args[1]))
if (len(args) > 2):
    type_args = [int(i) for i in args[2:]]

if (opt not in networks):
    print("Error, graph type: {} Not Recognized".format(opt))
    exit()

print("Generating {} Graph with {} Nodes | Arguments: {}".format(opt, limit, type_args))

# Load from small dataset
vsm = dict()
word_list = []
word_to_idx = dict()
stopwords_filter = set()

print("Loading VSM .... ", end="")
sys.stdout.flush()
with open("common_subset/" + DATASET + ".json", "r") as fin:
    vsm = json.load(fin)
fin.close()
print("done")
sys.stdout.flush()

if (False):
    print("Loading nltk english stopwords ... ", end="")
    sys.stdout.flush()
    with open("nltk_stopwords.txt", "r") as fin:
        for line in fin:
            stopwords_filter.add(line.split()[0])
    fin.close()
    print("done")
    sys.stdout.flush()

print("Loading " + DATASET + "words ... ", end="")
sys.stdout.flush()
with open("common_subset/" + DATASET + ".txt", "r") as fin:
    conut = 0
    for line in fin:
        w = line.split()[0]
        if (w not in stopwords_filter and len(w) > 1):
            word_list.append(w)
            word_to_idx[w] = conut
            conut += 1
fin.close()
word_list = word_list[:limit]
print("done")
sys.stdout.flush()

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
            sys.stdout.flush()
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
        model.load(DATASET + ".ann")
        print("Annoying Tree Loaded")
        sys.stdout.flush()

###############################
# WRITE GRAPH TO FILE FORMATS #
###############################
# Write to .json
def write_json(graph, fname):
    json_graph = dict()
    json_graph['nodes'] = {'name': n for n in graph['nodes']}
    # 'source': 0, 'target': 0, 'value': 0
    json_graph['links'] = [{'source': graph['edges'][k][0], 'target': graph['edges'][k][1], 'value': graph['edges'][k][2]} for k in range(len(graph['edges']))]
    with open(fname, "w+") as fout:
        json.dump(json_graph, fout)
    fout.close()
    with open(fname.split('.')[0]+"_log.json", "w+") as fout:
        json.dump(graph, fout);
    fout.close()

# Write to .gexf
def write_gexf(graph, fname):
    print("Generating .gexf file for graph with {} Nodes | {} Edges".format(len(graph['nodes']), len(graph['edges'])))
    # Write Actual file in proper format
    gexf_header = """<?xml version="1.0" encoding="UTF-8"?>
    <gexf xmlns="http://www.gexf.net/1.2draft" version="1.2">
        <meta lastmodifieddate="2009-03-20">
            <creator>devYaoYH</creator>
            <description>Linguistic Association Network Graph</description>
        </meta>
        <graph mode="static" defaultedgetype="undirected">
            <nodes>"""
    gexf_footer = """            </edges>
        </graph>
    </gexf>"""
    with open(fname, "w+") as fout:
        fout.write(gexf_header)
        # Extract All Nodes Information
        for i, node in enumerate(graph['nodes']):
            fout.write("                <node id=\"{}\" label=\"{}\" />\n".format(i, node))
        fout.write("            </nodes>\n            <edges>\n")
        # Extract All Edges Information
        for i, tup in enumerate(graph['edges']):
            source, target, value = tup
            fout.write("                <edge id=\"{}\" source=\"{}\" target=\"{}\" />\n".format(i, source, target))
        fout.write(gexf_footer)
    fout.close()
    with open(fname.split('.')[0]+"_log.json", "w+") as fout:
        json.dump(graph, fout);
    fout.close()


############################
# GRAPH PLOTTING UTILITIES #
############################
# Uniform Random build our smallworld network
def random_smallworld(m, k):    # m -> Number of edges formed per iteration | k -> Number of neighbors 'activated'
    global model
    global limit
    global opt
    if (model is None):
        load_tree()
    graph = dict()
    graph['nodes'] = word_list
    graph['edges'] = []
    for w in word_list:
        cur_idx = word_to_idx[w]
        li = model.get_nns_by_item(cur_idx, k)
        # We pick m nodes to connect with
        for i in range(m):
            source = cur_idx
            target = random.choice(li)
            value = model.get_distance(source, target)
            graph['edges'].append((source, target, value))

    # Write result to file
    fname = "network_{}_{}".format(opt, limit)
    if ('f' in optional_args):
        fname = optional_args['f']
    if ('t' in optional_args):
        if (optional_args['t'] == 'json'):
            write_json(graph, "{}.json".format(fname))
        elif (optional_args['t'] == 'gexf'):
            write_gexf(graph, "{}.gexf".format(fname))
    else:
        write_json(graph, "{}.json".format(fname))

# Complete Graph - We connect at least the k-nearest nodes
def complete_network(k, k2=None):
    global model
    global limit
    global opt
    if (k2 is None):
        k2 = k + 10
    if (model is None):
        load_tree()
    graph = dict()
    graph['nodes'] = word_list
    graph['edges'] = []    # 'source': 0, 'target': 0, 'value': 0

    # cur_idx = 0
    # source = cur_idx
    # li = sorted([(ow, abs(1 - model.get_distance(source, word_to_idx[ow]))) for ow in word_list if word_to_idx[ow] != cur_idx], key=lambda x: x[1])
    # print(word_list[0], li)

    for w in word_list:
        #print(w)
        cur_idx = word_to_idx[w]
        source = cur_idx
        li = sorted([(word_to_idx[ow], abs(1 - model.get_distance(source, word_to_idx[ow]))) for ow in word_list if word_to_idx[ow] != cur_idx], key=lambda x: x[1])
        #print("Processing word: {} | len(li): {}".format(cur_idx, len(li)))
        #li = model.get_nns_by_item(cur_idx, k)
        # We connect all k-nearest nodes
        tmp_neighbors = 0
        for target, value in li:
            if ((value > 0.1 and tmp_neighbors > k) or tmp_neighbors > k2):
                break
            tmp_neighbors += 1
            graph['edges'].append((source, target, value))

    # Write result to file
    fname = "network_{}_{}".format(opt, limit)
    if ('f' in optional_args):
        fname = optional_args['f']
    if ('t' in optional_args):
        if (optional_args['t'] == 'json'):
            write_json(graph, "{}.json".format(fname))
        elif (optional_args['t'] == 'gexf'):
            write_gexf(graph, "{}.gexf".format(fname))
    else:
        write_json(graph, "{}.json".format(fname))

#############
# EXECUTION #
#############
#interactive_test()
if (opt == SMALLWORLD):
    random_smallworld(type_args[0], type_args[1])
elif (opt == COMPLETE):
    if (len(type_args) < 2):
        complete_network(type_args[0])
    else:
        complete_network(type_args[0], k2=type_args[1])