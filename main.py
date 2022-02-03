from automate import *
from getMonotoneOfHeat import *
import subprocess
import numpy as np

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



def filenames(nbsimu):
    file_names=[]
    for i in range(nbsimu):
        file_names.append("C:\\TRNSYS18\\Automatisation\\Results\\ResultSimu"+str(i)+".plt")
    return file_names

def MultiCategories(files_names):#nb_building : number of buildings per categories
        #nb_buildings = [74, 81, 60, 78, 63, 79, 97, 138, 29, 46, 69, 94, 122, 160, 140, 184, 39, 65, 72, 95, 116, 141, 164, 188, 45, 74, 80, 140, 128, 156, 129, 163, 54, 106, 85, 117, 128, 123, 164, 137, 56, 126, 94, 146, 199, 98, 122, 85, 159, 120, 155, 151, 68, 100, 104, 60, 180, 146, 114, 86, 89, 82, 84, 59]
        nb_buildings = [48, 74, 81, 60, 78, 63, 79, 97, 138, 334, 31, 29, 46, 69, 94, 122, 160, 140, 184, 172, 43, 39, 65, 72, 95, 116, 141, 164, 188, 126, 36, 45, 74, 80, 140, 128, 156, 129, 163, 94, 53, 54, 106, 85, 117, 128, 123, 164, 137, 84, 79, 56, 126, 94, 146, 199, 98, 122, 85, 46, 70, 159, 120, 155, 151, 68, 100, 104, 60, 55, 132, 180, 146, 114, 86, 89, 82, 84, 59, 55, 225, 171, 157, 166, 97, 106, 22, 31, 23, 50, 318, 232, 121, 150, 44, 29, 88, 13, 13, 26]

        tab_prod = []
        tab_pow = []
        tab_pow_h=[]
        tab_cat_demand = []
        for b in range(len(nb_buildings)):
            Ps=readCol(files_names[b])
            QHeat = float(readColQ(files_names[b])[-1])
            Ph=intoHourly(Ps,6)
            Pd = intoDaily(Ph,nbday)
            
            tab_cat_demand.append(QHeat*nb_buildings[b])
            
            tab_prod.append([24*nb_buildings[b]*i/1000000 for i in Pd])
            
            tab_pow.append([nb_buildings[b]*i/1000 for i in Pd])
            
            tab_pow_h.append([nb_buildings[b]*i/1000 for i in Ph])
            
        sum_prod=[0 for t in range(len(tab_prod[0]))]
        sum_pow =[0 for e in range(len(tab_pow[0]))]
        sum_pow_h = [0 for e in range(len(tab_pow_h[0]))]
        
        
        for c in range(len(tab_prod[0])):
                for l in range(len(tab_prod)):
                       sum_prod[c]=sum_prod[c]+tab_prod[l][c]
                       
        for c in range(len(tab_pow[0])):
            for l in range(len(tab_pow)):
                sum_pow[c]=sum_pow[c]+tab_pow[l][c]
                
        for c in range(len(tab_pow_h[0])):
            for l in range(len(tab_pow_h)):
                sum_pow_h[c]=sum_pow_h[c]+tab_pow_h[l][c]
        
        
        
        return sum_prod,sum_pow, sortPdmoy(sum_pow),sum_pow_h, tab_cat_demand
 
#somme_prod, somme_pow, monotone, somme_Ph, tab_cat_demand = MultiCategories(filenames(100))
#print(tab_cat_demand)
"""
x = [x for x in range(365)]
xh = [x for x in range(8760)]

fig,ax = plt.subplots(figsize=(15,10))
#ax.plot(x,monotone,label = "Monotone (MW)")
#ax.plot(x,somme_pow,label="Power of heat demand (Mw)")
ax.plot(xh,somme_Ph,label = "Evolution of hourly heat needs")
ax.plot(xh,sortPdmoy(somme_Ph),label="Monotone of heat demand(MW)")
#ax2=ax.twinx()
#ax2.plot(x,np.cumsum(somme_prod),color='r',label="Cumulative heat demand (MWh)")
#•ax.set_ylim(0,850)
ax.set_xlim(0,8760)
ax.set_xlabel("Hours",fontsize=18)
ax.set_ylabel("Heat power need (MW as hour average)",fontsize=18)
#ax2.set_ylabel("Cumulative heat need (GWh)",fontsize=18)

# ax2.legend()
ax.legend()
plt.show()
print(np.mean(somme_pow))
print(np.sum(somme_prod))
print(np.sum(somme_Ph))
"""
def trace_all(nbcurve,nbplotcol,nbplotline):
    plt.figure(figsize=(12, 8))
    c=0
    k=1
    num_curve = np.arange(0,nbcurve)
    for j in num_curve:
    		Pt = readCol("C:\\TRNSYS18\\Automatisation\\Results\\ResultSimu"+str(j)+".plt")
    		Pd = intoDaily(intoHourly(Pt,nbstep),nbday)
    		sortedPd = sortPdmoy(Pd)
    		x = [x for x in range(len(sortedPd))]
    
    		eneruse=[]
    		for i in range(len(Pd)):
    			eneruse.append(sum(Pd[0:i]))
    			eneruse[i]=(eneruse[i]*24)/1000 #to have a quantity of energy in Mwh
    		#print(eneruse)
    		plt.subplot(nbplotline,nbplotcol,c+1)
    		c+=1
    		plt.gcf().subplots_adjust(wspace = 0.5, hspace = 1.2)
    		ax1 = plt.gca()
    		#ax2 = ax1.twinx()
    		ax1.set_ylim(0,70)
    		#ax2.set_ylim(0,180)
    
    		ax1.set_xlim(0,365)
    		plt.xticks(fontsize=8)
    		plt.yticks(fontsize=8)
    		ax1.plot(x,sortedPd,label="Monotone of heat (kW)")	
    		ax1.plot(x,Pd,label="Time serie of heating rate(kW)")
    		#ax2.plot(x,eneruse,color= "r",label="Time serie heating rate (Mwh)")
    		ax1.set_ylabel("P (kW)",fontsize=11)
    		#ax2.set_ylabel("Energy MWh",fontsize=8)
    		#plt.ylabel('Power (kW)')
    		plt.xlabel("Days",fontsize=11)
    		#plt.title("Building "+str(c+1)+" basis case",fontsize=8)
    		#plt.title("Building "+str(c+1)+" basis case,  (U="+str(round(float(building_value[j]['Building loss coefficient']),2))+" KJ/h.m2.C)",fontsize=13)
    		plt.title("Range n°"+str(k+1)+" (U="+str(round(float(building_value[j]['Building loss coefficient']),2))+" KJ/h.m2.C)",fontsize=13)
    		k+=1
	 #print(sortedPd)
    ax1.legend(loc='lower center', bbox_to_anchor=(0.48, -1.4),fontsize=10,fancybox=True, shadow=True, ncol=2)
	
    plt.savefig("C:\\TRNSYS18\\Automatisation\\CumulativeCurves\\CumulatedCurvesAppComplex.pdf")
    plt.show()
	#num_curve = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]


def trace_selected(nbcurve,nbplotcol,nbplotline):
	#plt.figure(figsize=(5, 6))
	plt.figure(figsize=(5, 6))
	num_curve = [0,1,2,3,4,5,6,7]
	#num_curve = [12,13,14]
	#file_names = ["C:\\TRNSYS18\\Automatisation\\Results\\ResultSimu1.plt","C:\\TRNSYS18\\Automatisation\\Results\\ResultSimu5.plt","C:\\TRNSYS18\\Automatisation\\Results\\ResultSimu8.plt","C:\\TRNSYS18\\Automatisation\\Results\\ResultSimu6.plt","C:\\TRNSYS18\\Automatisation\\Results\\ResultSimu14.plt"]
	#sum_curve=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
	sum_curve = [0,6,12,13,14]
	file_names=[]
	for i in sum_curve:
		file_names.append("C:\\TRNSYS18\\Automatisation\\Results\\ResultSimu"+str(i)+".plt")

	#num_curve = [x for x in range(15)]
	st =[]
	for j in range(nbcurve+1):
		
		
		plt.subplot(nbplotline,nbplotcol,j+1)

		plt.gcf().subplots_adjust(wspace = 0.5, hspace = 0.9)
		
		if(j<nbcurve):
			
			Pt = readCol("C:\\TRNSYS18\\Automatisation\\Results\\ResultSimu"+str(num_curve[j])+".plt")
			Pd = intoDaily(intoHourly(Pt,nbstep),nbday)
			sortedPd = sortPdmoy(Pd)
			x = [x for x in range(len(sortedPd))]
			
			eneruse=[]
			for i in range(len(Pd)):
				eneruse.append(sum(Pd[0:i]))
				eneruse[i]=(eneruse[i]*24)/1000 #to have a quantity of energy in Mwh

			ax1 = plt.gca()
			#ax2 = ax1.twinx()
			ax1.set_ylim(0,70)
			#ax2.set_ylim(0,180)
			ax1.set_xlim(0,365)
			plt.xticks(fontsize=8)
			plt.yticks(fontsize=8)
			ax1.plot(x,sortedPd,label="Cumulative heating rate (kw)")	
			#ax2.plot(x,eneruse,color= "r",label="Time serie heating rate (Mwh)")
			ax1.set_ylabel("P (kW)",fontsize=11)
			#ax2.set_ylabel("Energy MWh",fontsize=8)
			#plt.ylabel('Power (kW)')
			plt.xlabel("Days",fontsize=11)
			U = building_value
			plt.title("Renovation case "+str(j+1)+",  (U="+str(round(float(building_value[j]['Building loss coefficient']),2))+"KJ/h.m2.C)",fontsize=13)
			
		else:
			ax = plt.gca()
			ax.set_ylim(0,250)
			ax.set_xlim(0,365)
			ax.set_ylabel("P (kW)",fontsize=11)
			globalcumu = MultiBuilding(len(sum_curve),file_names)
			plt.plot(x,globalcumu)
			plt.title("Cumulated curve of " +str(len(sum_curve))+ " buildings",fontsize=13)
		
	plt.savefig("C:\\TRNSYS18\\Automatisation\\CumulativeCurves\\CumulatedGlobal.pdf")
	plt.show()
"""    
dt=[]
nb_buildings = [74, 81, 60, 78, 63, 79, 97, 138, 29, 46, 69, 94, 122, 160, 140, 184, 39, 65, 72, 95, 116, 141, 164, 188, 45, 74, 80, 140, 128, 156, 129, 163, 54, 106, 85, 117, 128, 123, 164, 137, 56, 126, 94, 146, 199, 98, 122, 85, 159, 120, 155, 151, 68, 100, 104, 60, 180, 146, 114, 86, 89, 82, 84, 59]
nb_all_building = [48, 74, 81, 60, 78, 63, 79, 97, 138, 334, 31, 29, 46, 69, 94, 122, 160, 140, 184, 172, 43, 39, 65, 72, 95, 116, 141, 164, 188, 126, 36, 45, 74, 80, 140, 128, 156, 129, 163, 94, 53, 54, 106, 85, 117, 128, 123, 164, 137, 84, 79, 56, 126, 94, 146, 199, 98, 122, 85, 46, 70, 159, 120, 155, 151, 68, 100, 104, 60, 55, 132, 180, 146, 114, 86, 89, 82, 84, 59, 55, 225, 171, 157, 166, 97, 106, 22, 31, 23, 50, 318, 232, 121, 150, 44, 29, 88, 13, 13, 26]

for i in range(100):
    t = readColQ("C:\\TRNSYS18\\Automatisation\\Results\\ResultSimu"+str(i)+".plt")
    dt.append(nb_all_building[i]*float(t[-1]))
print(sum(dt))
"""
create_file(nb_simulation)
run_simulation(nb_simulation)

#trace_all(8,2,4)
#trace_selected(8,2,4)



#subprocess.call("C:\\TRNSYS18\\Exe\\trnexe64.exe"+ " " +"C:\\TRNSYS18\\MyProjects\\trnsysfiles\\Run1.dck /n", shell = True)
#subprocess.call("taskkill /f /im trnexe64.exe", shell = True)
# C:\TRNSYS18\Exe>trnexe64.exe C:\TRNSYS18\MyProjects\trnsysfiles\SimpleBuilding.dck
#subprocess.call("cd C:\TRNSYS18\Exe", shell=True)
#subprocess.call("C:\TRNSYS18\\Exe\\trnexe64.exe C:\\TRNSYS18\\MyProjects\\trnsysfiles\\SimpleBuilding.dck", shell = True)

# subprocess.call(['runas', '/user:thibault.colchen', 'cd Exe\\trnexe64.exe C:\\TRNSYS18\\MyProjects\\trnsysfiles\\SimpleBuilding.dck'])
