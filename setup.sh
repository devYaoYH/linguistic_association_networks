echo "Checking data/GoogleNews-vectors-negative300.bin Exists"
if [ -f "data/GoogleNews-vectors-negative300.bin" ]; then
	if [ ! -d "common_subset" ]; then
		mkdir common_subset
	fi
	echo "Installing python dependencies"
	pip install --upgrade setuptools
	pip install -r whl_packages/req.txt
	echo "Finished installing python dependenceis :)"
else
	echo "Error, GoogleNews Vectors do not exist, please download them and unzip from: https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/"
fi