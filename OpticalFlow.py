import cv2 as cv
import numpy as np

feature_params = dict(maxCorners=100,
                      qualityLevel=0.3,
                      minDistance=7,
                      blockSize=7)

lk_params = dict(winSize=(15, 15),
                 maxLevel=2,
                 criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

color = np.random.randint(0, 255, (100, 3))


class OpticalFlow:
    r"""
    # TODO documentation
    """

    def __init__(self, frame):
        self.previous_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        self.p0 = cv.goodFeaturesToTrack(self.previous_frame, mask=None, **feature_params)
        self.p1 = []
        self.mask = np.zeros_like(frame)
        self.good_new = []
        self.good_old = []

    def start(self, frame):
        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        self.p1, st, err = cv.calcOpticalFlowPyrLK(self.previous_frame, frame_gray, self.p0, None, **lk_params)

        # Select good points
        if self.p1 is not None:
            self.good_new = self.p1[st == 1]
            self.good_old = self.p0[st == 1]

        for i, (new, old) in enumerate(zip(self.good_new, self.good_old)):
            a, b = new.ravel()
            c, d = old.ravel()
            self.mask = cv.line(self.mask, (int(a), int(b)), (int(c), int(d)), color[i].tolist(), 2)
            frame = cv.circle(frame, (int(a), int(b)), 5, color[i].tolist(), -1)

        img = cv.add(frame, self.mask)

        self.previous_frame = frame_gray.copy()
        self.p0 = self.good_new.reshape(-1, 1, 2)

        return img
