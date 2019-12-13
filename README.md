# DNA-bending-angle

Under the actions of DNA binding proteins, the DNA can bend. Sometimes it may helpful to calculate the bending angle of the DNA. The script aims to calculate the angle between the principal axes of two double chain DNA. The current repository include two different method.

(1) find_bend_angel_1

The basic idea of axes_angle.py is to select two arms aside the bending site seperately and save them into two pdb files. Then you can use the script to calculate the principal axes of the two dna and then the angle between them. This angle can be used as the DNA bending angle.

Usage:
   python axes_angle.py dna1.pdb dna2.pdb
   
(2) find_bend_angle_2
   find_dna_axis.py 
