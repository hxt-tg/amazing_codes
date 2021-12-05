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
        print(x.shape)
        # ax.quiver(x, y, dx, dy, width=size * 0.002, color=color, pivot='middle')
        ax.streamplot(x, y, dx, dy, color=color)

    single_graph = ax is None
    if single_graph:
        fig = plt.figure(figsize=(9, 9))
        ax = plt.gca()
    for line in simplex_frame:
        ax.plot(line[:, 0], line[:, 1], 'k')
    for point, name in zip(simplex_point, simplex_point_name):
        ax.text(point[0], point[1], name, color='k')

    for i in np.arange(0, 1 + 1e-7, interval):
        data_x, data_y, data_u, data_v = [], [], [], []
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
            data_x.append(x[0])
            data_y.append(x[1])
            data_u.append(d[0])
            data_v.append(d[1])
        _draw_vec_2d(np.array(data_x), np.array(data_y), np.array(data_u), np.array(data_v))

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
