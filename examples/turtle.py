import xy

def main(iteration):
    turtle = xy.Turtle()
    for i in range(1, 2 ** iteration):
        turtle.forward(1)
        if (((i & -i) << 1) & i) != 0:
            turtle.circle(-1, 90, 36)
        else:
            turtle.circle(1, 90, 36)
    drawing = turtle.drawing.rotate_and_scale_to_fit(110, 85, step=90)
    # im = drawing.render()
    # im.write_to_png("out.png")
    xy.draw(drawing, verbose = True)

if __name__ == '__main__':
    main(12)