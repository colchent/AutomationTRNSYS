#to read the data from the xlsx file 
import pandas as pd

file = pd.read_excel("./SimulationParameters.xlsx")
#print(file.iloc[0,:].tolist())
nb_simulation = len(file)
#nb_simulation = 1

#Create a dictionnary for each simulation parameter
def create_dictionnary(nb):
	building = []
	window = []
	power = []
	external = []
	dT = []
	for n in range(nb):
		building.append({"Building loss coefficient": getvalue(file,n,0),"Building capacitance":getvalue(file,n,1),"Building surface area":getvalue(file,n,2),"Building volume":getvalue(file,n,3)})
		window.append({"Window South":getvalue(file,n,4),"Window East":getvalue(file,n,5),"Window West":getvalue(file,n,6),"Window North":getvalue(file,n,7)})
		power.append({"Heating power":getvalue(file,n,8),"Cooling power":getvalue(file,n,9)})
		external.append({"Ventilation losses": getvalue(file,n,10),"Energy gain from people":getvalue(file,n,11)})
		dT.append({"ONTh":getvalue(file,n,12),"OFFTh":getvalue(file,n,12),"ONTc":getvalue(file,n,12),"OFFTc":getvalue(file,n,12)})
	return building, window, power, external, dT

#Return specific value from the file
def getvalue(file,line,nb):
	return str(file.iloc[line,:].tolist()[nb])

