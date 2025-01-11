import cv2
from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np

class CustomerTracking:
    def __init__(self):
        self.customers = OrderedDict()
        self.disappeared = OrderedDict()
        self.customer_id_counter = 0
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.max_disappeared = 50

    def register(self, centroid, bbox):
        self.customers[self.customer_id_counter] = (centroid, bbox)
        self.disappeared[self.customer_id_counter] = 0
        self.customer_id_counter += 1

    def deregister(self, customer_id):
        del self.customers[customer_id]
        del self.disappeared[customer_id]

    def update(self, rects):
        if len(rects) == 0:
            for customer_id in list(self.disappeared.keys()):
                self.disappeared[customer_id] += 1
                if self.disappeared[customer_id] > self.max_disappeared:
                    self.deregister(customer_id)
            return self.customers

        input_centroids = []
        input_bboxes = []
        for (x, y, w, h) in rects:
            cX = int((x + x + w) / 2.0)
            cY = int((y + y + h) / 2.0)
            input_centroids.append((cX, cY))
            input_bboxes.append((x, y, w, h))

        if len(self.customers) == 0:
            for i in range(0, len(input_centroids)):
                self.register(input_centroids[i], input_bboxes[i])
        else:
            customer_ids = list(self.customers.keys())
            customer_centroids = [data[0] for data in self.customers.values()]

            D = dist.cdist(np.array(customer_centroids), np.array(input_centroids))

            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]

            used_rows = set()
            used_cols = set()

            for (row, col) in zip(rows, cols):
                if row in used_rows or col in used_cols:
                    continue

                customer_id = customer_ids[row]
                self.customers[customer_id] = (input_centroids[col], input_bboxes[col])
                self.disappeared[customer_id] = 0

                used_rows.add(row)
                used_cols.add(col)

            unused_rows = set(range(0, D.shape[0])).difference(used_rows)
            unused_cols = set(range(0, D.shape[1])).difference(used_cols)

            if D.shape[0] >= D.shape[1]:
                for row in unused_rows:
                    customer_id = customer_ids[row]
                    self.disappeared[customer_id] += 1
                    if self.disappeared[customer_id] > self.max_disappeared:
                        self.deregister(customer_id)
            else:
                for col in unused_cols:
                    self.register(input_centroids[col], input_bboxes[col])

        return self.customers

    def track_customer(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        rects = [(x, y, w, h) for (x, y, w, h) in faces]
        customers = self.update(rects)
        return list(customers.keys())

    def get_customer_data(self):
        return self.customers