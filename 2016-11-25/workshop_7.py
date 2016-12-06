from pyplasm import *

"""This function resizes the model in base of the given input."""
def resize(x,y,dx,dy):
	sumX=sum(x)
	sumY=sum(y)
	
	for i in range(len(x)-2):
		x[i+1]=x[i+1]/(sumX/dx)
	for j in range(len(y)-2):
		y[j+1]=y[j+1]/(sumY/dy)
	
"""This function creates the window. It takes in input the mesaures for the x and y axes'arrays"""
def ggpl_window(x,y,b):
	

	def ggpl_aux(dx,dy,dz):
		s=STRUCT([CUBOID([0,0,0])])
		resize(x,y,dx,dy)

		for i in range(len(x)):
			#counter for translation
			sumX=sum(x[:i])
		
			for j in range(len(y)):
				sumY=sum(y[:j])
				if b[j][i]==1:
					cube=CUBOID([x[i],y[j],dz])
					s=STRUCT([s,T([1,2])([sumX,sumY])(cube)])
		s = COLOR(Color4f([93/255., 94/255., 107/255., 1]))(s)
		VIEW(s)
	return ggpl_aux

"""This function creates the door. It takes in input the mesaures for the x and y axes'arrays. It puts and handle on the structure too"""
def ggpl_door(x,y,b):
	
	def ggpl_aux(dx,dy,dz):
		s=STRUCT([CUBOID([0,0,0])])
		resize(x,y,dx,dy)
		for i in range(len(x)):
			#counter for translation
			sumX=sum(x[:i])
		
			for j in range(len(y)):
				sumY=sum(y[:j])
				if b[j][i]==1:
					cube=CUBOID([x[i],y[j],dz])
					s=STRUCT([s,T([1,2])([sumX,sumY])(cube)])
		s = COLOR(Color4f([102/255.0,51/255.0,0/255.0,1]))(s)	
		hx=sum(x)/10
		hy=sum(y)/42
		dimX=sum(x[2:])+x[0]*3/2
		handle = CUBOID([hx,hy,dz+dz/2])
		handle=T([1,2])([dimX,sum(y)/2])(handle)
		
		s=STRUCT([s,handle])
		VIEW(s)
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
	

