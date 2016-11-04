from pyplasm import *
import math

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
			vertexList.append(v)
		else: 
			dct.get(key).append(i)
		i+=1
	
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
					cell[index]=key
		

"""It receivs a poligon from the function produce_hpc_value() and creates the roof using vertex and cells"""
def ggpl_hip_roof():
	roof=produce_hpc_value()
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
	
	finalRoof=MKPOL([vertexList,cells,1])
	skel=SKEL_1(finalRoof)	
	VIEW(finalRoof)

	VIEW(OFFSET([.2,.2,.6])(skel))



"""Produces the hpc value, input for the above function"""
def produce_hpc_value():
	verts=[[0,0,0],[0,5,0],[8,5,0],[8,0,0],[4,0,3],[4,5,3]]
	cells=[[1,4,5],[2,6,3],[3,4,5,6],[1,2,5,6],[1,4,3,2]]
	pols=None
	roof=MKPOL([verts,cells,pols])
	return roof

if __name__=='__main__':
	ggpl_hip_roof()
