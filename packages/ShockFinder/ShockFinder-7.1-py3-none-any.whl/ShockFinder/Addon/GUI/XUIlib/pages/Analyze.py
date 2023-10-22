#This is a model file for XUI page
#Junxiang H. 2023.07.09
import os,copy
from XenonUI.XUIlib.imgtool import add_image
from XenonUI.XUIlib.page import *
import ShockFinder.Addon.Time as Time
from tkinter import *
from tkinter import ttk,filedialog
from multiprocessing import cpu_count
class page(page):
	img={
		"logo":Image_A
	}
	pars={}
	parmax=50
	def get(self):
		pass
	def GS_MPE(self):
		MPE=self.add_menu("Multi-process",submenu=1)
		self.pars["MultiprocessEngine"]={}
		#Multiprocessing
		self.add_row(MPE) #skip row (empty row)
		self.add_title(MPE,"Multi-process")
		Label(self.add_row(MPE,bx=150),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(MPE,bx=150)
		Label(box,text="Engine",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		egs=list(self.pageargs["Infobj"].Config["MultiprocessEngine"].keys())+[None]
		MPE_ENG=ttk.Combobox(box,width=18,height=len(egs) if len(egs)<=10 else 10,values=egs)
		if self.pageargs["Infobj"].Default_MPE in self.pageargs["Infobj"].Config["MultiprocessEngine"]:
			MPE_ENG.set(self.pageargs["Infobj"].Default_MPE)
		else:
			MPE_ENG.set(str(egs[0]))
		MPE_ENG.pack(side="left")
		Label(box,text="| ").pack(side="left")
		def fun_mpeeng(event):
			self.pars["MultiprocessEngine"]["Engine"]=MPE_ENG.get()
			self.tkobj.io_recv("Updated MultiprocessEngine-Engine to",self.pars["MultiprocessEngine"]["Engine"])
		self.pars["MultiprocessEngine"]["Engine"]=MPE_ENG.get()
		button_mpeeng=Button(box,text="Update",width=5)
		button_mpeeng.bind("<ButtonRelease>",fun_mpeeng)
		button_mpeeng.pack(side="left")
		Label(self.add_row(MPE,bx=150),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(MPE,bx=150)
		Label(box,text="Cores Num",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		MPE_PNUM=Entry(box,width=20)
		MPE_PNUM.insert(0,cpu_count() if cpu_count()<=4 and cpu_count()>1 else 4 if cpu_count()>4 else 1)
		MPE_PNUM.pack(side="left")
		Label(box,text="| ").pack(side="left")
		def fun_MPE_PNUM(event):
			self.pars["MultiprocessEngine"]["pnum"]=int(MPE_PNUM.get())
			self.tkobj.io_recv("Updated MultiprocessEngine-pnum to",self.pars["MultiprocessEngine"]["pnum"])
		self.pars["MultiprocessEngine"]["pnum"]=int(MPE_PNUM.get())
		button_MPE_PNUM=Button(box,text="Update",width=5)
		button_MPE_PNUM.bind("<ButtonRelease>",fun_MPE_PNUM)
		button_MPE_PNUM.pack(side="left")
		Label(self.add_row(MPE,bx=150),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(MPE,bx=150)
		Label(box,text="Use log",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		do_with_log=ttk.Combobox(box,width=18,height=2,values=[True,False])
		do_with_log.set(str(True))
		do_with_log.pack(side="left")
		Label(box,text="| ").pack(side="left")
		def fun_button_do_with_log(event):
			self.pars["MultiprocessEngine"]["do_with_log"]=True if do_with_log.get()=="True" else False
			self.tkobj.io_recv("Updated MultiprocessEngine-do_with_log to",self.pars["MultiprocessEngine"]["do_with_log"])
		self.pars["MultiprocessEngine"]["do_with_log"]=True if do_with_log.get()=="True" else False
		button_do_with_log=Button(box,text="Update",width=5)
		button_do_with_log.bind("<ButtonRelease>",fun_button_do_with_log)
		button_do_with_log.pack(side="left")
		Label(self.add_row(MPE,bx=150),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(MPE,bx=150)
		Label(box,text="Log file",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		logfile=Entry(box,width=15)
		logfile.insert(0,str(None))
		logfile.pack(side="left")
		def fun_logfile(event):
			folder_path=filedialog.asksaveasfilename()
			if folder_path!="":
				logfile.delete(0,"end")
				logfile.insert(0,folder_path)
		button=Button(box,text="Select",width=5)
		button.bind("<ButtonRelease>",fun_logfile)
		button.pack(side="left")
		Label(box,text="| ").pack(side="left")
		def fun_logfile(event):
			if logfile.get()!="":
				self.pars["MultiprocessEngine"]["logfile"]=None if logfile.get()=="None" else logfile.get()
				self.tkobj.io_recv("Updated MultiprocessEngine-logfile to",self.pars["MultiprocessEngine"]["logfile"])
		self.pars["MultiprocessEngine"]["logfile"]=None if logfile.get()=="None" else logfile.get()
		button_logfile=Button(box,text="Update",width=5)
		button_logfile.bind("<ButtonRelease>",fun_logfile)
		button_logfile.pack(side="left")
		Label(self.add_row(MPE,bx=150),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(MPE,bx=150)
		Label(box,text="Show MPE info",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		show_version_info=ttk.Combobox(box,width=18,height=2,values=[True,False])
		show_version_info.set(str(True))
		show_version_info.pack(side="left")
		Label(box,text="| ").pack(side="left")
		def fun_show_version_info(event): 
			self.pars["MultiprocessEngine"]["show_version_info"]=True if show_version_info.get()=="True" else False
			self.tkobj.io_recv("Updated MultiprocessEngine-show_version_info to",self.pars["MultiprocessEngine"]["show_version_info"])
		button_show_version_info=Button(box,text="Update",width=5)
		button_show_version_info.bind("<ButtonRelease>",fun_show_version_info)
		button_show_version_info.pack(side="left")
		self.pars["MultiprocessEngine"]["show_version_info"]=True if show_version_info.get()=="True" else False
		Label(self.add_row(MPE,bx=150),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(MPE,bx=150)
		Label(box,text="Show log in screen",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		print_in_screen=ttk.Combobox(box,width=18,height=2,values=[True,False])
		print_in_screen.set(str(True))
		print_in_screen.pack(side="left")
		Label(box,text="| ").pack(side="left")
		def fun_sprint_in_screen(event): 
			self.pars["MultiprocessEngine"]["print_in_screen"]=True if print_in_screen.get()=="True" else False
			self.tkobj.io_recv("Updated MultiprocessEngine-print_in_screen to",self.pars["MultiprocessEngine"]["print_in_screen"])
		self.pars["MultiprocessEngine"]["print_in_screen"]=True if print_in_screen.get()=="True" else False
		button_print_in_screen=Button(box,text="Update",width=5)
		button_print_in_screen.bind("<ButtonRelease>",fun_sprint_in_screen)
		button_print_in_screen.pack(side="left")
		Label(self.add_row(MPE,bx=150),text="="*500).place(x=0,y=0,anchor="nw") #end
	def GS_IO(self):
		#Loader
		IO=self.add_menu("Database Storage",submenu=1)
		self.pars["IO"]={}
		self.add_row(IO) #skip row (empty row)
		self.add_title(IO,"After-Analysis Data Storage")
		Label(self.add_row(IO,bx=150),text="="*500).place(x=0,y=0,anchor="nw") #begin
		box=self.add_row(IO,bx=150)
		Label(box,text="Engine",width=20).pack(side="left")
		Label(box,text="|").pack(side="left")
		IO_ENG=ttk.Combobox(box,width=18,height=5,values=list(self.pageargs["Infobj"].Config["IO"].keys()))
		if self.pageargs["Infobj"].Default_IO in self.pageargs["Infobj"].Config["IO"]:
			IO_ENG.set(self.pageargs["Infobj"].Default_IO)
		else:
			IO_ENG.set(list(self.pageargs["Infobj"].Config["IO"].keys())[0])
		IO_ENG.pack(side="left")
		Label(box,text="| ").pack(side="left")
		def fun_Loader_ENG(event):
			self.pars["IO"]["Engine"]=IO_ENG.get()
			self.tkobj.io_recv("Updated IO-Engine to",self.pars["IO"]["Engine"])
		button_IO_ENG=Button(box,text="Update",width=5)
		button_IO_ENG.bind("<ButtonRelease>",fun_Loader_ENG)
		button_IO_ENG.pack(side="left")
		self.pars["IO"]["Engine"]=IO_ENG.get()
		Label(self.add_row(IO,bx=150),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(IO,bx=150)
		Label(box,text="Project name",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		filename=Entry(box,width=15)
		filename.pack(side="left")
		def fun_lfd(event):
			folder_path=filedialog.asksaveasfilename()
			if folder_path!="":
				filename.delete(0,"end")
				filename.insert(0,folder_path)
		button=Button(box,text="Select",width=5)
		button.bind("<ButtonRelease>",fun_lfd)
		button.pack(side="left")
		Label(box,text="| ").pack(side="left")
		def fun_filename(event):
			if filename.get()!="":
				self.pars["IO"]["filename"]=filename.get()
				self.tkobj.io_recv("Updated IO-filename to",self.pars["IO"]["filename"])
			else:
				if "filename" in self.pars["IO"].keys():
					del(self.pars["IO"])
		button_filename=Button(box,text="Update",width=5)
		button_filename.bind("<ButtonRelease>",fun_filename)
		button_filename.pack(side="left")
		if filename.get()!="":
			self.pars["IO"]["filename"]=filename.get()
		Label(self.add_row(IO,bx=150),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(IO,bx=150)
		Label(box,text="Drop Buffer",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		DropBuffer=ttk.Combobox(box,width=18,height=2,values=[True,False])
		DropBuffer.set(str(True))
		DropBuffer.pack(side="left")
		Label(box,text="| ").pack(side="left")
		def fun_DropBuffer(event): 
			self.pars["IO"]["DropBuffer"]=True if DropBuffer.get()=="True" else False
			self.tkobj.io_recv("Updated IO-DropBuffer to",self.pars["IO"]["DropBuffer"])
		self.pars["IO"]["DropBuffer"]=True if DropBuffer.get()=="True" else False
		button_DropBuffer=Button(box,text="Update",width=5)
		button_DropBuffer.bind("<ButtonRelease>",fun_DropBuffer)
		button_DropBuffer.pack(side="left")
		Label(self.add_row(IO,bx=150),text="="*500).place(x=0,y=0,anchor="nw") #end
	def GS_Loader(self):
		#Loader
		Loader=self.add_menu("Simulation Data Loader",submenu=1)
		self.pars["Loader"]={}
		self.add_row(Loader) #skip row (empty row)
		self.add_title(Loader,"Simulation Data Loader")
		Label(self.add_row(Loader,bx=150),text="="*500).place(x=0,y=0,anchor="nw") #begin
		box=self.add_row(Loader,bx=150)
		Label(box,text="Type",width=20).pack(side="left")
		Label(box,text="|").pack(side="left")
		Loader_ENG=ttk.Combobox(box,width=18,height=5,values=list(self.pageargs["Infobj"].Config["Loader"].keys()))
		Loader_ENG.set(list(self.pageargs["Infobj"].Config["Loader"].keys())[0])
		Loader_ENG.pack(side="left")
		Label(box,text="| ").pack(side="left")
		def fun_Loader_ENG(event):
			self.pars["Loader"]["Engine"]=Loader_ENG.get()
			self.tkobj.io_recv("Updated Loader-Engine to",self.pars["Loader"]["Engine"])
		button_fun_Loader_ENG=Button(box,text="Update",width=5)
		button_fun_Loader_ENG.bind("<ButtonRelease>",fun_Loader_ENG)
		button_fun_Loader_ENG.pack(side="left")
		self.pars["Loader"]["Engine"]=Loader_ENG.get()
		Label(self.add_row(Loader,bx=150),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(Loader,bx=150)
		Label(box,text="File Dir",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		Loader_FileDir=Entry(box,width=15)
		Loader_FileDir.insert(0,os.getcwd())
		Loader_FileDir.pack(side="left")
		def fun_lfd(event):
			folder_path=filedialog.askdirectory()
			if folder_path!="":
				Loader_FileDir.delete(0,"end")
				Loader_FileDir.insert(0,folder_path)
		button=Button(box,text="Select",width=5)
		button.bind("<ButtonRelease>",fun_lfd)
		button.pack(side="left")
		Label(box,text="| ").pack(side="left")
		def fun_Loader_FileDir(event):
			self.pars["Loader"]["FileDir"]=Loader_FileDir.get()
			self.tkobj.io_recv("Updated Loader-FileDir to",self.pars["Loader"]["FileDir"])
		button_Loader_FileDir=Button(box,text="Update",width=5)
		button_Loader_FileDir.bind("<ButtonRelease>",fun_Loader_FileDir)
		button_Loader_FileDir.pack(side="left")
		self.pars["Loader"]["FileDir"]=Loader_FileDir.get()
		Label(self.add_row(Loader,bx=150),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(Loader,bx=150)
		Label(box,text="File type",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		Loader_Filetype=Entry(box,width=20)
		Loader_Filetype.insert(0,"dbl")
		Loader_Filetype.pack(side="left")
		Label(box,text="| ").pack(side="left")
		def fun_Loader_Filetype(event):
			self.pars["Loader"]["Filetype"]=Loader_Filetype.get()
			self.tkobj.io_recv("Updated Loader-Filetype to",self.pars["Loader"]["Filetype"])
		button_Loader_Filetype=Button(box,text="Update",width=5)
		button_Loader_Filetype.bind("<ButtonRelease>",fun_Loader_Filetype)
		button_Loader_Filetype.pack(side="left")
		self.pars["Loader"]["FileType"]=Loader_Filetype.get()
		Label(self.add_row(Loader,bx=150),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(Loader,bx=150)
		Label(box,text="Interval",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		Loader_InterVal=Entry(box,width=20)
		Loader_InterVal.insert(0,1)
		Loader_InterVal.pack(side="left")
		Label(box,text="| ").pack(side="left")
		def fun_Loader_InterVal(event):
			self.pars["Loader"]["Interval"]=int(Loader_InterVal.get())
			self.tkobj.io_recv("Updated Loader-Interval to",self.pars["Loader"]["Interval"])
		button_Loader_InterVal=Button(box,text="Update",width=5)
		button_Loader_InterVal.bind("<ButtonRelease>",fun_Loader_InterVal)
		button_Loader_InterVal.pack(side="left")
		self.pars["Loader"]["Interval"]=int(Loader_InterVal.get())
		Label(self.add_row(Loader,bx=150),text="="*500).place(x=0,y=0,anchor="nw") #end
	def A_Parameters(self):
		#Parameters
		Parameters=self.add_menu("Parameters",submenu=1)
		self.pars["Update"]={}
		self.add_row(Parameters) #skip row (empty row)
		self.add_title(Parameters,"Parameters")
		Label(self.add_row(Parameters,bx=190),text="="*500).place(x=0,y=0,anchor="nw") #begin
		box=self.add_row(Parameters,bx=190)
		Label(box,text="Parameter Name",width=20,fg="green").pack(side="left")
		Label(box,text="| ").pack(side="left")
		Label(box,text="Parameter Value",width=20,fg="green").pack(side="left")
		Label(box,text="| ").pack(side="left")
		Label(box,text="Opera",width=5,fg="green").pack(side="left")
		keys=set(self.pageargs["Infobj"].testdb.data[0].quantities.keys())-set(("vx1","vx2","vx3","SimTime","geometry","rho","prs","Bx1","Bx2","Bx3","output","logfile"))
		def fun(box,entry1,entry2,button,value=None):
			def fun_del(event):
				try:
					del(self.pars["Update"][entry1.get()])
					self.tkobj.io_recv("Delete parameter",entry1.get())
				except:
					self.tkobj.io_recv("Warning: parameter",entry1.get(),"dosen't exist!!!",color="blue")
				entry1.config(state="normal")
				entry2.config(state="normal")
				button.config(text="Save")
				button.bind("<ButtonRelease>",fun_cre)
			def fun_cre(event):
				sttr=str_clean(entry1.get())
				entry1.delete(0,"end")
				entry1.insert(0,sttr)
				sttr=str_clean(entry2.get())
				entry2.delete(0,"end")
				entry2.insert(0,sttr)
				if entry1.get()!="":
					try:
						self.pars["Update"][entry1.get()]=float(entry2.get())
					except:
						self.pars["Update"][entry1.get()]=entry2.get()
					self.tkobj.io_recv("Add parameter",entry1.get(),"to",self.pars["Update"][entry1.get()])
					entry1.config(state="readonly")
					entry2.config(state="readonly")
					button.config(text="Modify")
					button.bind("<ButtonRelease>",fun_del)
			if entry1.get()!="":# normal
				if value!=None:
					entry2.insert(0,str(value))
				else:
					try:
						entry2.insert(0,str(self.pageargs["Infobj"].testdb.data[0].quantities[entry1.get()]))
					except Exception as err:
						print(err)
				try:
					self.pars["Update"][entry1.get()]=float(entry2.get())
				except:
					self.pars["Update"][entry1.get()]=entry2.get()
				entry1.config(state="readonly")
				entry2.config(state="readonly")
				button.config(text="Modify")
				button.bind("<ButtonRelease>",fun_del)
			else:
				button.config(text="Save")
				button.bind("<ButtonRelease>",fun_cre)
		
		for i in range(self.parmax):
			Label(self.add_row(Parameters,bx=190),text="-"*500).place(x=0,y=0,anchor="nw") #next
			box=self.add_row(Parameters,bx=190)
			entry1=Entry(box,width=20)
			if i < len(keys):
				entry1.insert(0,list(keys)[i])
			entry1.pack(side="left")
			Label(box,text="| ").pack(side="left")
			entry2=Entry(box,width=20)
			entry2.pack(side="left")
			Label(box,text="| ").pack(side="left")
			button=Button(box,width=5)
			button.pack(side="left")
			fun(box,entry1,entry2,button)
		Label(self.add_row(Parameters,bx=190),text="="*500).place(x=0,y=0,anchor="nw") #end
	def A_Quantities(self):
		Quantities=self.add_menu("Quantities",submenu=1)
		self.add_row(Quantities) #skip row (empty row)
		self.add_title(Quantities,"Quantities")
		Label(self.add_row(Quantities,bx=20),text="="*500).place(x=0,y=0,anchor="nw") #begin
		box=self.add_row(Quantities,bx=20)
		Label(box,text="Approach",width=20,fg="green").pack(side="left")
		Label(box,text="| ").pack(side="left")
		Label(box,text="Target Quantity",width=20,fg="green").pack(side="left")
		Label(box,text="| ").pack(side="left")
		Label(box,text="Saved Result",width=20,fg="green").pack(side="left")
		Label(box,text="| ").pack(side="left")
		Label(box,text="Arguments",width=20,fg="green").pack(side="left")
		Label(box,text="| ").pack(side="left")
		Label(box,text="Opera",width=5,fg="green").pack(side="left")
		operationlist=list(self.pageargs["Infobj"].Config["AnalysisTool"].keys())+["Gradient","Divergence","Harmonic","Mean","Radial"]
		def get_result(qtname,qto):
			result=""
			try:
				result=self.pageargs["Infobj"].Config["AnalysisTool"][qto].result(qtname,qto)
				if len(result)==1:
					result=result[0]
				else:
					result=str(result)
			except:
				if qto in ("Gradient","Divergence"):
					result=self.pageargs["Infobj"].Config["AnalysisLib"]["Differential"].result(qtname,qto)
					if len(result)==1:
						result=result[0]
					else:
						result=str(result)
				elif qto=="Harmonic":
					result=self.pageargs["Infobj"].Config["AnalysisLib"]["Harmonic_src"].result(qtname,qto)
					if len(result)==1:
						result=result[0]
					else:
						result=str(result)
				elif qto=="Mean":
					result=self.pageargs["Infobj"].Config["AnalysisLib"]["Mean_src"].result(qtname,qto)
					if len(result)==1:
						result=result[0]
					else:
						result=str(result)
				elif qto=="Radial":
					result=self.pageargs["Infobj"].Config["AnalysisLib"]["Radial_src"].result(qtname,qto)
					if len(result)==1:
						result=result[0]
					else:
						result=str(result)
			return strc_vva(result)
		def strc_vva(result):
			return result.replace("(","").replace(")","").replace("[","").replace("]","").replace("\'","").replace("\"","")
		def fun(box,cmbox1,entry2,entry3,entry4,button5,button6):
			def fun_set(event):
				entry3.delete(0,"end")
				ss=""
				for i in [get_result(i,cmbox1.get()) for i in entry2.get().split(",")]:
					ss+=i.replace(" ","")+","
				if ss!="":
					ss=ss[:-1]
				entry3.insert(0,ss)
			def fun_cre(event):
				sttr=str_clean(entry2.get())
				entry2.delete(0,"end")
				entry2.insert(0,sttr)
				sttr=str_clean(entry4.get())
				entry4.delete(0,"end")
				entry4.insert(0,sttr)
				sttr=str_clean(entry3.get())
				entry3.delete(0,"end")
				entry3.insert(0,sttr)
				sttr=str_clean(entry4.get())
				entry4.delete(0,"end")
				entry4.insert(0,sttr)
				if cmbox1.get()!="":
					self.pars[cmbox1.get()]={}
					if strc_vva(entry2.get())!="":
						self.pars[cmbox1.get()]["quantity_name"]=strc_vva(entry2.get())
					if strc_vva(entry3.get())!="":
						self.pars[cmbox1.get()]["result"]=strc_vva(entry3.get())
					for i in entry4.get().split("@"):
						if i!="" and len(i.split("="))==2:
							qu,qv=i.split("=")
							self.pars[cmbox1.get()][qu]=qv.replace(" ","")
					self.tkobj.io_recv("Add approach",cmbox1.get(),"@",self.pars[cmbox1.get()])
					cmbox1.config(state="disable")
					entry2.config(state="readonly")
					entry3.config(state="readonly")
					entry4.config(state="readonly")
					button6.config(text="Modify")
					button6.bind("<ButtonRelease>",fun_del)
			def fun_del(event):
				try:
					del(self.pars[cmbox1.get()])
					self.tkobj.io_recv("Delete approach",cmbox1.get())
				except:
					self.tkobj.io_recv("Warning: approach",cmbox1.get(),"dosen't exist!!!",color="blue")
				cmbox1.config(state="normal")
				entry2.config(state="normal")
				entry3.config(state="normal")
				entry4.config(state="normal")
				button6.config(text="Save")
				button6.bind("<ButtonRelease>",fun_cre)
			button5.bind("<ButtonRelease>",fun_set)
			button6.bind("<ButtonRelease>",fun_cre)
		for i in range(self.parmax):
			Label(self.add_row(Quantities,bx=20),text="-"*500).place(x=0,y=0,anchor="nw") #next
			box=self.add_row(Quantities,bx=20)
			cmbox1=ttk.Combobox(box,width=18,height=len(operationlist) if len(operationlist)<=10 else 10,values=operationlist)
			cmbox1.pack(side="left")
			Label(box,text="| ").pack(side="left")
			entry2=Entry(box,width=20)
			entry2.pack(side="left")
			Label(box,text="| ").pack(side="left")
			entry3=Entry(box,width=14)
			entry3.pack(side="left")
			button5=Button(box,text="Get",width=5)
			button5.pack(side="left")
			Label(box,text="| ").pack(side="left")
			entry4=Entry(box,width=20)
			entry4.pack(side="left")
			Label(box,text="| ").pack(side="left")
			button6=Button(box,text="Save",width=5)
			button6.pack(side="left")
			fun(box,cmbox1,entry2,entry3,entry4,button5,button6)
		Label(self.add_row(Quantities,bx=20),text="="*500).place(x=0,y=0,anchor="nw") #end
	def save(self):
		save=self.add_menu("Save Configuration")
		self.add_row(save) #skip row (empty row)
		self.add_title(save,"Save Configuration")
		box=self.add_row(save,bx=300)
		def Test(event):
			self.tkobj.io_recv("Get Parameters:")
			for i in self.pars.keys():
				self.tkobj.io_recv(i,":",self.pars[i])
			self.tkobj.io_recv(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
			self.pageargs["Infobj"].testdb.update(**self.pars["Update"])
			self.tkobj.io_recv("Ready for testing..............")
			ext_tools=("Harmonic","Mean","Gradient","Divergence","Radial")
			for i in self.pars.keys():
				if i in self.pageargs["Infobj"].Config["AnalysisTool"].keys():
					anaf=self.pageargs["Infobj"].Config["AnalysisTool"][i].get
				elif i in ext_tools:
					anaf=self.pageargs["Infobj"].Config["AnalysisLib"][i]
				else:
					continue
				pas=copy.deepcopy(self.pars[i])
				pas.update({"info":i})
				for j in pas.keys():
					pas[j]=retype_string(pas[j])

				#if "quantity_name" in pas.keys():
				#	pas["quantity_name"]=pas["quantity_name"].split(",")
				self.pageargs["Infobj"].testdb.analysis_data(anaf,**pas)
				if "result" in pas.keys():
					self.pageargs["Infobj"].testdb.check_quantities(pas["result"])
			self.tkobj.io_recv("Operation completed",color="green")
		button=Button(box,text="Test",width=5)
		button.pack(side="left")
		button.bind("<ButtonRelease>",Test)
		def Save(event):
			file=filedialog.asksaveasfile()
			if file!=None:
				self.tkobj.io_recv("Collecting Parameters:")
				for i in self.pars.keys():
					self.tkobj.io_recv(i,":",self.pars[i])
				self.tkobj.io_recv("Saving to file @",file)
				strc="#ShockFinder Analyzing Configurations\n"
				try:
					strc+="#Built at "+Time.now()+"\n"
				except:
					pass
				strc+="#Wacmk.cn/com\n"
				strc+="#https://www.github.com/wacmkxiaoyi/shockfinder\n\n"
				#write MPE
				for key in ("MultiprocessEngine","IO","Loader","Update"):#maintain sequency
					if key in self.pars.keys():
						strc+=key
						for i in self.pars[key].keys():
							strc+="@"+i+"="+str(self.pars[key][i])
						strc+="\n"
				for i in self.pars.keys():
					if i not in ("MultiprocessEngine","IO","Loader","Update"):
						strc+=i
						for j in self.pars[i].keys():
							strc+="@"+j+"="+str(self.pars[i][j])
						strc+="\n"
				file.writelines(strc)
				file.close()
				self.tkobj.io_recv("Operation completed",color="green")
		Label(box,width=10).pack(side="left")
		button=Button(box,text="Save",width=5)
		button.pack(side="left")
		button.bind("<ButtonRelease>",Save)
	def initial(self):
		self.save()
		self.set_image(self.img["logo"])
		self.add_useless_menu("Global Settings↓")
		self.GS_MPE()
		self.GS_IO()
		self.GS_Loader()
		self.add_useless_menu("Analysis↓")
		self.A_Parameters()
		self.A_Quantities()