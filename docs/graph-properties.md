# Graph properties

We screened for properties of spatial structures that correlated with transitionability scores.
We included the following 21 graph properties in these analyses:

- Density - The density, d, of a graph is given by $d = \frac{2m}{n(n-1)}$ where n is the number of nodes and m is the number of edges in the graph.
- Mean degree - Average degree of all nodes in the graph.
- Median degree - Median degree of all nodes in the graph.
- Variance degree - Variance in degree values for all nodes in the graph.
- Girth - The girth of a graph is the length of the shortest cycle in the graph.
- Degree assortativity coefficient - Also known as assortative mixing. Measures the tendency for a graph's nodes to attach to others with a similar degree.
- Number of bridges - Number of "bridges" in the graph. A bridge is an edge that, if deleted, would increase the graph's number of connected components.
- Max clique size - Size of the largest clique (fully connected component) in the graph.
- Transitivity - The fraction of all possible triangle structures present in the graph.
- Average clustering - Estimate of the graph's [clustering coefficient](https://en.wikipedia.org/wiki/Clustering_coefficient).
- Number of connected components
- Number of articulation points - A node is an articulation point if removing that node and all of its edges would disconnect the graph.
- Average node connectivity - Average local connectivity of nodes in the graph.
- Edge Connectivity - The edge connectivity of the graph is the minimum number of edges that must be removed to disconnect the graph.
- Node Connectivity - The minimum number of nodes that must be removed to disconnect the graph.
- Diameter - Maximum eccentricity of the graph. The eccentricity of each node in the graph is equal to the maximum distance from that node to all other nodes in the graph.
- Radius - Minimum eccentricity of nodes in the graph graph.
- Kemeny constant - The expected number of steps to transition from one node to a random other node in the graph. This measures the time needed for spreading across a graph: low values indicate a closely connected graph, whereas large values indicate a more diffuse graph.
- Global Efficiency - The average efficiency of the graph. The efficiency of a pair of nodes is the multiplicative inverse of the shortest path distance between the nodes.
- Wiener index - Sum of the shortest-path distances between each pair of reachable nodes.
- Longest shortest path - the maximum path length among all shortest paths between all pairs of nodes in the graph.

The code used to compute these properties for each graph structure used in this work can be found in this repository `scripts/graph-properties.py`.
The majority of these properties were computed using the [networkx library](https://networkx.org/documentation/stable/index.html).