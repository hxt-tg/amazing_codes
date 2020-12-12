from projection import ProjectionSimplexS3
from itertools import combinations
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = ["Times New Roman"]
matplotlib.use('Qt5Agg')

s3 = ProjectionSimplexS3()

valid_plot_style = ['scatter', 'curve', 'vector']

simplex_point = s3.project(np.diag([1.2] * 4))
simplex_point_name = ['X', 'Y', 'Z', 'W']

simplex_frame = [
    np.vstack((p1, p2)) for p1, p2 in
    combinations([
        s3.project(np.array([[1., 0., 0., 0.]])),
        s3.project(np.array([[0., 1., 0., 0.]])),
        s3.project(np.array([[0., 0., 1., 0.]])),
        s3.project(np.array([[0., 0., 0., 1.]])),
    ], 2)
]


def plot_data_on_simplex_s3(data, /, style='curve', interval=2, color='b', size=1):
    def _draw_vec_3d(x, y, z, x_t, y_t, z_t):
        plt.quiver(x, y, z, x_t - x, y_t - y, z_t - z, color=color)

    if style not in valid_plot_style:
        raise ValueError(f'Unsupported plot style. Support one of {valid_plot_style}.')

    data = s3.project(data)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for line in simplex_frame:
        ax.plot3D(line[:, 0], line[:, 1], line[:, 2], 'k')
    for point, name in zip(simplex_point, simplex_point_name):
        ax.text(point[0], point[1], point[2], name, color='k')

    if style == 'scatter':
        ax.scatter3D(data[:, 0], data[:, 1], data[:, 2], s=size, c=color)
    elif style == 'curve':
        ax.plot3D(data[:, 0], data[:, 1], data[:, 2], c=color)
    elif style == 'vector':
        d_from = data[::interval, :]
        d_to = data[interval - 1::interval, :]
        for i in range(d_from.shape[0]):
            _draw_vec_3d(d_from[i, 0], d_from[i, 1], d_from[i, 2], d_to[i, 0], d_to[i, 1], d_to[i, 2])

    scaling = np.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz'])
    ax.auto_scale_xyz(*[[np.min(scaling), np.max(scaling)]] * 3)
    ax.set_axis_off()
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    data_4d = np.array([
        [np.sin(x) / 5 + 1 / 5, np.cos(x) / 5 + 1 / 5, x / 150,
         1 - (np.sin(x) / 5 + 1 / 5 + np.cos(x) / 5 + 1 / 5 + x / 150)] for x in np.arange(0, 50, 0.25)
    ])
    print(f'data (4D) {simplex_point_name}:\n', data_4d)
    plot_data_on_simplex_s3(data_4d)
