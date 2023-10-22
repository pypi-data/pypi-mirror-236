#File type: <Function>
#By Junxiang H., 2023/07/03
#wacmk.com/cn Tech. Supp.
try:
	import ShockFinder.Addon.Painter.Basic as Basic
except:
	import Basic
import pandas as pd,numpy as np
def CreateLine(**args):
	x=Basic.get_par(args,"x")
	y=Basic.get_par(args,"y")
	z=Basic.get_par(args,"z")
	if type(x) == type(None) or type(y) == type(None):
		return None
	label=Basic.get_par(args,"label","")
	color=Basic.get_par(args,"color")
	linestyle=Basic.get_par(args,"linestyle","-")
	if type(z)!=type(None):
		line={
			"x":x,
			"y":y,
			"z":z}
	else:
		line={
			"x":x,
			"y":y}
	lineinfo={
			"label":None if label==None else Basic.CharUndecode(label),
			"color":Basic.set_None(color),
			"linestyle":linestyle
		}
	for i in args.keys():
		if i not in lineinfo.keys() and i not in line.keys():
			lineinfo[i]=args[i]
	return (line,lineinfo)

def FormatLine(line,lineinfo,lineid):
	lineframe=pd.DataFrame(line,dtype=float)
	lineinfoframe=pd.DataFrame(lineinfo,index=[lineid])
	return (lineframe,lineinfoframe)

def DecodeLine(lineframe,lineinfoframe):
	data=dict(zip(["x","y","z"],[np.array(list(lineframe.to_dict()[i].values())) for i in lineframe.keys()])) 
	data.update(lineinfoframe.to_dict())
	return CreateLine(**data)

def info():
	print("Module:",__file__)


if __name__=="__main__":
	x=np.arange(0,100,0.1)
	line0,lineinfo0=CreateLine(x=x,y=x**2)
	line0frame,line0infoframe=FormatLine(line0,lineinfo0,0)
	#print(line0frame,"\n",line0infoframe)
	print(DecodeLine(line0frame,line0infoframe.loc[0]))