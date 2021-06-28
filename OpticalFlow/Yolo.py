import cv2 as cv
import numpy as np


class Yolo:

    def __init__(self):
        # Net paramenters
        self.net = None
        self.layers_names = None
        self.output_layers = None

        # Predict
        self.outputs = None
        self.boxes = []
        self.confidence = []
        self.class_ids = []

        self.classes = None
        self.colors = None

        # Image parameters
        self.img = None
        self.height = 0
        self.width = 0

    def load_yolo(self):
        self.net = cv.dnn.readNet("yolo/yolov2.weights", "yolo/yolo.cfg")

        with open("yolo/coco.names", "r") as f:
            self.classes = [line.strip() for line in f.readlines()]

        self.layers_names = self.net.getLayerNames()
        self.output_layers = [self.layers_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))

    def load_image(self, img):
        self.img = img
        self.img = cv.resize(self.img, None, fx=0.4, fy=0.4)
        self.height, self.width, _ = self.img.shape

    def detect_objects(self):

        blob = cv.dnn.blobFromImage(self.img, scalefactor=0.00392, size=(320, 320), mean=(0, 0, 0), swapRB=True,
                                    crop=False)
        self.net.setInput(blob)
        self.outputs = self.net.forward(self.output_layers)

    def get_box_dimensions(self):

        for output in self.outputs:
            for detect in output:

                scores = detect[5:]
                # print(scores)
                class_id = np.argmax(scores)
                conf = scores[class_id]

                if conf > 0.3:
                    center_x = int(detect[0] * self.width)
                    center_y = int(detect[1] * self.height)

                    w = int(detect[2] * self.width)
                    h = int(detect[3] * self.height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    self.boxes.append([x, y, w, h])
                    self.confidence.append(float(conf))
                    self.class_ids.append(class_id)

        return self.boxes, self.confidence, self.class_ids

    def draw_labels(self):
        indexes = cv.dnn.NMSBoxes(self.boxes, self.confidence, 0.5, 0.4)

        try:
            for i in range(len(self.boxes)):
                if i in indexes:
                    x, y, w, h = self.boxes[i]
                    label = str(self.classes[self.class_ids[i]])
                    color = self.colors[i]
                    cv.rectangle(self.img, (x, y), (x + w, y + h), color, 2)
                    cv.putText(self.img, label, (x, y - 5), cv.FONT_HERSHEY_PLAIN, 1, color, 1)
        except Exception as e:
            print(f"Exception: {e}")

        cv.imshow("YOLO", self.img)
