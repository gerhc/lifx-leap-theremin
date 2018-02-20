from __future__ import division, print_function

import colorsys
import leap
import sys
import time

from lifxlan import LifxLAN


X_MAX = 300
Y_MAX = 600
Z_MAX = 300


class Listener(leap.Listener):

    def __init__(self, *args, **kwargs):
        super(Listener, self).__init__()
        self.last = time.time()
        lifx = LifxLAN(1)
        devices = lifx.get_lights()
        self.bulb = devices[0]

    def on_connect(self, controller):
        print("Connected")

    def scale_value(self, value, _from, to):
        return int((min(value, _from) / _from) * to)

    def on_frame(self, controller):
        if time.time() - self.last > 0.08:
            self.last = time.time()
            frame = controller.frame()
            hands = frame.hands
            if not hands.is_empty:
                hand = hands.rightmost
                vector = hand.palm_position
                r = self.scale_value(abs(vector.x), X_MAX, 255)
                g = self.scale_value(abs(vector.y), Y_MAX, 255)
                b = self.scale_value(abs(vector.z), Z_MAX, 255)
                h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
                lifx_color = [65535 * h, 65535 * s, 65535 * v, 3500]
                self.bulb.set_color(lifx_color)


def main():
    controller = leap.Controller()
    listener = Listener()
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print("Press Enter to quit...")
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
