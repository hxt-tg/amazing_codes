from .projection import ProjectionSimplexS2
from itertools import combinations
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = ["Times New Roman"]
matplotlib.use('Qt5Agg')

s2 = ProjectionSimplexS2()

valid_plot_style = ['scatter', 'curve', 'vector',
                    '3d_scatter', '3d_curve', '3d_vector']

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


def plot_data_on_simplex_s2(data, /, style='curve', interval=2, color='b', size=1):
    def _draw_vec_2d(x, y, x_t, y_t):
        plt.quiver(x, y, x_t - x, y_t - y, width=size * 0.002, color=color, pivot='mid')

    def _draw_vec_3d(x, y, z, x_t, y_t, z_t):
        plt.quiver(x, y, z, x_t - x, y_t - y, z_t - z, color=color)

    if style not in valid_plot_style:
        raise ValueError(f'Unsupported plot style. Support one of {valid_plot_style}.')

    fig = plt.figure()
    if style.startswith('3d_'):
        ax = fig.add_subplot(111, projection='3d')
    else:
        data = s2.project(data)
        ax = fig.add_subplot(111)
        for line in simplex_frame:
            ax.plot(line[:, 0], line[:, 1], 'k')
        for point, name in zip(simplex_point, simplex_point_name):
            ax.text(point[0], point[1], name, color='k')

    if style == 'scatter':
        ax.scatter(data[:, 0], data[:, 1], s=size, c=color)
    elif style == 'curve':
        ax.plot(data[:, 0], data[:, 1], c=color)
    elif style == 'vector':
        d_from = data[::interval, :]
        d_to = data[interval - 1::interval, :]
        for i in range(d_from.shape[0]):
            _draw_vec_2d(d_from[i, 0], d_from[i, 1], d_to[i, 0], d_to[i, 1])
    elif style == '3d_scatter':
        ax.scatter3D(data[:, 0], data[:, 1], data[:, 2], s=size, c=color)
    elif style == '3d_curve':
        ax.plot3D(data[:, 0], data[:, 1], data[:, 2], c=color)
    elif style == '3d_vector':
        d_from = data[::interval, :]
        d_to = data[interval - 1::interval, :]
        for i in range(d_from.shape[0]):
            _draw_vec_3d(d_from[i, 0], d_from[i, 1], d_from[i, 2], d_to[i, 0], d_to[i, 1], d_to[i, 2])

    if style.startswith('3d_'):
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])
        ax.set_zlim([0, 1])
        scaling = np.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz'])
        ax.auto_scale_xyz(*[[np.min(scaling), np.max(scaling)]] * 3)
    else:
        ax.set_aspect('equal')
        ax.set_axis_off()
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    data_3d = np.array([
        [np.sin(x) / 8 + 1 / 3, np.cos(x) / 8 + 1 / 4 + x / 200,
         1 - (np.sin(x) / 8 + 1 / 3 + np.cos(x) / 8 + 1 / 4 + x / 200)] for x in np.arange(-10, 40, 0.05)
    ])
    print('data (3D) [x, y, z]:\n', data_3d)
    plot_data_on_simplex_s2(data_3d, style='3d_curve')
