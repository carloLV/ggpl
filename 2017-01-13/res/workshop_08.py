from larlib import *
import workshop_7 as w7
import workshop_09 as w9
import workshop_03 as w3
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

"""This function calculates the right values to traslate the house and the roof in the same point.
   
   @params: filename of external walls
   @return: traslation's values
"""
def calculate_traslate_factor(fileName):
	xTrasl = 0
	yTrasl = 0
	with open("lines_file/" + fileName +  ".lines", "rb") as file:
		reader = csv.reader(file, delimiter=",")
		for line in reader:
			
			"""p1 = [float(line[0]), float(line[1])]
			p2 = [float(line[2]), float(line[3])]
			dist = w9.distance(p1,p2)
			if round(p1[0],1) == round(p2[0],1) and yTrasl < dist:
				yTrasl = p1[1]
				xTrasl = p2[0]
			if round(p1[1],1) == round(p2[1],1) and xTrasl < dist:
				xTrasl = p1[0]
				yTrasl = p2[1]
			
			if xTrasl<float(line[0]):
				xTrasl = float(line[0])
			elif xTrasl<float(line[2]):
				xTrasl = float(line[2])
			if yTrasl<float(line[1]):
				yTrasl = float(line[1])
			elif yTrasl<float(line[3]):
				yTrasl = float(line[3])
			"""	
		if float(line[0]) > float(line[2]):
			xTrasl= float(line[0])
			yTrasl= float(line[1])
		else: 
			xTrasl = float(line[2])
			yTrasl= float(line[3])
	return xTrasl,yTrasl
				
		


"""This functions reads a .line file and creates all spaces in wall in which a door will be placed. Then it creates the Hpc models
   that will be placed in the created holes. The input is necessary for adequaty scaling the models. 
   It return 2 STRUCT: one for holes and one for doors
	@params: xFactor, yFactor
	@return (doors,holes)"""
def make_doors(xFactor,yFactor):

	
	#@param for doors
	xDo=[.06,.07,.12,.09,.06]
	yDo=[.15,.15,.15,.15,.15,.15,.15]
	bDo=[[1,1,1,1,1],[1,1,0,0,1],[1,1,1,1,1],[1,0,0,1,1],[1,1,1,1,1],[1,1,0,0,1],[1,1,1,1,1]]

	with open("lines_file/" + 'porte' + ".lines", "rb") as csvFile:
		reader = csv.reader(csvFile, delimiter=",")
		holes = []
		basePol = []
		cont = 0
		yDim=0
		xDim=0
		createdDoors = []
		for line in reader:
			cont +=1
			basePol.append([float(line[0])*xFactor,float(line[1])*yFactor])
			if cont < 3: 
				if round(float(line[0]), 1) == round(float(line[2]), 1):
					yDim = abs(float(line[3]) - float(line[1]))
				 		
				elif round(float(line[1]), 1) == round(float(line[3]), 1):
                    			xDim = abs(float(line[2]) - float(line[0]))
									
			#create a cube with 4 vertices and restart finding
			if(cont == 4):
				holes.append(MKPOL([basePol,[[1,2,3,4]],None]))
				basePol = []
				door = CUBOID([0,0,0])
				cont = 0
				if (xDim < yDim):
					door = w7.ggpl_door(xDo,yDo,bDo)(yDim*yFactor,.2,3)
					door = T([1,2])([-0.1,0.4])(door)
					door = R([1,2])(-PI/2)(door)
				else:
					door = w7.ggpl_door(xDo,yDo,bDo)(xDim*xFactor,.2,3)
					door = T([1,2])([0,0.1])(door)
				door = T([1,2])([float(line[0])*xFactor,float(line[1])*yFactor])(door)
				createdDoors.append(door)
	doors = STRUCT(createdDoors)

	holes = STRUCT(holes)
	
	#VIEW(doors)
	return doors,holes

"""This functions reads a .line file and creates all spaces in wall in which a window will be placed. Then it creates the Hpc models
   that will be placed in the created holes. The input is necessary for adequaty scaling the models. 
   It return 2 STRUCT: one for holes and one for windows
	@params: xFactor, yFactor
	@return (windows,holes)"""
def make_windows(xFactor,yFactor):
	
	#@param for building windows
	xWin=[.05,.7,.05,.7,.05]
	yWin=[.05,.7,.05,.7,.05]
	bWin=[[1,1,1,1,1],[1,0,1,0,1],[1,1,1,1,1],[1,0,1,0,1],[1,1,1,1,1]]

	
	with open("lines_file/" + 'finestre' + ".lines", "rb") as csvFile:
		reader = csv.reader(csvFile, delimiter=",")
		holes = []
		basePol = []
		createdWindows = []
		cont = 0
		for line in reader:
			cont +=1
			basePol.append([float(line[0])*xFactor,float(line[1])*yFactor])
			if cont < 3: 
				if round(float(line[0]), 1) == round(float(line[2]), 1):
					yDim = abs(float(line[3]) - float(line[1]))
				 		
				elif round(float(line[1]), 1) == round(float(line[3]), 1):
                    			xDim = abs(float(line[2]) - float(line[0]))
									

			#create a cube with 4 vertices and restart finding
			if(cont == 4):
				holes.append(MKPOL([basePol,[[1,2,3,4]],None]))
				basePol = []
				window = CUBOID([0,0,0])
				cont = 0
				if (xDim < yDim):
					window = w7.ggpl_window(xWin,yWin,bWin)(yDim*yFactor,.6,1.5)
					window = R([1,2])(-PI/2)(window)
				else:
					window = w7.ggpl_window(xWin,yWin,bWin)(xDim*xFactor,.6,1.5)
					window = T(2)(-0.2)(window)
				window = T([1,2,3])([float(line[0])*xFactor, float(line[1])*yFactor,1])(window)
				createdWindows.append(window)

	windows = STRUCT(createdWindows)

	holes = STRUCT(holes)
	
	#VIEW(windows)
	return windows,holes


"""This is the analog function of make_doors; it is used for external doors. """
def make_external_doors(xFactor, yFactor):
	#@param for doors
	xDo=[.06,.07,.12,.09,.06]
	yDo=[.15,.15,.15,.15,.15,.15,.15]
	bDo=[[1,1,1,1,1],[1,1,0,0,1],[1,1,1,1,1],[1,0,0,1,1],[1,1,1,1,1],[1,1,0,0,1],[1,1,1,1,1]]

	with open("lines_file/" + 'porte_esterne' + ".lines", "rb") as csvFile:
		reader = csv.reader(csvFile, delimiter=",")
		holes = []
		basePol = []
		cont = 0
		yDim=0
		xDim=0
		createdDoors = []
		for line in reader:
			cont +=1
			basePol.append([float(line[0])*xFactor,float(line[1])*yFactor])
			if cont < 3: 
				if round(float(line[0]), 1) == round(float(line[2]), 1):
					yDim = abs(float(line[3]) - float(line[1]))
				 		
				elif round(float(line[1]), 1) == round(float(line[3]), 1):
                    			xDim = abs(float(line[2]) - float(line[0]))
			
			#create a cube with 4 vertices and restart finding
			if(cont == 4):
				holes.append(MKPOL([basePol,[[1,2,3,4]],None]))
				basePol = []
				door = CUBOID([0,0,0])
				cont = 0
				if (xDim < yDim):
					door = w7.ggpl_door(xDo,yDo,bDo)(yDim*yFactor,.2,2.5)
					door = T([1,2])([-0.1,0.4])(door)
					door = R([1,2])(-PI/2)(door)
				else:
					door = w7.ggpl_door(xDo,yDo,bDo)(xDim*xFactor,.2,2.5)
					door = T([1,2])([0,0.1])(door)
				door = T([1,2])([float(line[0])*xFactor,float(line[1])*yFactor])(door)
				createdDoors.append(door)
	doors = STRUCT(createdDoors)

	holes = STRUCT(holes)
	
	stair = w3.ggpl_stair(4.,3.,3.5)
	stair = T([1,2])([float(line[0]) * xFactor-4.5, float(line[1]) * yFactor])(stair)	
	stair= TEXTURE("texture/bricks.jpg")(stair)
	
	
	return (doors,holes,stair)


"""using the functions previous created, here it is computated the entire structure.
   It takes in input the files .lines needed for computation in this order: external_walls, internal_walls, doors, windows"""
def ggpl_build_house(ext,intr,door,windw):

	#generating 2D external walls
	external = generate_2D_walls(ext)

	#defining scaling factors
	xfactor = 16/SIZE([1])(external)[0]
	yfactor = 16/SIZE([2])(external)[0]
	zfactor = xfactor

	#building external 3D-walls
	external = S([1,2])([xfactor,yfactor])(external)
	floor = SOLIDIFY(external)
	walls = OFFSET([.2,.2])(external)
	walls = PROD([walls, Q(3.5)]) 	

	#generating internal 2D-walls
	internal = generate_2D_walls(intr)

	#building internal 3D-walls
	internal =  S([1,2])([xfactor,yfactor])(internal)
	internals = OFFSET([.2,.2])(internal)
	internals = PROD([internals, Q(3)])

	#producing Hpc values for polygons that will be holes in walls
	(doors,dHoles)=make_doors(xfactor,yfactor)
	dHoles = OFFSET([.2,.15])(dHoles)
	dHoles = PROD([dHoles,Q(3)])
	#doors = PROD([doors, Q(2/xfactor)])

	(windows,wHoles) = make_windows(xfactor,yfactor)
	wHoles = OFFSET([0.15,0.15])(wHoles)
	wHoles = PROD([wHoles,Q(1.5)])
	wHoles = T(3)(1)(wHoles)

	(extDoors,extHoles,stairs)=make_external_doors(xfactor,yfactor)
	extHoles = OFFSET([0,.15])(extHoles)
	extHoles = PROD([extHoles,Q(2.5)])

	#applying holes to structure using DIFFERENCE
	internals = DIFFERENCE([internals,dHoles])
	internals = STRUCT([internals,doors])
	walls = DIFFERENCE([walls,extHoles])
	walls = DIFFERENCE([walls,wHoles])
	walls = COLOR(Color4f([102/255., 255/255., 102/255., 1]))(walls)
	walls = STRUCT([walls,windows,extDoors])

	house = STRUCT([walls,internals])
	floor = TEXTURE("texture/floor.jpg")(floor)

	"""
	stairs = w3.ggpl_stair(4.,3.,3.5)
	stairs = TEXTURE("bricks.jpg")(stairs)
	stair = w_03.ggpl_single_stair(8.,6.,3.5)
	stair = R([1,2])(PI)(stair)
	stair = T([1,2])([float(row[0]) * xScale+2.5, float(row[1]) * yScale+6])(stair)	
	#stairs = T([1,2])([1,2])(stairs)
	"""
	
	#calculating traslation factors
	xTrasl,yTrasl =  calculate_traslate_factor(ext)
	
	house = STRUCT([house,floor])
	#house = T([1,2])([-xTrasl,-yTrasl])(house)

	secondFloor = T(3)(3.5)(house)

	roof = w9.ggpl_build_roof(ext)
	#roof = T([1,2])([xTrasl,yTrasl])(roof)
	roof =  S([1,2,3])([xfactor,yfactor,zfactor])(roof)
	roof = T(3)(7)(roof)
	roof = TEXTURE("texture/tegole3.png")(roof)
		
	struct = STRUCT([house,stairs,secondFloor,roof])
	
	#VIEW(struct)
	return struct


"""if __name__=='__main__':
	house = ggpl_build_house("external","internal","doors","window")
	#house2 = ggpl_build_house("external2","internal2","doors2","windows2")
	VIEW(house)
	#VIEW(house2)"""
