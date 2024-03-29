import cv2 as cv
import mediapipe as mp


class HandDetector:
    r"""
    Class hand detector
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
        self.tip_ids = [4, 8, 12, 16, 20]

    def find_hands(self, img, draw=True):
        r"""
        Find hands.
        :param img: image in which to draw the found hands.
        :param draw: flag, true if draw the hands.
        """

        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:  # Detect multi hands
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, handLms, self.mp_hands.HAND_CONNECTIONS)

        return img

    def find_position(self, img, hand_no=0, draw=True):
        r"""
        Find position hands by your ids
        :param img: image in which to draw the positions.
        :param hand_no: index of the array containing the hands.
        :param draw: flag, true if draw the positions.
        :return: list containing the position of hands.
        """

        self.lm_list = []

        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            for _id, lm in enumerate(my_hand.landmark):
                r"""
                :param id: id della coordinata
                :param lm: coordinate x,y,z rispetto al piano
                """
                height, width, n_channel = img.shape
                cx, cy = int(lm.x * width), int(lm.y * height)
                self.lm_list.append([_id, cx, cy])

                if draw:
                    cv.circle(img, (cx, cy), 7, (0, 255, 255), cv.FILLED)

        return self.lm_list

    def fingers_up(self):
        r"""
        Detect which fingers are ups.
        """
        fingers = []

        # Thumb
        if self.lm_list[self.tip_ids[0]][1] < self.lm_list[self.tip_ids[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for _id in range(1, 5):
            if self.lm_list[self.tip_ids[_id]][2] < self.lm_list[self.tip_ids[_id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

            # totalFingers = fingers.count(1)

        return fingers
