from pyplasm import *
import math

"""round values for vertex list"""
def round_vertex(verts):
	for v in verts:
		v[0]=math.fabs(round( v[0] , 3  ))
		v[1]=math.fabs(round( v[1] , 3  ))
		v[2]=math.fabs(round( v[2] , 3  ))

"""creates a dictionary using all rounded skel's vertex""" 
def create_dict(verts,cells):
	dct={}
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
	
	return dct
	
"""replaces the indexes of merged vertex, with the needed one"""
def replace_cell(dct,cells):
	
	i=1


	for el in dct.keys():
		checkingList=dct.get(el)
		for index in checkingList:
			for cell in cells:
				for c in cell:
					if c==index:
						c=i
		i+=1


def ggpl_hip_roof():
	roof=produce_hpc_value()
	skel=SKEL_2(roof)
	#gets all values from the skeleton
	(verts,cells,pol)=UKPOL(skel)
	
	#rounds the vertex values
	round_vertex(verts)

	vertexDict=create_dict(verts,cells)
	
	replace_cell(vertexDict,cells)
	
	#creates an helper dictionary for iterating on cells, using a counter as key
	helperDict={}
	count=1
	for el in vertexDict.keys():
		helperDict[count]=vertexDict.get(el)	
		count+=1
		
	print helperDict
	
	#VIEW(OFFSET([.6,.6,.6])(skel))



"""Produces the hpc value, input for the above function"""
def produce_hpc_value():
	verts=[[0,0,0],[0,5,0],[8,5,0],[8,0,0],[4,0,3],[4,5,3]]
	cells=[[1,2,3,4,5,6]]
	pols=None
	roof=MKPOL([verts,cells,pols])
	return roof

if __name__=='__main__':
	ggpl_hip_roof()
