from readfile import *
import shutil
import time
#Dictionnary containing key : the variable name, value : the line number in the .dck file -1 (in the dck file line number start at 1, in python list number start at 0 )
building_line = {"Building loss coefficient": 134,"Building capacitance":135,"Building surface area":138,"Building volume":139}
window_line = {"Window South":500,"Window East":501,"Window West":502,"Window North":503}
power_line = {"Heating power":225,"Cooling power":226}

external_line= {"Ventilation losses":156,"Energy gain from people":156}

#liste of dictionnaries
building_value, window_value, power_value, external_value = create_dictionnary(nb_simulation)

def create_file(nb):
	for n in range(nb):
		f_string = "C:\\TRNSYS18\\Automatisation\\deckfiles\\simu" + str(n) + ".dck"
		shutil.copy("C:\\TRNSYS18\\MyProjects\\Automatisation\\Run1.dck",f_string)

def create_results(num):
	r_string = "C:\\TRNSYS18\\Automatisation\\Results\\ResultSimu" + str(num) + ".plt"
	shutil.copy("C:\\TRNSYS18\\MyProjects\\trnsysfiles\\testauto.plt",r_string)


def modif_deck(filename,simu): 
	with open(filename,"r") as data :
		deck_file = data.readlines()
	for key in building_value[simu].keys():
		deck_file[building_line[key]]=replace_building_params(deck_file[building_line[key]],key,simu)

	for key in window_value[simu].keys():
		deck_file[window_line[key]]=replace_window(deck_file[window_line[key]],key,simu)

	for key in power_value[simu].keys():
		deck_file[power_line[key]]=replace_power(deck_file[power_line[key]],key,simu)

	for key in external_value[simu].keys():
		deck_file[external_line[key]]= replace_external(deck_file[external_line[key]],key,simu)


	file = open(filename,"w")
	str_deck_file = "".join(deck_file)
	file.write(str_deck_file)
	file.close()

def replace_external(fileline,key,simu):
	value_tab = fileline.split(" ")
	value_tab[2] = external_value[simu]["Ventilation losses"]
	value_tab[8] = external_value[simu]["Energy gain from people"]
	return " ".join(value_tab)

def replace_building_params(fileline,key,simu):
	list_line = list(fileline)
	ind = 0
	for l in range(len(list_line)):
		if list_line[l]=="!":
			ind = l
			break
	right_part = list_line[ind:]
	left_part = building_value[simu][key]
	new_line = "".join(left_part) +"		"+ "".join(right_part)
	return new_line
def replace_power(fileline,key,simu):
	list_line = list(fileline)
	ind1= 0
	ind2 = 0
	for l in range(len(list_line)):
		if list_line[l]=="=":
			ind1 = l
		if list_line[l]=="*":
			ind2 = l
			break
	left_part = list_line[:ind1]
	right_part = list_line[ind2:]
	pow_value = power_value[simu][key]
	new_line = "".join(left_part)+"= " + "".join(pow_value)+ "".join(right_part)
	return new_line


def replace_window(fileline,key,simu):
	list_line = list(fileline)
	ind = 0
	for l in range(len(list_line)):
		if list_line[l]=="=":
			ind = l
			break
	left_part = list_line[:ind]
	right_part = window_value[simu][key]
	new_line = "".join(left_part) +" = "+"".join(right_part)+"\n"
	
	return new_line
