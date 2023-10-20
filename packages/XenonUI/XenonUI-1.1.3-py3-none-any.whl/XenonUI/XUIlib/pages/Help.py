#Help.py
import os
from XenonUI.XUIlib.imgtool import add_image
from XenonUI.XUIlib.page import *
from tkinter import *
class page(page):
	def page_default(self):	
		self.default_page_smbindex=self.add_menu("XUI v1.1")
		self.default_page_roindex=self.add_item(self.default_page_smbindex,self.ro_height)
		add_image(self.tkobj.ro_item[self.fmbindex][self.default_page_smbindex][self.default_page_roindex][1],Image_XUI,width=self.ro_width,height=self.ro_height)
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
		self.set_image(Image_H)
		self.page_default()
		self.page_author_information()
		self.page_Document()
	def show(self):
		self.tkobj.open_smb(None,self.fmbindex)
		self.tkobj.open_ro(None,self.fmbindex,self.default_page_smbindex)