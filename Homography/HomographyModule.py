import cv2 as cv
import numpy as np
import math


class HomographyModule:

    def __init__(self):
        self.contours_card = None
        self.frame = None

    def find_obj(self, img, th1=50, th2=150, draw_box=False):

        if self.frame is None:
            self.frame = img.copy()

        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img_norm = cv.normalize(img_gray, None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX)
        img_blur = cv.blur(img_norm, (3, 3))
        img_canny = cv.Canny(img_blur, th1, th2)

        contours, _ = cv.findContours(img_canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        max_area = 0

        for cnt in contours:
            area = cv.contourArea(cnt)
            peri = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.05 * peri, True)

            if len(approx) == 4:
                if area > max_area:
                    # Get rectangle with max area
                    max_area = area
                    self.contours_card = approx.reshape(4, 2)

        if draw_box:
            x, y, w, h = cv.boundingRect(self.contours_card)
            img_bounding_box = self.frame.copy()
            cv.rectangle(img_bounding_box, (x, y), (x + w, y + h), (36, 255, 12), 2)
            cv.imshow("Bounding box", img_bounding_box)

        return img_canny

    def get_obj(self, draw_crop=False):
        rect = get_points_obj(self.contours_card)
        rect_int = np.int32(rect)
        p1, p2, p3, p4 = rect_int

        if draw_crop:
            x1, y1 = p1
            x2, y2 = p4
            cv.imshow("Rectangle", self.frame[y1:y2, x1:x2])

        img_vertices = self.frame.copy()
        for point in rect_int:
            x, y = point
            cv.circle(img_vertices, (x, y), 3, (0, 0, 255), 7)
        cv.imshow("Vertices", img_vertices)

        dst, height, width = calc_side_obj(rect)
        matrix = cv.getPerspectiveTransform(rect, dst)
        img_warped = cv.warpPerspective(self.frame, matrix, (width, height))
        cv.imshow("Warped", img_warped)

    def set_frame(self, frame):
        self.frame = frame


def get_points_obj(points):
    rect = np.zeros((4, 2), dtype=np.float32)

    sum_coord = np.sum(points, axis=1)  # Sum of the coordinates. Output> array with sum

    rect[0] = points[np.argmin(sum_coord)]  # Top-Left
    rect[3] = points[np.argmax(sum_coord)]  # Bottom-Right

    diff = np.diff(points, axis=1)  # (y-x) of each point
    rect[1] = points[np.argmin(diff)]  # Top-Right
    rect[2] = points[np.argmax(diff)]  # Bottom-Left

    return rect


def calc_side_obj(rect):
    p1, p2, p3, p4 = rect

    width_1 = np.sqrt(math.pow(p2[0] - p1[0], 2) + math.pow(p2[1] - p1[1], 2))
    width_2 = np.sqrt(math.pow(p4[0] - p3[0], 2) + math.pow(p4[1] - p3[1], 2))
    max_width = max(int(width_1), int(width_2))

    height_1 = np.sqrt(math.pow(p3[0] - p1[0], 2) + math.pow(p3[1] - p1[1], 2))
    height_2 = np.sqrt(math.pow(p4[0] - p2[0], 2) + math.pow(p4[1] - p2[1], 2))
    max_height = max(int(height_1), int(height_2))

    dst = np.array([[0, 0], [0, max_height - 1], [max_width - 1, 0], [max_width - 1, max_height - 1]], dtype="float32")

    return dst, max_height, max_width
