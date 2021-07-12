import numpy as np
import cv2 as cv
import pafy
import math
import utility as Utility
import color as Color
from Frame_Rate import FrameRate

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
    flag = False  # Fix unknown exception of pafy

    while not flag:
        try:
            video_pafy = pafy.new(url)
            play = video_pafy.getbest()

            cap = cv.VideoCapture(play.url)
            cap.set(cv.CAP_PROP_FRAME_WIDTH, width)
            cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)
            flag = True
        except:
            pass

    return cap


def callback_mouse(event, x, y, flag, param):
    if event == cv.EVENT_LBUTTONDOWN:
        print(f"Click image in position ({x},{y})")


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
        self.previous_frame = None
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
        parameters_mask = np.zeros((250, 600))

        # Polygons
        view_polygon = np.array([[56, 278], [184, 277], [222, 507], [71, 509], [55, 384], [56, 416], [61, 456]])
        frame_rate_polygon = np.array([[590, 18], [590, 50], [725, 50], [725, 18]])
        rectangle_polygon = np.array([[12, 11], [144, 11], [144, 65], [12, 65]])

        poly_lane_1 = np.array([[140, 271], [182, 274], [217, 508], [168, 510]])
        poly_lane_2 = np.array([[138, 271], [98, 271], [115, 510], [166, 510]])

        cv.fillConvexPoly(view_mask, view_polygon, 1)
        cv.fillConvexPoly(view_mask, frame_rate_polygon, 1)
        cv.fillConvexPoly(view_mask, rectangle_polygon, 1)

        # Other parameters (corners, velocity)
        v1, c1 = 0, 0
        v2, c2 = 0, 0

        while self.camera.isOpened():
            ret, frame = self.camera.read()

            if ret:
                # Resize
                frame = cv.resize(frame, (self.width, self.height))
                frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                frame_copy = frame.copy()  # Temporary frame to execute operations

                img = cv.bitwise_and(frame_copy, frame_copy, mask=view_mask)

                # Draw text
                Utility.set_text(parameters_mask, f"1-Lane speed: {v1} km/h,  ", (20, 30), color=Color.WHITE, dim=1.2,
                                 thickness=1)
                Utility.set_text(parameters_mask, f"corners 1: {c1}", (270, 30), color=Color.WHITE, dim=1.2,
                                 thickness=1)
                Utility.set_text(parameters_mask, f"2-Lane speed: {v2} km/h,  ", (20, 60), color=Color.WHITE, dim=1.2,
                                 thickness=1)
                Utility.set_text(parameters_mask, f"corners 2: {c2}", (270, 60), color=Color.WHITE, dim=1.2,
                                 thickness=1)

                # Draw numbers
                Utility.set_text(img, "1", (100, 257), color=Color.CYAN, dim=3, thickness=3)
                Utility.set_text(img, "2", (145, 257), color=Color.RED, dim=3, thickness=3)

                # Draw lines
                cv.line(img, (182, 274), (217, 508), Color.RED, 3)  # Lane 1
                cv.line(img, (140, 271), (168, 510), Color.RED, 3)  # Lane 1/2
                cv.line(img, (98, 279), (113, 510), Color.RED, 4)  # Lane 2

                # Frame rate
                self.frame_rate.run(img)

                # Draw polygons
                img_poly_lane = frame_copy.copy()
                cv.fillPoly(img_poly_lane, [poly_lane_1], Color.VIOLA, cv.LINE_AA)
                cv.fillPoly(img_poly_lane, [poly_lane_2], Color.CYAN, cv.LINE_AA)
                img = cv.addWeighted(img_poly_lane, self.alpha, img, 1 - self.alpha, 0)

                if len(self.tracks) > 0:
                    prev_img, current_img = self.previous_frame, frame_gray
                    prev_points = np.float32([point[-1] for point in self.tracks]).reshape(-1, 1, 2)

                    # Optical flow scattered
                    points_1, st_1, err_1 = cv.calcOpticalFlowPyrLK(prev_img, current_img, prev_points, None,
                                                                    **lk_params)
                    points_2, st_2, err_2 = cv.calcOpticalFlowPyrLK(current_img, prev_img, points_1, None, **lk_params)

                    # Difference between points
                    difference = abs(prev_points - points_2).reshape(-1, 2).max(-1)
                    good = difference < 1
                    new_tracks = []

                    for track, (x, y), good_features in zip(self.tracks, points_1.reshape(-1, 2), good):
                        if not good_features:
                            continue

                        track.append((x, y))
                        if len(track) > self.track_len:
                            del track[0]

                        new_tracks.append(track)
                        cv.circle(frame, (int(x), int(y)), 3, Color.YELLOW, -1)

                    # Update tracks
                    self.tracks = new_tracks

                    for index, track in enumerate(self.tracks):

                        is_inside_1 = cv.pointPolygonTest(poly_lane_1, track[0], True)

                        if is_inside_1 > 0:
                            pass
                            # TODO continue
                            # ptn1 += 1
                            # dif1 = tuple(map(lambda i, j: i - j, track[0], track[1]))
                            # mm1 += math.sqrt(dif1[0] * dif1[0] + dif1[1] * dif1[1])
                            # mmm1 = mm1 / ptn1
                            # v1 = mmm1 * px2m1 * fps * ms2kmh

                if self.id_frame % self.detect_interval == 0:
                    f"""Update values each n-interval ({self.detect_interval}) frames"""

                    mask = np.zeros_like(frame_gray)
                    mask[:] = 255
                    for x, y in [np.int32(track[-1]) for track in self.tracks]:
                        # Draw circles (good points), if they exist
                        cv.circle(mask, (x, y), 3, Color.GREEN, -1)
                    # cv.imshow("Mask points", mask)

                    # Calculation good points
                    points = cv.goodFeaturesToTrack(frame_gray, mask=mask, **feature_params)
                    if points is not None:
                        for x, y in points.reshape(-1, 2):
                            self.tracks.append([(x, y)])

                # Update id and current frame
                self.id_frame += 1
                self.previous_frame = frame_gray

                # Show views
                cv.imshow("Original", frame)
                cv.imshow(NAME_WINDOW, img)
                cv.imshow("Parameters", parameters_mask)
                cv.waitKey(10)


if __name__ == "__main__":
    # jackson_hole = "https://youtu.be/1EiC9bvVGnk"  # Jackson Hole (United States)
    taipei_url = "https://youtu.be/XV1q_2Cl6mI"  # Taipei (Taiwan)

    app = App(video_url=taipei_url)
    app.run()
