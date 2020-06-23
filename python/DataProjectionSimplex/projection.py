import abc

import numpy as np
import matplotlib.pyplot as plt


class Projection(metaclass=abc.ABCMeta):
    def __init__(self):
        self.projection_matrix = None

    def project(self, points: np.ndarray):
        return (self.projection_matrix @ points.T).T


class ProjectionSimplexS2(Projection):
    def __init__(self):
        super().__init__()
        self.projection_matrix = np.array([
            [0, 1]
        ])


class ProjectionSimplexS3(Projection):
    def __init__(self):
        super().__init__()
        self.projection_matrix = np.array([
            [-np.cos(1 / 6 * np.pi), np.cos(1 / 6 * np.pi), 0.],
            [-np.sin(1 / 6 * np.pi), -np.sin(1 / 6 * np.pi), 1.]
        ])


class ProjectionSimplexS4(Projection):
    def __init__(self):
        super().__init__()
        self.projection_matrix = np.array([
            [2 / 3 * np.sqrt(2), -np.sqrt(2) / 3, -np.sqrt(2) / 3, 0.],
            [0, np.sqrt(6) / 3, -np.sqrt(6) / 3, 0.],
            [-1 / 3, -1 / 3, -1 / 3, 1.]
        ])


if __name__ == '__main__':
    data_2d = np.array([
        [1., 0.],
        [0., 1.],
        [0.1, 0.9],
    ])
    data_3d = np.array([
        [1., 0., 0.],
        [0., 1., 0.],
        [0., 0., 1.],
        [.33, .33, .34],
    ])
    data_4d = np.array([
        [1., 0., 0., 0.],
        [0., 1., 0., 0.],
        [0., 0., 1., 0.],
        [0., 0., 0., 1.],
        [.25, .25, .25, .25],
    ])
    s2 = ProjectionSimplexS2()
    s3 = ProjectionSimplexS3()
    s4 = ProjectionSimplexS4()
    print(data_2d, s2.project(data_2d), sep='\n')
    print(data_3d, s4.project(data_3d), sep='\n')
    print(data_4d, s4.project(data_4d), sep='\n')
