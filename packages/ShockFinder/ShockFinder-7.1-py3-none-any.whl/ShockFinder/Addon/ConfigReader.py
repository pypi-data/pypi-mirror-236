#File type: <Function> set
#By Junxiang H., 2023/07/4
#wacmk.com/cn Tech. Supp.

def str_clean(strc):
	if strc[-1]=="\n":
		strc=strc[:-1]
	result=""
	while len(strc)>1 and strc[0]==" ":
		strc=strc[1:]
	for i in ("#","//"):
		strc=strc.split(i)[0] 
	stat=False
	for i in strc:
		if i==" ":
			if not stat:
				stat=True
				result+=i
		else:
			stat=False
			result+=i
	return result if result!="" else None
def retype_string(string):
	if "." in string or "e" in string:
		try:
			string=float(string)
		except:
			if string=="None":
				string=None
			elif string=="True":
				string=True
			elif string=="False":
				string=False
	else:
		try:
			string=int(string)
		except:
			pass
	return string if type(string) !=str or len(string.split(","))==1 else [retype_string(i) for i in string.split(",")]

def get_config(config_file):
	file=open(config_file,"r")
	commands={}
	for line in file.readlines():
		result=str_clean(line)
		if result!=None:
			if len(result.split("@"))>=2:#type2
				#type 1:
				#key=values
				#type 2: key as command
				#command@key1=value1@key2=value2@...
				tt=result.split("@")
				key=tt[0]
				subcommands={}
				for subcmd in tt[1:]:
					if subcmd!="":
						subkey,value=subcmd.split("=")
						subcommands[subkey]=retype_string(value)
				commands[key]=subcommands
			else:#type1
				if len(result.split("="))==2:
					key,value=result.split("=")
					commands[key]=retype_string(value)
				else:
					print("Unknow configuration:",result)
	file.close()
	return commands