import numpy as np
import cv2
import os

drawing = False
mode = True

x_cordinate = []
y_cordinate = []

def begueradj_draw(event,former_x,former_y,flags,param):
    global current_former_x,current_former_y,drawing, mode

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing == True
        current_former_x,current_former_y = former_x,former_y
    
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing==True:
            if mode==True:
                cv2.line(new_img,(current_former_x,current_former_y),(former_x,former_y),(0,0,255),5)
                current_former_x = former_x
                current_former_y = former_y
                print(former_x)
                x_cordinate.append(current_former_x)
                y_cordinate.append(current_former_y)



    elif event==cv2.EVENT_LBUTTONUP:
        drawing=False
        if mode==True:
            cv2.line(new_img,(current_former_x,current_former_y),(former_x,former_y),(0,0,255),5)
            current_former_x = former_x
            current_former_y = former_y
            x_cordinate.append(current_former_x)
            y_cordinate.append(current_former_y)
    return former_x,former_y


dir_name = '/Users/mac/Desktop/lab/pupil_1/original_image/'

file_name = os.listdir(dir_name)[1]
img_array = np.loadtxt(dir_name + file_name)
img_array1 = (img_array/np.max(img_array)*200).astype(np.uint8)
new_img = cv2.cvtColor(img_array1.astype(np.uint8), cv2.COLOR_GRAY2BGR)
new_img = cv2.rotate(new_img, cv2.ROTATE_90_COUNTERCLOCKWISE)

cv2.namedWindow("cornea")
cv2.setMouseCallback("cornea", begueradj_draw)
while(1):
    cv2.imshow("cornea", new_img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        cv2.destroyAllWindows()
        break


print(x_cordinate)
