import cv2 as cv
import numpy as np


class Edge:

    def __init__(self):
        self.contours_card = None
        self.frame = None

    def find_card(self, img):
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img_norm = cv.normalize(img_gray, None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX)
        img_blur = cv.blur(img_norm, (3, 3))
        img_canny = cv.Canny(img_blur, 50, 150)

        _, contours, _ = cv.findContours(img_canny, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        max_area = 0

        for cnt in contours:
            area = cv.contourArea(cnt)
            peri = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.05 * peri, True)

            if len(approx) == 4:
                if area > max_area:
                    max_area = area
                    self.contours_card = approx.reshape(4, 2)

        x, y, w, h = cv.boundingRect(self.contours_card)
        cv.rectangle(self.frame, (x, y), (x + w, y + h), (36, 255, 12), 2)
        cv.imshow("Rectangle", self.frame)

        return img_canny

    def get_card(self, img):
        rect = get_points(self.contours_card)

        x1, y1 = np.int32(rect[0])
        x2, y2 = np.int32(rect[1])

        print(f"Rectangle coordinate: ({x1},{y1}), ({x2},{y2})")
        cv.imshow("Rectangle 2", img[x1:y1, x2:y2])

    def set_frame(self, frame):
        self.frame = frame


def get_points(points):
    rect = np.zeros((4, 2), dtype=np.float32)

    y_axis = np.sum(points, axis=1)

    rect[0] = points[np.argmin(y_axis)]  # Top-Left
    rect[2] = points[np.argmax(y_axis)]  # Top-Right

    diff = np.diff(points, axis=1)  # (y-x) of each point
    rect[1] = points[np.argmin(diff)]  # Bottom-Right
    rect[3] = points[np.argmax(diff)]  # Bottom-Left

    return rect
