# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 15:17:55 2020

@author: Akshay
"""

import glob
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import imutils


images = glob.glob("D:\\My_project\\Image segmentation model\\Main image folde\\Apple\\*.jpg")

file_count = len(images)
for i in range(0,file_count):
    i=5
    image = images[i]
    image = cv.imread(image)
    
    im_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    plt.imshow(im_rgb)
    
    plt.imshow(image)
    # Convert image in grayscale
    gray_im = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    plt.imshow(gray_im)
    # # plt.subplot(221)
    # plt.title('Grayscale image')
    # plt.imshow(gray_im, cmap="gray", vmin=0, vmax=255)
    blur = cv.GaussianBlur(image, (9,9), 0)
    blur2 = cv.GaussianBlur(image, (27,27), 0)
    plt.imshow(blur)
    edges = cv.Canny(blur,75,75)
    edges2 = cv.Canny(blur2,75,75)
    plt.imshow(edges)
    
    ### Morphological transformations
    kernel =np.ones((6,6))
    closing = cv.morphologyEx(edges, cv.MORPH_CLOSE, kernel)
    closing=closing/255
    plt.imshow(closing)
    
    kernel =np.ones((15,15))
    erosion = cv.dilate(edges2, kernel, iterations= 1 )
    erosion = erosion/255
    plt.imshow(erosion)

    mask = np.zeros(gray_im.shape, dtype=np.uint8)
    diff = cv.bitwise_and(erosion,closing)
    diff = diff.astype(np.uint8)
    # plt.figure()
    # plt.subplot(221)
    # plt.title('Image_1')
    # plt.imshow(closing)
    # plt.subplot(222)
    # plt.title('Image_2')
    # plt.imshow(erosion)
    # plt.subplot(223)
    # plt.title('Difference')
    # plt.imshow(diff)
    
    
    
    def flood_fill(input_img):
    	im_floodfill = input_img.copy()
    
        # Taking two pixels more than the actual image
    	h, w = input_img.shape[:2]
    	mask = np.zeros((h+2, w+2), np.uint8)
    
    	# Floodfill from point (0, 0)
    	cv.floodFill(im_floodfill, mask, (0,0), 255);
    
    	# Inverting floodfilled image
    	im_floodfill_inv = cv.bitwise_not(im_floodfill)
    
    	# Combine the two images to get the foreground.
    	out_img = input_img | im_floodfill_inv
    
    	return out_img
    
    fill = flood_fill(diff)
    plt.imshow(fill)
 
    
    ret,thresh = cv.threshold(fill,0,1,0)
    plt.imshow(thresh)
    
    im2,contours,hierarchy = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    # This step is for finding actual contours
    items = cv.findContours(thresh,cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    
    for c in contours:
        # cv.boundingRect(c)::  straight rectangle, it doesn't consider the rotation of the object.
        #For rotatiated boundbox use cv.minAreaRect(cnt)
        rect = cv.boundingRect(c)    
        x,y,w,h = rect
        Boundbox = cv.rectangle(im_rgb,(x,y),(x+w,y+h),(0,255,0),1)
        plt.imshow(Boundbox)
        # Saving the region of interest
        image_patch = im_rgb[y:y+h, x:x+w]
        plt.imshow(image_patch)
        plt.imsave("ROI.png", image_patch)
        
        
        #FInding actual contours of the object        
        cnts = imutils.grab_contours(items)
        c = max(cnts, key=cv.contourArea)
        # draw the contours of c
        Act_con= cv.drawContours(im_rgb, [c], -1, (0, 0, 255), 1)
        plt.imshow(Act_con) 

        
        
        #### Additional physical parameters
        M = cv.moments(c)
        print( M )
        # Calculating centroid of the region
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        print('\nCx = ', cx)
        print('Cy = ', cy)
        print('Centroid = ',(cx,cy))
        ###Contour area
        area = cv.contourArea(c)
        print('Area = ',area)
        

        # plt.figure()
        # plt.subplot(221)
        # plt.title('Image_1')
        # plt.imshow(Boundbox)
        # plt.subplot(222)
        # plt.title('ROI')
        # plt.imshow(image_patch)
    

    
    
    
    
    
    
   

   
    