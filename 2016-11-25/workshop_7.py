from pyplasm import *

def ggpl_doors_and_window(x,y,b):
	s=STRUCT([CUBOID([0,0,0])])

	for i in range(len(x)):
		#counter for translation
		sumX=sum(x[:i])
		
		for j in range(len(y)):
			sumY=sum(y[:j])
			if b[j][i]==1:
				cube=CUBOID([x[i],y[j],.05])
				s=STRUCT([s,T([1,2])([sumX,sumY])(cube)])
	VIEW(s)	
	
	
	
			
		


if __name__=='__main__':
	x=[.05,.7,.05,.7,.05]
	y=[.05,.7,.05,.7,.05]
	b=[[1,1,1,1,1],[1,0,1,0,1],[1,1,1,1,1],[1,0,1,0,1],[1,1,1,1,1]]
	x1=[.5,1,.05,1,.05,1,.5]
	y1=[.5,.7,.1,.7,.5]
	b1=[[1,1,1,1,1,1,1],[1,0,1,0,1,0,1],[1,1,1,1,1,1,1],[1,0,1,0,1,0,1],[1,1,1,1,1,1,1]]
	ggpl_doors_and_window(x,y,b)
	ggpl_doors_and_window(x1,y1,b1)

