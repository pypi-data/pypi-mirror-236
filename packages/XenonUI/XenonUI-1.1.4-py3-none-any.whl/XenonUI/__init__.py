from tkinter import *
import threading,time,os
from XenonUI.XUIlib.imgtool import add_image
from XenonUI.XUIlib.ImageLibConfig import Image_XUI as info_image, img_encode as img_encode

#XUI V1.1
#Junxiang H. 2023.03.07

class VerticalScrolledFrame(Frame):
	"""A pure Tkinter scrollable frame that actually works!
	* Use the 'interior' attribute to place widgets inside the scrollable frame.
	* Construct and pack/place/grid normally.
	* This frame only allows vertical scrolling.
	"""
	def __init__(self, parent,width,height,scrollwidth,image=None, *args, **kw):
		Frame.__init__(self, parent, *args, **kw)
 
		# Create a canvas object and a vertical scrollbar for scrolling it.
		vscrollbar = Scrollbar(self,width=scrollwidth, orient=VERTICAL)
		vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
		hocrollbar = Scrollbar(self,width=scrollwidth, orient=HORIZONTAL)
		hocrollbar.pack(fill=X, side=BOTTOM, expand=FALSE)
		if image!=None:
			canvas = Canvas(self, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set,xscrollcommand=hocrollbar.set,width=width,height=height,image=image)
		else:
			canvas = Canvas(self, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set,xscrollcommand=hocrollbar.set,width=width,height=height) #这里设定canvas的大小是frame内界面的大小，如果frame内定义的子项的大小超过了canvas的大小，则滚动条生效
		canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
		#canvas.place(x=0,y=0,anchor="nw")
		vscrollbar.config(command=canvas.yview)
		hocrollbar.config(command=canvas.xview)
 
		# Reset the view
		canvas.xview_moveto(0)
		canvas.yview_moveto(0)
 
		# Create a frame inside the canvas which will be scrolled with it.
		self.interior = interior = Frame(canvas)
		self.interior_id = canvas.create_window(0, 0, window=interior,anchor=NW)

		# Track changes to the canvas and frame width and sync them,
		# also updating the scrollbar.
		def _configure_interior(event):
			# Update the scrollbars to match the size of the inner frame.
			size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
			canvas.config(scrollregion="0 0 %s %s" % size)
		interior.bind('<Configure>', _configure_interior)
		def _configure_canvas(event):
			if interior.winfo_reqwidth() != canvas.winfo_width():
				# Update the inner frame's width to fill the canvas.
				#canvas.itemconfigure(self.interior_id, width=canvas.winfo_width())
				self.interior.config(width=canvas.winfo_width())
			if interior.winfo_reqheight() != canvas.winfo_height():
				# Update the inner frame's width to fill the canvas.
				#canvas.itemconfigure(self.interior_id, height=canvas.winfo_height())
				self.interior.config(height=canvas.winfo_height())
		canvas.bind('<Configure>', _configure_canvas)
		self.canvas=canvas
class auto_frame:
	frame_list=[]
	margin={
		"left":10,
		"right":10,
		"top":10,
		"bottom":10
	}
	scrollwidth=20
	def get_margin(self,key,margin={}):
		try:
			return margin[key]
		except:
			try:
				return self.margin[key]
			except:
				return None
	def __init__(self,frame,width,height,margin={},scrollwidth=None):
		self.ori_frame=frame
		if scrollwidth!=None:
			self.scrollwidth=scrollwidth
		self.width=width-self.get_margin("left",margin)-self.get_margin("right",margin)
		self.height=height-self.get_margin("top",margin)-self.get_margin("bottom",margin)
		self.useframe=Frame(self.ori_frame,width=self.width-self.scrollwidth,height=self.height-self.scrollwidth)
		self.useframe.place(x=self.get_margin("left",margin),y=self.get_margin("top",margin),anchor="nw")
		self.frame=VerticalScrolledFrame(self.useframe,width=self.width-self.scrollwidth,height=self.height-self.scrollwidth,scrollwidth=self.scrollwidth)
		self.frame.pack()
	def add_item(self,width,height):
		self.frame_list.append(Frame(self.frame.interior,bd=0,width=width,height=height))
	def add_item_x(self,width):
		self.add_item(width=width,height=self.height-self.scrollwidth)
		self.frame_list[-1].pack(side=LEFT)
		return self.frame_list[-1]
	def add_item_y(self,height,anchor="nw",side=None):
		self.add_item(width=self.width-self.scrollwidth,height=height)
		if side==None:
			self.frame_list[-1].pack(anchor=anchor)
		else:
			self.frame_list[-1].pack(side=side)
		return self.frame_list[-1]
class XUI:
	default_args={
		#window
		"windows_width":1440,
		"windows_height":900,
		"windows_title":"XUI v1.1",
		"windows_bg":"#fcffc8",

		#mainwin
		"mainwin_x":20,
		"mainwin_y":20,
		"mainwin_width":1400,
		"mainwin_height":860,
		"mainwin_bg":"#fcffc8",#"#fcffc8",

		#first menu bar (fmb)
		"fmb_x":0,
		"fmb_y":0,
		"fmb_width":1400,
		"fmb_height":160,
		"fmb_bg":"#dae1e3",#"#dae1e3",
		"fmb_bd":20,

		#Second menu bar (smb)
		"smb_x":0,
		"smb_y":160,
		"smb_width":300,
		"smb_height":700,
		"smb_bg":"#a9ecfd",#"#a9ecfd",
		"smb_bh":35,

		#info (info)
		"info_x":1100,
		"info_y":660,
		"info_width":300,
		"info_height":200,
		"info_bg":"#51f9bc",#"#51f9bc",
		"info_image":info_image,

		#Result output (ro)
		"ro_x":300,
		"ro_y":160,
		"ro_width":800,
		"ro_height":500,
		"ro_bg":"#fcffc8",#"#fcffc8",

		#IO (io)
		"io_x":300,
		"io_y":660,
		"io_width":800,
		"io_height":200,
		"io_bg":"#000000",#"#000000",
		"io_max_length":100,
		"io_item_height":30,

		#cpu (cpu)
		"cpu_x":1100,
		"cpu_y":160,
		"cpu_width":300,
		"cpu_height":500,
		"cpu_bg":"#ffb1f5",#"#ffb1f5",

		#item_padding (ip)
		"ip_left":10,
		"ip_right":10,
		"ip_top":10,
		"ip_bottom":10
	}
	current_fmb=None
	current_fmb2=None
	current_smb=None
	def get_pars(self,key,args={}):
		try:
			return args[key]
		except:
			try:
				return self.default_args[key]
			except:
				return None
	def __init__(self):
		img_encode()
		self.window=Tk()
		self.message=[]
		self.message_color=[]
		self.io_state=True
		threading.Thread(target=self.io_add).start()
	def build_frame(self,father_frame,key_x,key_y,key_width,key_height,key_bg,args={},anchor="nw",af=True):
		try:
			f=Frame(father_frame.canvas,bg=self.get_pars(key_bg,args),width=self.get_pars(key_width,args),height=self.get_pars(key_height,args))
		except:
			f=Frame(father_frame,bg=self.get_pars(key_bg,args),width=self.get_pars(key_width,args),height=self.get_pars(key_height,args))
		f.place(x=self.get_pars(key_x,args),y=self.get_pars(key_y,args),anchor=anchor)
		if af:
			return auto_frame(f,self.get_pars(key_width,args),self.get_pars(key_height,args))
		return f
	def build(self,**args):
		#tk window
		self.window.geometry(str(self.get_pars("windows_width",args))+"x"+str(self.get_pars("windows_height",args)))
		self.window.config(bg=self.get_pars("windows_bg",args))
		self.window.title(self.get_pars("windows_title",args))

		#main
		self.mainwin=self.build_frame(self.window,"mainwin_x","mainwin_y","mainwin_width","mainwin_height","mainwin_bg",args,af=False)

		#First menu bar
		self.fmb=self.build_frame(self.mainwin,"fmb_x","fmb_y","fmb_width","fmb_height","fmb_bg",args)
		self.fmb_item=[]

		#Second menu bar
		self.smb=self.build_frame(self.mainwin,"smb_x","smb_y","smb_width","smb_height","smb_bg",args)
		self.smb_item=[]

		#Third menu bar
		self.info=self.build_frame(self.mainwin,"info_x","info_y","info_width","info_height","info_bg",args)
		add_image(self.add_item(self.info,height=self.info.height-self.info.scrollwidth)[1],self.default_args["info_image"],width=self.info.width-self.info.scrollwidth,height=self.info.height-self.info.scrollwidth)

		#ro
		self.ro=self.build_frame(self.mainwin,"ro_x","ro_y","ro_width","ro_height","ro_bg",args)
		self.ro_item=[]
		#self.ro

		#io
		self.io=self.build_frame(self.mainwin,"io_x","io_y","io_width","io_height","io_bg",args)
		self.io_item=[]
		self.io_item_info=[]
		for i in range(self.get_pars("io_max_length",args)):
			self.io_item.append(self.add_item(self.io,height=self.get_pars("io_item_height",args),padding={"pl":0,"pt":0,"pb":0,"pr":0}))
			self.io_item_info.append(Label(self.io_item[-1][1]))
			self.io_item_info[-1].pack(anchor="nw")
			self.io_item[-1][0].pack_forget() #anchor="nw"
		self.io_oriwidth_dif=self.io_item[0][0].winfo_reqwidth()-self.io_item[0][1].winfo_reqwidth()
		self.io_open=0
		self.io_all=False

		#cpu
		self.cpu=self.build_frame(self.mainwin,"cpu_x","cpu_y","cpu_width","cpu_height","cpu_bg",args)
	def open_smb(self,event,fmb_index):
		if self.current_fmb!=None:
			for i in self.smb_item[self.current_fmb]:
				i[0].pack_forget()
		self.current_fmb=fmb_index
		reqw=0
		for i in self.smb_item[fmb_index]:
			i[0].pack(anchor="nw")
		self.smb.frame.canvas.yview_moveto(0)
	def open_ro(self,event,fmb_index,smb_index):
		if self.current_fmb2!=None and self.current_smb!=None:
			for i in self.ro_item[self.current_fmb2][self.current_smb]:
				i[0].pack_forget()
		self.current_fmb2=fmb_index
		self.current_smb=smb_index
		for i in self.ro_item[fmb_index][smb_index]:
			i[0].pack(anchor="n")
		self.ro.frame.canvas.yview_moveto(0)
	def add_first_menu(self,**args):
		self.fmb_item.append(self.add_item(self.fmb,width=self.get_pars("fmb_height",args)-self.get_pars("fmb_bd",args)))
		self.fmb_item[-1][1].config(cursor="hand2")
		self.smb_item.append([])
		self.ro_item.append([])
		fmb_index=len(self.fmb_item)-1
		self.fmb_item[fmb_index][1].bind("<Button-1>",lambda x:self.open_smb(x,fmb_index))
		return fmb_index

	def add_second_menu(self,fmb_index,**args):
		self.smb_item[fmb_index].append(self.add_item(self.smb,height=self.get_pars("smb_bh",args)))
		self.smb_item[fmb_index][-1][1].config(cursor="hand2")
		self.ro_item[fmb_index].append([])
		smb_index=len(self.smb_item[fmb_index])-1
		self.smb_item[fmb_index][smb_index][0].pack_forget()
		self.smb_item[fmb_index][smb_index][1].bind("<Button-1>",lambda x:self.open_ro(x,fmb_index,smb_index))
		return smb_index
	def add_ro(self,fmb_index,smb_index,height=None):
		self.ro_item[fmb_index][smb_index].append(self.add_item(self.ro,height=height,anchor="n"))
		ro_index=len(self.ro_item[fmb_index][smb_index])-1
		self.ro_item[fmb_index][smb_index][ro_index][0].pack_forget()
		return ro_index
	def add_item(self,frame,width="undef",height="undef",padding={},anchor="nw",side=None):
		pt=self.get_pars("ip_top",padding)
		pr=self.get_pars("ip_right",padding)
		pb=self.get_pars("ip_bottom",padding)
		pl=self.get_pars("ip_left",padding)
		srcbox=None
		box=None
		if width=="undef" and height!="undef":
			if height!=None:
				height+=2
			srcbox=frame.add_item_y(height,anchor=anchor,side=side)
			if height==None:
				box=Frame(srcbox,bd=0,width=frame.width-pr-pl-frame.scrollwidth)
			elif height-pt-pb>0:
				box=Frame(srcbox,bd=0,width=frame.width-pr-pl-frame.scrollwidth,height=height-pt-pb)
			else:
				box=Frame(srcbox,bd=0,width=frame.width-pr-pl-frame.scrollwidth,height=0)
		elif width!="undef" and height=="undef":
			if width!=None:
				width+=2
			srcbox=frame.add_item_x(width)
			if width==None:
				box=Frame(srcbox,bd=0,height=frame.height-pt-pb-frame.scrollwidth)
			elif width-pl-pr>0:
				box=Frame(srcbox,bd=0,height=frame.height-pt-pb-frame.scrollwidth,width=width-pl-pr)
			else:
				box=Frame(srcbox,bd=0,height=frame.height-pt-pb-frame.scrollwidth,width=0)
		if srcbox!=None and box!=None:
			box.place(x=pl,y=pt,anchor="nw")
			return (srcbox,box)
		return None
	def show(self):
		self.window.mainloop()
	def io_add(self):
		while self.io_state:
			try:
				if len(self.message)>0:
					message=self.message[0]
					color=self.message_color[0]
					self.message=self.message[1:]
					self.message_color=self.message_color[1:]
					self.io_item[self.io_open][0].pack_forget()
					self.io_item[self.io_open][0].pack(anchor="nw")
					text=""
					for i in message:
						text+=str(i)+" "
					if text!="":
						text=text[:-1]
					self.io_item_info[self.io_open].config(text=text,fg=color)
					reqw=self.io_item_info[self.io_open].winfo_reqwidth()
					self.io_item[self.io_open][1].config(width=reqw)
					self.io_item[self.io_open][0].config(width=reqw+self.io_oriwidth_dif)
					self.io_open+=1
					if self.io_open==len(self.io_item):
						self.io_open=0
						self.io_all=True
					self.io.frame.canvas.yview_moveto(1)
				time.sleep(0.1)
			except:
				break
	def io_recv(self,*message,color="black"):
		self.message.append(message)
		self.message_color.append(color)
if __name__=="__main__":
	CollectPages()
	#show()