from larlib import *

"""This function creates some school furniture, using the room's dimensions"""
def ggpl_create_furniture(dx,dy,dz):
	skel=SKEL_1(CUBOID([dx,dy,dz]))
	desks=create_desks(dx,dy,dz)
	blackBoard=create_blackboard(dx,dy,dz)
	teachingDesk=create_teaching_desk(dx,dy,dz)
	create_guardrobe(dx,dy,dz)
	
	classFurniture=STRUCT([desks,skel])
	classFurniture=STRUCT([classFurniture,blackBoard])
	classFurniture=STRUCT([classFurniture,teachingDesk])
	VIEW(classFurniture)

"""This function creates a simple desk,"""
def create_desks(dx,dy,dz):
	
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

	"""In this section the code duplicates desks to fill the class space"""

	#these are distances from walls
	spaceX=dx/4.0
	spaceY=dy/4.0 
	#counters for filling classroom
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
	return desks
	

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

def create_blackboard(dx,dy,dz):
	blackBoard=COLOR(BLACK)(CUBOID([0.1,3.5,1.3]))
	skel=SKEL_1(CUBOID([0.1,3.5,1.3]))
	skel=OFFSET([.05,.05,.05])(skel)
	struct=STRUCT([skel,blackBoard])
	struct=T([1,2,3])([dx,dy/2-2.0,dz/3])(struct)
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

	desk=T([1,2])([(dx-dx/6),dy/2])(desk)
	
	return desk

def create_guardrobe(dx,dy,dz):
	#crea i lati
	lateral=CUBOID([.8,.01,1.6])
	back=CUBOID([.01,1.2,1.6])
	laterals=STRUCT([lateral,T(2)(.6),(lateral)])
	laterals=STRUCT([laterals,T(2)(1.2),(lateral)])
	guardrobe=STRUCT([laterals,back])
	VIEW(guardrobe)
	

if __name__=='__main__':
	ggpl_create_furniture(15,10,3)
