#File type: extension <Function> set
#By Junxiang H., 2023/06/30
#wacmk.com/cn Tech. Supp.

import os,re
#return Filesdir/Filename.type
def GetFiles(filedir=os.getcwd(),filetype=""):
	result=()
	'''
	for root, dirs,files in os.walk(filedir,topdown=False):
		for file in files:
			if file.endswith(filetype):
				result+=(os.path.join(root,file),)
	'''
	for file in os.listdir(filedir):
		if file.endswith(filetype):
			result+=(os.path.join(filedir,file),)
	result = tuple(sorted(result, key=lambda x: (int(re.sub('\D', '', x)), x)))
	return result

if __name__=="__main__":
	print("Testing Model:",__file__)
	print("Testing Function:", GetFiles)
	print("Testing Result:", GetFiles(filetype="py"))