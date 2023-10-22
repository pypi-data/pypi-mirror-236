#File type: algroithm <Function> set
#By Junxiang H., 2023/07/01
#wacmk.com/cn Tech. Supp.

import numpy as np
def get_dx(a):
	if a.ndim==3:
		return a[1:,:,:]-a[:-1,:,:]
	elif a.ndim==2:
		return a[1:,:]-a[:-1,:]
	else:
		return a[1:]-a[:-1]

def get_x(a):
	if a.ndim==3:
		return (a[1:,:,:]+a[:-1,:,:])/2
	elif a.ndim==2:
		return (a[1:,:]+a[:-1,:])/2
	else:
		return (a[1:]+a[:-1])/2

def get_dy(a):
	if a.ndim==3:
		return a[:,1:,:]-a[:,:-1,:]
	elif a.ndim==2:
		return a[:,1:]-a[:,:-1]
	else:
		return None

def get_y(a):
	if a.ndim==3:
		return (a[:,1:,:]+a[:,:-1,:])/2
	elif a.ndim==2:
		return (a[:,1:]+a[:,:-1])/2
	else:
		return None

def get_dz(a):
	if a.ndim==3:
		return a[:,:,1:]-a[:,:,:-1]
	else:
		return None

def get_z(a):
	if a.ndim==3:
		return (a[:,:,1:]+a[:,:,:-1])/2
	else:
		return None

def gradient(Dataobj,quantity_name):
	if type(quantity_name) in (np.ndarray,list,tuple):
		for i in quantity_name:
			Dataobj=gradient(Dataobj,i)
		return Dataobj
	if "geometry" not in Dataobj.quantities.keys() or quantity_name not in Dataobj.quantities.keys():
		print("Warning: args: geometry and",quantity_name,"are needed without definding in 3d gradient calculation")
		return Dataobj
	quantities={}
	if Dataobj.quantities[quantity_name].ndim==1:#1d
		quantities["Gradient_"+quantity_name]=np.gradient(Dataobj.quantities[quantity_name],Dataobj.grid["x1"])
	elif Dataobj.quantities[quantity_name].ndim==2:#2d
		gd=np.gradient(Dataobj.quantities[quantity_name],Dataobj.grid["x1"],Dataobj.grid["x2"])
		if Dataobj.quantities["geometry"] in ("SPHERICAL","POLAR"):
			quantities["Gradient_"+quantity_name+"_x1"]=gd[0]
			quantities["Gradient_"+quantity_name+"_x2"]=gd[1]/Dataobj.grid["x1"].reshape((len(Dataobj.grid["x1"]),1))
		else:
			quantities["Gradient_"+quantity_name+"_x1"]=gd[0]
			quantities["Gradient_"+quantity_name+"_x2"]=gd[1]
	elif Dataobj.quantities[quantity_name].ndim==3:#3d
		gd=np.gradient(Dataobj.quantities[quantity_name],Dataobj.grid["x1"],Dataobj.grid["x2"],Dataobj.grid["x3"])
		if Dataobj.quantities["geometry"] in ("SPHERICAL","POLAR"):
			quantities["Gradient_"+quantity_name+"_x1"]=gd[0]
			quantities["Gradient_"+quantity_name+"_x2"]=gd[1]/Dataobj.grid["x1"].reshape((len(Dataobj.grid["x1"]),1,1))
			if Dataobj.quantities["geometry"]=="SPHERICAL":
				quantities["Gradient_"+quantity_name+"_x3"]=gd[2]/Dataobj.grid["x1"].reshape((len(Dataobj.grid["x1"]),1,1))/np.sin(Dataobj.grid["x2"].reshape((1,len(Dataobj.grid["x2"]),1)))
			else:
				quantities["Gradient_"+quantity_name+"_x3"]=gd[2]
		else:
			quantities["Gradient_"+quantity_name+"_x1"]=gd[0]
			quantities["Gradient_"+quantity_name+"_x2"]=gd[2]
			quantities["Gradient_"+quantity_name+"_x3"]=gd[3]
	Dataobj.update(quantities)
	return Dataobj

def divergence(Dataobj,quantity_name):
	if type(quantity_name) in (np.ndarray,list,tuple):
		for i in quantity_name:
			Dataobj=divergence(Dataobj,i)
		return Dataobj
	quantities={}
	if "geometry" not in Dataobj.quantities.keys() or quantity_name not in Dataobj.quantities.keys():
			print("Warning: args: geometry and",quantity_name,"are needed without definding in 3d gradient calculation")
			return Dataobj
	if Dataobj.quantities[quantity_name].ndim==1:#1d
		if Dataobj.quantities["geometry"] in ("SPHERICAL","POLAR"):
			if Dataobj.quantities["geometry"]=="SPHERICAL":
				quantities["Divergence_"+quantity_name]=np.gradient(Dataobj.grid["x1"]**2*Dataobj.quantities[quantity_name],Dataobj.grid["x1"])/Dataobj.grid["x1"]**2
			else:
				quantities["Divergence_"+quantity_name]=np.gradient(Dataobj.grid["x1"]*Dataobj.quantities[quantity_name],Dataobj.grid["x1"])/Dataobj.grid["x1"]
		else:
			quantities["Divergence_"+quantity_name]=np.gradient(Dataobj.quantities[quantity_name],Dataobj.grid["x1"])
	elif Dataobj.quantities[quantity_name].ndim==2:#2d
		if Dataobj.quantities["geometry"] in ("SPHERICAL","POLAR"):
			if Dataobj.quantities["geometry"]=="SPHERICAL":
				gd1=np.gradient(Dataobj.grid["x1"].reshape((len(Dataobj.grid["x1"]),1))**2*Dataobj.quantities[quantity_name],Dataobj.grid["x1"],Dataobj.grid["x2"])[0]/Dataobj.grid["x1"].reshape((len(Dataobj.grid["x1"]),1))**2
				gd2=np.gradient(np.sin(Dataobj.grid["x2"].reshape((1,len(Dataobj.grid["x2"]))))*Dataobj.quantities[quantity_name],Dataobj.grid["x1"],Dataobj.grid["x2"])[1]/Dataobj.grid["x1"].reshape((len(Dataobj.grid["x1"]),1))/np.sin(Dataobj.grid["x2"].reshape((1,len(Dataobj.grid["x2"]))))
			else:
				gd1=np.gradient(Dataobj.grid["x1"].reshape((len(Dataobj.grid["x1"]),1))*Dataobj.quantities[quantity_name],Dataobj.grid["x1"],Dataobj.grid["x2"])[0]/Dataobj.grid["x1"].reshape((len(Dataobj.grid["x1"]),1))
				gd2=np.gradient(Dataobj.quantities[quantity_name],Dataobj.grid["x1"],Dataobj.grid["x2"])[1]/Dataobj.grid["x1"].reshape((len(Dataobj.grid["x1"]),1))
		else:
			gd1,gd2=np.gradient(Dataobj.quantities[quantity_name],Dataobj.grid["x1"],Dataobj.grid["x2"])
		quantities["Divergence_"+quantity_name]=gd1+gd2
	elif Dataobj.quantities[quantity_name].ndim==3:#3d
		if Dataobj.quantities["geometry"] in ("SPHERICAL","POLAR"):
			if Dataobj.quantities["geometry"]=="SPHERICAL":
				gd1=np.gradient(Dataobj.grid["x1"].reshape((len(Dataobj.grid["x1"]),1,1))**2*Dataobj.quantities[quantity_name],Dataobj.grid["x1"],Dataobj.grid["x2"],Dataobj.grid["x3"])[0]/Dataobj.grid["x1"].reshape((len(Dataobj.grid["x1"]),1,1))**2
				gd2=np.gradient(np.sin(Dataobj.grid["x2"].reshape((1,len(Dataobj.grid["x2"]),1)))*Dataobj.quantities[quantity_name],Dataobj.grid["x1"],Dataobj.grid["x2"],Dataobj.grid["x3"])[1]/Dataobj.grid["x1"].reshape((len(Dataobj.grid["x1"]),1,1))/np.sin(Dataobj.grid["x2"].reshape((1,len(Dataobj.grid["x2"]),1)))
				gd3=np.gradient(Dataobj.quantities[quantity_name],Dataobj.grid["x1"],Dataobj.grid["x2"],Dataobj.grid["x3"])[2]/Dataobj.grid["x1"].reshape((len(Dataobj.grid["x1"]),1,1))/np.sin(Dataobj.grid["x2"].reshape((1,len(Dataobj.grid["x2"]),1)))
			else:
				gd1=np.gradient(Dataobj.grid["x1"].reshape((len(Dataobj.grid["x1"]),1,1))*Dataobj.quantities[quantity_name],Dataobj.grid["x1"],Dataobj.grid["x2"],Dataobj.grid["x3"])[0]/Dataobj.grid["x1"].reshape((len(Dataobj.grid["x1"]),1,1))
				gd2=np.gradient(Dataobj.quantities[quantity_name],Dataobj.grid["x1"],Dataobj.grid["x2"],Dataobj.grid["x3"])[1]/Dataobj.grid["x1"].reshape((len(Dataobj.grid["x1"]),1,1))
				gd3=np.gradient(Dataobj.quantities[quantity_name],Dataobj.grid["x1"],Dataobj.grid["x2"],Dataobj.grid["x3"])[2]
		else:
			gd1,gd2,gd3=np.gradient(Dataobj.quantities[quantity_name],Dataobj.grid["x1"],Dataobj.grid["x2"],Dataobj.grid["x3"])
		quantities["Divergence_"+quantity_name]=gd1+gd2+gd3
	Dataobj.update(quantities)
	return Dataobj

def result(quantity_name=None,anafname=None):
	if anafname=="Gradient":
		return ("Gradient_"+quantity_name+"_x1","Gradient_"+quantity_name+"_x2","Gradient_"+quantity_name+"_x3")
	elif anafname=="Divergence":
		return ("Divergence_"+quantity_name,)
	return ()

def integrate(fx,x): #inte@ f(x)dx
	if len(x)>0:
		result=integrate(fx,x[1:])
		if type(result) !=np.ndarray or result.ndim==0:
			result=np.full((len(x[0]),),result)
		return np.trapz(result,x=x[0])	
	return fx

def integrate_single(fx,x):
	if type(fx) !=np.ndarray or fx.ndim==0:
		fx=np.full((len(x),),fx)
	return np.trapz(fx,x)

def integrate_body(f,x,y=None,z=None):
	if type(f)!=np.ndarray or f.ndim<=1:
		if type(y)==None:
			y=np.arange(0,1,1/len(x))
		if type(z)==None:
			z=np.arange(0,1,1/len(x))
		return integrate_single(integrate(f,(y,z)),x)
	elif f.ndim==2:
		if type(y)==None:
			y=np.arange(0,1,1/len(f[0]))
		if type(z)==None:
			z=np.arange(0,1,1/len(f[0]))
		return integrate(integrate_single(f,z),(x,y))
	elif f.ndim==3:
		if type(y)==None:
			y=np.arange(0,1,1/len(f[0]))
		if type(z)==None:
			z=np.arange(0,1,1/len(f[0][0]))
		return integrate(f,(x,y,z))

def integrate_surface_xoy(f,x=None,y=None,default_step=10000):
	if type(f)!=np.ndarray or f.ndim<=1:
		if type(x)==None:
			x=np.arange(0,1,1/len(f))
		if type(y)==None:
			y=np.arange(0,1,1/default_step)
		return integrate(f,(x,y))
	elif f.ndim>=2:
		if type(x)==None:
			x=np.arange(0,1,1/len(f))
		if type(y)==None:
			y=np.arange(0,1,1/len(f[0]))
		return integrate(f,(x,y))

def integrate_sph_body(f,r,th=None,phi=None):
	if type(f) !=np.ndarray or f.ndim<=1:
		if type(th)==type(None):
			th=np.arange(0,np.pi,np.pi/len(r))
		if type(phi)==type(None):
			phi=np.arange(0,2*np.pi,2*np.pi/len(r))
		return integrate_single(f*r**2*integrate(np.sin(th),(th,phi)),r)
	elif f.ndim==2:#r th
		if type(th)==type(None):
			th=np.arange(0,np.pi,np.pi/len(f[0]))
		if type(phi)==type(None):
			phi=np.arange(0,2*np.pi,2*np.pi/len(r))
		return integrate(f*r.reshape((len(r),1))**2*np.sin(th.reshape((1,len(th))))*integrate_single(1,phi),(r,th))
	else: #r th phi
		if type(th)==type(None):
			th=np.arange(0,np.pi,np.pi/len(f[0]))
		if type(phi)==type(None):
			phi=np.arange(0,2*np.pi,2*np.pi/len(f[0][0]))
		return integrate(f*r.reshape((len(r),1,1))**2*np.sin(th.reshape((1,len(th),1))),(r,th,phi))

def integrate_sph_sur(f,r,th=None,phi=None,default_step=10000): #r is fixed
	if type(th)==type(None):
		if type(f) !=np.ndarray or f.ndim==0:
			th=np.arange(0,np.pi,np.pi/default_step)
		elif f.ndim==1:
			th=np.arange(0,np.pi,np.pi/len(f))
		elif f.ndim==2:
			th=np.arange(0,np.pi,np.pi/len(f[0]))
		elif f.ndim==3:
			th=np.arange(0,np.pi,np.pi/len(f[0][0]))
	if type(phi)==type(None):
		if type(f) !=np.ndarray or f.ndim==0:
			phi=np.arange(0,2*np.pi,2*np.pi/default_step)
		elif f.ndim==1:
			phi=np.arange(0,2*np.pi,2*np.pi/len(f))
		elif f.ndim==2:
			phi=np.arange(0,2*np.pi,2*np.pi/len(f[0]))
		elif f.ndim==3:
			phi=np.arange(0,2*np.pi,2*np.pi/len(f[0][0]))
	if type(f) !=np.ndarray or f.ndim<=1: #th
		return integrate_single(f*r**2*np.sin(th)*integrate_single(1,phi),th)
	elif f.ndim==2: #th phi
		return integrate(f*r**2*np.sin(th.reshape((1,len(th)))),(th,phi))
	elif f.ndim==3: #th phi
		return integrate(f*r**2*np.sin(th.reshape((1,len(th),1))),(th,phi))

def integrate_pol_body(f,r,phi=None,z=None):
	#f=f(x,th,z)
	if type(f) !=np.ndarray or f.ndim<=1: #r 
		if type(phi)==type(None):
			phi=np.arange(0,2*np.pi,2*np.pi/len(r))
		if type(z)==type(None):
			z=np.arange(0,1,1/len(r))
		return integrate_single(f*r*integrate(1,(phi,z)),r)
	elif f.ndim==2:#r phi
		if type(phi)==type(None):
			phi=np.arange(0,2*np.pi,2*np.pi/len(f[0]))
		if type(z)==type(None):
			z=np.arange(0,1,1/len(r))
		return integrate(f*r.reshape((len(r),1))*integrate_single(1,z),(r,phi))
	else: #x z th
		if type(phi)==type(None):
			phi=np.arange(0,2*np.pi,2*np.pi/len(f[0]))
		if type(z)==type(None):
			z=np.arange(0,1,1/len(f[0][0]))
		return integrate(f*r.reshape((len(r),1,1))*phi.reshape((1,len(phi),1)),(r,phi,z))


def integrate_pol_sur_xoz(f,x,z,phi=None,default_step=10000): #x is fixed
	if type(phi)==type(None):
		if type(f) !=np.ndarray or f.ndim==0:
			phi=np.arange(0,np.pi,2*np.pi/default_step)
		elif f.ndim==1:
			phi=np.arange(0,np.pi,2*np.pi/len(f))
		elif f.ndim==2:
			phi=np.arange(0,np.pi,2*np.pi/len(f[0]))
		elif f.ndim==3:
			phi=np.arange(0,np.pi,2*np.pi/len(f[0][0]))
	if type(f) !=np.ndarray or f.ndim<=1: #z
		return integrate_single(f*x*integrate_single(1,phi),z)
	elif f.ndim==2: #z th
		return integrate(f*x*phi.reshape((1,len(phi))),(phi,z))
	elif f.ndim==3: #z th
		return integrate(f*x*phi.reshape((1,len(phi),1)),(phi,z))


def integrate_pol_sur_xop(f,x,z,phi=None,default_step=10000): #z is fixed
	if type(phi)==type(None):
		if type(f) !=np.ndarray or f.ndim==0:
			phi=np.arange(0,np.pi,2*np.pi/default_step)
		elif f.ndim==1:
			phi=np.arange(0,np.pi,2*np.pi/len(f))
		elif f.ndim==2:
			phi=np.arange(0,np.pi,2*np.pi/len(f[0]))
		elif f.ndim==3:
			phi=np.arange(0,np.pi,2*np.pi/len(f[0][0]))
	if type(f) !=np.ndarray or f.ndim<=1: #x
		return integrate_single(f*x*integrate_single(1,phi),x)
	elif f.ndim==2: #x th
		return integrate(f*x.reshape((len(x),1))*phi.reshape((1,len(phi))),(x,phi))
	elif f.ndim==3: #x th
		return integrate(f*x.reshape((len(x),1,1))*phi.reshape((1,len(phi),1)),(x,phi))

if __name__=="__main__":
	print("Testing Model:",__file__)
	from TestData import TestData
	TestData=gradient(TestData,"rho")
	print("Testing Result:", TestData.quantities["Gradient_rho_x1"], TestData.quantities["Gradient_rho_x2"]) #update 
	TestData=divergence(TestData,"rho")
	print("Testing Result:", TestData.quantities["Divergence_rho"]) #update
	''' 
	from matplotlib import pyplot as plt
	plt.figure("imshow",facecolor="lightgray")
	plt.imshow(TestData.quantities["Divergence_rho"],cmap="RdBu",extent=[TestData.grid["x1"][0],TestData.grid["x1"][-1],TestData.grid["x2"][0],TestData.grid["x2"][-1]])
	plt.colorbar()
	plt.xticks(TestData.grid["x1"])
	plt.yticks(TestData.grid["x2"])
	plt.show()
	'''
	r=np.arange(0,10,0.01)
	print(integrate_sph_body(1,r))