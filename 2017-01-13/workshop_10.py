from pyplasm import *
from res import workshop_08 as w8
from res import workshop_7 as w7
from res import workshop_03 as w3


""" This functions uses some of the previous created in past workshop, to build a full model of a house.
    Functions from past workshop has been modified in some cases, to perform their task in a better way.
	@params: None
	@return: Hpc value for all models """
def house_builder():
	#builds externals wall using previous function
	walls = w8.ggpl_build_house('muri_esterni','muri_interni','porte','finestre')
	

	
if __name__ == '__main__':
	
	house_builder()