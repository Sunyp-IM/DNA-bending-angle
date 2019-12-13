
            from pymol.cgo import *
            axis_dna1=  [ BEGIN, LINES, COLOR, 1.0, 0.0, 0.0,             VERTEX,  -19.176,    5.156,   56.049, VERTEX,    5.149,   17.442,  -24.689, END ]
            cmd.load_cgo(axis_dna1, 'axis_dna1')
            cmd.set('cgo_line_width', 4)
            