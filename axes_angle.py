#! /usr/bin/env python

"""
Computes principal axes from a PDB file.

Produces also a .pml script for a nice rendering with PyMOL.
"""

import sys
import os.path
import numpy
import math


# scale factor to enhance the length of axis in Pymol
scale_factor = 20


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
            if line.startswith("ATOM"):
                # extract x, y, z coordinates for carbon alpha atoms
                x = float(line[30:38].strip())
                y = float(line[38:46].strip())
                z = float(line[46:54].strip())
                if line[12:16].strip() == "P":
                    xyz.append([x, y, z])
    return xyz


def check_argument(arguments):
    """
    Check if filename passed as argument exists. 

    Parameters
    ----------
    arguments : list
        list of arguments passed to the script

    Returns
    -------
    string
        file name
    """
    if len(arguments) == 3:
        file_name_list = arguments[1:]
    else:
        message = """
        ERROR: missing pdb filename as argument
        usage: %s file1.pdb file2.pdb""" %(arguments[0])
        sys.exit(message)

    # check if argument are two existing files
    if not os.path.exists(file_name_list[0]):
        sys.exit("ERROR: file %s does not seem to exist" %(file_name_list[0]))
    if not os.path.exists(file_name_list[1]):
        sys.exit("ERROR: file %s does not seem to exist" % (file_name_list[0]))


    return file_name_list

def write_pml(pymol_name, center, point1, point2, point3):
    dna = pymol_name[:4]
    print('dna=', dna)
    with open(pymol_name, "w") as pymol_file:
        pymol_file.write(
            """
            from pymol.cgo import *
            axis1_%s=  [ BEGIN, LINES, COLOR, 1.0, 0.0, 0.0, \
            VERTEX, %8.3f, %8.3f, %8.3f, VERTEX, %8.3f, %8.3f, %8.3f, END ]
            axis2_%s=  [ BEGIN, LINES, COLOR, 0.0, 1.0, 0.0, \
            VERTEX, %8.3f, %8.3f, %8.3f, VERTEX, %8.3f, %8.3f, %8.3f, END ]
            axis3_%s=  [ BEGIN, LINES, COLOR, 0.0, 0.0, 1.0, \
            VERTEX, %8.3f, %8.3f, %8.3f, VERTEX, %8.3f, %8.3f, %8.3f, END ]
            cmd.load_cgo(axis1_%s, 'axis1_%s')
            cmd.load_cgo(axis2_%s, 'axis2_%s')
            cmd.load_cgo(axis3_%s, 'axis3_%s')
            cmd.set('cgo_line_width', 4)
            """ % ( \
                dna, center[0], center[1], center[2], point1[0], point1[1], point1[2], \
                dna, center[0], center[1], center[2], point2[0], point2[1], point2[2], \
                dna, center[0], center[1], center[2], point3[0], point3[1], point3[2],\
                dna, dna,\
                dna, dna,\
                dna, dna))

def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))

# start program
if __name__ == '__main__':

    # check if argument file exists
    pdb_name_list = check_argument(sys.argv)

    #--------------------------------------------------------------------------
    # compute principal axes
    #--------------------------------------------------------------------------
    # read pdb
    xyz_dna1 = read_pdb_xyz(pdb_name_list[0])
    print("%d P atomes found in dna1" %(len(xyz_dna1)))

    xyz_dna2 = read_pdb_xyz(pdb_name_list[1])
    print("%d P atomes found in dna2" %(len(xyz_dna1)))


    #create coordinates array
    coord_dna1 = numpy.array(xyz_dna1, float)
    coord_dna2 = numpy.array(xyz_dna2, float)

    # compute geometric center
    center_dna1 = numpy.mean(coord_dna1, 0)
    print("\nCoordinates of the geometric center of dna1:\n", center_dna1)

    center_dna2 = numpy.mean(coord_dna2, 0)
    print("Coordinates of the geometric center of dna2:\n", center_dna2)

    # center with geometric center
    coord_dna1 = coord_dna1 - center_dna1
    coord_dna2 = coord_dna2 - center_dna2

    # compute principal axis matrix
    inertia_dna1 = numpy.dot(coord_dna1.transpose(), coord_dna1)
    e_values_dna1, e_vectors_dna1 = numpy.linalg.eig(inertia_dna1)

    inertia_dna2 = numpy.dot(coord_dna2.transpose(), coord_dna2)
    e_values_dna2, e_vectors_dna2 = numpy.linalg.eig(inertia_dna2)
    # warning eigen values are not necessary ordered!
    # http://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.eig.html
    print("\n(Unordered) eigen values of dna1:")
    print(e_values_dna1)
    print("(Unordered) eigen vectors  of dna2:")
    print(e_vectors_dna2)

    print("\n(Unordered) eigen values of dna1 pdb file1:")
    print(e_values_dna2)
    print("(Unordered) eigen vectors  of dna1 pdb file1:")
    print(e_vectors_dna2)

    #--------------------------------------------------------------------------
    # order eigen values (and eigen vectors)
    #
    # axis1 is the principal axis with the biggest eigen value (eval1)
    # axis2 is the principal axis with the second biggest eigen value (eval2)
    # axis3 is the principal axis with the smallest eigen value (eval3)
    #--------------------------------------------------------------------------
    order = numpy.argsort(e_values_dna1)
    eval3_dna1, eval2_dna1, eval1_dna1 = e_values_dna1[order]
    axis3_dna1, axis2_dna1, axis1_dna1 = e_vectors_dna1[:, order].transpose()
    print("\nInertia axis of dna1 are now ordered !")

    order = numpy.argsort(e_values_dna2)
    eval3_dna2, eval2_dna2, eval1_dna2 = e_values_dna2[order]
    axis3_dna2, axis2_dna2, axis1_dna2 = e_vectors_dna2[:, order].transpose()
    print("Inertia axis of dna2 are now ordered !")

    #--------------------------------------------------------------------------
    # center axes to the geometric center of the molecule
    # and rescale them by order of eigen values
    #--------------------------------------------------------------------------
    # the large vector is the first principal axis
    point1_dna1 = 3 * scale_factor * axis1_dna1 + center_dna1
    # the medium vector is the second principal axis
    point2_dna1 = 2 * scale_factor * axis2_dna1 + center_dna1
    # the small vector is the third principal axis
    point3_dna1 = 1 * scale_factor * axis3_dna1 + center_dna1

    point1_dna2 = 3 * scale_factor * axis1_dna2 + center_dna2
    # the medium vector is the second principal axis
    point2_dna2 = 2 * scale_factor * axis2_dna2 + center_dna2
    # the small vector is the third principal axis
    point3_dna2 = 1 * scale_factor * axis3_dna2 + center_dna2

    #--------------------------------------------------------------------------
    # create .pml script for a nice rendering in Pymol
    #  output usage
    #--------------------------------------------------------------------------
    pymol_name_dna1 = pdb_name_list[0].replace(".pdb", "_axes.pml")
    write_pml(pymol_name_dna1, center_dna1, point1_dna1, point2_dna1, point3_dna1)
  
    print("coordinates of dna1: ", axis1_dna1)
    print("eigen value of dna1: ", eval1_dna1)

    print("\nSecond principal axis of dna1 (in green)")
    print("coordinates:", axis2_dna1)
    print("eigen value:", eval2_dna1)

    print("\nThird principal axis of dna1 (in blue)")
    print("coordinates:", axis3_dna1)
    print("eigen value:", eval3_dna1)

    print("\nYou can view principal axes of dna1 with PyMOL:")
    print("pymol %s %s" %(pymol_name_dna1, pdb_name_list[0]))

    pymol_name_dna2 = pdb_name_list[1].replace(".pdb", "_axes.pml")
    write_pml(pymol_name_dna2, center_dna2, point1_dna2, point2_dna2, point3_dna2)

    print("coordinates of dna2: ", axis1_dna2)
    print("eigen value of dna2: ", eval1_dna2)

    print("\nSecond principal axis of dna1 (in green)")
    print("coordinates:", axis2_dna2)
    print("eigen value:", eval2_dna2)

    print("\nThird principal axis of dna1 (in blue)")
    print("coordinates:", axis3_dna2)
    print("eigen value:", eval3_dna2)

    print("\nYou can view principal axes of dna1 with PyMOL:")
    print("pymol %s %s" % (pymol_name_dna2, pdb_name_list[0]))

    # --------------------------------------------------------------------------
    # calculate the angle between the first principal axes
    # --------------------------------------------------------------------------
    v1 = point1_dna1 - center_dna1
    v2 = point1_dna2 - center_dna2
    angle_v12 = angle(v1, v2) * 180 / numpy.pi
    print('angele = ', angle_v12)
