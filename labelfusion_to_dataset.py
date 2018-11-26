import json
import cv2
import glob
import matplotlib.pyplot as plt
import re
import numpy as np

read_path = '/home/aass/Hoang-Cuong/LabelFusion/data/logs_test/jacky-5/images/'
write_path = '/home/aass/Hoang-Cuong/Mask_RCNN/datasets/jacky/'
visual = False

if read_path[len(read_path)-1] != '/':
    print read_path
    print 'The read path should have / in the end'
    exit()
if write_path[len(write_path)-1] != '/':
    print write_path
    print 'The write path should have / in the end'
    exit()

# read addresses and labels from the 'train' folder
img_addrs = glob.glob(read_path + '*_rgb.png')

join_index = 208
max_numOfimg = 10000000000
for i in range(len(img_addrs)):
    if not i % 20:
        print 'Image: {}/{}'.format(i, len(img_addrs))

    if not i % 15:
        read_index = 10000000000 + i + 1
        write_index = 10000000000 + join_index                
        str_read_index = str(read_index)[1:11]        
        str_write_index = str(write_index)[1:11]

        rgb_addrs = read_path + str_read_index + '_rgb.png'
        depth_addrs = read_path + str_read_index + '_depth.png'
        label_addrs = read_path + str_read_index + '_labels.png'
        
        
        rgb_img = cv2.imread(rgb_addrs, -1)
        depth_img = cv2.imread(depth_addrs, -1)
        label_img = cv2.imread(label_addrs, -1)
        
        write_path_rgb = write_path + 'rgb/' + str_write_index + '_rgb.png'
        write_path_depth = write_path + 'depth/' + str_write_index + '_depth.png'
        write_path_label = write_path + 'labels/' + str_write_index + '_labels.png'
        cv2.imwrite(write_path_rgb, rgb_img)
        cv2.imwrite(write_path_depth, depth_img)
        cv2.imwrite(write_path_label, label_img)

        join_index += 1
        max_numOfimg += i

