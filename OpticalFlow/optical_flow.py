import numpy as np
import cv2 as cv
import pafy
import time

import color
import utility as Utility
import color as Color

# Params for Shi-Tomasi corner detection
feature_params = dict(maxCorners=500,
                      qualityLevel=0.3,
                      minDistance=7,
                      blockSize=7)

# Parameters for Lucas-Kanade optical flow
lk_params = dict(winSize=(15, 15),
                 maxLevel=2,
                 criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

NAME_WINDOW = "Optical Flow"


def get_cap(url, height, width):
    video_pafy = pafy.new(url)
    play = video_pafy.getbest()

    cap = cv.VideoCapture(play.url)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)

    return cap


def callback_mouse(event, x, y, flag, param):
    if event == cv.EVENT_LBUTTONDOWN:
        print(f"Click image in position ({x},{y})")


class FrameRate:

    def __init__(self):
        self.current_time = 0
        self.previous_time = 0

    def run(self, img):
        self.current_time = time.time()
        fps = np.divide(1, (self.current_time - self.previous_time))
        self.previous_time = self.current_time
        Utility.set_text(img, f"FPS: {int(fps)}", (610, 40), dim=1.5, color=Color.RED, thickness=2)


class App:

    def __init__(self, video_url, height_cam=512, width_cam=750):
        # Camera
        self.height = height_cam
        self.width = width_cam
        self.camera = get_cap(video_url, self.height, self.width)

        # Optical flow
        self.tracks = []
        self.track_len = 2
        self.detect_interval = 4
        self.id_frame = 0

        # Frame Rate
        self.frame_rate = FrameRate()

        self.alpha = 0.5  # Used for addWeighted

    def run(self):
        _, first_frame = self.camera.read()
        first_frame = cv.resize(first_frame, (self.width, self.height))

        cv.namedWindow(NAME_WINDOW)
        cv.setMouseCallback(NAME_WINDOW, callback_mouse)

        # Mask
        view_mask = np.zeros_like(first_frame[:, :, 0])
        frame_rate_mask = np.zeros_like(first_frame[:, :, 0])

        # Polygons
        view_polygon = np.array([[56, 278], [184, 277], [222, 507], [71, 509], [55, 384], [56, 416], [61, 456]])
        frame_rate_polygon = np.array([[590, 18], [725, 18], [590, 38], [725, 38]])
        poly_1 = np.array([[140, 271], [182, 274], [217, 508], [168, 510]])

        cv.fillConvexPoly(view_mask, view_polygon, 1)
        cv.fillConvexPoly(frame_rate_mask, frame_rate_polygon, 1)

        # Other parameters (corners, velocity)
        v1 = 0
        c1 = 0

        while self.camera.isOpened():
            ret, frame = self.camera.read()

            if ret:
                # Resize
                frame = cv.resize(frame, (self.width, self.height))
                img = frame.copy()

                img = cv.bitwise_and(img, img, mask=view_mask)
                img_2 = cv.bitwise_and(frame.copy(), frame.copy(), mask=frame_rate_mask)

                # Draw text
                Utility.set_text(img, f"1-Lane speed: {v1} km/h,  ", (350, 495), color=Color.WHITE, dim=1.2)
                Utility.set_text(img, f"corners 1: {c1}", (596, 495), color=Color.WHITE, dim=1.2)

                # Draw lines
                cv.line(img, (140, 271), (168, 510), Color.RED, 3)
                cv.line(img, (182, 274), (217, 508), Color.RED, 3)

                # Frame rate
                self.frame_rate.run(img)

                # Draw polygons
                lane_mask = frame.copy()
                cv.fillPoly(lane_mask, [poly_1], color.VIOLA, cv.LINE_AA)
                img = cv.addWeighted(lane_mask, self.alpha, img, 1 - self.alpha, 0)

                cv.imshow(NAME_WINDOW, img)
                cv.imshow("img2", img_2)
                cv.waitKey(10)


jackson_hole = "https://youtu.be/1EiC9bvVGnk"  # Jackson Hole (United States)
taipei = "https://youtu.be/XV1q_2Cl6mI"  # Taipei (Taiwan)

app = App(video_url=taipei)
app.run()
