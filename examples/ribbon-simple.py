import eleksdrawpy as xy
import math
import random
import sys

BOUNDS = xy.A4_BOUNDS

def main():
    d = xy.Drawing.load(sys.argv[1]).scale(1, -1)
    print(len(d.paths))
    d = d.join_paths(0.005)
    d = d.rotate_and_scale_to_fit(*BOUNDS[-2:])
    d = d.sort_paths()
    d = d.join_paths(0.005)
    d = d.simplify_paths(0.0001)
    print(len(d.paths))
    print(d.bounds)
    d.dump('out.xy')
    d.render(bounds=BOUNDS).write_to_png('out.png')

if __name__ == '__main__':
    main()
