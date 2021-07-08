import time
import numpy as np
import utility as Utility
import color as Color


class FrameRate:

    def __init__(self):
        self.current_time = 0
        self.previous_time = 0

    def run(self, img):
        self.current_time = time.time()
        fps = np.divide(1, (self.current_time - self.previous_time))
        self.previous_time = self.current_time
        Utility.set_text(img, f"FPS: {int(fps)}", (610, 40), dim=1.5, color=Color.RED, thickness=4)
