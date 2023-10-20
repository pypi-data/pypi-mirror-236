# Xenon-UI (XUI)

XUI is a page management GUI framework for python that is based on the platform-independent GUI package tinker.

Author Junxiang H.
If you have any questions and suggestions
Please contact: huangjunxiang@mail.ynu.edu.cn

Latest version: 1.1
date 2023-07-11

# Install

Please enter the following code on the command line to install

```shell
pip3 install XenonUI
```

# Create a page

XUI is based on **page** management. The page is the basic unit of XUI, and here we will create a page "pageA" and place it into the folder **pages**.

**You must download libraries of XUI and release in upper folder of** ***pages*** 

Download Link see https://github.com/wacmkxiaoyi/Xenon-UI

And each page has many **menus**, and all information will be concentrated in each **menu**.

```python
#pageA
import os
from XenonUI.XUIlib.imgtool import add_image
from XenonUI.XUIlib.page import *
logo=os.path.join("XenonUI","XUIlib","image","A.png") #select a logo you like
from tkinter import *

class page(page):
	img={
		"logo":logo
	}
	def menu1(self):	
		self.menu1=self.add_menu("menu1") #set menu

		#add a title, can be call repeatedly
		self.add_title(self.menu1,"Title of Menu 1")
		#other arguments of add_title:
		#bg: color of title, default "blue"
		#fontsize: size of title, default 18
		#height: title height, default 50

		#add a row object
		row=self.add_row(self.menu1)
		#other arguments of add_row:
		#bx: boundary x, (like margin_left/right in HTML), default 50
		#height: height of row

		#dosomething like using the tinker, with father object row
		#e.g. a label
		Label(row,text="this is a label").pack(side="left")
		#an input box
		Entry(row).pack(side="left")
		#a button
		Button(row).pack(side="left")
		#.....

	def menu2(self):
		menu2=self.add_menu("menu2") #set menu2
		self.add_title(menu2,"Title of Menu 2")
		#do something as your wish
	def initial(self): # this function builds up this page
		self.set_image(self.img["logo"])
		self.menu1()
		self.menu2()
	def show(self): #Default page
		#This function means that as soon as you open XUI, the contents of this directory will be displayed
		#you have to define default menu with the attribute of <class page>, such as self.menu1
		self.tkobj.open_smb(None,self.fmbindex)
		self.tkobj.open_ro(None,self.fmbindex,self.menu1)
```

# Readable Page

XUI has two readable pages: **Help** and **Exit**. You can directly copy the following code and save it as **Help.py** and **Exit.py**

```python
#Help.py
import os
from XenonUI.XUIlib.imgtool import add_image
from XenonUI.XUIlib.page import *
logo=os.path.join("XenonUI","XUIlib","image","H.png")
main_logo=os.path.join("XenonUI","XUIlib","image","XUI.png")

from tkinter import *
class page(page):
	img={
		"main_logo":main_logo,
		"logo":logo
	}
	def page_default(self):	
		self.default_page_smbindex=self.add_menu("XUI v1.1")
		self.default_page_roindex=self.add_item(self.default_page_smbindex,self.ro_height)
		add_image(self.tkobj.ro_item[self.fmbindex][self.default_page_smbindex][self.default_page_roindex][1],self.img["main_logo"],width=self.ro_width,height=self.ro_height)
	def page_Document(self):
		intro=self.add_menu("Readme")
		self.add_row(intro,50)
		self.add_title(intro,"Document of XUI please see:",fg="red")
		self.add_title(intro,"https://www.github/wacmkxiaoyi/Xenon-UI",fontsize=10)
	def page_author_information(self):
		aui=self.add_menu("Author information")
		self.add_row(aui,50)
		self.add_title(aui,"Junxiang H.",fg="black")
		self.add_title(aui,"huangjunxiang@mail.ynu.edu.cn",fontsize=10)
	def initial(self):
		self.set_image(self.img["logo"])
		self.page_default()
		self.page_author_information()
		self.page_Document()
	def show(self):
		self.tkobj.open_smb(None,self.fmbindex)
		self.tkobj.open_ro(None,self.fmbindex,self.default_page_smbindex)
```

```python
#Exit.py
import os
from XenonUI.XUIlib.imgtool import add_image
from XenonUI.XUIlib.page import *
logo=os.path.join("XenonUI","XUIlib","image","E.png")
from tkinter import messagebox
class page(page):
	img={
		"logo":logo,
	}
	def initial(self):
		def fun(event):
			stt=""
			if "windows_title" in self.pageargs.keys():
				stt=" "+self.pageargs["windows_title"]
			if messagebox.askokcancel(title="Warnning",message="Exit"+stt+" ?"):
				#stop siobj.thread
				try:
					self.pageargs["XUIOBJ"].systeminfo.run=False
					self.tkobj.io_state=False
				except:
					pass
				self.tkobj.window.quit()
		add_image(self.tkobj.fmb_item[self.fmbindex][1],self.img["logo"],width=self.tkobj.fmb.height-self.tkobj.fmb.scrollwidth-self.tkobj.get_pars("fmb_bd"),height=self.tkobj.fmb.height-self.tkobj.fmb.scrollwidth-self.tkobj.get_pars("fmb_bd"),event="<Button-1>",fun=fun)
```

# Show pages

You can use the code (save as a new python script) below to call XUI and show the pages you create

```python
#Example.py
import os
try:
	from Config import Pages #those folders/packages path modified by yourself
except:
	pass
from XenonUI import XUI
from XenonUI.XUIlib.SystemInfo import SystemInfo
config_file="Config.py"  
pages_import="pages" #aa.bb.cc.pages 


def CollectPages():
	pages_dir=os.path.join(*pages_import.split("."))
	import datetime
	pages_except=("__init__","page_model")
	def FileNamePreProcess(filename):
		filedir,filename=os.path.split(filename)
		fileindex,filetype=os.path.splitext(filename)
		return (fileindex.split(".")[-1],filedir,filetype.split(".")[1])
	def GetFiles(filedir=os.getcwd(),filetype=""):
		result=()
		for file in os.listdir(filedir):
			if file.endswith(filetype):
				result+=(os.path.join(filedir,file),)
		return result
	strc="#File type: extension <class page> set\n#By Junxiang H., 2023/07/9\n#wacmk.com/cn Tech. Supp.\n\n#This script updates automaticly! Do not Modify!\n#Update time:"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"\n\nPages={}\n"
	for i in tuple(set([FileNamePreProcess(i)[0] for i in GetFiles(pages_dir,"py")])-set(pages_except)):
		strc+="import "+pages_import+"."+i+" as "+i+"\n"+"Pages[\""+i+"\"]="+i+"\n"
	file=open(config_file,"w")
	file.writelines(strc)
	file.close()
def build(**args):
	class XUIOBJ:
		def __init__(self,**args):
			args.update({"XUIOBJ":self})
			self.guiobj=XUI()
			self.guiobj.build(**args)
			#systeminfo
			self.systeminfo=SystemInfo(self.guiobj)
			self.systeminfo.lunch(1)
			self.Pages={}
			for i in reversed(Pages.keys()):
				if i not in ("Exit","Help"):
					self.Pages[i]=Pages[i].page(self.guiobj,**args)
			if "Help" in Pages.keys():
				self.Pages["Help"]=Pages["Help"].page(self.guiobj,**args)
			if "Exit" in Pages.keys():
				self.Pages["Exit"]=Pages["Exit"].page(self.guiobj,**args)
			self.iofun=self.guiobj.io_recv
	return XUIOBJ(**args)
if __name__=="__main__":
	show=os.path.exists(config_file)
	CollectPages()
	if show:
		xui=build() #you can set some arguments in here as you need
		xui.guiobj.show()
	else:
		print("XUI configurates completed, please rerun script again")
```




