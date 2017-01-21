from pyplasm import *

"""This function resizes the model in base of the given input."""
def resize(x,y,occurences,dx,dz):
	sumY = sum(y)
	sumX = sum(x)
	emptyCells = 0
	for j in range(len(y)):
		for i in range(len(x)):
			if occurences[j][i] == 0:
				emptyCells += 1
	diffX = (dx-sumX)/emptyCells
	diffY = (dz-sumY)/emptyCells

	for j in range(len(y)):
		for i in range(len(x)):
			if occurences[j][i] ==0:
				x[i]+=diffX
				y[j]+= diffY
	
"""This function creates the window. It takes in input the mesaures for the x and y axes'arrays"""
def ggpl_window(x,y,b):
	

	def ggpl_aux(dx,dy,dz):
		s=STRUCT([CUBOID([0,0,0])])
		resize(x,y,b,dx,dz)

		for i in range(len(x)):
			#counter for traslation
			sumX=sum(x[:i])
		
			for j in range(len(y)):
				sumY=sum(y[:j])
				if b[j][i]==1:
					cube=CUBOID([x[i],y[j],dy])
					s=STRUCT([s,T([1,2])([sumX,sumY])(cube)])
		s = COLOR(Color4f([93/255., 94/255., 107/255., 1]))(s)
		s=R([2,3])(PI/2)(s)
		s = T(2)(dy)(s)
		return s
	return ggpl_aux

"""This function creates the door. It takes in input the mesaures for the x and y axes'arrays. It puts and handle on the structure too"""
def ggpl_door(x,y,b):
	
	def ggpl_aux(dx,dy,dz):
		s=STRUCT([CUBOID([0,0,0])])
		resize(x,y,b,dx,dz)
		for i in range(len(x)):
			#counter for translation
			sumX=sum(x[:i])
		
			for j in range(len(y)):
				sumY=sum(y[:j])
				if b[j][i]==1:
					cube=CUBOID([x[i],y[j],dy])
					s=STRUCT([s,T([1,2])([sumX,sumY])(cube)])
		s = COLOR(Color4f([102/255.0,51/255.0,0/255.0,1]))(s)	
		"""hx=sum(x)/10
		hy=sum(y)/42
		dimX=sum(x[2:])+x[0]*3/2
		handle = CUBOID([hx,hy,dz+dz/2])
		handle=T([1,2])([dimX,sum(y)/2])(handle)
		
		"""

		lockBase = CUBOID([.01,0.1,0.5])
		lockCylinder = CYLINDER([0.02,0.1])(30)
		lockCylinder = R([1,3])(PI/2)(lockCylinder)
		lockOrizzontalCylinder =CYLINDER([0.02,0.2])(30)
		lockOrizzontalCylinder = R([2,3])(PI/2)(lockOrizzontalCylinder)
		lockOrizzontalCylinderReverse = R([2,3])(-PI)(lockOrizzontalCylinder) 
		lock = STRUCT([lockBase,T([2,3])([0.05,0.3]),lockCylinder])
		lock = STRUCT([lock,T([1,2,3])([-0.1,0.065,0.3]),lockOrizzontalCylinder])
		lock = TEXTURE(["Texture/gold_texture.jpg"])(lock)
		lock = R([1,2])(-PI/2)(lock)
		door = STRUCT([s,SKEL_1(CUBOID([dx,dy,dz]))])
		door = STRUCT([door,T([1,2,3])([dx-0.15,dy+0.01,dz/2.5]),lock])
		lockReverse = STRUCT([lockBase,T([2,3])([0.05,0.3]),lockCylinder]) 
		lockReverse = STRUCT([lockReverse,T([1,2,3])([-0.1,0.065,0.3]),lockOrizzontalCylinderReverse])
		lockReverse = TEXTURE(["Texture/gold_texture.jpg"])(lockReverse)
		lockReverse = R([1,2])(-PI/2)(lockReverse)
		lockReverse = R([1,2])(PI)(lockReverse)
		door = STRUCT([door,T([1,2,3])([dx-0.015,-0.01,dz/2.5]),lockReverse])
		s=R([2,3])(PI/2)(s)		
		return s
	return ggpl_aux
	
			
		


if __name__=='__main__':
	x=[.05,.7,.05,.7,.05]
	y=[.05,.7,.05,.7,.05]
	b=[[1,1,1,1,1],[1,0,1,0,1],[1,1,1,1,1],[1,0,1,0,1],[1,1,1,1,1]]
	x1=[.05,1,.05,1,.05,1,.05]
	y1=[.05,.7,.1,.7,.05]
	b1=[[1,1,1,1,1,1,1],[1,0,1,0,1,0,1],[1,1,1,1,1,1,1],[1,0,1,0,1,0,1],[1,1,1,1,1,1,1]]
	x2=[.06,.07,.12,.09,.06]
	y2=[.15,.15,.15,.15,.15,.15,.15]
	b2=[[1,1,1,1,1],[1,1,0,0,1],[1,1,1,1,1],[1,0,0,1,1],[1,1,1,1,1],[1,1,0,0,1],[1,1,1,1,1]]
	ggpl_window(x,y,b)(.8,.8,.1)
	ggpl_window(x1,y1,b1)(1.8,2,.1)
	ggpl_window(x1,y1,b1)(1.8,4,.3)
	ggpl_door(x2,y2,b2)(1.8,2,.1)
	

