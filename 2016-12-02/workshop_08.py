from larlib import *
import csv


"""This function generates a 2D model based on a .lines file. """
def generate_2D_walls(fileName):
	with open("lines_file/" + fileName +  ".lines", "rb") as file:
		reader = csv.reader(file, delimiter=",")
		polygonLines = []
		for line in reader:
			polygonLines.append(POLYLINE([[float(line[0]), float(line[1])],[float(line[2]), float(line[3])]]))
	wall = STRUCT(polygonLines)
	return wall

"""This functions generates all 2D models in the points were a door or a window is supposed to be. Using the difference these cubes will be deleted from the walls, to reach the model"""
def make_holes(fileName):
	with open("lines_file/" + fileName + ".lines", "rb") as file:
		reader = csv.reader(file, delimiter=",")
		holes = []
		basePol = []
		cont = 0
		for line in reader:
			cont +=1
			#creating polygon base using vertices
			basePol.append([float(line[0]),float(line[1])])
			#create a cube with 4 vertices and restart finding
			if(cont == 4):
				holes.append(MKPOL([basePol,[[1,2,3,4]],None]))
				basePol = []
				cont = 0
	holes = STRUCT(holes)
	return holes
	

"""using the functions previous created, here it is computated the entire structure.
   It takes in input the files .lines needed for computation in this order: external_walls, internal_walls, doors, windows"""
def ggpl_build_house(ext,intr,door,windw):

	#generating 2D external walls
	external = generate_2D_walls(ext)
	floor = SOLIDIFY(external)

	#defining scaling factors
	xfactor = 15/SIZE([1])(external)[0]
	yfactor = 15.1/SIZE([2])(external)[0]
	zfactor = xfactor

	#building external 3D-walls
	walls = OFFSET([15,15])(external)
	walls = PROD([walls, Q(3/xfactor)])

	#generating internal 2D-walls
	internal = generate_2D_walls(intr)

	#building internal 3D-walls
	internals = OFFSET([8,8])(internal)
	internals = PROD([internals, Q(3/xfactor)])

	#producing Hpc values for polygons that will be holes in walls
	doors=make_holes(door)
	doors = PROD([doors, Q(3/xfactor)])
	windows = make_holes(windw)
	windows = PROD([windows, Q(2/xfactor)])
	windows = T(3)(SIZE([3])(walls)[0]/4.)(windows)
	
	#applying holes to structure using DIFFERENCE
	internals = DIFFERENCE([internals,doors])
	walls = DIFFERENCE([walls,doors,windows])
	
	house = S([1,2,3])([xfactor,yfactor, zfactor])(STRUCT([walls,internals]))
		
	floor = (S([1,2,3])([xfactor,yfactor, xfactor])(floor))
	floor = TEXTURE("floor.jpg")(floor)
	
	house= TEXTURE("bricks.jpg")(house)
	return STRUCT([house,floor])	


if __name__=='__main__':
	house = ggpl_build_house("external","internal","doors","window")
	#house2 = ggpl_build_house("external2","internal2","doors2","winodws2")
	VIEW(house)
	#VIEW(house2)
