# DNA-bending-angle

Under the actions of DNA binding proteins, the DNA can bend. Sometimes it may helpful to calculate the bending angle of the DNA. The script aims to calculate the angle between the principal axes of two double chain DNA. The current repository include two different method.

1. find_bend_angel_1

The basic idea of axes_angle.py is to select two arms aside the bending site seperately and save them into two pdb files. Then you can use the script to calculate the principal axes of the two dna and then the angle between them. This angle can be used as the DNA bending angle.

Usage:
   python axes_angle.py dna1.pdb dna2.pdb
   
   
   
2. find_bend_angle_2
  This method first use the center_of_mass.py script to find the center of mess of the C6 and N9 atoms in the each nucleotide pair in the dna, make a psuedoatom for each center of mass, then  fit a line with coordinates of all the psuedoatom. By calculating the angle between two lines represent two DNA, the bending angle between the two dna is obtained.
  
Usage
(1) load the DNA in pymol; 
(2) run the "import center_of_mass" command in the pymol command
(3) select the C6 and N9 atoms in a nucleotide pair
(4) run the "com sele" command in the pymol command to create a psuedoatom at the center of mass of the selected C6 and N9 atoms
(5) create psuedoatoms for each nucleotide pairs
(6) save the the psuedoatom coordinates as a pdb file (dna1_psd.pdb)
(7) fit a line with the psuedoatom coordinates by running the find_dna_axis.py script in linux shell.
       python find_dna_axis.py dna1_psd.pdb
    This script will generate a dna1_axis.pml file which can be visualized in pymol
(8) repeat the above steps to fit axis for other dna (for example, dna2)
(9) run the script bend_angle.py
       python bend_angle.py dna1_axis.pml dna2_axis.pml
    

