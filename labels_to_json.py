import json
import cv2
import glob
import matplotlib.pyplot as plt
import re
import numpy as np

#data_path = '/home/hoang/Datasets/data-test/labels/'
data_path = '/home/aass/Hoang-Cuong/Mask_RCNN/datasets/jacky/labels/val/'
visual = False

if data_path[len(data_path)-1] != '/':
    print data_path
    print 'The data path should have / in the end'
    exit()

data = {}
image_addrs = glob.glob(data_path + '*.png')

def load_label_image(addr):
    img = cv2.imread(image_addrs[i], -1)
    if visual == True:
        cv2.imshow('img', img)
        cv2.waitKey(100)
        plt.imshow(img)
        plt.show()
    return img

def is_edge_point(img, row, col):
    rows, cols = img.shape
    value = (int)(img[row, col])
    if value == 0:
        return False
    count = 0
    for i in range(-1,2):
        for j in range(-1,2):
            if row + i >= 0 and row + i < rows and col + j >= 0 and col + j < cols:
                value_neib = (int)(img[row+i, col+j])
                if value_neib == value:
                    count = count + 1 
    if count > 2 and count < 8:
        return True
    return False

def edge_downsample(img):
    rows, cols = img.shape
    for row in range(rows):
        for col in range(cols):
            if img[row, col] > 0:
                for i in range(-2, 3):
                    for j in range(-2, 3):
                        if i==0 and j==0:
                            continue
                        roww = row + i
                        coll = col + j
                        if roww>=0 and roww<rows and coll>=0 and coll<cols:
                            if img[roww, coll] == img[row, col]:
                                img[roww, coll] = 0
    return img

def next_edge(img, obj_id, row, col):
    rows, cols = img.shape
    incre = 1
    while(incre < 10):            
        for i in range(-incre, incre+1, 2*incre):
            for j in range(-incre, incre+1, 1):        
                roww = row + i
                coll = col + j
                if roww>=0 and roww<rows and coll>=0 and coll<cols:
                    value =img[roww, coll]
                    if value == obj_id:
                        return True, roww, coll
        for i in range(-incre+1, incre, 1):
            for j in range(-incre, incre+1, 2*incre):        
                roww = row + i
                coll = col + j
                if roww>=0 and roww<rows and coll>=0 and coll<cols:
                    value =img[roww, coll]
                    if value == obj_id:
                        return True, roww, coll
        incre = incre + 1
    return False, row, col

def find_region(img, obj_id, row, col):
    region = {}
    region['region_attributes'] = {}
    region['shape_attributes'] = {}

    rows, cols = img.shape
    roww = row
    coll = col
    edges_x = []
    edges_y = []
    find_edge = True
    poly_img = np.zeros((rows, cols), np.uint8)
    
    while(find_edge):
        edges_x.append(coll)
        edges_y.append(roww)
        img[roww, coll] = 0
        poly_img[roww, coll] = 255
        if visual==True:
            cv2.imshow('polygon', poly_img)
            cv2.waitKey(3)
        find_edge, roww, coll = next_edge(img, obj_id, roww, coll)
        #print(find_edge)

    edges_x.append(col)
    edges_y.append(row)
    region['shape_attributes']["name"] = "polygon"
    region['shape_attributes']["all_points_x"] = edges_x
    region['shape_attributes']["all_points_y"] = edges_y
    return region, img

def write_to_json(img, img_name):
    rows, cols = img.shape
    regions = {}

    edge_img = np.zeros((rows, cols), np.uint8)      
    
    for row in range(rows):
        for col in range(cols):
            if is_edge_point(img, row, col) == True:
                edge_img[row, col] = img[row, col]
                #print(edge_img[row, col])

    edge_img = edge_downsample(edge_img)

    if visual == True:
        plt.imshow(edge_img)
        plt.show()

    ids = []
    ids.append(0)
    count = 0
    for row in range(rows):
        for col in range(cols):
            id = edge_img[row, col]
            if id not in ids:
                #print(id)
                region, edge_img = find_region(edge_img, id, row, col)
                regions[str(count)] = region
                count = count + 1
                ids.append(id)

    #cv2.imwrite("edge.png", edge_img)

    img_name = img_name.replace('labels', 'rgb')
    #print(img_name)
    obj_name = img_name + "1024"
    data[obj_name] = {}
    data[obj_name]['fileref'] = ""
    data[obj_name]['size'] = 1024
    data[obj_name]['filename'] = img_name
    data[obj_name]['base64_img_data'] = ""
    data[obj_name]['file_attributes'] = {}
    data[obj_name]['regions'] = regions
    return

#for i in range(2):
for i in range(len(image_addrs)):
    #if not i % 10:
    print 'Image: {}/{}'.format(i, len(image_addrs))
    img_name = image_addrs[i][len(data_path):]
    #print(img_name)
    label_img = load_label_image(image_addrs[i])
    write_to_json(label_img, img_name)

with open('via_region_data.json', 'w') as outfile:  
    json.dump(data, outfile, sort_keys=True)