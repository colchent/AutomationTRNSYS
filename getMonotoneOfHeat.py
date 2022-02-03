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

def readCol(name):#read the power values at each simulation time step
	Pt = []
	numcol = 6
	file =open(name,"r")
	lines = file.readlines()
	time = len(lines)-2#total number of simulation for a 10min time step
	for i in range(time):
		sepLine = lines[i+2].split()
		Pt.append(sepLine[numcol-1])#Get Heatingsng
	file.close()#ferme
	return Pt

def readColQ(name):
	Pt = []
	numcol = 8
	file =open(name,"r")
	lines = file.readlines()
	time = len(lines)-2#total number of simulation for a 10min time step
	for i in range(time):
		sepLine = lines[i+2].split()#Get Heatingsng
	file.close()
	return Pt

def intoHourly(Pt,nbstep):#Get an averaged power on an hour 
	h=0
	Phmoy = []
	while h<52560:#Number of iteration in a year 
		somme = 0
		for m in range(nbstep):#sum the power on an hour
			somme += float(Pt[h+m])
		Phmoy.append(somme/nbstep)
		h+=nbstep
	return Phmoy

def intoDaily(Phmoy,nbday):#Get an averaged power on a day 
	d=0
	Pdmoy = []
	while d<8760:
		somme=0
		for n in range(nbday):#Sum the power on a day
			somme+=Phmoy[d+n]
		Pdmoy.append(somme/nbday)
		d+=24
	return Pdmoy

def sortPdmoy(Pdmoy):#Sort by decreasing order of power (day)
	sPdmoy = Pdmoy.copy()
	for i in range(len(Pdmoy)):
		for j in range(len(Pdmoy)):
			if sPdmoy[i]>sPdmoy[j]:
				a= sPdmoy[j]
				b= sPdmoy[i]
				sPdmoy[i]= a
				sPdmoy[j]= b
	return sPdmoy

def sortPhmoy(Phmoy):#Sort by decreasing order of power (hour)
	sPhmoy = Phmoy.copy()
	for i in range(len(Phmoy)):
		for j in range(len(Phmoy)):
			if sPhmoy[i]>sPhmoy[j]:
				a= sPhmoy[j]
				b= sPhmoy[i]
				sPhmoy[i]= a
				sPhmoy[j]= b
	return sPhmoy
