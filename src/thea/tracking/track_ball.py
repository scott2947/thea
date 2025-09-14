from picamera2 import Picamera2
import cv2
import numpy as np

picam2 = Picamera2()
picam2.preview_configuration.main.size = (1000, 800)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()

while True:
    frame = picam2.capture_array()
    frame = cv2.flip(frame, 1)
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv, (80, 90, 90), (95, 255, 255))

    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)

        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.circle(frame, (x + w//2, y + h//2), 5, (0, 0, 255), -1)
        cv2.putText(frame, f"Ball ({x+w//2}, {y+h//2})", (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    cv2.imshow("Tennis Ball Tracker", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

picam2.close()
cv2.destroyAllWindows()