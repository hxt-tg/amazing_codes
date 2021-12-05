# Dependencies: pip install igraph celluloid
import numpy as np
import random
import matplotlib.pyplot as plt
from numba import jit
# import hypernetx.algorithms as hx
import hypernetx.algorithms.generative_models as gm
from hypergraphs import UniformRandomHypergraph, hypergraph_to_membership_matrix

g = 5
n = 2000
m = 1400
k = 7
alpha = 0.6
G = np.array([[1, 0], [2, 0]], dtype=np.float64)
action_num = 2
action_space = np.array(list(range(action_num)), dtype=np.int64)
r = 10

T = 10000

tau = 2
eta = 0.1

mem_adj = np.zeros(0)  # should be numpy.ndarray


@jit(nopython=True)
def initial():
    # a = np.zeros((n, m), dtype=np.float64)
    # # b =[i for i in range(n)]
    # b = np.arange(n)
    #
    # for L in range(m):
    #     c = np.random.choice(b, g, replace=False)
    #     # c = random.sample(b, g)
    #     for x in range(g):
    #         a[c[x]][L] = 1
    # print('total', np.sum(a))
    return mem_adj


@jit(nopython=True)
def init_q_table():
    Q_table = np.array([[0, 0]] * n, dtype=np.float64)
    for q in Q_table:
        q[0] = beta(20, 80, 0, 3)
        q[1] = beta(10, 90, 0, 3)
    return Q_table


@jit(nopython=True)
def update_policy(Q_table, policy, i):
    policy[i] = np.exp(tau * Q_table[i]) / np.sum(np.exp(tau * Q_table[i]))


@jit(nopython=True)
def beta(a, b, r_min, r_max):
    k = (r_max - r_min) * np.random.beta(a, b) + r_min
    return k


@jit(nopython=True)
def update_action(policy, action, i):
    action[i] = action_space[np.searchsorted(
        np.cumsum(policy[i]), np.random.random(), side="right")]


@jit(nopython=True)
def get_av_Q(Q_table, i):
    return np.sum(Q_table[:, i]) / n


@jit(nopython=True)
def get_av_x(policy, i):
    return np.sum(policy[:, i]) / n


@jit(nopython=True)
def algorithm(r):
    x_history = []
    r_history = []
    theta = np.array([0] * n, dtype=np.int64)
    action = np.array([0] * n, dtype=np.int64)
    policy = np.array([[0, 0]] * n, dtype=np.float64)
    reward = np.array([0] * n, dtype=np.float64)
    rcount = np.array([0] * n, dtype=np.float64)
    Q_table = init_q_table()
    a_array = initial()

    for i in range(n):
        update_policy(Q_table, policy, i)
    t = 0
    while t < T:
        x = []
        q = []
        for i in range(action_num):
            x.append(get_av_x(policy, i))
            q.append(get_av_Q(Q_table, i))
        x_history.append(x)
        r_history.append(q)
        t += 1

        for i in range(n):
            reward[i] = 0
            rcount[i] = 0
            update_action(policy, action, i)

        m_num = np.count_nonzero(a_array, axis=0)
        # m_num = m_num.astype(np.float64)
        c_idx = np.zeros_like(action, dtype=np.float64)
        c_idx[action == 0] = 1
        # print(c_idx, a_array)
        c_num = c_idx @ a_array

        # print(c_num)
        # print(c_idx * a_array)
        # print(np.mat(c_idx) * a_array)
        # print(np.array([c_idx]) * a_array)
        # print("c_idx.shape:", c_idx.shape)
        # print("np.mat(c_idx).shape", np.mat(c_idx).shape)
        # print("a_array.shape", a_array.shape)

        # print("np.mat(c_idx):", np.mat(c_idx))
        # print("a_array:", a_array)
        # np.savetxt("{}array.csv".format(t), a_array, delimiter=',', fmt="%d")
        # rewards_m = np.squeeze(c_num * r / m_num, axis=0)
        # print(r)
        # print(c_num * r)
        rewards_m = c_num * r / m_num
        # print(rewards_m)

        for i in range(n):
            for j in range(m):
                if a_array[i][j] == 1:
                    rcount[i] += 1
                    if action[i] == 0:  # c
                        reward[i] += -1 + rewards_m[j]
                    elif action[i] == 1:  # d
                        reward[i] += rewards_m[j]

        for i in range(n):
            reward[i] = reward[i] / rcount[i] if rcount[i] != 0 else 0
            Q_table[i][action[i]] = (1 - eta) * Q_table[i][action[i]] + eta * reward[i]
            update_policy(Q_table, policy, i)
            theta[i] = 0

    return x_history, r_history, Q_table


def main():
    labels = ['C', 'D']
    print(n)
    colors = [(77 / 255, 133 / 255, 189 / 255), (247 / 255, 144 /
                                                 255, 61 / 255), (89 / 255, 169 / 255, 90 / 255)]
    import tqdm

    for r in np.linspace(1, g, 51):
        # print("here:", r)
        x_history, r_history, Q_table, = algorithm(r)
        x = np.mean(x_history[-1000:], axis=0)
        print(r, x)


def build_graph():
    """Graph nodes start at 0."""
    # hyper_g = gm.Hypergraph([{0, 1}, {0, 1, 2}, {0, 1, 12}, {3, 4}])
    # hyper_g = gm.erdos_renyi_hypergraph(20, 30, 0.3)
    hyper_g = UniformRandomHypergraph(100, 5, 200)

    global mem_adj, n, m
    mem_adj = hypergraph_to_membership_matrix(hyper_g)
    n, m = mem_adj.shape


if __name__ == '__main__':
    build_graph()
    main()
