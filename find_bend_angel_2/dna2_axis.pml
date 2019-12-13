
            from pymol.cgo import *
            axis_dna2=  [ BEGIN, LINES, COLOR, 1.0, 0.0, 0.0,             VERTEX,   13.553,  -33.158,   66.949, VERTEX,   22.531,  -12.833,  -32.573, END ]
            cmd.load_cgo(axis_dna2, 'axis_dna2')
            cmd.set('cgo_line_width', 4)
            