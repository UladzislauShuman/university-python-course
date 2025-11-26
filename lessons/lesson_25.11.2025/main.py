import cv2
import numpy as np
def adjust_contrast(frame, alpha):
    # alpha >1—увеличение контрастности
    new_frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=0)
    return new_frame
cap = cv2.VideoCapture('1.mp4')
out = cv2.VideoWriter('contrast_video.mp4',
cv2.VideoWriter_fourcc(*'mp4v'), cap.get(cv2.CAP_PROP_FPS),
(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

while True:
    ret, frame = cap.read()
    if not ret:
       break
    contrasted = adjust_contrast(frame, alpha=1.5)
    out.write(contrasted)
cap.release()
out.release()