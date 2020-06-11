import cv2

videoPath="2.mp4"
imagePath="back2.png"
cap=cv2.VideoCapture(videoPath)
_,frame=cap.read()
cv2.imwrite(imagePath,frame)
cap.release()
cv2.destroyAllWindows()
