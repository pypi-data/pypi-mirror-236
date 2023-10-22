# ShockFinder

**ShockFinder** is an interactive scientic simulation data analysis software based on python and supports multi-process, multi-mode, I/O access and drawing.

Author Junxiang H. & C. B. Singh<br>
If you have any questions and suggestions<br>
Please contact: huangjunxiang@mail.ynu.edu.cn

You can download the **outdate** version at **"Releases"** in your right hand.

Latest Version: 7.0, date: 2023-07-11
\<Inner Version: XME 3.1, XUI 1.1\>

# Install

Please follow one of the ways to install **ShockFinder**


```shell
pip3 install ShockFinder
```

And then download and release the zip (XUI libraries for Shockfinder) into the **folder** you would like to use ShockFinder (e.g., same folder with the ***shockfinder.py*** shown in **Useage**)

Link see https://github.com/wacmkxiaoyi/Shockfinder/releases

# Useage

Enter the following code and save it into a file (like ***shockfind.py***, version >=7.1)

```python
try:
	import XME
except:
	print("Warning: The default Multiprocess Engine XME is not installed, Multiprocess mode might not be used!")
	print("Please type: pip3 install XME to install")
	print("More infomation see: https://github.com/wacmkxiaoyi/Xenon-Multiprocessing-Engine")
	print("\n")
try:
	import XenonUI
except:
	print("Warning: The default GUI Engine XUI (XenonUI) is not installed, GUI mode might not be used!")
	print("Please type: pip3 install XenonUI to install")
	print("More infomation see: https://github.com/wacmkxiaoyi/Xenon-UI")
	print("\n")

import sys,os
import ShockFinder
from ShockFinder.Config import ShockFinderDir
from ShockFinder.Update import Update_all

def drop_bk(strc):
	if strc!="" and (strc[0]=="'" and strc[-1]=="'" or strc[0]=='"' and strc[-1]=='"'):
		strc=strc[1:-1]
	return strc
if __name__=="__main__":#windows support
	gui=True
	for i in sys.argv[1:]:
		if i.split("=")[0] in ("f","-f","file"):
			ShockFinder.ShockFinder(drop_bk(i.split("=")[1]))
			gui=False
		elif i.split("=")[0] in ("u","-u","update"):
			Update_all()
			gui=False
		elif i.split("=")[0] in ("n","-n","new"):#new=module@filename
			LoaderDir=os.path.join(ShockFinderDir,"Addon","Loader")
			AnalysisToolDir=os.path.join(ShockFinderDir,"Addon","AnalysisTool")
			PainterDir=os.path.join(ShockFinderDir,"Addon","Painter")
			IODir=os.path.join(ShockFinderDir,"Addon","IO")
			MultiprocessEngineDir=os.path.join(ShockFinderDir,"Addon","MultiprocessEngine")
			GUIDir=os.path.join(ShockFinderDir,"Addon","GUI")
			modu=i.split("=")[1].split("@")[0]
			mfname=i.split("=")[1].split("@")[1]
			if modu in ("Loader","AnalysisTool","Painter","IO","MultiprocessEngine","GUI"):
				import shutil
				if modu=="Loader":
					shutil.copy(mfname,LoaderDir)
				elif modu=="AnalysisTool":
					shutil.copy(mfname,AnalysisToolDir)
				elif modu=="Painter":
					shutil.copy(mfname,PainterDir)
				elif modu=="IO":
					shutil.copy(mfname,IODir)
				elif modu=="MultiprocessEngine":
					shutil.copy(mfname,MultiprocessEngineDir)
				elif modu=="GUI":
					shutil.copy(mfname,GUIDir)
			Update_all()
			gui=False
	if gui:
		ShockFinder.ShockFinder()
```

# GUI MODE

GUI Mode is used to **generate analysis configuration file** and **visualize analysis results**!

Entry GUI Mode:

```shell
python shockfind.py
```

The GUI engine for the ShockFinder is **XUI** (see https://github.com/wacmkxiaoyi/Xenon-UI). (This libraries is only used to **GUI mode**, the **PAM Mode** does not require)

Four pages can be used: **Analyze**, **Figure**, **Help** and **Exit**

Page **Exit** used to interrupt multithreading monitoring and exit the Shockfinder, and **Help** shown some basic information of ShockFinder (e.g., version, author)

## Page Analyze

Page **Analyze** has Three Menus, **Save Configuration**, **Global Settings** and **Analysis**

### Global Settings

Menu **Global Settings** has three sub-menus:

1. **Multi-process** : the configuration about multiprocessing analysis, default multiprocessing engine is **XME** (see https://github.com/wacmkxiaoyi/Xenon-Multiprocessing-Engine, some advanced optiones can follow this link).

2. **Database Storage**: the configuration about storing the after-analyzing data, default engine is **HDF5**, default project name (saving target file name) is **current timestampe** and Drop Buffer is the buffer cleared during the analysis process (default and recommend **True**)

3. **Simulation Data Loader**: in this submenu, you have to define which type of simulation data you used.

### Analysis

Menu **Analysis** has two sub-menus:

1. **Parameters**: in here you can define the global variable during the analyzing

2. **Quantities**: in here you can define which analysis approch will be used during the analyzing

### Save Configurations:

1. Button **Test**: to test cn the analysis process proceed normally

2. Button **Save**: save the analysis configuration file

## Page Figure

Page **Figure** has Two Menus, **Database**, and **Figure**

### Database

Menu **Database** has two sub-menus:

1. **Load**: before you figure the picture you like, you should load the **after-analyzing data** firstly. In this menu, data reading, browsing, and other functions can be performed

2. **Global Settings**: the configuration of loader of **after-analyzing data**

### Figure

Menu **Figure** has three sub-menus: **Set unit**, **2d** and **3d** (easy to understand without additional explanation)

# Parallel analysis mode (PAM)

After producing the analysis configration file (e.g., config1.ini, config2.ini), you can start to analyze:

```shell
python shockfinder.py -f=config1.ini -f=config2.ini ...
```

# How to add a new type of simulation or an analysis approach:

There are two of module models by ShockFinder's suggestion:

1. **LoaderModel.py**:
```python
#This is a model file for the Loader Addon
#It will be created when creating a new Loader
#Note!!!!: places which marke "<>" have to be updated, and delete "<>".

#File type: <Function> return <Object: Data>
#By Junxiang H., 2023/06/30
#wacmk.com/cn Tech. Supp.

#var filename includes the file_dir

#if you would like to import some packages,
#during the data loading.
#Please put that packages into this folder and using:

'''
try:
	import ShockFinder.Addon.Loader.<package1name> as <package1name>
	import ShockFinder.Addon.Loader.<package2name> as <package2name>
	#...
except:
	import <package1name> #debug
	import <package2name> #debug
	#...
'''


#A default Loader Addon can preprocess the filename,
#into to a formation with (time_index, file_dir, file_type)
#You can denote the below sentence to use it.

'''
try:
	import ShockFinder.Addon.Loader.FileNamePreProcess.FileNamePreProcess as FNPP
except:
	import FileNamePreProcess.FileNamePreProcess #debug
'''

try:
	import ShockFinder.Data
except:
	pass
def load(filename): #updated here
	#Loading Process
	read=<reader Process>(filename) #updated here
	#grid definded
	grid={}
	#GEOMETRY:	SPHERICAL	CYLINDRICAL		POLAR		CARTESIAN
	#			x1-x2-x3	x1-x2			x1-x2-x3	x1-x2-x3
	#			r-theta-phi r-z				r-phi-z		x-y-z
	grid["x1"]=read.<x1> #updated here
	grid["x2"]=read.<x2> #updated here
	grid["x3"]=read.<x3> #updated here 
	#basic quantities
	quantities={}
	quantities["vx1"]=read.<vx1> #updated here
	quantities["vx2"]=read.<vx2> #updated here
	quantities["vx3"]=read.<vx3> #updated here
	quantities["rho"]=read.<rho> #updated here
	quantities["prs"]=read.<prs> #updated here
	quantities["geometry"]=read.<geometry>
	#user definded...
	try:
		return Data.Data(grid,quantities)
	except:
		return (grid,quantities)
```

2. **AnalysisToolModel.py**:
```python
#This is a model file for the Loader Addon
#It will be created when creating a new Loader
#Note!!!!: places which marke "<>" have to be updated, and delete "<>".

#File type: <Function> return a new <Object: Data>
#By Junxiang H., 2023/07/01
#wacmk.com/cn Tech. Supp.

#if you would like to import some packages,
#during the data loading.
#Please put that packages into this folder and using:

try:
	from ShockFinder.Addon.AnalysisTool.Basic import *
	#if AvgTh_CAL is True
	#import ShockFinder.Addon.AnalysisTool.Mean as Mean
	#import ShockFinder.Addon.AnalysisTool.<packages name> as <packages name>
except:
	from Basic import *
	#import Mean #debug
	#import <packages name>

need=[]
#args will be inserted into Data Object
#vargs will not be inserted into Data Object
import numpy as np
def get(Dataobj,args={},vargs={}):
	Dataobj.quantities.update(args)
	for i in need:
		if i not in Dataobj.quantities.keys() and i not in vargs.keys():
			print("Warning: args:",i,"is needed without definding")
			return Dataobj
	quantities={
		#operation with dict args
		#...
		<quantity name>:... #update here
	}
	Dataobj.quantities.update(quantities)
	return Dataobj
def result(quantity_name=None,anafname=None):
	return () #this function will return result types shown in GUI
#if AvgTh mode is needed, please set AvgTh_cal=True
#The below code can be ignored, if set to False
AvgTh_cal=False
def get_AvgTh(Dataobj,args={},vargs={"Mean_axis":(1,)}):
	try:
		if AvgTh_cal:
			import copy
			newneed=copy.copy(need)
			if "Mean_axis" not in newneed:
				newneed.append("Mean_axis")
			Dataobj.quantities.update(args)
			for i in newneed:
				if i not in Dataobj.quantities.keys() and i not in vargs.keys():
					print("Warning: args:",i,"is needed without definding")
					return Dataobj
			meanstr=""
			try:
				meanaxis=vargs["Mean_axis"]
			except:
				meanaxis=Dataobj.quantities["Mean_axis"]
			for i in meanaxis:
				meanstr+=str(i)+"@"+str((round(vargs["Mean_axis"+str(i)][0],2),round(vargs["Mean_axis"+str(i)][1],2)))+"_" if "Mean_axis"+str(i) in vargs.keys() else meanstr+=str(i)+"@"+str((round(Dataobj.quantities["Mean_axis"+str(i)][0],2),round(Dataobj.quantities["Mean_axis"+str(i)][1],2)))+"_" if "Mean_axis"+str(i) in Dataobj.quantities.keys() else ""
			quantities={"AvgTh_"+meanstr+"<quantity name>":...} #update here
			Dataobj.quantities.update(quantities)
		else:
			print("Warning: AvgTh mode is not opened: <quantity name>") #update here
	except:
		print("Warning: AvgTh mode is not definded:", __file__) #update here
	return Dataobj

if __name__=="__main__":
	print("Testing Model:",__file__)
	from TestData import TestData
	TestData=get(TestData)
	print("Testing Result:", TestData.quantities[<quantity name>]) #update here!
	if AvgTh_cal:
		TestData=get_AvgTh(TestData)
		print("Testing Result:", TestData.quantities["AvgTh_<quantity name>"]) #update here!
```

Firstly, you have to put it in ShockFinder dir, by using

```shell
python shockfinder.py -n={module@filename/path}
```

in the DOC window. Then the new simulation Data type or analysis approach will be shown in **GUI** mode
