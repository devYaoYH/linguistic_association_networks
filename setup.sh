echo "Checking data/GoogleNews-vectors-negative300.bin Exists"
if [ -f "$data/GoogleNews-vectors-negative300.bin" ]; then
	if [ -d "$common_subset" ]; then
		mkdir common_subset
	fi
	echo "Running setup python scripts"
	python filter_words.py
	python save_dict.py
	python indexing_tree_setup.py
	python smallworld.py
	echo "Generated smallworld network graph as .json file"
else
	echo "Error, GoogleNews Vectors do not exist, please download them and unzip from: https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/"
fi