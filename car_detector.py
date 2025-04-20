import cv2
import torch


CAR_CLASS_ID = 2  # (COCO class 2 is 'car')


class CarDetector:
    def __init__(self):
        """
        Load a Yolov5 model for car detection
        TODO Load the model from the local file without downloading again
        """
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5s.pt', force_reload=False)
        print(self.model)

    def detect_cars(self, frame):
        """
        Run YOLO inference to detect cars only.
        """
        results = self.model(frame)
        detections = results.xyxy[0]  # x1, y1, x2, y2, conf, class
        car_boxes = []

        for *box, conf, cls in detections:
            if int(cls) == CAR_CLASS_ID:
                x1, y1, x2, y2 = map(int, box)
                car_boxes.append((x1, y1, x2, y2, conf.item()))

                # Draw bounding box and label on frame
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"Car {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        print(f"Detected {len(car_boxes)} cars.")
        return frame
