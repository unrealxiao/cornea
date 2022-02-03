from cmath import nan
import numpy as np
import cv2
import os

drawing = False
mode = True

layer_1_x = []
layer_1_y = []

layer_2_x = []
layer_2_y = []

layer_3_x = []
layer_3_y = []

current_former_x = nan
current_former_y = nan

def begueradj_draw(event,former_x,former_y,flags,param):
    global current_former_x,current_former_y,drawing, mode

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        current_former_x,current_former_y = former_x,former_y
    
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing==True:
            if mode==True and layer_num == 1:
                cv2.line(new_img,(current_former_x,current_former_y),(former_x,former_y),(0,0,255),5)
                current_former_x = former_x
                current_former_y = former_y
                layer_1_x.append(current_former_x)
                layer_1_y.append(current_former_y)
            elif mode == True and layer_num == 2:
                cv2.line(new_img,(current_former_x,current_former_y),(former_x,former_y),(0,255,0),5)
                current_former_x = former_x
                current_former_y = former_y
                layer_2_x.append(current_former_x)
                layer_2_y.append(current_former_y)
            elif mode == True and layer_num == 3:
                cv2.line(new_img,(current_former_x,current_former_y),(former_x,former_y),(255,0,0),5)
                current_former_x = former_x
                current_former_y = former_y
                layer_3_x.append(current_former_x)
                layer_3_y.append(current_former_y)



    elif event==cv2.EVENT_LBUTTONUP:
        drawing=False
        if mode==True and layer_num == 1:
            cv2.line(new_img,(current_former_x,current_former_y),(former_x,former_y),(0,0,255),5)
            current_former_x = former_x
            current_former_y = former_y
            layer_1_x.append(current_former_x)
            layer_1_y.append(current_former_y)
        elif mode == True and layer_num == 2:
            cv2.line(new_img,(current_former_x,current_former_y),(former_x,former_y),(0,255,0),5)
            current_former_x = former_x
            current_former_y = former_y
            layer_2_x.append(current_former_x)
            layer_2_y.append(current_former_y)
        elif mode == True and layer_num == 3:
            cv2.line(new_img,(current_former_x,current_former_y),(former_x,former_y),(255,0,0),5)
            current_former_x = former_x
            current_former_y = former_y
            layer_3_x.append(current_former_x)
            layer_3_y.append(current_former_y)

    return former_x,former_y


dir_name = '/Users/mac/Desktop/lab/pupil_1/original_image/'

file_name = os.listdir(dir_name)[1]
img_array = np.loadtxt(dir_name + file_name)
img_array1 = (img_array/np.max(img_array)*200).astype(np.uint8)
new_img = cv2.cvtColor(img_array1.astype(np.uint8), cv2.COLOR_GRAY2BGR)
new_img = cv2.rotate(new_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
input_img = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)#for combining mask image later

layer_num = 1
cv2.namedWindow("cornea")
cv2.setMouseCallback("cornea", begueradj_draw)
while(1):
    cv2.imshow("cornea", new_img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        cv2.destroyAllWindows()
        break
    elif k == ord('t'):
        layer_num = 1
    elif k == ord('m'):
        layer_num = 2
    elif k == ord('l'):
        layer_num = 3
    elif k == ord('d'):
        mask_img = np.zeros((new_img.shape[0], new_img.shape[1]), np.uint8)
        for i in range(0, len(layer_1_x) - 1):
            cv2.line(mask_img,(layer_1_x[i],layer_1_y[i]),(layer_1_x[i + 1],layer_1_y[i + 1]), 1, 5)
        add_image = cv2.addWeighted(input_img, 0.7, mask_img, 3, 0)
        cv2.imshow('combine', add_image)

print(layer_1_x[1:10])
print(layer_2_x[1:10])
print(layer_3_x[1:10])
