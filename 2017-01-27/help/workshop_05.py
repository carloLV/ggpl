from larlib import *

"""This program creates a school class furniture. The dimension of objects are in meters. The parameters are the room's dimensions. Bigger are dimensions, more object can be inserted in the class"""

"""This function creates some school furniture, using the room's dimensions and makes the appropriates translation for positioning objects."""
"""It duplicates the object needed more than once, too"""
def ggpl_create_furniture(dx,dy,dz):
	skel=SKEL_1(CUBOID([dx,dy,dz]))
	desk=create_desk(dx,dy,dz)
	blackBoard=create_blackboard(dx,dy,dz)
	teachingDesk=create_teaching_desk(dx,dy,dz)
	guardrobe=create_guardrobe(dx,dy,dz)

	"""In this section the code duplicates desks to fill the class space"""

	#these are distances from walls, supposing the same distance from walls is always mantained in all classes
	#if you want less or more distance from wall, just change this two variables

	spaceX= 2.6 #at least the double of teaching_desk, from the two walls
	spaceY=0.8 #at least one desk, from the two walls 

	#counters for filling classroom with desks
	countX=(0.5*2)
	countY=(0.7*2)
	
	desks=desk
	#cycle for creating all desks till their dimension arrives to the wall
	while countX<(dx-(spaceX*2)):
		desks = STRUCT([desks,T(1)(countX),desk])
		countX+=(0.5*2)
	deskLine=desks
	while countY<(dy-(spaceY*2)):
		desks=STRUCT([desks,T(2)(countY),deskLine])
		countY+=(0.7*2)

	#traslate desk using this parameters
	desks=T([1,2])([spaceX,spaceY])(desks)

	"""In this section all object are appropriately traslated"""
	
	blackBoard=T([1,2,3])([dx,dy/2-2.0,dz/3])(blackBoard)
	teachingDesk=T([1,2])([(dx-1.6),dy/3])(teachingDesk)

	#the bigger is the class, more guardrobe will be inserted
	guardrobeLimit=1.8 #distance from wall for guardrobe
	guardrobeCounter=guardrobeLimit+1.2 #1.2 is the dimension on y of the guardrobe created
	g_robes=guardrobe
	while guardrobeCounter<(dy-(guardrobeLimit*2)):
		g_robes=STRUCT([g_robes,T(2)(guardrobeCounter),guardrobe])
		guardrobeCounter+=(1.2*2)
	
	g_robes=T(2)(1.8)(g_robes)


	#merging all pieces for creating the class
	classFurniture=STRUCT([desks,skel])
	classFurniture=STRUCT([classFurniture,blackBoard])
	classFurniture=STRUCT([classFurniture,teachingDesk])
	classFurniture=STRUCT([classFurniture,g_robes])
	#VIEW(classFurniture)
	return classFurniture
"""This function creates a simple desk, and puts under it a chair, created in the below function"""
def create_desk(dx,dy,dz):
	
	#creates desk's legs
	leg=CUBOID([0.03,0.03,0.7])
	legs=STRUCT([leg,T(2)(0.7)(leg)])
	legs=STRUCT([legs,T(1)(0.5)(legs)])
	
	#creates the plane
	plane = CUBOID([0.53,0.73,0.01])
	plane=COLOR(GREEN)(plane)
	desk = STRUCT([legs,T(3)(0.7)(plane)])
	
	#adding chairs to desk
	chair=create_chair()
	desk=STRUCT([desk,T([1,2])([-0.05,0.3]),chair])

	return desk
	
"""It creates the chair"""
def create_chair():
	leg=CUBOID([0.03,0.03,0.4])
	legs=STRUCT([leg,T(2)(0.3)(leg)])
	legs=STRUCT([legs,T(1)(0.4)(legs)])
	
	#creates the sit
	sit = CUBOID([0.43,0.33,0.01])
	sit=COLOR(RED)(sit)
	chair = STRUCT([legs,T(3)(0.4)(sit)])
	
	back = CUBOID([0.03,0.33,0.4])
	chair=STRUCT([chair,T(3)(0.4),back])
	return chair

"""It creates a blackboard"""
def create_blackboard(dx,dy,dz):
	blackBoard=COLOR(BLACK)(CUBOID([0.1,3.5,1.3]))
	skel=SKEL_1(CUBOID([0.1,3.5,1.3]))
	skel=OFFSET([.05,.05,.05])(skel)
	struct=STRUCT([skel,blackBoard])
	
	return struct

def create_teaching_desk(dx,dy,dz):
	leg=CYLINDER([0.05,0.9])(30)
	legs=STRUCT([leg,T(2)(1.3)(leg)])
	legs=STRUCT([legs,T(1)(0.7)(legs)])
	legs=COLOR(BLACK)(legs)

	#supposing this desk has covering planes on three edges
	coveringFront=CUBOID([0.01,1.35,0.7])
	coveringFront=COLOR(Color4f([205/255.0,170/255.0,125/255.0,1]))(coveringFront)
	desk=STRUCT([legs,T(3)(0.2),coveringFront])
	coverLateral=CUBOID([0.75,0.01,0.7])
	coverLateral=COLOR(Color4f([205/255.0,170/255.0,125/255.0,1]))(coverLateral)
	desk=STRUCT([desk,T([2,3])([1.3,0.2]),coverLateral])
	desk=STRUCT([desk,T(3)(0.2),coverLateral])

	plane=CUBOID([0.7,1.3,0.02])
	plane=COLOR(Color4f([205/255.0,170/255.0,125/255.0,1]))(plane)
	desk=STRUCT([desk,T(3)(0.9),plane])
	chair = create_chair()
	chair = S([1,2,3])([1.3,1.3,1.3])(chair)
	chair = R([1,2])(PI)(chair)
	desk=STRUCT([desk,T([1,2])([.8,0.65]),chair])

	return desk

def create_guardrobe(dx,dy,dz):

	lateral=CUBOID([.8,.01,1.6])
	back=CUBOID([.01,1.2,1.6])
	laterals=STRUCT([lateral,T(2)(.6),(lateral)])
	laterals=STRUCT([laterals,T(2)(1.2),(lateral)])
	lowPlane=CUBOID([0.8,1.2,.01])
	guardrobe=STRUCT([laterals,back])
	guardrobe=STRUCT([guardrobe,lowPlane])
	guardrobe=STRUCT([guardrobe,T(3)(1.6),lowPlane])
	guardrobe=STRUCT([guardrobe,T(3)(0.5),lowPlane])
	guardrobe=STRUCT([guardrobe,T(3)(1.1),lowPlane])
	guardrobe=COLOR(Color4f([102/255.0,51/255.0,0/255.0,1]))(guardrobe)
		
	return guardrobe


	

if __name__=='__main__':
	#Insert the dimension of your room. Please use only appropriate dimensions for a school room in meters.
	ggpl_create_furniture(10,8,3)
