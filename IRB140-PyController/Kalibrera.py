import measurement
import cv2
import numpy as np
import math

#översätt värden i cm på sågbordet till pixlar i image
global xPixel_5cm
global xPixel_10cm
global xPixel_15cm
global pixels_per_mm 
global depth_at_calibration

def calibrate2():
    counter = 0
    depth = 0

    for a in range(1, 4):
        
        print("Place the block at", a*5 , "cm, on the sawing table. When the block is in place; push enter.") #förtydliga att det är mot bordskanten
        key = cv2.waitKey(0)
        
        x = checkX(230,250,100,250)
        key = cv2.waitKey(0)
        #x2 = checkX_RL(230,250,100,350)
        depth = depth + distToImageCenter() #block is placed right in front of the fence of the sawing table - the distance for every position should be the same
        counter = counter +1 
        print("x has parameters:", x)
                        
        if(a == 1):
            xPixel_5cm = x
            print("5cm => pixel:", x)#, "ends att pixel:", x2)
        if(a == 2):   
            xPixel_10cm = x         
            print("10cm => pixel:", x)
        if(a == 3):
            xPixel_15cm = x
            print("15cm => pixel:", x)
    pixels_per_50mm = ((xPixel_10cm - xPixel_5cm)/50 + (xPixel_15cm - xPixel_10cm)/50)/2
    pixels_per_100mm = (xPixel_15cm - xPixel_5cm)/100
    pixels_per_mm = (pixels_per_50mm + pixels_per_100mm)/2
    depth_at_calibration = round(depth/counter)

def angle(): # challange here is to find the angles for pixels in between the values from the calibration
    
    pi = math.pi
    angle = 0
    closest_distance_to_block = defineObject()[0] - 320

    #if(defineObject[0] < 0):

    nearest_edge = defineObject()[0]
    right_edge = checkX_RL(230,250,100,250)

    # case 1 (left edge located left of image center and short side of block hidden from camera point of view):
    dist_to_left_edge = nearest_edge[1]
    pixel_of_left_edge = nearest_edge[0]
    dist_to_image_center = distToImageCenter()
    sinKatet = 0
    cosKatet = 0

    if (pixel_of_left_edge < 320): # solve problem if "pixel_of_left_edge" is 320 - solution: search right edge
        nbr_pixels = (320-1) - pixel_of_left_edge
        angle = math.atan(depth_at_calibration/(nbr_pixels/pixels_per_mm))*(360/pi)# angle between image center and obj left edge
        
        sinKatet = math.sin*dist_to_left_edge*(360/pi)
        cosKatet = math.cos*dist_to_left_edge*(360/pi)


    # tells robot how much closer to the camera block has to move, to be at the wanted position 
def distToPos(wantedPos = 150) -> int: # wantedPo - how close the user wants the block to be, to the camera
    
    wantedPosition = wantedPos
    distance = distToObj()
    distToMove = distance - wantedPos
    return distToMove

def distToObj(minY, maxY, minDist = 70, maxDist = 350) -> int: # minY - maxY, selected band of rows. min/maxDist distances to filter 
    
    
    while True:

        matrix = measurement.measure()
        object = checkXforObj(minY,maxY,minDist,maxDist)
        minX = int(object[0])
        maxX = int(object[1])
        midX = round((minX+maxX)/2)
        minY = int(object[2])
        sumDist = 0
        counter = 0
        print("center of object is at pixel:", midX)
        

        for y in range(minY-10, minY+30):
            for x in range(midX-5,midX+5):
                #measurement.showImage(x,y,"Finding center distanse")
                distance = round((matrix[x][y])/10)
                if (distance != 0):
                    sumDist = sumDist + distance
                    counter = counter + 1
        break
    return int(sumDist/counter)

def distToImageCenter():
    
    loop(30) # might skip this one
    while True:
        
        matrix = measurement.measure()
        sumDist = 0
        counter = 0        

        for y in range(220, 260):
            for x in range(315,325):
                #measurement.showImage(x,y,"Finding distanse to center of image")
                distance = round((matrix[x][y])/10)
                print("distance to point", distance)
                if (distance != 0):
                    sumDist = sumDist + distance
                    counter = counter + 1
        break
    return round(sumDist/counter)

def checkXforObj(minY, maxY, minDist = 70, maxDist = 500) -> int: # minY - maxY, selected band of rows. min/maxDist distances to filter 
    
    loop(30)
    matrix = measurement.measure()         
    xcoordinates = []
    prex = 1000
    sum = 0
    i = 0
    
    # search a band of rows in the image, left to right
    for y in range (minY, maxY, 1): 
        for x in range (0, 640-1): # search for block edge, one row at a time  
                #print("fine search - x-koordinat is:", x)    
                if ((round(matrix[y][x]/10)) < maxDist) and (minDist < (round(matrix[y][x]/10))): # checkX - skillt fr 0 o mindre än back tableEdge
                    xcoordinates.append(x)
                    sum = sum+x
                    i = i+1
                    if(x < prex):
                        prex = x
                    break                 
    print("x-coordinat is:", x,"in y:", y)
    #print("xcoordinates:", np.sort(xcoordinates))
    if (i != 0):
        avrundatX = round(sum/i)
        #measurement.showImage(avrundatX,y, "med avrundat vaerde:") 
        #measurement.showImage(x,y, "utan avrundat vaerde:") #testa vad som funkar bäst på blocken, avrundat värde eller ej
    else:
        x = "there's nothing in that range of distance" 
   
    xcoordinates2 = []
    prex = 1000
    sum = 0
    i = 0
    # search a band of rows in the image, right to left
    for y2 in range (minY, maxY, 1):        # search for block edge, one row at a time
        for x2 in range (640-1, 0, -1):     # search row for block edge   
                #print("fine search - x-koordinat is:", x)    
                if ((round(matrix[y2][x2]/10)) < maxDist) and (minDist < (round(matrix[y2][x2]/10))): # checkX - skillt fr 0 o mindre än back tableEdge
                    xcoordinates2.append(x2)
                    sum = sum+x2
                    i = i+1
                    if(x2 > prex):
                        prex = x2
                    break
    #measurement.showImage(x2,y2, "utan avrundat vaerde:") #testa vad som funkar bäst på blocken, avrundat värde eller ej        
    #print("Xcoordinat is:", x2,"in y2:", y2)
    print("xcoordinates:", np.sort(xcoordinates2))
    if (i != 0):
        avrundatX = round(sum/i)
        #measurement.showImage(avrundatX,y, "med avrundat vaerde:") 
    else:
        x2 = "there's nothing in that range of distance" 
    points = ([x,y],[x2,y2])
    print("object found:",points)
    #measurement.multPoints(points, "Object found")
    if(y2>y):
        y2 = y

    object = [x,x2,y]
    return object # (returns min & max x value and the highest y-value)



def matrix(x, y, minY=0, maxY=640, ):
    measurement.measure()

# nbr - how many images you wanna take to let the camera calibrate, and in what band of rows you are interested
def loop(nbr, minY = 0, maxY = 480-1): 
    counter = 0
    least_zeros = 1000000

    for i in range(0, nbr):
        counter = counter +1  
        zeros = 0  
        current_image = measurement.measure() 
        if(counter >= int((nbr*2)/3)): #check for best depth_image quality, in users wanted y-range  
            for y in range (minY, maxY):
                for x in range(0, 640-1):
                    if(current_image[y][x] == 0):   #check if the pixel has a zero value
                        zeros = zeros +1
            if(zeros < least_zeros):
                deliver_image = current_image
                least_zeros = zeros
    return deliver_image


def checkX(minY, maxY, minDist = 70, maxDist = 500) -> int: # minY - maxY, selected band of rows. min/maxDist distances to filter 

    loop(30)
    matrix = measurement.measure()         
    xcoordinates = []
    prex = 1000
    medDistX = 0
    sum = 0
    i = 0
    
    # search a band of rows in the image
    for y in range (minY, maxY): 
        for x in range (0, 640-1): # search for block edge, one row at a time  
                #print("fine search - x-koordinat is:", x)    
                if ((round(matrix[y][x]/10)) < maxDist) and (minDist < (round(matrix[y][x]/10))): # checkX - skillt fr 0 o mindre än back tableEdge
                    xcoordinates.append(x)
                    if(x>190):
                        measurement.showImage(x,y,"checkX search:")
                    medDistX = medDistX + round(matrix[y][x]/10)
                    print("depth of x-pixels are:", round(matrix[y][x]/10))
                    sum = sum+x
                    i = i+1
                    if(x < prex):
                        prex = x
                    break
    medDistX = round(medDistX/i)       
    print("x-coordinat is:", x,"in y:", y)
    print("xcoordinates:", np.sort(xcoordinates))
    
    if (i != 0):
        avrundatX = round(sum/i)
        #measurement.showImage(avrundatX,y, "med avrundat vaerde:") 
        #measurement.showImage(x,y, "utan avrundat vaerde:") #testa vad som funkar bäst på blocken, avrundat värde eller ej

    else:
        x = "there's nothing in that range of distance" 
   
       
    return [x, medDistX] # (returns most left x pixel and its depth value)

def checkX_RL(minY, maxY, minDist = 70, maxDist = 500) -> int: # minY - maxY, selected band of rows. min/maxDist distances to filter 

    loop(30)
    matrix = measurement.measure()         
    xcoordinates = []
    prex = 1000
    sum = 0
    medDistX = 0
    i = 0
    
    # search a band of rows in the image
    for y in range (minY, maxY, 1): 
        for x in range (640-1, 0, -1): # search for block edge, one row at a time  

                #print("fine search - x-koordinat is:", x)    
                if ((round(matrix[y][x]/10)) < maxDist) and (minDist < (round(matrix[y][x]/10))): # checkX - skillt fr 0 o mindre än back tableEdge
                    xcoordinates.append(x)
                    #measurement.showImage(x,y,"checkX search:")
                    medDistX = medDistX + round(matrix[y][x]/10)
                    print("depth of x-pixels are:", round(matrix[y][x]/10))
                    sum = sum+x
                    i = i+1
                    if(x > prex):
                        prex = x
                    break
    #measurement.showImage(x,y, "utan avrundat vaerde:") #testa vad som funkar bäst på blocken, avrundat värde eller ej        
    #print("Xcoordinat is:", x,"in y:", y)
    print("xcoordinates:", np.sort(xcoordinates))
    medDistX = round(medDistX/i) 

    if (i != 0):
        avrundatX = round(sum/i)
        #measurement.showImage(avrundatX,y, "med avrundat vaerde:") 
       
    else:
        x = "there's nothing in that range of distance" 
   
       
    return [x, medDistX] # (returns minimum x value)

def defineObject(minY, maxY, minDist = 70, maxDist = 500) -> int: # minY - maxY, selected band of rows. min/maxDist distances to filter 

    loop(60, minY, maxY)
    matrix = measurement.measure()         
    coordinates = []
    shortest_distance = [1000,0,0]
    medDistX = 0
    #prev_distance = 1000
    sum = 0
    i = 0
    b = 20
    c = 25

    #find object with checkXforObj and let it set values for angle_search
    boundries = checkXforObj(minY, maxY, minDist, maxDist) 
    minX = boundries[0] -25
    maxX = boundries[1] +25
    print("minX:", minX, "maxX", maxX)

    # search a band of rows in the image
    for y in range (minY, maxY): 
        i = 0
        prev_distance = 0
        for x in range (minX, maxX): # search for block edge, one row at a time  
            currDist = int(matrix[y][x]/10) 
                #print("curr x", x)  
                
            """if(currDist == 0): # this might be to much
                print("currDist = 0, at:",x ,y)
                spec_point = measurement.measurePoint(x,y)
                print("found this value:", round(spec_point/10))
                if(spec_point > 0):
                    currDist = round(spec_point/10)"""

            if (currDist < maxDist) and (minDist < currDist): # checkX - skillt fr 0 o mindre än back tableEdge
                    
                #coordinates.append([currDist,x,y])
                #measurement.showImage(x,y, "search closest pixel:")
                if (currDist > prev_distance):
                        i = i + 1
                        print("prev_distance", prev_distance)
                        print("current distance is:", currDist)
                        print("i is:", i) 
                        if (i == b):        #if the distances becomming longer, break loop 
                            maxX = x
                            b = b-1
                            break
                else:
                        minX = x-c     #set new boundries for minX(-10, at first)
                        c = c -1
                        if (currDist < shortest_distance[0]): # if current value is shorter then prev shortest value, replace the prev with current
                            shortest_distance.remove(shortest_distance[0])
                            shortest_distance = [currDist,x,y]
                prev_distance = currDist
                 # ARRAY = [a,b,c,d]
                 # POINT = (A,B)  
                points = ([boundries[0],boundries[2]],[boundries[1],boundries[2]])
                frameToReturn = measurement.returnImage(points) #(x,y, "search closest pixel:")
    
    #print("sorted list", np.sort(coordinates))
    #measurement.showImage(np.sort(coordinates)[1][2],np.sort(coordinates)[1][1], "closest pixel:")
    #print("xcoordinates:", np.sort(coordinates)[0])
    print("shortest distance of block is:", shortest_distance)
    #measurement.showImage(shortest_distance[1], shortest_distance[2], "shortest distance")
    return [shortest_distance[0],shortest_distance[1],frameToReturn] # (returns most left x pixel and its depth value)


"""==========================================

# = används inte, ny version calibrate2
def calibrate():
    
    tableEdge = 500 
    sum = 0
    i = 0
    for a in range(1, 4):
        
        print("Place the block at", a*5 , "cm, on the sawing table. When the block is in place; push enter.") #förtydliga att det är mot bordskanten
        key = cv2.waitKey(0)
        loop(30)
        matrix = measurement.measure()  
        
        xcoordinates = []
        pixels = []
        prex = 1000
        
        # search a band of rows in the image
        for y in range (220, 260, 2): 
            for x in range (0, 640-1): # search for block edge, one row at a time  

                #print("fine search - x-koordinat is:", x)    
                if (0 < (round(matrix[y][x]/10)) < tableEdge):# and (0 < (round(matrix[y][x]/10))): # checkX - skillt fr 0 o mindre än back tableEdge
                    xcoordinates.append(x)
                    pixels.append([x,y])
                    sum = sum+x
                    i = i+1
                    if(x < prex):
                        prex = x
                    break
                        
        print("x-coordinat is:", x,"in y:", y)
        print("xcoordinates:", np.sort(xcoordinates))
        print("pixel coordinates is:", pixels)
        if(a == 1):
            measurement.showImage(x,y, "Color Frame, utan avrundning")
            xPixel_5cm = x
            xTest = round(sum/i)
            measurement.showImage(xTest,y, "Color Frame, med avrundning")
            measurement.multPoints(pixels, "Color Frame Pixels")
            print("5cm avrundad", xTest)
            print("5cm", xPixel_5cm)
        if(a == 2):            
            measurement.showImage(x,y)
            xPixel_10cm = x
            print("10cm", xPixel_10cm)
        if(a == 3):
            measurement.showImage(x,y)
            xPixel_15cm = x
            print("15cm", xPixel_15cm)
            #np.clear(xcoordinates)"""
