#File type: <Function> set
#By Junxiang H., 2023/07/03
#wacmk.com/cn Tech. Supp.



import numpy as np
import math

def get_par(args,name,default=None):
	try:
		return args[name]
	except:
		return default

def set_None(string):
	return None if string=="None" else string

def CharUndecode(string):
	return string.replace("$",r"$")

def find_index(x,value):
	result=np.where(x<value)[0]
	if len(result)==0:
		return 0
	elif len(x)==len(result):
		return None
	if value-x[result[-1]]>x[result[-1]+1]-value:
		return result[-1]+1
	return result[-1]

def get_2drp_value(r,phi,x,y,v,default):
	tr=(x**2+y**2)**0.5
	tp=math.atan(y/x)
	if x<0:
		tp+=np.pi
	elif y<0:
		tp+=2*np.pi
	rind=find_index(r,tr)
	if rind==None:
		return default
	pind=find_index(phi,tp)
	if pind==None:
		return default
	return v[rind][pind]

def rop_to_xoy(r,phi,v=None):
	if type(v)==type(None):
		return (r*np.cos(phi),r*np.sin(phi))
	x=y=np.union1d(-r,r)
	newv=np.full((len(x),len(y)),0.5*np.min(v) if np.min(v)>0 else 1.5*np.min(v))
	newv=np.array([np.array([get_2drp_value(r,phi,x[i],y[j],v,newv[i][j]) for j in range(len(newv[i]))]) for i in range(len(newv))])
	return (x,y,newv)

def get_2drt_value(r,theta,x,z,v,default):
	tr=(x**2+z**2)**0.5
	tt=math.acos(z/tr)
	rind=find_index(r,tr)
	if rind==None:
		return default
	tind=find_index(theta,tt)
	if tind==None:
		return default
	return v[rind][tind]
def rot_to_xoz(r,theta,v=None):
	if type(v)==type(None):
		return (r*np.sin(theta),r*np.cos(theta))
	x=z=np.union1d(-r,r)
	newv=np.full((len(x),len(z)),0.5*np.min(v) if np.min(v)>0 else 1.5*np.min(v))
	newv=np.array([np.array([get_2drt_value(r,theta,x[i],z[j],v,newv[i][j]) for j in range(len(newv[i]))]) for i in range(len(newv))])
	return (x,z,newv)

def get_3drzp_value(r,phi,x,y,k,v,default):
	tr=(x**2+y**2)**0.5
	tp=math.atan(y/x)
	if x<0:
		tp+=np.pi
	elif y<0:
		tp+=2*np.pi
	rind=find_index(r,tr)
	if rind==None:
		return default
	pind=find_index(phi,tp)
	if pind==None:
		return default
	return v[rind][pind][k]

def rzp_to_xyz(r,z,phi,v=None):
	if type(v)==type(None):
		return (r*np.cos(phi),r*np.sin(phi),z)
	x=y=np.union1d(-r,r)
	newv=np.full((len(x),len(y),len(z)),0.5*np.min(v) if np.min(v)>0 else 1.5*np.min(v))
	newv=np.array([np.array([np.array([get_3drzp_value(r,phi,x[i],y[j],k,v,newv[i][j][k]) for k in range(len(newv[i][j]))]) for j in range(len(newv[i]))]) for i in range(len(newv))])
	return (x,y,z,newv)

def get_3drtp_value(r,theta,phi,x,y,z,v,default):
	tr=(x**2+y**2+z**2)**0.5
	tt=math.acos(z/tr)
	tp=math.atan(y/x)
	if x<0:
		tp+=np.pi
	elif y<0:
		tp+=2*np.pi
	rind=find_index(r,tr)
	if rind==None:
		return default
	tind=find_index(theta,tt)
	if tind==None:
		return default
	pind=find_index(phi,tp)
	if pind==None:
		return default
	
	return v[rind][tind][pind]
def rtp_to_xyz(r,theta,phi,v=None):
	if type(v)==type(None):
		return (r*np.sin(theta)*np.cos(phi),r*np.sin(theta)*np.sin(phi),r*np.cos(theta))
	x=y=z=np.union1d(-r,r)
	newv=np.full((len(x),len(y),len(z)),0.5*np.min(v) if np.min(v)>0 else 1.5*np.min(v))
	newv=np.array([np.array([np.array([get_3drtp_value(r,theta,phi,x[i],y[j],z[k],v,newv[i][j][k]) for k in range(len(newv[i][j]))]) for j in range(len(newv[i]))]) for i in range(len(newv))])
	return (x,y,z,newv)

def _3D_to_2D(x,y,z,v,cx,cy,cz): #in this case, len(cx)=len(cy)=len(cz)
	cx=np.sort(cx)
	cy=np.sort(cy)
	cz=np.sort(cz)
	if len(cx) !=len(cy) or len(cx)!=len(cz) or len(cy)!=len(cz):
		return None
	r=(cx[-1]**2+cy[-1]**2+cz[-1]**2)**0.5
	newx=np.arange(-r,r,2*r/len(cx))
	newy=np.arange(-r,r,2*r/len(cx))
	newv=np.full((len(newx),len(newy)),0.5*np.min(v) if np.min(v)>0 else 1.5*np.min(v)) 
	for i in range(len(newx)):
		r=(cx[i]**2+cy[i]**2+cz[i]**2)**0.5
		theta=math.acos(cz[i]/r)
		for j in range(len(newy)):
			phi=math.atan(newy[j]/newx[i])
			if newx[i]<0:
				phi+=np.pi
			elif newy[j]<0:
				phi+=2*np.pi
			nr=(newx[i]**2+newy[j]**2)**0.5
			sz=nr*math.cos(theta)
			sx=nr*math.sin(theta)*math.cos(phi)
			sy=nr*math.sin(theta)*math.sin(phi)
			sxind=Basic.find_index(x,sx)
			if sxind==None:
				continue
			syind=Basic.find_index(y,sy)
			if syind==None:
				continue
			szind=Basic.find_index(z,sz)
			if szind==None:
				continue
			newv[i][j]=v[sxind][syind][szind]
	return (newx,newy,newv)

def info():
	print("Module:",__file__)

if __name__=="__main__":
	info()