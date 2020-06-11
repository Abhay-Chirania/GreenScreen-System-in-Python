import cv2
cap=cv2.VideoCapture('1b.mp4')
width,height=512,288
op=cv2.VideoWriter('1bResize.mp4',cv2.VideoWriter_fourcc(*'XVID'),5,(512,384))
while 1:
    ret,frame=cap.read()
    if ret:
        b=cv2.resize(frame,(512,384),fx=0,fy=0,interpolation=cv2.INTER_CUBIC)
        op.write(b)
    else:
        break
print("Done")
cap.release()
op.release()
cv2.destroyAllWindows()
