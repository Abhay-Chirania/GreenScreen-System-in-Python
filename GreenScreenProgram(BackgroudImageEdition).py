import cv2
import numpy as np
from time import sleep
def nothing(x):
        pass


def customColorTool(frame):
    #frame=cv2.rotate(frame,cv2.ROTATE_90_CLOCKWISE)
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    while 1:  
        lh=cv2.getTrackbarPos('LH',"Trackbars")
        ls=cv2.getTrackbarPos('LS',"Trackbars")
        lv=cv2.getTrackbarPos('LV',"Trackbars")
        uh=cv2.getTrackbarPos('UH',"Trackbars")
        us=cv2.getTrackbarPos('US',"Trackbars")
        uv=cv2.getTrackbarPos('UV',"Trackbars")
        l_b=np.array([lh,ls,lv])
        u_b=np.array([uh,us,uv])   
        mask=cv2.inRange(hsv,l_b,u_b)
        kernel=np.ones((5,5),np.uint8)
        mask=cv2.medianBlur(mask,5)
        mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
        mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)

        bg=cv2.bitwise_and(frame,frame,mask=mask)
        cv2.putText(bg,"Adjust the bars to as to select only the background that is to be removed",(30,30),cv2.FONT_HERSHEY_SIMPLEX,0.35,(0,255,0))
        cv2.putText(bg,"Press s to save and start",(20,65),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0))
        cv2.imshow("original",frame)
        cv2.imshow("mask",mask)
        cv2.imshow("bg",bg)

        if cv2.waitKey(1) & 0xFF==ord('s'):
            break
    cv2.destroyAllWindows()
    return l_b,u_b

ogVideo="1aResize.mp4"                                          #Unedited_Video
bgImg="bg.png"                                                #Background_Image
cap=cv2.VideoCapture(ogVideo)  
bg_img=cv2.imread(bgImg)                                   #background image
ret,frame=cap.read()
bg_img=cv2.resize(bg_img,(frame.shape[1],frame.shape[0]))       #reshaping the background to fit the foreground
#bg_img=cv2.resize(bg_img,(frame.shape[0],frame.shape[1]))       #reshaping the background to fit the foreground
print(frame.shape,bg_img.shape)

x=int(input("Enter 1 to enter hardcoded range or 2 for picking the range using Tool: "))
if x==1:
    print("\nEnter values between 0-255 seperated by ','")
    lh,ls,lv=input("Enter Low-Hue,Low-Sat,Low-Value: ").split(',')
    uh,us,uv=input("Enter High-Hue,High-Sat,High-Value: ").split(',')
    lh,ls,lv=int(lh),int(ls),int(lv)
    uh,us,uv=int(uh),int(us),int(uv)
    l_b=np.array([lh,ls,lv])
    u_b=np.array([uh,us,uv])
else:
    cv2.namedWindow("Trackbars")
    cv2.createTrackbar('LH',"Trackbars",0,255,nothing)
    cv2.createTrackbar('LS',"Trackbars",0,255,nothing)
    cv2.createTrackbar('LV',"Trackbars",0,255,nothing)
    cv2.createTrackbar('UH',"Trackbars",255,255,nothing)
    cv2.createTrackbar('US',"Trackbars",255,255,nothing)
    cv2.createTrackbar('UV',"Trackbars",255,255,nothing)
    if ret:
        l_b,u_b=customColorTool(frame)

saveVideo=cv2.VideoWriter('Result.mp4',cv2.VideoWriter_fourcc(*'XVID'),10,(frame.shape[0],frame.shape[1]))
#sleep(5)
while 1:
    ret,frame=cap.read()
    if ret:
        #frame=cv2.rotate(frame,cv2.ROTATE_90_CLOCKWISE)
        hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        
        
        #making the mask and applying smoothening and removing some bg noise
        mask=cv2.inRange(hsv,l_b,u_b)
        kernel=np.ones((5,5),np.uint8)
        mask=cv2.medianBlur(mask,5)
        mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
        mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
        mask_inv=cv2.bitwise_not(mask)

        #bitwise operations
        bg=cv2.bitwise_and(bg_img,bg_img,mask=mask)
        fg=cv2.bitwise_and(frame,frame,mask=mask_inv)
        result=cv2.add(fg,bg)

        #displayig the video
        cv2.imshow("Original",frame)
        cv2.imshow("Result",result)
        cv2.moveWindow("Original",100,200)
        cv2.moveWindow("Result",700,200)
        saveVideo.write(result)
        if cv2.waitKey(15) & 0xFF==ord('q'):
            break
    else:
         break
cap.release()
saveVideo.release()
cv2.destroyAllWindows()
print("Your Video has been saved")

