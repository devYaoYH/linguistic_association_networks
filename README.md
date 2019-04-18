# Constructing Networks from word2vec vectors

## Setup Instructions:

1. Download googlenews pre-trained vectors, unzip it and place it within a 'data/' folder in this project
2. Make sure you have python3.7 64bit installed and have it in your PATH
3. Run `sh setup.sh` bash script from an admin console
4. Run `sh cache.sh` bash script to run python scripts to generate file dependencies
5. Run `python network.py -t gexf <graph> <limit>` to run the graph generating script and generate a .gexf graph output for visualization
6. See `python network.py -h` for the full utilization options

A `network_<graph>_<limit>.json` file will be generated which contains our graph information.

## Graph Visualization:

[Gephi](https://gephi.org/) is used to visualize our graph data.

![Sample.PNG](sample.PNG)

The above network is plotted using the data in complete_network_tight3.gexf generated from running `python network.py -t gexf -f complete_network_tight3 complete 1000 3 15`. It contains 1000 Nodes (representing the top 1000 most frequently used english words) and 6465 Edges.

Filtering low-similarity edges (cosine similarity further from 1) from our initially dense complete graph:
```python
dist = abs(1 - model.get_distance(source, word_to_idx[ow]))
if (dist > 0.1 and edges > k):
	break
```
We limit a 0.1 deviation from 1 (exactly similar) to our edges (but ensure we have at least k edges per node).

## References:
1. http://www.leonidzhukov.net/hse/2015/networks/lectures/lecture4.pdf
	- Preferential attachment models
	- Random method of growing smallworld networks adopted in implementation
2. https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit?usp=sharing
	- Pre-trained Google word2vec vectors (3 million words | 300 dimensions)
3. https://github.com/first20hours/google-10000-english/blob/master/google-10000-english.txt
	- Top 10000 common english words (used to take subset of the pretrained vectors)
4. https://gist.github.com/sebleier/554280
	- List to filter out common 'stopwords' - Not much semantic meaning here