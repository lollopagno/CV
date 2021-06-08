import cv2 as cv
import mediapipe as mp
import time
import numpy as np


class HandDetector:
    r"""
    # TODO documentation
    """

    def __init__(self, mode=False, max_hands=2, detection_confidence=0.5, tracking_confidence=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode,
                                         self.max_hands,
                                         self.detection_confidence,
                                         self.tracking_confidence)

        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        r"""
        # TODO documentation
        :param img:
        :param draw:
        :return:
        """

        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:  # Detect multi hands
            for handLms in self.results.multi_hand_landmarks:
                if draw:        
                    self.mp_draw.draw_landmarks(img, handLms, self.mp_hands.HAND_CONNECTIONS)

    def find_position(self, img, hand_no=0, draw=True):
        r"""
        # TODO documentation
        :param img:
        :param hand_no:
        :param draw:
        :return:
        """

        lm_list = []

        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            for _id, lm in enumerate(my_hand.landmark):
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