import cv2 as cv
import numpy as np
import time
import os
from FeatureMatching.FeatureMatching import Matching

NAME_WINDOW = "Original"


def load_images(path):
    cards = []
    cards_name = []
    my_cards = os.listdir(path)

    for card in my_cards:
        img = cv.imread(f"{path}/{card}", cv.IMREAD_GRAYSCALE)
        img = cv.resize(img, (150, 150))
        cards.append(img)
        cards_name.append(os.path.splitext(card)[0])

    return cards, cards_name


cards, cards_name = load_images("../Homography/cards")

feature_matcher = Matching(cards)
descriptors = feature_matcher.get_descriptors()

# Camera
cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_AUTOFOCUS, 1)

previous_time = 0

while True:

    success, frame = cap.read()

    if success:

        # Frame rate
        current_time = time.time()
        fps = np.divide(1, current_time - previous_time)
        previous_time = current_time
        # ******************** #

        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        original_frame = frame.copy()

        # Feature matching
        id_card, kp_input_card, good = feature_matcher.find_card(frame)
        if id_card != -1:
            cv.putText(frame, cards_name[id_card], (450, 35), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)

        img_kp = cv.drawKeypoints(frame, kp_input_card, None, (255, 0, 0), 2)
        # ******************** #

        cv.putText(frame, f"FPS: {int(fps)}", (10, 35), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        # cv.imshow("Keypoint", img_kp)
        # cv.imshow("Current frame", frame)
        cv.imshow(NAME_WINDOW, original_frame)
        cv.waitKey(1)

        if len(good) != 0:
            img_match = cv.drawMatchesKnn(cards[0], descriptors[0][0], frame_gray, kp_input_card, good, None,
                                          flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

            cv.imshow("Matches", img_match)
            cv.waitKey(1)

    else:
        print("An error is occurred!")
        break
