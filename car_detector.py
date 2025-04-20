import cv2
from ultralytics import YOLO


CAR_CLASS_ID = 2  # (COCO class 2 is 'car')


class CarDetector:
    def __init__(self):
        """
        Load a Yolov5 model for car detection.
        """
        self.model = YOLO("yolov8n.pt")  # or "yolov8s.pt" for a slightly better accuracy TODO benchmark with some metric
        print(self.model)

    def detect_cars(self, frame):
        """
        Run YOLO inference to detect cars only.
        """
        results = self.model(frame)
        boxes = results[0].boxes

        car_boxes = []

        for xyxy, conf, cls in zip(boxes.xyxy, boxes.conf, boxes.cls):
            if int(cls.item()) == CAR_CLASS_ID:
                x1, y1, x2, y2 = map(int, xyxy.tolist())
                car_boxes.append((x1, y1, x2, y2, float(conf.item())))
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"Car {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        print(f"Detected {len(car_boxes)} cars.")
        return frame
