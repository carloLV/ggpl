from pyplasm import *
import csv
from help import workshop_10 as w10
from help import workshop_05 as w5
#from help import workshop_7 as w7


"""This function creates a sign and applies a defined texture to it.
    @params: float h -> the height of buildings
    @return: Hpc sign -> the model created
"""
def create_sign(h):
	pillar = CYLINDER([.3,h])(20)
	pillar = MATERIAL([.13,.13,.13,1,  0,0,0,1,  0,0,0,0, 0,0,0,0, 1])(pillar)
	sign = CUBOID([h,.3,h/2])
	sign = TEXTURE("texture/logo.jpg")(sign)
	sign = STRUCT([pillar,T([1,3])([-h/2,h])(sign)])
	return sign


"""This function creates a bench and applies some color to it thanks to MATERIAL primitive.
    @params: float r, float h ->  The length of bench andthe height of buildings.
    @return: Hpc bench -> the model created
"""
def create_bench(r,h):
	#bench's base dimensions
	hBase = h/2
	lBase = r/6
	wBase = r/3

	base = CUBOID([lBase,wBase,hBase])
	base2 = T(1)(r-lBase)(base)
	base = STRUCT([base,base2])
	base = MATERIAL([0,0,.2,1,  0,0,0,1,  0,0,0,0, 0,0,0,0, 1])(base)
	sitting = CUBOID([r,wBase,.3])
	sitting = MATERIAL([.6,.3,0,1,  0,0,0,1,  0,0,0,0, 0,0,0,0, 1])(sitting)	
	back = 	CUBOID([r,.2,hBase*1.5])
	back = MATERIAL([.63,.63,.63,1,  0,0,0,1,  0,0,0,0, 0,0,0,0, 1])(back)
	sitting = STRUCT([sitting,back])
	sitting = T(3)(hBase)(sitting)	
	bench = STRUCT([base,sitting])
	return bench


"""This function creates a trees assembling some basic models (cylinder and spheres);
   then it applies some texture to the model.
    @params: float h ->  The height of buildings.
    @return: Hpc tree -> the model created
"""
def tree_creator(h):
	leafs = SPHERE(0)([1,1])
	r = h/15
	log = CYLINDER([r,h])(20)
	log = TEXTURE("texture/log.jpg")(log)
	leaf = SPHERE(h/8)([24,32])
	leaf = TEXTURE("texture/grass.jpg")(leaf)	
	leafs = STRUCT([leafs,T(1)(h/6)(leaf)])
	leafs = STRUCT([leafs,T(1)(-h/6)(leaf)])
	leafs2 = R([1,2])(PI/2)(leafs)
	leafs = STRUCT([leafs,leafs2])	
	
	leafs = T(3)(h)(leafs)
	tree = STRUCT([log,leafs,T(3)(h+h/8)(leaf)])
	return tree
	

"""This function creates a fountai sorrounded by some benches and trees. Then it applies some color to it thanks to MATERIAL primitive.
   All dimensions are in relation to buildings dimensions; this lets a scaling on buildings to have consequences to all other models
   created.
    @params: float r, float h ->  The ray of fountain and the height of buildings.
    @return: Hpc complete -> the model created
"""
def build_fountain(r,h):
	r2 = r-r/7
	hB= h/8

	tree = tree_creator(h)	
	
	basement = CYLINDER([r,hB])(20)
	basement = MATERIAL([.13,.13,.13,1,  0,0,0,1,  0,0,0,0, 0,0,0,0, 1])(basement)	
	hole = CYLINDER([r2,hB/2])(20)
	hole = T(3)(hB/2)(hole)
	hole = MATERIAL([.2,.4,1,1,  0,0,0,1,  0,0,0,0, 0,0,0,0, 1])(hole)
	obelisk = CYLINDER([r/9,h-hB])(6)
	obelisk = MATERIAL([.13,.13,.13,1,  0,0,0,1,  0,0,0,0, 0,0,0,0, 1])(obelisk)
	fountain = STRUCT([basement,hole,obelisk])
	
	treeSet = T(1)(r+r/3)(tree)
	treeSet = STRUCT([treeSet,T(1)(-r-r/3)(tree)])
	treeSet = STRUCT([treeSet,T(2)(-r-r/3)(tree)])
	treeSet = STRUCT([treeSet,T(2)(+r+r/3)(tree)])

	bench = create_bench(r,h/4)
	bench1 = R([1,2])(PI/3*2)(bench)	
	bench1 = T([1,2])([+r+r/2,+r+r/2])(bench1)
	
	
	bench2 = R([1,2])(PI/4)(bench)
	bench2 = T([1,2])([+r+r/2,-r-r/2])(bench2)
	
	bench3 = R([1,2])(-PI/4)(bench)
	bench3 = T([1,2])([-r-r/2,-r-r/2])(bench3)
	
	bench4 = R([1,2])(-PI/3*2)(bench)
	bench4 = T([1,2])([-r-r/2,+r+r/2])(bench4)	
		
	benches = STRUCT([bench1,bench2,bench3,bench4])
	complete = STRUCT([fountain,treeSet,benches])
	
	return complete


"""This function creates a simple children game and applies some color to it using MATERIAL.
    @params: float r ->  The ray of this game; also this input is in realtions to buildings dimensions.
    @return: Hpc s -> the model created
"""	
def child_game(r):
	base = CYLINDER([r,1])(16)
	base = MATERIAL([.5,.5,.5,1,  0,0,0,1,  0,0,0,0, 0,0,0,0, 1])(base)	
	fulcro = CYLINDER([r/18,4])(16)
	fulcro = MATERIAL([.13,.13,.13,1,  0,0,0,1,  0,0,0,0, 0,0,0,0, 1])(fulcro)
	handle = CYLINDER([r,3])(16)	
	handle = SKEL_1(handle)
	handle = OFFSET([.3,.3,.3])(handle)
	handle =  MATERIAL([.13,.13,.13,1,  0,0,0,1,  0,0,0,0, 0,0,0,0, 1])(handle)
	controller = CYLINDER([r/5,.5])(16)
	controller = MATERIAL([1,.2,.4,1,  0,0,0,1,  0,0,0,0, 0,0,0,0, 1])(controller)
	s = STRUCT([base,fulcro,T(3)(4)(controller),handle])
	return s
	

"""Next three functions creates groups of houses, using the function of workshop 10. To make a right shape of groups of buildings,
   some necessary rotation an traslation are performed. Houses created are then improved with some trees.  
    @params: None 
    @return: Hpc houses -> the model created
"""
def build_nbood():
	house = w10.house_builder('help/lines_file/')
	tree = tree_creator(SIZE(3)(house))
	house = STRUCT([house,tree,T(2)(SIZE(2)(house))(tree),T(1)(SIZE(1)(house))(tree)])
	house2 = T(1)(20)(house)
	houses = STRUCT([house,house2])
	houses2 = R([1,2])(PI)(houses)	
	houses2 = T([1,2])([40,-5])(houses2)
	quartier = STRUCT([houses,houses2])
	quartier = S([1,2,3])([.8,.8,.8])(quartier)
	return quartier

def build_bifamiliar_house():
	house = w10.house_builder('help/lines_file/')
	tree = tree_creator(SIZE(3)(house))
	house = STRUCT([house,tree,T(2)(SIZE(2)(house))(tree),T(1)(SIZE(1)(house))(tree)])
	house = T(1)(SIZE(1)(house)/2)(house)
	house2 = T(1)(-SIZE(1)(house))(house)
	houses = STRUCT([house,house2])
	houses = S([1,2,3])([.8,.8,.8])(houses)
	return houses

def build_single_house():
	house = w10.house_builder('help/lines_file/')
	tree = tree_creator(SIZE(3)(house))
	house = STRUCT([house,tree,T(2)(SIZE(2)(house))(tree),T(1)(SIZE(1)(house))(tree)])
	return house
	

"""This function builds the streets, in relation to a set of points created on paper. It is used the primitive BEZIERCURVE to build
   curves. Then, thanks to an appropriate OFFSET, the street is created and the use of a texture adds more realism to the model.
    @params: list of list of points -> a list of points for each part of street.
    @return: Hpc stRet -> the streets and the box in which are settled.
"""
def build_roads(pts):
	stRet=STRUCT([CUBOID([0,0,0])])
	for el in pts:
		st = MAP(BEZIERCURVE(el))(INTERVALS(1)(32))
		stRet = STRUCT([stRet,st])
	
	stRet = OFFSET([6,6,.5])(stRet)
	box = BOX([1,2])(stRet)
	box = TEXTURE("texture/grass2.jpg")(box)

	#defining scaling factors
	xfactor = 15/SIZE([1])(box)[0]
	yfactor = 15.1/SIZE([2])(box)[0]
	zfactor = xfactor

	stRet = TEXTURE("texture/asphalt.jpg")(stRet)
	stRet = STRUCT([stRet,box])
	return stRet 						
			

"""This is the main function It builds all things using previous functions and performs some traslation and rotation to 
   make a nice model. All parts are created and moved to the right position; at the end a STRUCT is performed and all the parts are 
   put together in the final model
    @params: None
    @return: Hpc st -> the complete model created using all these functions
"""
if __name__ == '__main__':
	
	points = [[[60,0],[58,7.5],[60,15],[52,18],[46,21],[42,28],[40,32],[40,60],[40,80],[40,90]],
	[[42,60],[46,60],[52,60],[60,60],[65,60],[74,63],[82,66],[90,69],[100,72],[110,75]],
	[[60,15],[65,15],[74,18],[82,20],[90,22],[95,25],[100,30],[110,38],[115,42]],
	[[60,15],[60,21],[60,38],[60,41],[60,60],[60,63]],
	[[110,38],[105,41],[100,45],[105,50],[110,70],[115,80],[115,90]]]

	le = build_roads(points)
	
	x,y=SIZE([1,2])(le)
	
	table = CUBOID([x,y,5])
	table = MATERIAL([.6,.3,0,1,  0,0,0,1,  0,0,0,0, 0,0,0,1, 1])(table)
	table = T(3)(-5.2)(table)

	q1=build_nbood()
	fact1 = SIZE(2)(q1)- SIZE(2)(q1)/3
	q1=T(2)(fact1)(q1)		

	fact2 = SIZE(2)(q1)+SIZE(2)(q1)/3
	q2 = T(2)(fact2)(q1)

	q3 = build_bifamiliar_house()
	q3 = R([1,2])(PI)(q3)	
	q3 = T([1,2])([SIZE(1)(q1)*2+3,y-1])(q3)

	q4 = build_single_house()
	q4 = T(1)(x-SIZE(1)(q4))(q4)

	game = child_game(SIZE(1)(q4)/4)
	game = T([1,2])([x/2+SIZE(1)(game)*1.5+3,SIZE(2)(game)-2])(game)

	tree = tree_creator(SIZE(3)(q1))
	treeDistance = SIZE(1)(tree) + SIZE(1)(tree)/2
	wood = tree
	wood = STRUCT([wood,T(1)(treeDistance)(tree),T(2)(treeDistance)(tree),T(1)(-treeDistance)(tree),T(2)(-treeDistance)(tree)]) 
	wood = T([1,2])([fact1*2-2,SIZE(2)(wood)/2])(wood)

	sign = create_sign(SIZE(3)(q1))
	sign = T([1,2])([fact1*2,fact2])(sign)

	fountain = build_fountain(SIZE(1)(q1)/5,SIZE(3)(q1))
	fountain = T([1,2])([fact1*3.5,fact2])(fountain)
	st = STRUCT([le,table,q1,q2,q3,q4,fountain,wood,sign,game])
	VIEW(st)

