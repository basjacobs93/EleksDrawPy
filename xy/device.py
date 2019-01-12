from serial import Serial
from serial.tools.list_ports import comports

import time

VID_PID = '1A86:7523'
BAUD = 115200

FEED_RATE = 4000 # millimeters per minute (max 5000)


def find_port():
    for port in comports():
        if VID_PID in port[2]:
            return port[0]
    return None

class Device(object):

    def __init__(self, verbose=False):
        self.verbose = verbose

        self.feed_rate = FEED_RATE

        port = find_port()
        if port is None:
            raise Exception('cannot find device')
        self.serial = Serial(port, baudrate=BAUD, timeout=1)

        self.configure()

    def configure(self):
        self.write('\r\n\r')
        time.sleep(3)
        self.serial.flushInput()
        self.write('F{}'.format(self.feed_rate)) # feed rate
        self.write('M3')
        self.pen_up()

    def write(self, *args):
        line = ' '.join(map(str, args))
        if self.verbose:
            print(line)
        self.serial.write((line + '\n').encode('utf-8'))
        response = self.serial.readline().strip().decode('utf-8')
        if self.verbose:
            print(response)

    def home(self):
        self.write('G28')

    def move(self, x, y):
        x = 'X%s' % -round(x, 2)
        y = 'Y%s' % -round(y, 2)
        self.write('G01', x, y)

    def pen_up(self):
        self.write('S0')

    def pen_down(self):
        self.write('S40')

    def draw(self, points):
        if not points:
            return

        self.move(*points[0])
        self.pen_down()
        time.sleep(0.15)
        for point in points:
            self.move(*point)
        self.pen_up()
        time.sleep(0.15)

    def gcode(self, g):
        for line in g.lines:
            self.write(line)
