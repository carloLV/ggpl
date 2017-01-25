from pyplasm import *
import csv
import math
import numpy
from itertools import *

"""This function generates a list of points based on a .lines file given in
   input, that represents the shape of the roof. 
	
   @params: a .lines file
   @return: a list representing all points of the shape"""
def generate_2D_vertecesList(fileName):
	with open( fileName + ".lines", "rb") as file:
		reader = csv.reader(file, delimiter=",")
		vertexList = []
		for line in reader:
			vertexList.append([float(line[0]), float(line[1])])
			vertexList.append([float(line[2]), float(line[3])])
	return vertexList 


"""Simply calculates distance from 2 points
   
   @params: two points
   @return: their distance
"""
def distance(p1,p2):
	return float(math.sqrt(math.pow((p1[0] - p2[0]), 2)+math.pow((p1[1] - p2[1]), 2)))


"""This function calculates the best heigth for the given roof, based on its area.
   
   @params: the area of the polygon
   @return : a float representing the heigth
"""
def calculate_height(vertexList):
	#iterates on sides for determing average value of side's length	
	sideNumber=0
	perimeter=0
	for i in range(len(vertexList)-1):
		p1 = vertexList[i]
		p2 = vertexList[i+1]
		perimeter += distance(p1,p2)
		sideNumber +=1
	p1 = vertexList[0]
	p2 = vertexList[-1]
	perimeter += distance(p1,p2)
	sideNumber +=1
	averageSide = perimeter / sideNumber
	area = calculate_area(*zip(*vertexList))
	h = area/(perimeter / 2)
	return h
	


"""This function is used to calculate the area of a given polygon

   @params: 
   @return:
"""
def calculate_area(x,y):
	area = .0
	for i in xrange(-1,len(x)-1):
		area += x[i] * (y[i+1]-y[i-1])
	return area/2.0


"""This function remove duplicates from a list.

   @params: a list that contains duplicates
   @return: the same list whithout duplicates
"""
def no_duplicates(l):
	retList = []
	for el in l:
		if el not in retList:
			retList.append(el)
	return retList


"""This function is used to visit all verteces in a clockwise order.
   It permits to create all faces of the roof well oriented

   @params: a list of verteces
   @return the list in a clockwise order
"""
def clockwise_order(verteces):
	pointOne = verteces[0]
	centroid = [pointOne[0],pointOne[1]+0.0000001]
	lengthOne =  float(math.sqrt(math.pow((centroid[0] - pointOne[0]), 2)+math.pow((centroid[1] - pointOne[1]), 2)))
	retVerteces = []

	while len(verteces)>0:
		cos = 400
		for i in range(len(verteces)):
			pt = verteces[i]
			angle =  math.atan2(pt[1]-centroid[1],pt[0]-centroid[0])
		if angle < cos:
			cos = angle
			temp = pt
		retVerteces.append(temp)
		
		for k in range(len(verteces)):
			if verteces[k]==temp:
				cont = k
		verteces.pop(cont)

	return retVerteces


"""This function uses a list of vertex in input and uses that for calculating the centroid.
   This centroid is then used for calculating the pyramid whith same center
   as centroid.

   @params: a list of verteces
   @return: x and y coordinate of centroid
"""
def calculate_centroid(vertexList):

	area = calculate_area(*zip(*vertexList))
	xRet =0
	yRet =0
	#length = len(vertexList)
	allPoints = cycle(vertexList)
	x1,y1 = next(allPoints)
	for i in xrange(len(vertexList)):
		x0,y0 = x1,y1
		x1,y1 = next(allPoints)
		cross =  (x0 * y1) - (x1 * y0)
                xRet += (x0 + x1) * cross
		yRet += (y0 + y1) * cross
	xRet /= area*6.0
	yRet /= area*6.0
	return (xRet,yRet) 


"""This is the main function that creates all parts of the roof. Using all the helper functions,
   firstly it calculates the basic shape, then it calculates the top part of 
   the roof, and eventually it builds the lateral planes for completing the structure.

   @params: the name of the file containing the .lines model of the shape
   @return: the Hpc model of the roof , completed with texture
"""
def ggpl_build_roof(filename):
	pol = []
	polTop=[]
	lateralPlanes = []
	j=0
	c=0
	verteces= generate_2D_vertecesList(filename)
	centroid = calculate_centroid(verteces)
	#height = calculate_height(verteces)
	height = 40
	for f in range(len(verteces)):
		verteces[f][0]=verteces[f][0]-centroid[0]
		verteces[f][1]=verteces[f][1]-centroid[1]
	while j<(len(verteces)):
		pol.append(POLYLINE([verteces[j],verteces[j+1]]))
		j+=2
	pol = STRUCT(pol)
	infPlane = SOLIDIFY(pol)	
	#this is the list for top part of the roof
	top_verteces = []
	for i in range(len(verteces)):
		top_verteces.append([verteces[i][0]/2.0,verteces[i][1]/2.0])
	
	verteces = no_duplicates(verteces)
	verteces = clockwise_order(verteces)
	top_verteces = no_duplicates(top_verteces)
	top_verteces = clockwise_order(top_verteces)
	top_verteces.append(top_verteces[0])
	verteces.append(verteces[0])
	
	while c < len(top_verteces)-1:
		polTop.append(POLYLINE([top_verteces[c],top_verteces[c+1]]))
		c += 1

	polTop = STRUCT(polTop)
	plane = SOLIDIFY(polTop)
	plane = T(3)(height)(plane) 	
		
	for w in range(len(verteces)):
		verteces[w] = verteces[w] + [float(0)]
		
	for q in range(len(top_verteces)):
		top_verteces[q] = top_verteces[q] + [float(height)]
	
	s = 0
	while s < len(no_duplicates(verteces)):
		lateralPlanes.append(MKPOL([[verteces[s],verteces[s+1],top_verteces[s],top_verteces[s+1]],[[1,2,3,4]],None]))
		s += 1
	lateralPlanes = STRUCT(lateralPlanes)
	completeRoof = STRUCT([infPlane,lateralPlanes,plane])

	xTrasl,yTrasl = centroid
	completeRoof = T([1,2])([xTrasl,yTrasl])(completeRoof)
	
	return completeRoof

if __name__=='__main__':
	ggpl_build_roof("roof")
	ggpl_build_roof("roof2")

