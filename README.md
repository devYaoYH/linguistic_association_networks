# Constructing Smallworld Networks from word2vec vectors

##Setup Instructions:

1. Download googlenews pre-trained vectors, unzip it and place it within a 'data/' folder in this project
2. Make sure you have python3.7 64bit installed and have it in your PATH
3. Run `sh setup.sh` bash script from an admin console
4. Run `sh cache.sh` bash script to run python scripts to generate file dependencies
5. Run `python smallworld.py` to run the graph generating script

A `smallworld_network.json` file will be generated which contains our graph information.

##References:
1. http://www.leonidzhukov.net/hse/2015/networks/lectures/lecture4.pdf
	- Preferential attachment models
	- Random method of growing smallworld networks adopted in implementation
2. https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit?usp=sharing
	- Pre-trained Google word2vec vectors (3 million words | 300 dimensions)
3. https://github.com/first20hours/google-10000-english/blob/master/google-10000-english.txt
	- Top 10000 common english words (used to take subset of the pretrained vectors)
4. https://gist.github.com/sebleier/554280
	- List to filter out common 'stopwords' - Not much semantic meaning here