from pyplasm import *

"""functions that creates a grid of pillars and beams"""
def build_frame((px,py),distancePillars,by,distanceBeams):

	"""variables to store QUOTE inputs"""
	bz=[]
	pillarX=[]
	pillarDim=[]
	bx=[]
	
	"""creating lists for QUOTE"""
	
	for dist in distancePillars:
		bx.append(-px)
		bx.append(-dist)
		pillarX.append(px)
		pillarX.append(dist)
	
	for dist in distanceBeams:
		bz.append(-dist)
		bz.append(by)
		pillarDim.append(dist+by)

	pillarX.append(px)

	"here we calculate the products to form our grids"
	xP=QUOTE(pillarX)
	yP=QUOTE([py])	
	firstGrid=PROD([xP,yP])
	pillarGrid=PROD([firstGrid,QUOTE(pillarDim)])

	xB=QUOTE(bx)
	yB=QUOTE([by])
	secondGrid=PROD([xB,yB])
	beamGrid=PROD([secondGrid,QUOTE(bz)])

	totalFrame=STRUCT([pillarGrid,beamGrid])

	VIEW(totalFrame)

"""this runs the function. Change here parameters for your frame"""
if __name__ == '__main__':
	build_frame((0.4,0.4),([-1,-2,-3,-6]),0.4,([1,2,3,5]))

		
