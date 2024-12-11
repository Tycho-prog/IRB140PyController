#import object2
import cv2
import measurement
import numpy as np
import Kalibrera


"""
h = Kalibrera.distToImageCenter()   
print("length to image center", h, "mm")
g = Kalibrera.distToObj(230,240)
print("length to object", g, "mm")"""

#Kalibrera.distToObj(230,250,120,300)
test = Kalibrera.defineObject(200,230,120,300)
print("NU KOMMER TEST")
print(test[0])
#print("pixels_per_mm are:",Kalibrera.pixels_per_100mm)
#Kalibrera.checkXforObj(230,250,150,250)
#dist = Kalibrera.distToObj(230,250,200,350) 
#print("distance to object center:", dist)
#print(Kalibrera.checkX_RL(240,260,70,400)) 
#val = Kalibrera.checkX(220,260)
#print("returnerat värde", val)

"""
depMat = object2.depth_matrix()
print("Hela matrisen:", depMat)

#print("längd av rad 320:", np.size(a[320]))
print("Pixel-rad nr 320:", depMat[320])

findPixNotZero = []
whatIsObj = []
for i in range(0, np.size(depMat[320]-1)):
    
    if(round(depMat[320][i]) != 0):
        findPixNotZero.append(i)
        
print("Antal pixlar i rad 320 som inte är nollor:", np.size(findPixNotZero))
print("Pixlar i rad 320 som inte är nollor:", findPixNotZero)

whereIsObj = []
prePixel = 0

for x in range (1, np.size(findPixNotZero)):
    
    if((round(depMat[320][findPixNotZero[prePixel]]) - round(depMat[320][findPixNotZero[x]])) > 200):
        whereIsObj.append(findPixNotZero[x])
        prePixel = x
    

print("whereIsObj längd:", np.size(whereIsObj))
print("whereIsObj innehåll:", whereIsObj)
h = 0
for b in range(0, np.size(whereIsObj)):
     h = measurement.showImage(320, whereIsObj[b])   
     print("object placement:", whereIsObj[b])

print("svar fr showImage:", h)"""
# ========================================================
"""
a = measurement.measure() 
print(a)
key = cv2.waitKey(0) 
print("Nu tar vi värdena")
print("1.", a[403][2])
#np.sort(a[403][2])
a[403][2].sort()  
print("2. sort:", a[403][2])

b = measurement.color()
print(b)



for i in range(320-160, 320):
    print(a[320][i])

 


dist_background = object2.background()
print("distance to background is: ", dist_background,("[mm]"))

while True:

    while True:
        key = cv2.waitKey(0)
        if key == 28:
            exit()
        
        distToMove = object.moveToHome()
        print("distance to move is:", distToMove, ("[mm]"))

        if (distToMove < 5) and (distToMove > -1):
            break

    key = cv2.waitKey(0)
    if key == 28:
        exit()
    object.defineObjX(dist_background)

    key = cv2.waitKey(0)
    if key == 28:
        exit()
    object.defineObjY(dist_background)"""