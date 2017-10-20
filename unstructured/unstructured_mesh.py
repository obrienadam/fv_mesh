import numpy as np
from scipy.spatial import Delaunay

import geometry as geom


class Node(geom.Point):
    def __init__(self, id, x=0., y=0.):
        super(Node, self).__init__(x, y)
        self.id = id


class Face(geom.Line):
    def __init__(self, l_node, r_node):
        super(Face, self).__init__(l_node, r_node)


class FvCell(geom.Triangle):
    def __init__(self, id, nodes):
        super(FvCell, self).__init__(nodes)
        self.id = id
        self.neighbours = []


class Neighbour:
    def __init__(self, cell, nb_cell):
        self.cell = cell
        self.nb_cell = nb_cell

    def sf(self):
        pass

    def rc(self):
        return self.nb_cell.centroid() - self.cell.centroid()


class UnstructuredMesh:
    def __init__(self, nodes=None, patches=None):
        self.nodes = nodes
        self.faces = []
        self.cells = []

        if nodes:
            self.triangulate()

    def triangulate(self):
        tris = Delaunay([[node.x, node.y] for node in self.nodes])

        # Build cells
        for id, tri in enumerate(tris.simplices):
            self.cells.append(FvCell(id, [self.nodes[node_id] for node_id in tri]))

        # Build connectivity
        for id, nbs in enumerate(tris.neighbors):
            cell = self.cells[id]

            for nb in nbs:
                if nb != -1:
                    nb = self.cells[nb]
                    cell.neighbours.append(Neighbour(cell, nb))

    def create_patch(self, name, node_ids):
        self.patches[name] = node_ids

    def save_tec360(self, fname):
        with open(fname, 'w') as f:
            f.write('TITLE = "{}"\n'.format(fname))
            f.write('VARIABLES = "X", "Y"\n')
            f.write('ZONE T = "mesh"\n')
            f.write('N = {}, E = {}, DATAPACKING=POINT, ZONETYPE=FETRIANGLE\n'.format(len(self.nodes), len(self.cells)))

            for node in self.nodes:
                f.write('{} {}\n'.format(node.x, node.y))

            for cell in self.cells:
                f.write('{} {} {}\n'.format(*[node.id + 1 for node in cell.vertices]))


if __name__ == '__main__':
    x, y = np.meshgrid(np.linspace(0, 1, 101), np.linspace(0, 1, 101), indexing='ij')
    pts = [Node(id, x=x, y=y) for id, (x, y) in enumerate(zip(x.flatten(), y.flatten()))]

    mesh = UnstructuredMesh(nodes=pts)
    mesh.save_tec360('test.dat')
