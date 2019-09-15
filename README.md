# Results

## Nelson 5018 Semantic Association Wordlist

![Nelson Word Network](nelson_bkg-01.png)

Graphed using a pruned complete network by cosine similarity distance between nodes (`abs(a.dot(b) - 1) < 0.1`) and a minimum number of 3 edges for each node.

Even within a much larger dataset, we observe clustering effects among the semantic concepts. For this graph, we have a average local clustering coefficient of `0.19355`.

### Predicting Response Times using path length in network

Using our constructed network, we query it with the (prompt, target) pairs given to human subjects and extract the path lenghts from prompt to target. To examine how this extracted path length is related to measured response time in human subjects, an average of each subjects' response time to a given (prompt, target) pair is taken. This mean is then added to the respective list for its path length. 

For example: the (prompt, target) pair (REVIEW, ADJECTIVE) has the path (review evaluate understand describe adjective) in our network with a path length of 5. The mean response time to the demasking task amongst all subjects who were presented with the (REVIEW, ADJECTIVE) prompt is then added to a list containing response times of all paths with length 5 (in our network).

*In this comparison, the minimum path length is **2** for a target that is directly connected to a prompt.*

### Mean response times of (prompt, target) pairs grouped by observed network path lengths from prompt to target:

![Nelson RT against Path Length Plot](nelson_plottedRT.png)

| Path Length | Mean Response Times | Standard Deviation | Number of Pairs |
| ----------- |:-------------------:| ------------------:| ---------------:|
| 2 | 1850.672788 | 253.341439 | 30 |
| 3 | 1955.860505 | 395.233799 | 69| 
| 4 | 2142.147454 | 455.5789075 | 87 |
| 5 | 2218.92387  | 475.9042756 | 102 |
| 6 | 2254.852955 | 529.4472688 | 125 |
| 7 | 2339.68549  | 466.4608815 | 58 |
| 8 | 2107.908918 | 279.5967494 | 4 |

Probably due to forcing a minimum of 3 edges for each node, we have a maximum path length of only 8. Results from [2-7] are promising though as a clear increasing trend is observed. Removing this minimum limit would likely yield a better result (strictly increasing trend perhaps?)