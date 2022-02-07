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
                cv2.line(new_img,(current_former_x,current_former_y),(former_x,former_y),(0,0,255),8)
                current_former_x = former_x
                current_former_y = former_y
                layer_1_x.append(current_former_x)
                layer_1_y.append(current_former_y)
            elif mode == True and layer_num == 2:
                cv2.line(new_img,(current_former_x,current_former_y),(former_x,former_y),(0,255,0),8)
                current_former_x = former_x
                current_former_y = former_y
                layer_2_x.append(current_former_x)
                layer_2_y.append(current_former_y)
            elif mode == True and layer_num == 3:
                cv2.line(new_img,(current_former_x,current_former_y),(former_x,former_y),(255,0,0),8)
                current_former_x = former_x
                current_former_y = former_y
                layer_3_x.append(current_former_x)
                layer_3_y.append(current_former_y)



    elif event==cv2.EVENT_LBUTTONUP:
        drawing=False
        if mode==True and layer_num == 1:
            cv2.line(new_img,(current_former_x,current_former_y),(former_x,former_y),(0,0,255),8)
            current_former_x = former_x
            current_former_y = former_y
            layer_1_x.append(current_former_x)
            layer_1_y.append(current_former_y)
        elif mode == True and layer_num == 2:
            cv2.line(new_img,(current_former_x,current_former_y),(former_x,former_y),(0,255,0),8)
            current_former_x = former_x
            current_former_y = former_y
            layer_2_x.append(current_former_x)
            layer_2_y.append(current_former_y)
        elif mode == True and layer_num == 3:
            cv2.line(new_img,(current_former_x,current_former_y),(former_x,former_y),(255,0,0),8)
            current_former_x = former_x
            current_former_y = former_y
            layer_3_x.append(current_former_x)
            layer_3_y.append(current_former_y)

    return former_x,former_y


dir_name = '/Users/mac/Desktop/lab/pupil_1/original_image/'


for m in range(0, len(os.listdir(dir_name))):
    file_name = os.listdir(dir_name)[m]
    img_array = np.loadtxt(dir_name + file_name)
    img_array1 = (img_array/np.max(img_array)*200).astype(np.uint8)
    new_img = cv2.cvtColor(img_array1.astype(np.uint8), cv2.COLOR_GRAY2BGR)
    new_img = cv2.rotate(new_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    input_img = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)#for combining mask image later
    reserve_img = new_img.copy()

    layer_num = 1
    cv2.namedWindow(str(file_name))
    cv2.setMouseCallback(str(file_name), begueradj_draw)
    while(1):
        cv2.imshow(str(file_name), new_img)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            layer_1_x = []
            layer_1_y = []

            layer_2_x = []
            layer_2_y = []

            layer_3_x = []
            layer_3_y = []
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
            if len(layer_1_x) >=2:
                for i in range(0, len(layer_1_x) - 1):
                    cv2.line(mask_img,(layer_1_x[i],layer_1_y[i]),(layer_1_x[i + 1],layer_1_y[i + 1]), 1, 8)
            if len(layer_2_x) >=2:
                for i in range(0, len(layer_2_x) - 1):
                    cv2.line(mask_img,(layer_2_x[i],layer_2_y[i]),(layer_2_x[i + 1],layer_2_y[i + 1]), 1, 8)
            if len(layer_3_x) >=2:
                for i in range(0, len(layer_3_x) - 1):
                    cv2.line(mask_img,(layer_3_x[i],layer_3_y[i]),(layer_3_x[i + 1],layer_3_y[i + 1]), 1, 8)
            #tf_input = tf.keras.utils.array_to_img(input_img)
            #tf_mask = tf.keras.utils.array_to_img(np.repeat(np.expand_dims(mask_img,-1),3,-1))
            #plt.imshow(tf.keras.utils.array_to_img(input_img), cmap = "gray")
            add_image = cv2.addWeighted(input_img, 0.7, mask_img, 0.3, 0)
            cv2.imshow('combine', add_image)
            #plt.imshow(tf.keras.utils.array_to_img(np.repeat(np.expand_dims(mask_img,-1),3,-1)), cmap = "jet", alpha = 0.2)
        elif k == ord('r'):#use this if i mess up creating mask
            layer_1_x = []
            layer_1_y = []

            layer_2_x = []
            layer_2_y = []

            layer_3_x = []
            layer_3_y = []
            new_img = reserve_img.copy()
        elif k == ord('s'):
            cv2.imwrite('/Users/mac/Desktop/lab/pupil_1/input_image/' + 'input_' + str(m) + '.jpg', reserve_img.copy())
            cv2.imwrite('/Users/mac/Desktop/lab/pupil_1/output_image/' + 'output_' + str(m) + '.jpg', mask_img)
            print("save data_" + str(m))



