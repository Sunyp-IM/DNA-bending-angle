
            from pymol.cgo import *
            axis_dna3=  [ BEGIN, LINES, COLOR, 1.0, 0.0, 0.0,             VERTEX,    0.025,   23.711,    6.336, VERTEX,   21.672,  -26.537,    0.180, END ]
            cmd.load_cgo(axis_dna3, 'axis_dna3')
            cmd.set('cgo_line_width', 4)
            