import numpy as np
import cv2 as cv
import pafy
import OpticalFlow.utility as Utility
import color as Color
from OpticalFlow.Frame_Rate import FrameRate

# Params for Shi-Tomasi corner detection
feature_params = dict(maxCorners=500,
                      qualityLevel=0.3,
                      minDistance=7,
                      blockSize=7)

# Parameters for Lucas-Kanade optical flow
lk_params = dict(winSize=(15, 15),
                 maxLevel=2,
                 criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

WINDOW_OPTICAL_FLOW = "Optical Flow"
WINDOW_PARAMETERS = "Parameters"

px2mm = 0.088  # TODO look this!


def get_cap(url, height, width):
    r"""
    Parse url video. Setting video capture.

    :param url: url-video.
    :param height: height of camera video.
    :param width: width of camera video.
    """
    flag = False  # Fix unknown exception of pafy

    while not flag:
        try:
            video_pafy = pafy.new(url)
            play = video_pafy.getbest()

            cap = cv.VideoCapture(play.url)
            cap.set(cv.CAP_PROP_FRAME_WIDTH, width)
            cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)
            flag = True
        except Exception as e:
            print(f"Exception in load video: {e}")

    return cap


def callback_mouse(event, x, y, flag, param):
    r"""
    Image callback after mouse click.
    """
    if event == cv.EVENT_LBUTTONDOWN:
        print(f"Click image in position ({x},{y})")


class App:

    def __init__(self, video_url, height_cam=512, width_cam=750):
        # Camera
        self.height = height_cam
        self.width = width_cam
        self.camera = get_cap(video_url, self.height, self.width)

        # Optical flow
        self.corners = []
        self.corners_len = 2
        self.detect_interval = 4
        self.previous_frame = None
        self.id_frame = 0

        # Lane 1
        self.v_1 = 0.0
        self.corn_1 = 0

        # Lane 2
        self.v_2 = 0.0
        self.corn_2 = 0

        # Frame Rate
        self.frame_rate = FrameRate()

        # Constants
        self.alpha = 0.5  # Used for addWeighted
        self.ms_2_kmh = 3.6  # Used to convert m/s into km/h
        self.minimum_corners = 5  # Minimum corners to update velocity

    def run(self):
        _, first_frame = self.camera.read()
        first_frame = cv.resize(first_frame, (self.width, self.height))

        cv.namedWindow(WINDOW_OPTICAL_FLOW)
        cv.namedWindow(WINDOW_PARAMETERS)
        cv.setMouseCallback(WINDOW_OPTICAL_FLOW, callback_mouse)
        cv.setMouseCallback(WINDOW_PARAMETERS, callback_mouse)

        # Mask
        view_mask = np.zeros_like(first_frame[:, :, 0])
        parameters_mask = np.zeros((250, 600))

        # Polygons
        view_polygon = np.array([[56, 278], [184, 277], [222, 507], [71, 509], [55, 384], [56, 416], [61, 456]])
        frame_rate_polygon = np.array([[590, 18], [590, 50], [725, 50], [725, 18]])
        rectangle_polygon = np.array([[12, 11], [144, 11], [144, 65], [12, 65]])

        poly_lane_1 = np.array([[140, 271], [182, 274], [187, 312], [149, 312]])
        poly_lane_2 = np.array([[138, 271], [98, 271], [103, 314], [147, 313]])

        cv.fillConvexPoly(view_mask, view_polygon, 1)
        cv.fillConvexPoly(view_mask, frame_rate_polygon, 1)
        cv.fillConvexPoly(view_mask, rectangle_polygon, 1)

        # Global parameters
        corn_1, corn_2 = 0, 0
        v_1, v_2 = 0, 0

        while self.camera.isOpened():
            ret, frame = self.camera.read()

            if ret:
                # Resize
                frame = cv.resize(frame, (self.width, self.height))
                frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                frame_copy = frame.copy()  # Temporary frame to execute operations

                img = cv.bitwise_and(frame_copy, frame_copy, mask=view_mask)

                # Draw text
                self.draw_param_lane_1(parameters_mask)
                self.draw_param_lane_2(parameters_mask)

                # Draw numbers
                Utility.set_text(img, "1", (145, 257), color=Color.RED, dim=3, thickness=3)
                Utility.set_text(img, "2", (100, 257), color=Color.CYAN, dim=3, thickness=3)

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

                if len(self.corners) > 0:
                    prev_img, current_img = self.previous_frame, frame_gray
                    prev_corners = np.float32([corner[-1] for corner in self.corners]).reshape(-1, 1, 2)

                    # Optical flow scattered
                    corners_1, st_1, err_1 = cv.calcOpticalFlowPyrLK(prev_img, current_img, prev_corners, None,
                                                                     **lk_params)
                    corners_2, st_2, err_2 = cv.calcOpticalFlowPyrLK(current_img, prev_img, corners_1, None,
                                                                     **lk_params)

                    # Difference between corners
                    difference = abs(prev_corners - corners_2).reshape(-1, 2).max(-1)
                    good = difference < 1
                    new_corners = []

                    for corner, (x, y), good_features in zip(self.corners, corners_1.reshape(-1, 2), good):

                        if not good_features:
                            continue

                        corner.append((round(x, 1), round(y, 1)))
                        if len(corner) > self.corners_len:
                            del corner[0]

                        new_corners.append(corner)
                        # cv.circle(frame, (int(x), int(y)), 3, Color.YELLOW, -1)

                    # Update corners
                    self.corners = new_corners

                    # Reset counter polygons
                    corn_1, corn_2 = 0, 0
                    v_1, v_2 = 0, 0
                    distance_1, distance_2 = 0, 0

                    for corner in self.corners:

                        # Determine which polygon the corner belongs to
                        is_inside_1 = cv.pointPolygonTest(poly_lane_1, corner[0], True)
                        is_inside_2 = cv.pointPolygonTest(poly_lane_2, corner[0], True)

                        if is_inside_1 > 0:
                            corn_1 += 1
                            distance_1 += Utility.calc_distance(corner[0], corner[1])
                            mmm_1 = distance_1 / corn_1
                            v_1 = self.get_velocity(mmm_1)

                        if is_inside_2 > 0:
                            corn_2 += 1
                            distance_2 += Utility.calc_distance(corner[0], corner[1])
                            mmm_2 = distance_2 / corn_2
                            v_2 = self.get_velocity(mmm_2)

                            # counter_2 += 1
                            # dif2 = tuple(map(lambda i, j: i - j, corner[0], corner[1]))
                            # mm2 += math.sqrt(dif2[0] * dif2[0] + dif2[1] * dif2[1])
                            # mmm2 = mm2 / counter_2
                            # velocity_2 = mmm2 * px2mm * self.frame_rate.fps * self.ms_2_kmh

                    self.corn_1, self.corn_2 = corn_1, corn_2

                if self.id_frame % self.detect_interval == 0:
                    f"""Update values each n-interval ({self.detect_interval}) frames"""

                    # Update velocity, corners
                    if corn_1 > self.minimum_corners:
                        self.v_1 = round(v_1, 2)
                        print(f"UPDATE VELOCITY\n1) V: {self.v_1}, C: {self.corn_1}", end="\n\n")

                        # Lane 1
                        self.draw_param_lane_1(parameters_mask)

                    if corn_2 > self.minimum_corners:
                        self.v_2 = round(v_2, 2)
                        print(f"UPDATE VELOCITY\n2) V: {self.v_2}, C: {self.corn_2}", end="\n\n")

                        # Lane 2
                        self.draw_param_lane_2(parameters_mask)

                    mask = np.zeros_like(frame_gray)
                    mask[:] = 255
                    for x, y in [np.int32(track[-1]) for track in self.corners]:
                        # Draw circles (corners), if they exist
                        cv.circle(mask, (x, y), 3, Color.GREEN, -1)

                    # cv.imshow("Mask points", mask)

                    # Calculation corners
                    corners = cv.goodFeaturesToTrack(frame_gray, mask=mask, **feature_params)
                    if corners is not None:
                        for x, y in corners.reshape(-1, 2):
                            self.corners.append([(x, y)])

                # Update id and current frame
                self.id_frame += 1
                self.previous_frame = frame_gray

                # Show views
                cv.imshow("Original", frame)
                cv.imshow(WINDOW_OPTICAL_FLOW, img)
                cv.imshow(WINDOW_PARAMETERS, parameters_mask)
                cv.waitKey(10)

    def get_velocity(self, distance):
        r"""
        Calculate velocity.
        :param distance: distance between two points.
        """
        return distance * px2mm * self.frame_rate.fps * self.ms_2_kmh

    def draw_param_lane_1(self, mask):
        r"""
        Update the parameters for lane 1.
        :param mask: mask to update the parameters.
        """
        # Portion image: (y1,y2), (x1,x2)
        mask[13:46, 170:368] = 0
        mask[44:73, 140:192] = 0

        Utility.set_text(mask, f"1-Lane speed: {self.v_1} km/h,  ", (20, 30),
                         color=Color.WHITE, dim=1.2, thickness=1)
        Utility.set_text(mask, f"1-Corners : {self.corn_1}", (20, 60), color=Color.WHITE,
                         dim=1.2, thickness=1)

    def draw_param_lane_2(self, mask):
        r"""
        Update the parameters for lane 2.
        :param mask: mask to update the parameters.
        """

        mask[84:113, 170:353] = 0
        mask[113:143, 146:210] = 0

        Utility.set_text(mask, f"2-Lane speed: {self.v_2} km/h,  ", (20, 100),
                         color=Color.WHITE, dim=1.2, thickness=1)
        Utility.set_text(mask, f"2-Corners : {self.corn_2}", (20, 130), color=Color.WHITE,
                         dim=1.2, thickness=1)


if __name__ == "__main__":
    # jackson_hole = "https://youtu.be/1EiC9bvVGnk"  # Jackson Hole (United States)
    taipei_url = "https://youtu.be/XV1q_2Cl6mI"  # Taipei (Taiwan)

    app = App(video_url=taipei_url)
    app.run()
