import cv2 as cv
import numpy as np
import time
import os

orb = cv.ORB_create(nfeatures=250)  # Descriptor
matcher = cv.BFMatcher()  # Matcher


def load_images(path):
    cards = []
    cards_name = []
    my_cards = os.listdir(path)

    for card in my_cards:
        img = cv.imread(f"{path}/{card}", 0)
        cards.append(img)
        cards_name.append(os.path.splitext(card)[0])

    print(f"Cards loaded: {len(cards)}")
    return cards, cards_name


def get_descriptors(cards):
    global orb
    descriptor_total = []

    for card in cards:
        _, desc = orb.detectAndCompute(card, None)
        descriptor_total.append(desc)

    return descriptor_total


def find_card(img, descriptors, threshold=15):
    global orb, matcher

    match_total = []
    result = -1
    kp, desc_2 = orb.detectAndCompute(img, None)

    try:
        for desc in descriptors:
            matches = matcher.knnMatch(desc, desc_2, k=2)
            good = []

            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append([m])
            match_total.append(len(good))
    except:
        pass

    if len(match_total) != 0:
        if max(match_total) > threshold:
            result = match_total.index(max(match_total))

    return result, kp


cards, cards_name = load_images("cards")
descriptors = get_descriptors(cards)

cap = cv.VideoCapture(0)
previous_time = 0

while True:

    success, frame = cap.read()

    if success:
        # Frame rate
        current_time = time.time()
        fps = np.divide(1, current_time - previous_time)
        previous_time = current_time

        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        id_card, kp_input_card = find_card(frame_gray, descriptors)
        if id_card != -1:
            cv.putText(frame, cards_name[id_card], (450, 35), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)

        img_kp = cv.drawKeypoints(frame, kp_input_card, None, (255, 0, 0), 2)

        cv.putText(frame, f"FPS: {int(fps)}", (10, 35), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        cv.imshow("Keypoint", img_kp)
        cv.imshow("Current frame", frame)
        cv.waitKey(1)
