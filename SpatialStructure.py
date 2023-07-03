"""
Programmer: John Shea
Project: Spatial Structure
Date: 06/30/2023
Version: 1

Reference
NetworkX
Aric A. Hagberg, Daniel A. Schult and Pieter J. Swart,
“Exploring network structure, dynamics, and function using NetworkX”,
 in Proceedings of the 7th Python in Science Conference (SciPy2008),
 Gäel Varoquaux, Travis Vaught, and Jarrod Millman (Eds), (Pasadena, CA USA), pp. 11–15, Aug 2008
"""

from itertools import chain
from itertools import tee
import math
from collections import defaultdict

import networkx as nx
from networkx.generators.random_graphs import _random_subset
from networkx.utils import py_random_state

from classic import complete_graph, empty_graph, path_graph, star_graph
from degree_seq import degree_sequence_tree

def fast_gnp_random_graph(n, p, seed=None, directed=False):
    """Returns a $G_{n,p}$ random graph, also known as an Erdős-Rényi graph or
    a binomial graph.

    Parameters
    ----------
    n : int
        The number of nodes.
    p : float
        Probability for edge creation.
    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.
    directed : bool, optional (default=False)
        If True, this function returns a directed graph.

    Notes
    -----
    The $G_{n,p}$ graph algorithm chooses each of the $[n (n - 1)] / 2$
    (undirected) or $n (n - 1)$ (directed) possible edges with probability $p$.

    This algorithm [1]_ runs in $O(n + m)$ time, where `m` is the expected number of
    edges, which equals $p n (n - 1) / 2$. This should be faster than
    :func:`gnp_random_graph` when $p$ is small and the expected number of edges
    is small (that is, the graph is sparse).

    See Also
    --------
    gnp_random_graph

    References
    ----------
    .. [1] Vladimir Batagelj and Ulrik Brandes,
       "Efficient generation of large random networks",
       Phys. Rev. E, 71, 036113, 2005.
    """
    G = empty_graph(n)

    if p <= 0 or p >= 1:
        return nx.gnp_random_graph(n, p, seed=seed, directed=directed)

    lp = math.log(1.0 - p)

    if directed:
        G = nx.DiGraph(G)
        v = 1
        w = -1
        while v < n:
            lr = math.log(1.0 - seed.random())
            w = w + 1 + int(lr / lp)
            while w >= v and v < n:
                w = w - v
                v = v + 1
            if v < n:
                G.add_edge(w, v)

    # Nodes in graph are from 0,n-1 (start with v as the second node index).
    v = 1
    w = -1
    while v < n:
        lr = math.log(1.0 - seed.random())
        w = w + 1 + int(lr / lp)
        while w >= v and v < n:
            w = w - v
            v = v + 1
        if v < n:
            G.add_edge(v, w)
    return G

def barabasi_albert_graph(n, m, seed=None, initial_graph=None):
    """Returns a random graph using Barabási–Albert preferential attachment

    A graph of $n$ nodes is grown by attaching new nodes each with $m$
    edges that are preferentially attached to existing nodes with high degree.

    Parameters
    ----------
    n : int
        Number of nodes
    m : int
        Number of edges to attach from a new node to existing nodes
    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.
    initial_graph : Graph or None (default)
        Initial network for Barabási–Albert algorithm.
        It should be a connected graph for most use cases.
        A copy of `initial_graph` is used.
        If None, starts from a star graph on (m+1) nodes.

    Returns
    -------
    G : Graph

    Raises
    ------
    NetworkXError
        If `m` does not satisfy ``1 <= m < n``, or
        the initial graph number of nodes m0 does not satisfy ``m <= m0 <= n``.

    References
    ----------
    .. [1] A. L. Barabási and R. Albert "Emergence of scaling in
       random networks", Science 286, pp 509-512, 1999.
    """

    if m < 1 or m >= n:
        raise nx.NetworkXError(
            f"Barabási–Albert network must have m >= 1 and m < n, m = {m}, n = {n}"
        )

    if initial_graph is None:
        # Default initial graph : star graph on (m + 1) nodes
        G = star_graph(m)
    else:
        if len(initial_graph) < m or len(initial_graph) > n:
            raise nx.NetworkXError(
                f"Barabási–Albert initial graph needs between m={m} and n={n} nodes"
            )
        G = initial_graph.copy()

    # List of existing nodes, with nodes repeated once for each adjacent edge
    repeated_nodes = [n for n, d in G.degree() for _ in range(d)]
    # Start adding the other n - m0 nodes.
    source = len(G)
    while source < n:
        # Now choose m unique nodes from the existing nodes
        # Pick uniformly from repeated_nodes (preferential attachment)
        targets = _random_subset(repeated_nodes, m, seed)
        # Add edges to m nodes from the source.
        G.add_edges_from(zip([source] * m, targets))
        # Add one node to the list for each new edge just created.
        repeated_nodes.extend(targets)
        # And the new node "source" has m edges to add to the list.
        repeated_nodes.extend([source] * m)

        source += 1
    return G

def pairwise(iterable, cyclic=False):
    "s -> (s0, s1), (s1, s2), (s2, s3), ..."
    a, b = tee(iterable)
    first = next(b, None)
    if cyclic is True:
        return zip(a, chain(b, (first,)))
    return zip(a, b)

def cycle_graph(n, create_using=None):
    """Returns the cycle graph $C_n$ of cyclically connected nodes.

    $C_n$ is a path with its two end-nodes connected.

    Parameters
    ----------
    n : int or iterable container of nodes
        If n is an integer, nodes are from `range(n)`.
        If n is a container of nodes, those nodes appear in the graph.
        Warning: n is not checked for duplicates and if present the
        resulting graph may not be as desired. Make sure you have no duplicates.
    create_using : NetworkX graph constructor, optional (default=nx.Graph)
       Graph type to create. If graph instance, then cleared before populated.

    Notes
    -----
    If create_using is directed, the direction is in increasing order.

    """
    _, nodes = n
    G = empty_graph(nodes, create_using)
    G.add_edges_from(pairwise(nodes, cyclic=True))
    return G

def grid_2d_graph(m, n, periodic=False, create_using=None):
    """Returns the two-dimensional grid graph.

    The grid graph has each node connected to its four nearest neighbors.

    Parameters
    ----------
    m, n : int or iterable container of nodes
        If an integer, nodes are from `range(n)`.
        If a container, elements become the coordinate of the nodes.

    periodic : bool or iterable
        If `periodic` is True, both dimensions are periodic. If False, none
        are periodic.  If `periodic` is iterable, it should yield 2 bool
        values indicating whether the 1st and 2nd axes, respectively, are
        periodic.

    create_using : NetworkX graph constructor, optional (default=nx.Graph)
        Graph type to create. If graph instance, then cleared before populated.

    Returns
    -------
    NetworkX graph
        The (possibly periodic) grid graph of the specified dimensions.

    """
    G = empty_graph(0, create_using)
    row_name, rows = m
    col_name, cols = n
    G.add_nodes_from((i, j) for i in rows for j in cols)
    G.add_edges_from(((i, j), (pi, j)) for pi, i in pairwise(rows) for j in cols)
    G.add_edges_from(((i, j), (i, pj)) for i in rows for pj, j in pairwise(cols))

    try:
        periodic_r, periodic_c = periodic
    except TypeError:
        periodic_r = periodic_c = periodic

    if periodic_r and len(rows) > 2:
        first = rows[0]
        last = rows[-1]
        G.add_edges_from(((first, j), (last, j)) for j in cols)
    if periodic_c and len(cols) > 2:
        first = cols[0]
        last = cols[-1]
        G.add_edges_from(((i, first), (i, last)) for i in rows)
    # both directions for directed
    if G.is_directed():
        G.add_edges_from((v, u) for u, v in G.edges())
    return G

def main():
    random_graph = barabasi_albert_graph(10,8)
    random_graph(10,8,None,None)
    print(random_graph)

if __name__ == '__main__':
    main()