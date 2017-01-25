from larlib import *

"""The following function creates a stairs divided by a platform in two halves. All dimensions are parametric, based on the dimension of a stair-containing box, given in input"""
def ggpl_stairs_and_platform(dx,dy,dz):

	#get steps dimensions
	stepX=dx/2
	stepY=dy/8 #suppose the platform big long as four steps
	stepZ=dz/11

	#counter for height and distance
	countH=stepZ
	countD=stepY
	#building single step
	step=CUBOID([stepX,stepY,stepZ])

	st=step
	#cycle for creating first group of stairs
	while countH<(stepZ*4):
		add_step=T(2)(countD)(step)
		countD+=stepY
		st=STRUCT([st,T(3)(countH),add_step])
		countH+=stepZ

	secondHalf=st	
	
	# VIEW(st)

	# creating the platform and using T transform
	platform=CUBOID([dx,4*stepY,stepZ])
	platform=T(2)(countD)(platform)
	
	#adding platform to struct
	st=STRUCT([st,T(3)(countH),platform])

	#VIEW(st)
	
	countH+=stepZ

	# applying transforms to the second half of stairs	
	secondHalf=R([1,2])(PI)(secondHalf)
		
	secondHalf=T(1)(stepX*2)(secondHalf)
	secondHalf=T(2)(4*stepY)(secondHalf)		
	secondHalf=T(3)(countH)(secondHalf)
	
	#VIEW(secondHalf)

	stairs=STRUCT([st,secondHalf])	
	VIEW(stairs)



def ggpl_stair(dx,dy,dz):
	#get steps dimensions
	stepX=dx/2
	stepY=dy/8 #suppose the platform big long as four steps
	stepZ=dz/11

	#counter for height and distance
	countH=stepZ
	countD=stepY
	#building single step
	step=CUBOID([stepX,stepY,stepZ])

	st=step
	#cycle for creating first group of stairs
	while countH<(stepZ*4):
		add_step=T(2)(countD)(step)
		countD+=stepY
		st=STRUCT([st,T(3)(countH),add_step])
		countH+=stepZ

	secondHalf=st	
	
	# VIEW(st)

	# creating the platform and using T transform
	platform=CUBOID([dx+dx/2,4*stepY,stepZ])
	
	#creating 
	rHeight = stepZ*4
	holder = CYLINDER([stepY/3,rHeight])(15)
	holder = T(2)(4*stepY-stepY/3)(holder)
	holder2 = T(1)(dx+dx/2-stepY/3)(holder)
	handle = CUBOID([dx+dx/2,stepY/2,stepZ/2])	
	handle = T([3,2])([rHeight,4*stepY-stepY/3])(handle)
	platform = STRUCT([platform,holder,holder2,handle])
	
	#adding platform to struct
	platform=T(2)(countD)(platform)
	st=STRUCT([st,T(3)(countH),platform])

	#VIEW(st)
	
	countH+=stepZ

	# applying transforms to the second half of stairs	
	secondHalf=R([1,2])(PI)(secondHalf)
		
	secondHalf=T(1)(stepX*2+dx/2)(secondHalf)
	secondHalf=T(2)(4*stepY)(secondHalf)		
	secondHalf=T(3)(countH)(secondHalf)
	countH = countH + 4*stepZ
	
	#VIEW(secondHalf)

	stairs=STRUCT([st,secondHalf,T([2,3])([-countD-4*stepY,countH]),platform])	
	#VIEW(stairs)
	stairs=T(2)(4*stepY)(stairs)
	return stairs


"""this function calls the main method and lets the ggpl function start"""
if __name__=='__main__':
	#insert any FLOAT value you want
	#ggpl_stairs_and_platform(50.0,50.0,50.0)
	ggpl_stair(50.0,50.0,50.0)

	
