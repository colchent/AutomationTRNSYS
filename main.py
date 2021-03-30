from automate import *
from getMonotoneOfHeat import *
import subprocess

def run_simulation(nb_simulation):
	for simu in range(nb_simulation):
		f = "C:\\TRNSYS18\\Automatisation\\deckfiles\\simu"+str(simu)+".dck"
		modif_deck(f,simu)
		subprocess.call("C:\\TRNSYS18\\Exe\\trnexe64.exe"+ " " +"C:\\TRNSYS18\\Automatisation\\deckfiles\\simu"+ str(simu)+ ".dck /n /h", shell = True)
		create_results(simu)
		#play_curve("C:\\TRNSYS18\\Automatisation\\Results\\ResultSimu"+str(simu)+".plt","C:\\TRNSYS18\\Automatisation\\CumulativeCurves\\CumulativePower"+str(simu)+".png")
	

def MultiBuilding(nbbuildings,fileNames):
	tabP=[]
	s=[]

	for b in range(nbbuildings):
		Ps = readCol(fileNames[b])
		Ph = intoHourly(Ps,6)
		Pd = intoDaily(Ph,nbday)
		tabP.append(Pd)
	
	somme =[0 for e in range(len(tabP[0]))]
	for c in range(len(tabP[0])):
		for l in range(len(tabP)):
			somme[c]=somme[c]+tabP[l][c]
	
	Pdsorted = sortPdmoy(somme)
	
	return Pdsorted

def trace_all(nbcurve,nbplotcol,nbplotline):
	plt.figure(figsize=(5, 6))
	num_curve = [0,3,6,9,12]
	#num_curve = [x for x in range(15)]
	for j in range(nbcurve):
		
		Pt = readCol("C:\\TRNSYS18\\Automatisation\\Results\\ResultSimu"+str(j)+".plt")
		Pd = intoDaily(intoHourly(Pt,nbstep),nbday)
		sortedPd = sortPdmoy(Pd)
		x = [x for x in range(len(sortedPd))]

		eneruse=[]
		for i in range(len(Pd)):
			eneruse.append(sum(Pd[0:i]))
			eneruse[i]=(eneruse[i]*24)/1000 #to have a quantity of energy in Mwh
		print(eneruse)
		plt.subplot(nbplotline,nbplotcol,j+1)

		plt.gcf().subplots_adjust(wspace = 0.5, hspace = 0.7)
		ax1 = plt.gca()
		ax2 = ax1.twinx()
		ax1.set_ylim(0,70)
		ax2.set_ylim(0,180)

		ax1.set_xlim(0,365)
		plt.xticks(fontsize=8)
		plt.yticks(fontsize=8)
		ax1.plot(x,sortedPd,label="Cumulative power (kw)")	
		ax2.plot(x,eneruse,color= "r",label="Time serie heating rate (Mwh)")
		ax1.set_ylabel("Power kW",fontsize=8)
		ax2.set_ylabel("Energy MWh",fontsize=8)
		#plt.ylabel('Power (kW)')
		plt.xlabel("Days",fontsize=8)
		plt.title("Simulation "+str(j+1),fontsize=8)
		
	#print(sortedPd)
	ax1.legend(loc='lower center', bbox_to_anchor=(0.2, -0.75),fontsize=6,
          fancybox=True, shadow=True, ncol=1)
	ax2.legend(loc='lower center', bbox_to_anchor=(0.6, -0.75),fontsize=6,
          fancybox=True, shadow=True, ncol=1)
	plt.savefig("C:\\TRNSYS18\\Automatisation\\CumulativeCurves\\CumulatedCurvesAppComplex.pdf")
	plt.show()
def trace_selected(nbcurve,nbplotcol,nbplotline):
	plt.figure(figsize=(5, 6))
	num_curve = [12,13,14]
	file_names = ["C:\\TRNSYS18\\Automatisation\\Results\\ResultSimu1.plt","C:\\TRNSYS18\\Automatisation\\Results\\ResultSimu5.plt","C:\\TRNSYS18\\Automatisation\\Results\\ResultSimu8.plt","C:\\TRNSYS18\\Automatisation\\Results\\ResultSimu6.plt","C:\\TRNSYS18\\Automatisation\\Results\\ResultSimu14.plt"]
	#num_curve = [x for x in range(15)]
	st =[]
	for j in range(nbcurve+1):
		
		
		plt.subplot(nbplotline,nbplotcol,j+1)

		plt.gcf().subplots_adjust(wspace = 0.5, hspace = 0.9)
		
		if(j<=2):

			Pt = readCol("C:\\TRNSYS18\\Automatisation\\Results\\ResultSimu"+str(num_curve[j])+".plt")
			Pd = intoDaily(intoHourly(Pt,nbstep),nbday)
			sortedPd = sortPdmoy(Pd)
			x = [x for x in range(len(sortedPd))]
			
			eneruse=[]
			for i in range(len(Pd)):
				eneruse.append(sum(Pd[0:i]))
				eneruse[i]=(eneruse[i]*24)/1000 #to have a quantity of energy in Mwh

			ax1 = plt.gca()
			ax2 = ax1.twinx()
			ax1.set_ylim(0,70)
			ax2.set_ylim(0,180)
			ax1.set_xlim(0,365)
			plt.xticks(fontsize=8)
			plt.yticks(fontsize=8)
			ax1.plot(x,sortedPd,label="Cumulative power (kw)")	
			ax2.plot(x,eneruse,color= "r",label="Time serie heating rate (Mwh)")
			ax1.set_ylabel("Power kW",fontsize=8)
			ax2.set_ylabel("Energy MWh",fontsize=8)
			#plt.ylabel('Power (kW)')
			plt.xlabel("Days",fontsize=8)
			plt.title("Renovation case "+str(j+1),fontsize=8)
		else:
			ax = plt.gca()
			ax.set_ylim(0,250)
			ax.set_xlim(0,260)
			globalcumu = MultiBuilding(5,file_names)
			plt.plot(x,globalcumu)
			plt.title("Cumulated curve of 5 buildings",fontsize=8)
		
	plt.savefig("C:\\TRNSYS18\\Automatisation\\CumulativeCurves\\CumulatedGlobal.pdf")
	plt.show()
	
#create_file(nb_simulation)
#run_simulation(nb_simulation)
trace_all(3,1,4)
#subprocess.call("C:\\TRNSYS18\\Exe\\trnexe64.exe"+ " " +"C:\\TRNSYS18\\MyProjects\\trnsysfiles\\Run1.dck /n", shell = True)
#subprocess.call("taskkill /f /im trnexe64.exe", shell = True)
# C:\TRNSYS18\Exe>trnexe64.exe C:\TRNSYS18\MyProjects\trnsysfiles\SimpleBuilding.dck
#subprocess.call("cd C:\TRNSYS18\Exe", shell=True)
#subprocess.call("C:\TRNSYS18\\Exe\\trnexe64.exe C:\\TRNSYS18\\MyProjects\\trnsysfiles\\SimpleBuilding.dck", shell = True)

# subprocess.call(['runas', '/user:thibault.colchen', 'cd Exe\\trnexe64.exe C:\\TRNSYS18\\MyProjects\\trnsysfiles\\SimpleBuilding.dck'])



	