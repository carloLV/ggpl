from larlib import *
import csv
import math


#***************************************

def dot(vA, vB):
    return vA[0]*vB[0]+vA[1]*vB[1]
def ang(lineA, lineB):
    # Get nicer vector form
    vA = [(lineA[0][0]-lineA[1][0]), (lineA[0][1]-lineA[1][1])]
    vB = [(lineB[0][0]-lineB[1][0]), (lineB[0][1]-lineB[1][1])]
    # Get dot prod
    dot_prod = dot(vA, vB)
    # Get magnitudes
    magA = dot(vA, vA)**0.5
    magB = dot(vB, vB)**0.5
    # Get cosine value
    cos_ = dot_prod/magA/magB
    # Get angle in radians and then convert to degrees
    angle = math.acos(dot_prod/magB/magA)
    # Basically doing angle <- angle mod 360
    ang_deg = math.degrees(angle)%360

    if ang_deg-180>=0:
        # As in if statement
        return 360 - ang_deg
    else: 

        return ang_deg


#****************************************


def make_couples(lines):
	t=[]	
	for i in range(len(lines)-1):
		temp=[[lines[i][0],lines[i][1]],[lines[i][2],lines[i][3]]]
		temp2=[[lines[i+1][0],lines[i+1][1]],[lines[i+1][2],lines[i+1][3]]]
		t.append((temp,temp2))
	temp2= [[lines[0][0],lines[0][1]],[lines[0][2],lines[0][3]]]
	temp=[[lines[i+1][0],lines[i+1][1]],[lines[i+1][2],lines[i+1][3]]]
	t.append((temp,temp2))
	return t

def make_angles(t):
	angles=[]
	for (temp,temp2) in t:
		angulus=ang(temp,temp2)
		angles.append((angulus,temp,temp2))
	"""angles is a variable of type -> (angle between line 1 and 2, line1, line2). With this operation I can traslate"""
	"""points to produce new lined that will be delimiters for the roof planes we want tu build"""
	return angles
	#print angles
	#print len(angles)
	#for el in t:
	#	print (math.atan2(el[0],el[1]))

"""This function generates a 2D model based on a .lines file for the roof. It also returns a list of tuples of type (angle,line1,line2)"""
def generate_2D_walls(fileName):
	with open(fileName, "rb") as file:
		reader = csv.reader(file, delimiter=",")
		polygonLines = []
		lines = []
		for line in reader:
			polygonLines.append(POLYLINE([[float(line[0]), float(line[1])],[float(line[2]), float(line[3])]]))
			lines.append([float(line[0]), float(line[1]),float(line[2]), float(line[3])])
	wall = STRUCT(polygonLines)
	c=make_couples(lines)
	#print c
	
	angles = make_angles(c)	
	return (wall,angles) 

def ggpl_build_roof():
	(lines,angles)= generate_2D_walls("roof.lines")
	#fixed dimensions for heigth and slope
	slope = PI/6
	heigth = 7
	tan = math.atan(slope)
	OH = tan/heigth
	#iterates on angles list to create lines
	#for (ang,l1,l2) in angles:
	VIEW(lines)
	p = PYRAMID(lines,MKPOL())		
	 
	#VIEW(lines)


if __name__=='__main__':
	ggpl_build_roof()

