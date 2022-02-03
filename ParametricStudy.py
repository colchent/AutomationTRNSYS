from getMonotoneOfHeat import *
import numpy as np

"""
Define files that represent different scenarios to be compared 
"""
FilesNames=["Run1","Run2","Run3","Run4","Run5","Run6","Run7","Run8","Run9","Run10","Run11","Run12","Run13","Run14","Run15"]
FolderNames=["BaseScenario","SolarGainGlaze","SolarGainshade","TempInf1","TempSup1","VentilationLosses04","VentilationLosses08"]

DicFilesNames={"Run1": 0,"Run2": 1,"Run3": 2,"Run4": 3,"Run5": 4,"Run6": 5,"Run7": 6,"Run8": 7,"Run9": 8,"Run10": 9,"Run11": 10,"Run12": 11,"Run13": 12,"Run14": 13,"Run15": 14}
DicFolderNames={"BaseScenario": 0,"SolarGainGlaze": 1,"SolarGainShade": 2,"TempInf1": 3,"TempSup1": 4,"VentilationLosses04": 5,"VentilationLosses08": 6}

nbday = 24
nbstep = 6
TotalHeat=[[x for x in range(15)]]*7
TabVal=[]

#For each scenario, read the associated results
for j in FolderNames:
	for i in FilesNames:
		col = readCol(str("C:\\TRNSYS18\\MyProjects\\ParametricStudy\\"+j+"\\"+i+".plt"))
		Ph = intoHourly(col,6)
		TabVal.append(sum(Ph))
		#TotalHeat[F][V]=Val
	
TotalHeat = np.reshape(TabVal,(7,15))

#For each simulation return the wanted value of results
def getHeatValue(Scenario,Simulation):
	return TotalHeat[DicFolderNames[Scenario]][DicFilesNames[Simulation]]
def get_absvalue_graph(Run):
	value = [getHeatValue("BaseScenario",Run)/1000,getHeatValue("SolarGainGlaze",Run)/1000,getHeatValue("SolarGainShade",Run)/1000,getHeatValue("TempInf1",Run)/1000,getHeatValue("TempSup1",Run)/1000,getHeatValue("VentilationLosses04",Run)/1000,getHeatValue("VentilationLosses08",Run)/1000]
	return value
def get_relativevalue_graph(Run):
	value = [getHeatValue("BaseScenario",Run)/getHeatValue("BaseScenario",Run),getHeatValue("SolarGainGlaze",Run)/getHeatValue("BaseScenario",Run),getHeatValue("SolarGainShade",Run)/getHeatValue("BaseScenario",Run),getHeatValue("TempInf1",Run)/getHeatValue("BaseScenario",Run),getHeatValue("TempSup1",Run)/getHeatValue("BaseScenario",Run),getHeatValue("VentilationLosses04",Run)/getHeatValue("BaseScenario",Run),getHeatValue("VentilationLosses08",Run)/getHeatValue("BaseScenario",Run)]
	return value
def get_relativezero_graph(Run):
	baseVal=getHeatValue("BaseScenario",Run)
	value = [0,100*(getHeatValue("SolarGainGlaze",Run)-baseVal)/baseVal,100*(getHeatValue("SolarGainShade",Run)-baseVal)/baseVal,100*(getHeatValue("TempInf1",Run)-baseVal)/baseVal,100*(getHeatValue("TempSup1",Run)-baseVal)/baseVal,100*(getHeatValue("VentilationLosses04",Run)-baseVal)/baseVal,100*(getHeatValue("VentilationLosses08",Run)-baseVal)/baseVal]
	return value
def get_abs_diff(Run):
	value = [abs(getHeatValue("BaseScenario",Run)-getHeatValue("BaseScenario",Run)),abs(getHeatValue("SolarGainGlaze",Run)-getHeatValue("BaseScenario",Run)),abs(getHeatValue("SolarGainShade",Run)-getHeatValue("BaseScenario",Run)),abs(getHeatValue("TempInf1",Run)-getHeatValue("BaseScenario",Run)),abs(getHeatValue("TempSup1",Run)-getHeatValue("BaseScenario",Run)),abs(getHeatValue("VentilationLosses04",Run)-getHeatValue("BaseScenario",Run)),abs(getHeatValue("VentilationLosses08",Run)-getHeatValue("BaseScenario",Run))]
	return value



def plot_figures(mode):
	legend=["Base","Solar+","Solar-","Tinf","Tsup","Vent04","Vent08"]
	#plt.figure(figsize=(11.8, 7))
	plt.figure(figsize=(6,5))
	plt.rc('xtick', labelsize=10) 
	num =[13,14,15]
	for i in range(len(num)):
		plt.subplot(3,1,i+1)
		if (mode==0):
			value = get_relativevalue_graph("Run"+str(num[i]))
			plt.ylabel("Relative diff %",fontsize=6)
		if(mode==1):
			value = get_absvalue_graph("Run"+str(num[i]))
			plt.ylabel("Heat consumption Mwh",fontsize=6)
		if(mode==2):
			value = get_abs_diff("Run"+str(num[i]))
			plt.ylabel("Absolute diff Kwh",fontsize=6)
		if(mode==3):
			value = get_relativezero_graph("Run"+str(num[i]))
			axe = plt.gca()
			axe.yaxis.set_ticks([-25,-15,-5,5,15,25])
			axe.yaxis.set_ticklabels(["-25","-15","-5","5","15","25"],fontsize=10)
			axe.set_ylim(-35, 35)
			plt.ylabel("Relative diff (%)",fontsize=10)
		#print(value)
		plt.bar(legend,value)
		plt.scatter(legend,value,marker='+',s=5,color='red')
		
		plt.gcf().subplots_adjust(wspace = 0.5, hspace = 0.6)
		plt.title("Renovation case "+str(i+1),fontsize=13)
	plt.savefig("C:\\TRNSYS18\\Automatisation\\CumulativeCurves\\ParametricStudy"+str(mode)+".pdf")
	plt.show()

plot_figures(3)
