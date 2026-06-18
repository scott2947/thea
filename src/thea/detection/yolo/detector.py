import numpy as np
from ultralytics import YOLO
from thea.detection.base import BaseDetector
from thea.config import GRID_WIDTH, GRID_HEIGHT


TENNIS_BALL_CLASS_ID = 32 # sports ball class includes tennis ball


class YoloDetector(BaseDetector):
    def __init__(self, model: str = "yolo26n.pt", conf: float = 0.25):
        self.model = YOLO(model)
        self.model.to("mps")
        self.conf = conf
    
    def detect(self, frame: np.ndarray) -> list:
        frame_h, frame_w = frame.shape[:2]

        results = self.model.predict(
            frame,
            conf=self.conf, 
            classes=[TENNIS_BALL_CLASS_ID],
            device="mps",
            verbose=False
        )
        
        targets = []
        for result in results:
            if result.boxes is None:
                continue
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                cx = (x1 + x2) / 2.0
                cy = (y1 + y2) / 2.0

                gx = cx / frame_w * GRID_WIDTH
                gy = cy / frame_h * GRID_HEIGHT
                targets.append([gx, gy])
        
        return targets


if __name__ == "__main__":
    pass
