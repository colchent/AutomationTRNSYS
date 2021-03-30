import matplotlib.pyplot as plt
time = int
power = 84#puissance de chauffe
nbday = 24
nbstep = 6
#fileName = "SecondSimulation\\MultiBlock1C2.plt"



def play_curve(fileName,filepng):
	Pt = readCol(fileName,6)
	Phmoy = intoHourly(Pt,nbstep)
	#getDurationOfPower()
	Pdmoy = intoDaily(Phmoy,nbday)
	sPdmoy = sortPdmoy(Pdmoy)
	#sPhmoy = sortPhmoy(Phmoy)
	traceMonotonous(sPdmoy,filepng)


def traceMonotonous(MeanPow,file):
	x = [x for x in range(len(MeanPow))]
	plt.bar(x,MeanPow)
	plt.ylabel('Power (kW)')
	plt.xlabel("Days")
	plt.title("Cumulated power")
	plt.savefig(file)
	#plt.show()

def readCol(name):#lis les valeurs de puissance par pas de simulation
	Pt = []
	numcol = 6
	file =open(name,"r")#ouvre en lecture
	lines = file.readlines()
	time = len(lines)-2#nb d'itération totale avec un pas de 10min
	for i in range(time):
		sepLine = lines[i+2].split()#sépare les ligne du fichier
		Pt.append(sepLine[numcol-1])#Récupère le 6e élément de chaque ligne (Heatingsng)
	file.close()#ferme
	return Pt
#print(Pt)

def intoHourly(Pt,nbstep):#avoir une puissance moyenne sur une heure
	h=0
	Phmoy = []
	while h<52560:#nombre d'itération (6*nb heure dans l'année)
		somme = 0
		for m in range(nbstep):#somme les puissance sur une heure
			somme += float(Pt[h+m])
		Phmoy.append(somme/nbstep)#ajoute la puissance moyenne sur l'heure dans Phmoy
		h+=nbstep
	return Phmoy

def intoDaily(Phmoy,nbday):#avoir une puissance moyenne sur une journée
	d=0
	Pdmoy = []
	while d<8760:
		somme=0
		for n in range(nbday):
			somme+=Phmoy[d+n]
		Pdmoy.append(somme/nbday)
		d+=24#avoir une puissance moyenne sur un mois
	return Pdmoy

def sortPdmoy(Pdmoy):#trier par ordre décroissant de puissance
	sPdmoy = Pdmoy.copy()
	for i in range(len(Pdmoy)):
		for j in range(len(Pdmoy)):
			if sPdmoy[i]>sPdmoy[j]:
				a= sPdmoy[j]
				b= sPdmoy[i]
				sPdmoy[i]= a
				sPdmoy[j]= b
	return sPdmoy

def sortPhmoy(Phmoy):#trier par ordre décroissant de puissance
	sPhmoy = Phmoy.copy()
	for i in range(len(Phmoy)):
		for j in range(len(Phmoy)):
			if sPhmoy[i]>sPhmoy[j]:
				a= sPhmoy[j]
				b= sPhmoy[i]
				sPhmoy[i]= a
				sPhmoy[j]= b
	return sPhmoy

def getTotalHeatConsumption(Power):
	return Power
	



# def getDurationOfPower():#temps d'usage pour chaque puissance
# 	v = 7#nombre de valeur de puissance moyenne différentes sur 1h
# 	for c in range(v):#créer un tableau contenant les différentes valeurs de puissance
# 		value.append(c*(power/nbstep))
# 		tab.append(0)
# 	for i in range(len(Phmoy)):#Conter le nombre de répétition dans Phmoy
# 		for j in range(v):
# 			if Phmoy[i]==value[j]:
# 				tab[j]+=1
# 	for h in range(len(Pdmoy)):
# 		for k in range(v):
# 			if Pdmoy[h]==value[k]:
# 				tabd[k]+=1




