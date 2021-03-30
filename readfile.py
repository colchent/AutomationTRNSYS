#to read the data from the csv file
import pandas as pd

file = pd.read_excel("./SimulationParameters.xlsx")
#print(file.iloc[0,:].tolist())
nb_simulation = len(file)
#nb_simulation = 1
def create_dictionnary(nb):
	building = []
	window = []
	power = []
	external = []
	for n in range(nb):
		building.append({"Building loss coefficient": getvalue(file,n,0),"Building capacitance":getvalue(file,n,1),"Building surface area":getvalue(file,n,2),"Building volume":getvalue(file,n,3)})
		window.append({"Window South":getvalue(file,n,4),"Window East":getvalue(file,n,5),"Window West":getvalue(file,n,6),"Window North":getvalue(file,n,7)})
		power.append({"Heating power":getvalue(file,n,8),"Cooling power":getvalue(file,n,9)})
		external.append({"Ventilation losses": getvalue(file,n,10),"Energy gain from people":getvalue(file,n,11)})
	return building, window, power, external
def getvalue(file,line,nb):
	return str(file.iloc[line,:].tolist()[nb])

