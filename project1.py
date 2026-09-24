"""Project 1: interpolate digitized topographic contours onto the field grid.

The ``Nechelik`` class below is provided and complete: it parses the digitized
``Nechelik_Data.csv`` file and performs the interpolation steps. Implement
``extrapolate_depth`` at the bottom of this module, then submit.

Digitize the map and save it as ``Nechelik_Data.csv`` in the repository root before
you start; README.md describes the file format and the required grid.
"""
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.interpolate

# Digitized columns, in file order: the field boundary followed by the depth contours.
COLUMNS = pd.MultiIndex.from_tuples(
    [('boundary', 'X'), ('boundary', 'Y'),
     ('C0', 'X'), ('C0', 'Y'),
     ('C25', 'X'), ('C25', 'Y'),
     ('C50', 'X'), ('C50', 'Y'),
     ('C75', 'X'), ('C75', 'Y'),
     ('C100', 'X'), ('C100', 'Y'),
     ('C125', 'X'), ('C125', 'Y'),
     ('C150', 'X'), ('C150', 'Y')])


class Nechelik:
    """Interpolate digitized depth contours and extend them to a block grid."""

    def __init__(self, filename, Nx, Ny):
        self.Nx = Nx
        self.Ny = Ny
        self.setup_df(filename)
        self.points, self.values = self.get_points_and_values()

    def setup_df(self, filename):
        self.df = pd.read_csv(filename, header=[0, 1])
        self.df.columns = COLUMNS

    def get_points_and_values(self):
        labels = self.df.columns.get_level_values(0).unique()[1:]

        points = np.empty((0, 2), dtype='double')
        values = np.array([], dtype='double')

        for label in labels:
            temp = self.df[label].dropna().to_numpy()
            points = np.concatenate((points, temp))
            values = np.append(values, np.ones(temp.shape[0]) * int(label[1:]))

        return points.reshape(-1, 2), values

    def create_grid(self):
        xmin = self.df['boundary']['X'].min()
        xmax = self.df['boundary']['X'].max()
        ymin = self.df['boundary']['Y'].min()
        ymax = self.df['boundary']['Y'].max()
        dx = (xmax - xmin) / self.Nx
        dy = (ymax - ymin) / self.Ny
        self.eps = np.min([0.5 * dx, 0.5 * dy])
        xx = np.linspace(xmin + dx / 2, xmax - dx / 2, self.Nx)
        yy = np.linspace(ymin + dy / 2, ymax - dy / 2, self.Ny)

        return np.meshgrid(xx, yy)

    def interpolate(self):
        self.X, self.Y = self.create_grid()

        self.Z = scipy.interpolate.griddata(self.points, self.values,
                                            (self.X, self.Y), method='cubic')
        return

    def extrapolate(self):
        mask = ~np.isnan(self.Z.flatten())
        points = (self.X.flatten()[mask], self.Y.flatten()[mask])
        values = self.Z.flatten()[mask]
        self.Z = scipy.interpolate.griddata(points, values, (self.X, self.Y),
                                            method='nearest')
        return

    def set_boundary(self):
        boundary = matplotlib.path.Path(self.df['boundary'].to_numpy(), closed=False)

        mask = boundary.contains_points(
            np.array([self.X.ravel(), self.Y.ravel()]).T,
            radius=-self.eps).reshape(self.X.shape)

        self.Z[self.Z < 0.0] = 0.0
        self.Z[~mask] = np.nan

    def plot(self):
        fig, ax = plt.subplots()
        ax.contourf(self.X, self.Y, self.Z)
        ax.set_aspect('equal')
        return fig


def extrapolate_depth(filename, Nx, Ny):
    """Return depth as an ``Ny x Nx`` array of block-centred values.

    Drive the provided ``Nechelik`` steps in the documented order and return the
    final depth array. README.md gives the grid definitions and the procedure.
    """
    raise NotImplementedError('Implement extrapolate_depth using the Nechelik class')
