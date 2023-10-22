#File type: <Function> set
#By Junxiang H., 2023/07/03
#wacmk.com/cn Tech. Supp.

try:
	import ShockFinder.Addon.Painter.Basic as Basic
except:
	import Basic

from matplotlib import pyplot as plt, colors
import pandas as pd,numpy as np
def set_figure_info(**Figureinfo):
	title=Basic.CharUndecode(Basic.get_par(Figureinfo,"title",""))
	x_axis=Basic.CharUndecode(Basic.get_par(Figureinfo,"x_axis",""))
	y_axis=Basic.CharUndecode(Basic.get_par(Figureinfo,"y_axis",""))
	xscale=Basic.get_par(Figureinfo,"xscale")
	yscale=Basic.get_par(Figureinfo,"yscale")
	plt.title(title)
	plt.xlabel(x_axis)
	plt.ylabel(y_axis)
	if xscale!=None:
		plt.xscale(xscale)
	if yscale!=None:
		plt.yscale(yscale)
	
def line(*lines,**Figureinfo):
	showlabel=False
	set_figure_info(**Figureinfo)
	x_lim=Basic.get_par(Figureinfo,"x_lim")
	y_lim=Basic.get_par(Figureinfo,"y_lim")
	if x_lim!=None:
		plt.xlim(*x_lim)
	if y_lim!=None:
		plt.ylim(*y_lim)
	for line in lines:
		le,li=line
		plt.plot(le["x"],le["y"],**li)
		if Basic.get_par(li,"label")!=None:
			showlabel=True
	if showlabel:
		plt.legend()
	plt.show()

def line_share_x(line2,*line1,**Figureinfo):
	set_figure_info(**Figureinfo)
	showlabel=False
	x_lim=Basic.get_par(Figureinfo,"x_lim")
	y_lim=Basic.get_par(Figureinfo,"y_lim")
	if x_lim!=None:
		plt.xlim(*x_lim)
	if y_lim!=None:
		plt.ylim(*y_lim)
	for line in line1:
		le,li=line
		plt.plot(le["x"],le["y"],**li)
		if Basic.get_par(li,"label")!=None:
			showlabel=True
	tx=plt.twinx()
	y2=Basic.get_par(Figureinfo,"y_axis2")
	if y2!=None:
		tx.set_ylabel(y2)
	le,li=line2
	tx.plot(le["x"],le["y"],**li)
	if Basic.get_par(li,"label")!=None:
		showlabel=True
	y_lim2=Basic.get_par(Figureinfo,"y_lim2")
	if y_lim2!=None:
		tx.set_ylim(*y_lim2)
	if showlabel:
		plt.legend()
	plt.show()

def line_share_y(line2,*line1,**Figureinfo):
	set_figure_info(**Figureinfo)
	x_lim=Basic.get_par(Figureinfo,"x_lim")
	y_lim=Basic.get_par(Figureinfo,"y_lim")
	if x_lim!=None:
		plt.xlim(*x_lim)
	if y_lim!=None:
		plt.ylim(*y_lim)
	for line in line1:
		le,li=line
		plt.plot(le["x"],le["y"],**li)
		if Basic.get_par(li,"label")!=None:
			showlabel=True
	tx=plt.twiny()
	x2=Basic.get_par(Figureinfo,"x_axis2")
	if x2!=None:
		tx.set_xlabel(x2)
	le,li=line2
	tx.plot(le["x"],le["y"],**li)
	if Basic.get_par(li,"label")!=None:
		showlabel=True
	x_lim2=Basic.get_par(Figureinfo,"x_lim2")
	if x_lim2!=None:
		tx.set_xlim(*x_lim2)
	if showlabel:
		plt.legend()
	plt.show()

def surface(surface,**Figureinfo):
	set_figure_info(**Figureinfo)
	sf,sfi=surface
	x_lim=Basic.get_par(Figureinfo,"x_lim")
	y_lim=Basic.get_par(Figureinfo,"y_lim")
	if x_lim!=None:
		plt.xticks(*x_lim)
	else:
		plt.xticks([i[int(len(i)/2)] for i in np.split(sf["x"][:10*int(len(sf["x"])/10)],10)] if len(sf["x"])>10 else sf["x"])
	if y_lim!=None:
		plt.yticks(*y_lim)
	else:
		plt.yticks([i[int(len(i)/2)] for i in np.split(sf["y"][:10*int(len(sf["y"])/10)],10)] if len(sf["y"])>10 else sf["y"])
	#plt.figure("imshow",facecolor="lightgray")
	plt.imshow(np.flipud(sf["v"].T),cmap="RdBu",extent=[sf["x"][0],sf["x"][-1],sf["y"][0],sf["y"][-1]],norm=colors.LogNorm(),**sfi)
	plt.colorbar()
	plt.show()

def info():
	print("Module:",__file__)

if __name__=="__main__":
	import Line,Surface,math
	
	x=np.arange(0,100,0.1)
	l1=Line.CreateLine(x=x,y=x**2,label="$x^2$")
	l2=Line.CreateLine(x=x,y=x**3,label="$x^3$")
	line_share_y(l2,l1,label=True,title="Test")
	
	
	r=np.arange(100)
	p=np.arange(0,(2+0.01)*np.pi,2*0.01*np.pi)
	from scipy.special import lpmv
	v=lpmv(0,3,r).reshape(100,1)*(np.cos(p)**2).reshape(1,101)
	x,y,v=Basic.rop_to_xoy(r,p,v)
	#print(v)
	sf=Surface.CreateSurface(x=x,y=y,v=v)
	surface(sf)
	