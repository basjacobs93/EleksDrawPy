import xy
from numpy import random

def square(t, size, wiggle):
    t.right(int((random.random()-0.5)*wiggle))
    t.pendown()
    for i in range(4):
        t.forward(size)
        t.right(90)
    t.penup()

def main():
    t = xy.Turtle(start_up = True)

    num_x = 10
    num_y = 10

    step_y = 10
    step_x = 10

    offset = [1 for _ in range(num_y)]
    wiggle = [1 for _ in range(num_y)]

    for ix in range(0, num_x):
        for iy in range(0, num_y):
            y = iy * step_y
            x = ix * step_x

            t.goto(x + offset[iy]-1, y)

            square(t, 10, wiggle[iy]-1)

            offset[iy] *= (1+random.random()*0.8)
            wiggle[iy] *= (1+random.random())

            
    drawing = t.drawing.origin().scale_to_fit(240, 165).center()
    drawing.render().write_to_png('out.png')
    xy.draw(drawing, verbose = False)

if __name__ == '__main__':
    main()
