from projection import ProjectionSimplexS2
from itertools import combinations
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = ["Times New Roman"]
matplotlib.use('Qt5Agg')

s2 = ProjectionSimplexS2()

simplex_point = s2.project(np.diag([1.1] * 3))
simplex_point_name = ['X', 'Y', 'Z']

simplex_frame = [
    np.vstack((p1, p2)) for p1, p2 in
    combinations([
        s2.project(np.array([[1., 0., 0.]])),
        s2.project(np.array([[0., 1., 0.]])),
        s2.project(np.array([[0., 0., 1.]])),
    ], 2)
]


def plot_bimatrix_game(A, interval=0.05, color='b', size=2, ax=None):
    def _draw_vec_2d(x, y, dx, dy):
        ax.quiver(x, y, dx, dy, width=size * 0.002, color=color, pivot='middle')

    single_graph = ax is None
    if single_graph:
        fig = plt.figure(figsize=(9, 9))
        ax = plt.gca()
    for line in simplex_frame:
        ax.plot(line[:, 0], line[:, 1], 'k')
    for point, name in zip(simplex_point, simplex_point_name):
        ax.text(point[0], point[1], name, color='k')

    for i in np.arange(0, 1 + 1e-7, interval):
        for j in np.arange(0, 1 - i + 1e-7, interval):
            x = np.array([i, j, 1 - i - j])
            if abs(x[0] - 1) < 1e-9 or abs(x[1] - 1) < 1e-9 or abs(x[2] - 1) < 1e-9:
                continue
            d = s2.project(np.array([
                x[0] * ((A @ x)[0] - x.T @ A @ x),
                x[1] * ((A @ x)[1] - x.T @ A @ x),
                x[2] * ((A @ x)[2] - x.T @ A @ x)
            ])) + 1e-7
            x = s2.project(x)
            _draw_vec_2d(x[0], x[1], d[0], d[1])

    ax.set_aspect('equal')
    ax.set_axis_off()


if __name__ == '__main__':
    A = np.array([
        [0, -1, 1],
        [1, 0, -1],
        [-1, 1, 0]
    ])
    plot_bimatrix_game(A)
    plt.tight_layout()
    plt.show()
