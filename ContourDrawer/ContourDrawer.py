import cv2 as cv
import numpy as np
import os
import xml.etree.ElementTree as ET

def convertTo8b(filename):
    img = cv.imread(filename)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    cv.imwrite(filename,gray)

# DRAW CONTOURS
def drawContours(contours, filename):
    # white blank image
    cont_img = 255 * np.ones(shape=[512, 512, 3], dtype=np.uint8)

    for cnt in contours:
        cv.drawContours(cont_img, [cnt], 0, (0,0,0), 1)
    
    cv.imshow('contours',cont_img)
    cv.waitKey(0)
    cv.imwrite(filename, cont_img)
    convertTo8b(filename)

# u,v - poloha miniobrazka vramci obrazka
# od x,y treba odcitat okraje edge_points a u,v
def makeContours(folder, filename, u, v, min_area, max_area, min_circ):
    # READ XML & SAVE CONTOURS
    root = ET.parse(folder+'/'+filename).getroot()

    ## hranicne body
    eX = eY = 30
    #edge_x = []
    #edge_y = []
    #i = 0
    #for point in root.findall('AOIs/AOI/Point'):
    #    x = int(point.get('x'))
    #    y = int(point.get('y'))
    #    if i < 2:
    #        edge_x.append(x)
    #    if i == 1 or i == 2:
    #        edge_x.append(y)

    contours = []
    contours_area = []
    contours_circ = []
    for cont in root.findall('Contours/Contour'):
        contour = []
        for point in cont.findall('Point'):
            x = int(point.get('x')) - eX - u*512
            y = int(point.get('y')) - eY - v*512
            contour.append([x,y])
        contour = np.array(contour, dtype=np.int32)
        contours.append(contour) # add to all contours
        print(contour)

        # filter according to area
        area = cv.contourArea(contour)
        if area > min_area and area < max_area:
            #print(area)
            contours_area.append(contour)

        # filter according to circularity
        circ = cv.approxPolyDP(contour,0.01*cv.arcLength(contour,True),True)
        if len(circ) > min_circ:
            #print(circ)
            contours_circ.append(contour)
    

    drawContours(contours, folder + '/' + str(v) + ',' + str(u) + 'cont_all.png')
    drawContours(contours_area, folder + '/' + str(v) + ',' + str(u) + 'cont_area.png')
    drawContours(contours_circ, folder + '/' + str(v) + ',' + str(u) + 'cont_circ.png')

#makeContours('c01', '0,1.txt', 1, 0, 100, 300, 10)

def readXMLfiles(folder):
    for filename in os.listdir(folder):
        s1 = filename.split('.')
        if s1[1] == 'txt':
            s2 = s1[0].split(',')
            makeContours(folder, filename, int(s2[1]), int(s2[0]), 100, 300, 10)

readXMLfiles('c01')