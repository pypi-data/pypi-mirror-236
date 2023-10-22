#File type: extension <Module> set
#By Junxiang H., 2023/07/1
#wacmk.com/cn Tech. Supp.

#This script updates automaticly! Do not Modify!
#Update time:2023-10-22 05:08:11

AnalysisTool={}
try:
	try:
		import ShockFinder.Addon.AnalysisTool.MassFlux as MassFlux
	except Exception as err:
		print("MassFluxin ShockFinder dir importing error, reimporting in current dir")
		import MassFlux
	AnalysisTool["MassFlux"]=MassFlux
except Exception as err:
	print("Module: MassFlux import failure:",err)

try:
	try:
		import ShockFinder.Addon.AnalysisTool.Bremsstrahlung as Bremsstrahlung
	except Exception as err:
		print("Bremsstrahlungin ShockFinder dir importing error, reimporting in current dir")
		import Bremsstrahlung
	AnalysisTool["Bremsstrahlung"]=Bremsstrahlung
except Exception as err:
	print("Module: Bremsstrahlung import failure:",err)

try:
	try:
		import ShockFinder.Addon.AnalysisTool.Temperature as Temperature
	except Exception as err:
		print("Temperaturein ShockFinder dir importing error, reimporting in current dir")
		import Temperature
	AnalysisTool["Temperature"]=Temperature
except Exception as err:
	print("Module: Temperature import failure:",err)

try:
	try:
		import ShockFinder.Addon.AnalysisTool.SoundSpeed as SoundSpeed
	except Exception as err:
		print("SoundSpeedin ShockFinder dir importing error, reimporting in current dir")
		import SoundSpeed
	AnalysisTool["SoundSpeed"]=SoundSpeed
except Exception as err:
	print("Module: SoundSpeed import failure:",err)

try:
	try:
		import ShockFinder.Addon.AnalysisTool.Entropy as Entropy
	except Exception as err:
		print("Entropyin ShockFinder dir importing error, reimporting in current dir")
		import Entropy
	AnalysisTool["Entropy"]=Entropy
except Exception as err:
	print("Module: Entropy import failure:",err)

try:
	try:
		import ShockFinder.Addon.AnalysisTool.Shocks as Shocks
	except Exception as err:
		print("Shocksin ShockFinder dir importing error, reimporting in current dir")
		import Shocks
	AnalysisTool["Shocks"]=Shocks
except Exception as err:
	print("Module: Shocks import failure:",err)

try:
	try:
		import ShockFinder.Addon.AnalysisTool.MachNumber as MachNumber
	except Exception as err:
		print("MachNumberin ShockFinder dir importing error, reimporting in current dir")
		import MachNumber
	AnalysisTool["MachNumber"]=MachNumber
except Exception as err:
	print("Module: MachNumber import failure:",err)

if __name__=="__main__":
	print("Testing Model:",__file__)
	print("AnalysisTool:")
	for i in AnalysisTool.keys():
		print(i,":",AnalysisTool[i])
		print("\t",AnalysisTool[i].get)