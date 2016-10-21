from larlib import * 

import csv

"""reads a csv file"""
def read_file(file_name):
	
	frameDist = []
	with open(file_name, 'rb') as csvfile:
		reader = csv.reader(csvfile)
		i=0
		for r in reader:
			if i%2==1:
                
				frameDist.append(float(r[0]))
				i=i+1
                
			elif i%2==0:
                
				(px,py)=(float(r[0]),float(r[1]))
				pillarsDist = []
				j=3
                
				while r[j]!="]":
                    
					pillarsDist.append(float(r[j]))
					j=j+1
				(by,bz)= (float(r[j+1]),float(r[j+2]))
				j= j+4
				beamsDist = []
                
				while r[j]!="]":
                    
					beamsDist.append(float(r[j]))
					j=j+1	
                    
				i=i+1
    
        """returns input for the build_frame function"""
	return (px,py, pillarsDist, by,bz, beamsDist, frameDist)

"""returns a 3D value of type HPC built from parameters"""
def build_frame(px,py,pillarsDist,by,bz, beamsDist, frameDist):

	pillarArray = [px]
    
	for value in pillarsDist:
		pillarArray = pillarArray+[-value]+[px]
    
	xPillar = QUOTE(pillarArray)
	yPillar = QUOTE([py])
	xyPillar = PROD([xPillar, yPillar])
	heightsPillar = []
	for value in beamsDist:
		heightsPillar.append((value+bz))
    
	zPillar = QUOTE(heightsPillar)
	pillars = PROD([xyPillar, zPillar])
	beamArray = []
    
	for value in pillarArray:
		beamArray.append(-value)
        
	xBeam = QUOTE(beamArray)
	yBeam = QUOTE([by])
	xyBeam = PROD([xBeam, yBeam])
	beamsArrayDist = []

	for value in beamsDist:
        
		beamsArrayDist.append(-value)
		beamsArrayDist.append(bz)
	beams = PROD([xyBeam, QUOTE(beamsArrayDist)])
	
        """here we create the single frame merging pillars and beams"""
	frame = STRUCT([pillars, beams])
	
	#the following code duplicates the frames and creates the beams between each frame
	framesArrayDist = []
	for value in frameDist:
        
		framesArrayDist.append(-py)
		framesArrayDist.append(value)
    
	yFrameBeams = QUOTE(framesArrayDist)
	xyFrameBeams = PROD([yBeam, yFrameBeams])
	xyzFrameBeams = PROD([xyFrameBeams, QUOTE(beamsArrayDist)])
	xyzFrame = STRUCT([xyzFrameBeams])
	
	contb = 0
	arrayBeams = []
	for value in frameDist:
		contb+=value
		arrayBeams.append(contb)
        
	distB=py
	structFrames=frame
	for value in arrayBeams:
		structFrames = STRUCT([structFrames, T(2)(value+distB), frame])
		distB+=py

	contp = 0
	arrayPillar = []
	for value in pillarsDist:
        
		contp+=value
		arrayPillar.append(contp)
        
	distP=px
	structBeams= xyzFrame
	for value in arrayPillar:
        
		structBeams = STRUCT([structBeams, T(1)(value+distP), xyzFrame])
		distP+=px

	"""merging all frames and beams and creating the final structure"""
	finalStruct =  STRUCT([structFrames, structBeams])

	return finalStruct

"""visualize a type HPC of a 3D structure. The data to build the structure are in a csv file given in input"""
def ggpl_bone_structure(file_name):

	#read data from the csv file and save them in structureData
	structure = read_file(file_name)
	
	#extract eache single parameter for buildStruct from structureData
	px = structure[0]
	py = structure[1]
	pillarDist = structure[2]
	by = structure[3]
	bz = structure[4]
	beamDist = structure[5]
	frameDist = structure[6]

	#create the structure
	struct = build_frame(px,py,pillarDist,by,bz,beamDist,frameDist)
	
	#visualize the structure
	VIEW(struct)

	

if __name__=='__main__':
	ggpl_bone_structure('frame_data_461959.csv')
