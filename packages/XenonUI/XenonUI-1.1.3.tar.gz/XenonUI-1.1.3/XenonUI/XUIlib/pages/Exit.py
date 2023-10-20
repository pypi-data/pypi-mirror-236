#Exit.py
import os
from XenonUI.XUIlib.imgtool import add_image
from XenonUI.XUIlib.page import *
from tkinter import messagebox
class page(page):
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
		add_image(self.tkobj.fmb_item[self.fmbindex][1],Image_E,width=self.tkobj.fmb.height-self.tkobj.fmb.scrollwidth-self.tkobj.get_pars("fmb_bd"),height=self.tkobj.fmb.height-self.tkobj.fmb.scrollwidth-self.tkobj.get_pars("fmb_bd"),event="<Button-1>",fun=fun)