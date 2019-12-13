'''
   This script take an pdbfile of a series psudoaton cooridnates as input and output a fitted line as a pml file.
   Usage:
        python find_dna_axis.py dna_psd.pdb
'''


import sys
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def read_pdb_xyz(pdb_name):
    """
    Reads atomic coordinates of C-alpha atoms from a .pdb file.

    Parameters
    ----------
    pdb_name : str
        Name of pdb file.

    Returns
    -------
    array of atomic coordinates
        [[x1 y1 z1]
         [x2 y2 z2]
         [.. .. ..]
         [xn yn zn]]
    """
    xyz = []
    with open(pdb_name, 'r') as pdb_file:
        for line in pdb_file:
            if line.startswith("HETATM"):
                # extract x, y, z coordinates for carbon alpha atoms
                x = float(line[30:38].strip());
                y = float(line[38:46].strip());
                z = float(line[46:54].strip());
                xyz.append([x, y, z])
    xyz = np.array(xyz)
    return xyz

def write_pml(pymol_name, linepts):
    dna = pymol_name[:-8]
    with open(dna + '_axis.pml', "w") as pymol_file:
        pymol_file.write(
            """
            from pymol.cgo import *
            axis_%s=  [ BEGIN, LINES, COLOR, 1.0, 0.0, 0.0, \
            VERTEX, %8.3f, %8.3f, %8.3f, VERTEX, %8.3f, %8.3f, %8.3f, END ]
            cmd.load_cgo(axis_%s, 'axis_%s')
            cmd.set('cgo_line_width', 4)
            """ % ( dna,\
                linepts[0][0], linepts[0][1], linepts[0][2],  linepts[1][0], linepts[1][1], linepts[1][2],\
                dna, dna\
                  ))

if __name__ == '__main__':
    pdb_name = sys.argv[1]
    xyz = read_pdb_xyz(pdb_name)

    # Calculate the mean of the points, i.e. the 'center' of the cloud
    datamean = xyz.mean(axis=0)

    # Do an SVD on the mean-centered data.
    uu, dd, vv = np.linalg.svd(xyz - datamean)

    # Now vv[0] contains the first principal component, i.e. the direction
    # vector of the 'best fit' line in the least squares sense.

    # Now generate some points along this best fit line, for plotting.

    # I use -7, 7 since the spread of the data is roughly 14
    # and we want it to have mean 0 (like the points we did
    # the svd on). Also, it's a straight line, so we only need 2 points.
    low = xyz.min() - 15
    up = xyz.max() + 15
    linepts = vv[0] * np.mgrid[low:up:2j][:, np.newaxis]

    # shift by the mean to get the line in the right place
    linepts += datamean

    # Verify that everything looks right.

    import matplotlib.pyplot as plt
    import mpl_toolkits.mplot3d as m3d

    ax = m3d.Axes3D(plt.figure())
    ax.scatter3D(*xyz.T)
    ax.plot3D(*linepts.T)
    plt.show()

    #write pml file for pymol visualization
    write_pml(pdb_name, linepts)
