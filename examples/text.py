import xy
import itertools
import string

TEXT = (
    'Bas Jacobs '
)

def word_wrap(text, width, measure_func):
    result = []
    for line in text.split('\n'):
        fields = itertools.groupby(line, lambda x: x.isspace())
        fields = [''.join(g) for _, g in fields]
        if len(fields) % 2 == 1:
            fields.append('')
        x = ''
        for a, b in zip(fields[::2], fields[1::2]):
            w, _ = measure_func(x + a)
            if w > width:
                if x == '':
                    result.append(a)
                    continue
                else:
                    result.append(x)
                    x = ''
            x += a + b
        if x != '':
            result.append(x)
    result = [x.strip() for x in result]
    return result

class Font(object):
    def __init__(self, font, point_size):
        self.font = font
        self.max_height = xy.Drawing(xy.text(string.printable, font)).height
        # self.cap_height = xy.Drawing(xy.text('H', font)).height
        height = point_size / 72
        self.scale = height / self.max_height
    def text(self, text):
        d = xy.Drawing(xy.text(text, self.font))
        d = d.scale(self.scale)
        return d
    def justify_text(self, text, width):
        d = self.text(text)
        w = d.width
        spaces = text.count(' ')
        if spaces == 0 or w >= width:
            return d
        e = ((width - w) / spaces) / self.scale
        d = xy.Drawing(xy.text(text, self.font, extra=e))
        d = d.scale(self.scale)
        return d
    def measure(self, text):
        return self.text(text).size
    def wrap(self, text, width, line_spacing=1, align=0, justify=False):
        lines = word_wrap(text, width, self.measure)
        ds = [self.text(line) for line in lines]
        max_width = max(d.width for d in ds)
        if justify:
            jds = [self.justify_text(line, max_width) for line in lines]
            ds = jds[:-1] + [ds[-1]]
        spacing = line_spacing * self.max_height * self.scale
        result = xy.Drawing()
        y = 0
        for d in ds:
            if align == 0:
                x = 0
            elif align == 1:
                x = max_width - d.width
            else:
                x = max_width / 2 - d.width / 2
            result.add(d.translate(x, y))
            y += spacing
        return result

def main():
    font = Font(xy.SCRIPTS, 600)
    d = font.wrap(TEXT, 115, 1, justify=True)
    d = d.center(130, 120)
    d = d.join_paths(tolerance = 0.1).simplify_paths(tolerance = 0.1)
    d.render(bounds=xy.A4_BOUNDS).write_to_png('out.png')
    xy.draw(d)

if __name__ == '__main__':
    main()
