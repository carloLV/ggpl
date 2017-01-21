from pyplasm import *
import math
from ast import literal_eval

"""round values for vertex list"""
def round_vertex(verts):
	for v in verts:
		v[0]=math.fabs(round( v[0] , 3  ))
		v[1]=math.fabs(round( v[1] , 3  ))
		v[2]=math.fabs(round( v[2] , 3  ))

"""creates a dictionary using all rounded skel's vertex. Returns the compact list of vertex too""" 
def create_dict(verts,cells):
	dct={}
	vertexList=[]
	#counter for index in vertex list
	i=1
	for v in verts:
		#creates string type keys
		key=",".join(str(x) for x in v)
		if not key in dct.keys():
			dct[key]=[i]
		else: 
			dct.get(key).append(i)
		i+=1

	for key in dct.keys():
		vertexList.append(literal_eval(key))

	return dct , vertexList
	
"""replaces the indexes of merged vertex, with the needed one"""
def replace_cell(dct,cells):
	
	#iterates on each cell.
	for cell in cells:
		#iterates on tuple in the cell
		for elT in cell:
			#iterates on dictionary
			for key, vals in dct.items():
				#checks if the tuple elemente is in the list of values and if True replaces the value with the key
				if elT in vals:
					index=cell.index(elT)
					cell[index]=int(key)
		

"""It receivs a poligon from the function produce_hpc_value() and creates the roof using vertex and cells"""
def ggpl_build_roof(val):
	roof=produce_hpc_value(val)
	skel=SKEL_2(roof)

	#gets all values from the skeleton
	(verts,cells,pol)=UKPOL(skel)
	
	#rounds the vertex values
	round_vertex(verts)

	(vertexDict,vertexList)=create_dict(verts,cells)

	#creates an helper dictionary for iterating on cells, using a counter as key
	helperDict={}
	count=1
	for el in vertexDict.keys():
		helperDict[count]=vertexDict.get(el)	
		count+=1
	
	replace_cell(helperDict,cells)
	
	finalRoof=MKPOL([vertexList,cells,None])

	

	skel1=SKEL_1(finalRoof)	
	
	#VIEW(finalRoof)
	#VIEW(skel1)
	skel1=(OFFSET([.1,.1,.3])(skel1))

	coveringCells=put_planes(vertexList,cells)
	coveringPol=MKPOL([vertexList,coveringCells,None])
	
	#VIEW(coveringPol)
	struct=STRUCT([skel1,COLOR(RED)(coveringPol)])
	VIEW(struct)


"""This function builds planes that will be put above the beams. It builds plane only for cells with at least one vertex having z!=0. 
    Moreover, according to the used models, we check if the vertex in cells have all the same x value. If true that cell isn't build"""
def put_planes(vertexList,cells):
	#list of all vertex that satisfies condition and cells needed
	ind=[]
	buildingCells=[]
	for v in vertexList:
		if v[2]> 0.0:
			i=vertexList.index(v)
			ind.append(i+1)
	
	for index in ind:
		for cell in cells:
			if index in cell and not check_y_value(cell,vertexList) and not cell in buildingCells:
				buildingCells.append(cell)
	
	return buildingCells

"""checks if all vertices in the given cell have the y value equals to 0"""
def check_y_value(cell,vertexList):
	check=False	
	helpList=[]
	for el in cell:
		vert=vertexList[el-1]	
		helpList.append(vert)
	temp=helpList[0]
	yValueTemp=temp[1]
	xValueTemp=temp[0] #if the input hpc value has a different axes'orientation
	for v in helpList:
		if v[1]==yValueTemp or v[0]==xValueTemp:
			check=True
		else:
			return False
	return check
				
"""Produces the hpc value, input for the above function"""
def produce_hpc_value(val):
	verts1=[[0,0,0],[0,6,0],[8,6,0],[8,0,0],[4,1,3],[4,5,3]]
	cells1=[[1,4,5],[2,6,3],[3,4,5,6],[1,2,6,5],[1,4,3,2]]
	pols=None
	hip_roof=MKPOL([verts1,cells1,pols])
	verts2=[[0,0,0],[2,0,3],[2,8,3],[0,8,0],[6,0,6],[6,8,6],[10,0,3],[10,8,3],[12,0,0],[12,8,0]]
	cells2=[[1,2,3,4],[2,3,6,5],[5,6,8,7],[7,8,10,9],[1,4,9,10],[1,2,5,7,9],[3,4,6,8,10]]
	gambrel_roof=MKPOL([verts2,cells2,pols])

	
	### Following this examplas,add your polygon model in this section and ###
	### update the if statement to let the program execute it              ###
	
	if val==1:
		return hip_roof
	elif val==2:
		return gambrel_roof

if __name__=='__main__':
	ggpl_build_roof(1)
	ggpl_build_roof(2)
