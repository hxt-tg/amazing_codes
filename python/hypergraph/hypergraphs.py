import hypernetx.algorithms.generative_models as gm
from hypernetx.classes.entity import Entity, EntitySet
from itertools import combinations
from math import comb
from random import sample
from collections import Counter
import numpy as np
from numpy.random import random

__all__ = ['UniformRandomHypergraph', 'hypergraph_to_membership_matrix']


class UniformRandomHypergraph(gm.Hypergraph):
    def __init__(self, n_nodes, edge_size, n_links='1*Lc', start_id=0):
        self.N = n_nodes
        self.g = edge_size
        if isinstance(n_links, str):
            assert n_links.endswith('*Lc')
            self.L = int(int(n_links[:-3]) * self.L_c)
        elif isinstance(n_links, int):
            self.L = n_links
        else:
            raise ValueError('Invalid `n_links`.')
        self.start_id = start_id
        self.edge_dist = Counter(self.random_sample_from_combinations())
        self.edge_set = self.edge_dist.keys()
        super().__init__(self.edge_set)

    def random_sample_from_combinations(self):
        """Warning: This method may cause conflict/repeated edges under low number of nodes."""

        def _sub_sample(N, g, L, prev_: tuple = None):
            if g == 0:
                # leaves node
                return [prev_] * L
            if prev_ is None:
                prev_ = tuple()
                start = self.start_id
            else:
                start = prev_[-1] + 1
            sampled_nodes = Counter(self.sample_comb(N, g, start) for _ in range(L))

            result = sum((_sub_sample(N, g - 1, next_L, prev_=prev_ + (node,))
                          for node, next_L in sampled_nodes.items()), [])
            return result

        return _sub_sample(self.N, self.g, self.L)

    def sample_comb(self, N, g, start=1):
        rnd = 1 - np.power(1 - random(), 1 / g)
        return int(rnd * (N + self.start_id - g - start + 1)) + start

    @property
    def L_c(self):
        return np.log(self.N) * self.N / self.g


class PowerRandomHypergraph(UniformRandomHypergraph):
    def __init__(self, n_nodes, edge_size, n_links, mu, start_id=0):
        self.mu = mu
        assert 0 <= mu <= 1, "`mu` should be in [0, 1]."
        super().__init__(n_nodes, edge_size, n_links, start_id=start_id)

    def sample_comb(self, N, g, start=1):
        rnd = 1 - np.power(1 - random(), 1 / (g * (1 + self.mu)))
        return int(rnd * (N + self.start_id - g - start + 1)) + start


def hypergraph_to_membership_matrix(hg: gm.Hypergraph):
    nodes = list(hg.nodes())
    if isinstance(nodes[0], Entity):
        nodes = list(map(lambda x: x.uid, nodes))
    else:
        nodes = list(map(int, nodes))

    assert sum(not isinstance(_n, int) for _n in nodes) == 0, "Only support `int` nodes."
    n_nodes = max(nodes) + 1
    n_edges = hg.number_of_edges()
    mem_mat = np.zeros((n_nodes, n_edges))
    incidence_dict = hg.incidence_dict
    for e in hg.edges():
        e = e.uid if isinstance(e, Entity) else e
        for node in incidence_dict[e]:
            mem_mat[node, int(e)] = 1
    return mem_mat


# =========== TEST CODE ==========
def random_sample_from_combinations_low_performance(n_nodes, g, n_links):
    all_items = list(combinations(range(1, n_nodes + 1), g))
    return sample(all_items, k=n_links)


def recursive_combinations(n_nodes, size_edge):
    """TEST ONLY"""

    def _sub_comb(N, g, prev_: tuple = None):
        if g == 0:
            # leaves node
            return prev_
        end = N - (g - 1)
        if prev_ is None:
            prev_ = tuple()
            start = 1
        else:
            start = prev_[-1] + 1
        result = [_sub_comb(N, g - 1, prev_=prev_ + (s,)) for s in range(start, end + 1)]
        return result

    return _sub_comb(n_nodes, size_edge)

    # all_items = list(combinations(range(1, n_nodes + 1), size_edge))
    # return sample(all_items, k=n_edges)


# =========== END OF TEST CODE ==========

def check_degree_distribution(n=1000, g=3):
    import hypernetx.reports.descriptive_stats as stats
    import matplotlib.pyplot as plt
    prh = PowerRandomHypergraph(n, g, '1*Lc', mu=1)
    dist = np.array(sorted(list(stats.degree_dist(prh, aggregated=True).items()),
                           key=lambda x: x[0]))
    plt.plot(dist[:, 0], dist[:, 1], 'bo')
    plt.show()


if __name__ == '__main__':
    # print(len(random_sample_from_combinations_low_performance(5, 3, 3)))
    # print(comb(5, 2))
    # print(recursive_combinations(5, 3))
    check_degree_distribution()
