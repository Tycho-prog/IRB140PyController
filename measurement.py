import PIL.Image
import cv2
import pyrealsense2
from realsense_depth import *
import numpy as np #till test av ny metod

#Initialize Depth camera
dc = DepthCamera()


#def measure(x, y)-> int:

"""def color():
    
    cap = cv2.VideoCapture(0)
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.inshow("frame", frame)
    return hsv"""



def measure():  
    ret, depth_frame, color_frame = dc.get_frame()
    return depth_frame#color_frame

def measurePoint(x,y):  
    ret, depth_frame, color_frame = dc.get_frame()

    point = (y,x)
    #cv2.circle(depth_frame, point, 4, (0, 0, 255))
    #cv2.imshow("Depth frame", depth_frame)
    cv2.circle(color_frame, point, 4, (0, 0, 255))
    cv2.imshow("Color frame", color_frame)
    key = cv2.waitKey(500)
    return depth_frame[y][x]#color_frame

def showImage(x, y, name = "Color frame"): #x,y - where to put the point, name = name of image window
    ret, depth_frame, color_frame = dc.get_frame()

    point = (x, y)
    cv2.circle(color_frame, point, 4, (0, 0, 255))
    
    cv2.imshow(name, color_frame)
    key = cv2.waitKey(1)
    return color_frame

def returnImage(points, name = "Color frame"): #x,y - where to put the point, name = name of image window
    ret, depth_frame, color_frame = dc.get_frame()
    for q in range (0, len(points)):
        point = points[q]

        cv2.circle(color_frame, point, 4, (0, 0, 255))
    
    cv2.imshow(name, color_frame)
    #key = cv2.waitKey(1)
    return color_frame
 

def multPoints(points, name = "Color frame") -> int: #x,y - where to put the point, name = name of image window
    ret, depth_frame, color_frame = dc.get_frame()

    for q in range (0, len(points)):
        point = points[q]

        cv2.circle(color_frame, point, 4, (0, 0, 255))
    cv2.imshow(name, color_frame)
    
    key = cv2.waitKey(1)
    return 1
"""
    #Show distance for specific point
    point = (x, y)
    #point = (320,340)
    cv2.circle(color_frame, point, 4, (0, 0, 255))
    #Arrayn blir x, y för point omkastade
    distance = int(round((depth_frame[point[1], point[0]]))/10)
    #Verkar mäta i 0,1 mm
    #print(distance/10)


    cv2.imshow("Color frame", color_frame)
    key = cv2.waitKey(1) # waitKey(1), show screen 1ms -- waitKey(0), show screen infinitly 

    return distance
    

def BGR_frame():
    
    ret, depth_frame, color_frame = dc.get_frame()

    cv2.imshow("Color frame", color_frame)
    key = cv2.waitKey(1)

    return color_frame """