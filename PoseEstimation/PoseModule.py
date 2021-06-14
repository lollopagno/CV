import mediapipe as mp
import cv2 as cv


class PoseDetector:
    r"""
    Class pose estimation
    """

    def __init__(self,
                 mode=False,
                 up_body=False,
                 smooth=True,
                 detection_confidence=0.5,
                 tracking_confidence=0.5):

        self.mode = mode
        self.up_body = up_body
        self.smooth = smooth
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        self.mp_draw = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(self.mode, self.up_body, self.smooth, self.detection_confidence,
                                      self.tracking_confidence)

    def find_pose(self, img, draw=True):
        r"""
        Find pose estimation.
        :param img: image in which to draw the pose estimation.
        :param draw: flag, true if draw the pose estimation.
        """
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.result = self.pose.process(imgRGB)

        if self.result.pose_landmarks:
            if draw:
                self.mp_draw.draw_landmarks(img, self.result.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

        return img

    def find_position(self, img, draw=True):
        r"""
        Find pose estimation by your ids
        :param img: image in which to draw the pose estimation.
        :param draw: flag, true if draw the pose estimation.
        :return: list containing the position of pose.
        """

        lm_list = []

        for _id, lm in enumerate(self.result.pose_landmarks.landmark):
            r"""
            :param id: id della coordinata
            :param lm: coordinate x,y,z rispetto al piano
            """
            height, width, n_channel = img.shape
            cx, cy = int(lm.x * width), int(lm.y * height)
            lm_list.append([_id, cx, cy])

            if draw:
                cv.circle(img, (cx, cy), 7, (0, 255, 255), cv.FILLED)

        return lm_list
