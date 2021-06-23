import cv2 as cv


class Matching:
    # TODO Matching not found

    def __init__(self, cards):
        self.cards = cards
        self.descriptors = []
        self.orb = cv.ORB_create()
        self.matcher = cv.BFMatcher()

    def get_descriptors(self):

        for card in self.cards:
            kp, desc = self.orb.detectAndCompute(card, None)
            self.descriptors.append([kp, desc])

    def find_card(self, img, threshold=15):

        match_total = []
        good = []
        result = -1

        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        kp, desc_2 = self.orb.detectAndCompute(img_gray, None)

        try:
            for desc in self.descriptors:
                matches = self.matcher.knnMatch(desc[1], desc_2, k=2)

                for m, n in matches:
                    if m.distance < 0.75 * n.distance:
                        good.append([m])
                match_total.append(len(good))

        except Exception as e:
            # print(f"Error: {e}")
            pass

        if len(match_total) != 0:
            if max(match_total) > threshold:
                result = match_total.index(max(match_total))

        return result, kp, good
