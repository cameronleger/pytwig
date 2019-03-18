#this is where the graphical node editor happens

import tkinter as tk
import random
import math
import copy
from pytwig import bw_file, bw_device
from tkinter import ttk
from tkinter import filedialog
import os

DEBUG = False

MED_FONT = ("Verdana", 9)
BOL_FONT = ("Verdana bold", 9)
THK_FONT = ("Arial bold", 14)
CODEFONT = ("Consolas", 8)
DOT_SIZE = 5
PORT_OFF = 15
TOTAL_OFF = 25
LINE_WID = 3
LINE_COL = "#fd811a"
H_MULT = 3
V_MULT = 1
UI_H_MULT = 5
UI_V_MULT = UI_H_MULT
BORDER = 8
NODECOL = "#eee"
BASECOL = "#414141"
ACCCOL1 = "#535353"
ACCCOL2 = "#888"
ACCCOL3 = "#3dd9ff"
INSP_WIDTH = 50

#TODO add ui editor
#TODO add node name tooltip viewer

class Application(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		try:
			tk.Tk.iconbitmap(self, default="bwEdit.ico")
		except:
			try:
				tk.Tk.iconbitmap(self, default="@bwEdit.xbm")
			except:
				pass
		tk.Tk.wm_title(self, "bwEdit")

		# === Menu Configuration ===
		top = self.winfo_toplevel()
		self.menuBar = tk.Menu(top)
		top['menu'] = self.menuBar
		self.subMenu = tk.Menu(self.menuBar, tearoff=0) #file
		self.menuBar.add_cascade(label='File', menu=self.subMenu)
		self.subMenu.add_command(label='Save As', command=self.savefile)
		self.subMenu.add_command(label='Load', command=self.openfile)
		self.subMenu.add_command(label='Export to JSON', command=self.exportfile)
		self.subMenu.add_separator()
		self.subMenu.add_command(label='Exit',)
		self.subMenu = tk.Menu(self.menuBar, tearoff=0) #help
		self.menuBar.add_cascade(label='Help', menu=self.subMenu)
		self.subMenu.add_command(label='About',)

		self.file = ''
		container = tk.Frame(self)
		container.pack(side = "top", fill = "both", expand = True)
		container.grid_rowconfigure(0,weight = 1)
		container.grid_columnconfigure(0,weight = 1)
		self.frames = {}
		for f in (MainPage,):
			frame = f(container, self)
			self.frames[f] = frame
			frame.grid(row=0, column=0, sticky="nsew")
		self.show_frame(MainPage)

	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

	def openfile(self):
		filename = tk.filedialog.askopenfilename(filetypes = (("All Files", "*.*"),
															("Bitwig Devices", "*.bwdevice"),
															("Bitwig Modulators", "*.bwmodulator"),
															("Bitwig Presets", "*.bwpreset"),
															))
		f = ''
		print ('-'+filename)
		tk.Tk.wm_title(self, filename)
		self.frames[MainPage].editor.load(filename)

	def savefile(self):
		with tk.filedialog.asksaveasfile(mode='wb', defaultextension=".bw", filetypes = (("", ""), #TODO automatically find filetype
																				("Bitwig Devices", "*.bwdevice"),
																				("Bitwig Modulators", "*.bwmodulator"),
																				("Bitwig Presets", "*.bwpreset"),
																				)) as f:
			if f is None: #in case of cancel
				return
			self.frames[MainPage].editor.data.write(output)

	def exportfile(self): #same as save except it serializes the json instead of encoding it
		self.frames[MainPage].editor.treeifyData()
		with tk.filedialog.asksaveasfile(mode='wb', defaultextension=".bw") as f:
			if f is None: #in case of cancel
				return
			f.write(self.frames[MainPage].editor.data.serialize())

class MainPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.editor = NodeEditorCanvas(self)
		self.editor.pack(fill="both", expand=True)

class NodeEditorCanvas(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)

		# === Canvas initialization ===
		self.canvas = tk.Canvas(self, bg = "#2e2e2e")
		self.canvas.config(width=1500, height=1000)
		# Scrollbars
		self.hbar=tk.Scrollbar(self,orient='horizontal')
		self.hbar.pack(side='bottom',fill='x')
		self.hbar.config(command=self.canvas.xview)
		self.vbar=tk.Scrollbar(self,orient='vertical')
		self.vbar.pack(side='right',fill='y')
		self.vbar.config(command=self.canvas.yview)
		self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
		# Putting canvas in page
		self.canvas.pack(side = 'top', fill="both", expand=True)
		self.update()
		self.canvas.config(scrollregion=self.canvas.bbox("all"))

		#self.canvas.create_oval(0,0,10,10, activeoutline = "black" , outline=NODECOL, fill=NODECOL ,tags=("poop"))

		self._drag_data = {"relPos": {}, "item": None}
		#self._new_conn_data = {"start": 0, "end": 0, "type0": '', "type1": '', "port0": '', "port1": ''}
		self._new_conn_data = {}
		self._currentlyConnecting = False
		self._dragged = False
		self._inspector_active = False
		self._input_active = False
		self._manager_active = False
		self._browser_active = False
		self._rclicked = None
		self._selected = []
		self._browser_clicked = None
		self._currentlyConnecting = False

		self.num_atoms = 0

		#click and button bindings
		'''self.canvas.tag_bind("case||name||deco", "<ButtonPress-1>", self._on_atom_press)
		self.canvas.tag_bind("case||name||deco", "<ButtonRelease-1>", self._on_atom_release)
		self.canvas.tag_bind("case||name||deco", "<B1-Motion>", self._on_atom_motion)
		self.canvas.tag_bind("case||name||deco", "<ButtonPress-3>", self.on_atom_rc_press)
		self.canvas.tag_bind("case||name||deco", "<ButtonRelease-3>", self.on_atom_rc_release)'''
		self.canvas.tag_bind("delete", "<ButtonPress-1>", self._on_del_press)
		self.canvas.tag_bind("delete", "<ButtonRelease-1>", self._on_del_release)
		self.canvas.tag_bind("refresh", "<ButtonPress-1>", self._on_refresh_press)
		self.canvas.tag_bind("refresh", "<ButtonRelease-1>", self._on_refresh_release)
		self.canvas.tag_bind("exportnitro", "<ButtonPress-1>", self._on_export_nitro_press)
		self.canvas.tag_bind("exportnitro", "<ButtonRelease-1>", self._on_export_nitro_release)
		self.canvas.tag_bind("inspector", "<ButtonPress-1>", self.on_inspector_click)
		self.canvas.tag_bind("port", "<ButtonPress-1>", self.on_port_press)
		self.canvas.tag_bind("conn", "<ButtonPress-1>", self.on_conn_press)
		self.canvas.bind("<Motion>", self.on_move)
		self.canvas.bind("<ButtonPress-1>", self.on_click)
		self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
		self.canvas.bind_all("<Double-Button-1>", self._on_2c_press)
		self.canvas.bind_all("<ButtonPress-2>", self._on_mc_press)
		self.canvas.bind_all("<B2-Motion>", self._on_mc_motion)
		self.canvas.bind_all("<Return>", self._on_enter)

	def load(self, file):
		self.canvas.delete("all")
		self._currentlyConnecting = False

		# TODO: check input file extension, maybe check contents of file?

		self.data = bw_file.BW_Device()
		self.data.read(file)

		#draw atoms and connections and panels
		for item in self.data.get_atoms():
			self.drawKids(item)
		self.drawConnections()
		#self._draw_panel(self.paneList[0], xOff = 3*UI_V_MULT, yOff = 3*UI_H_MULT)

		# Fits scroll region to new node map
		self.update()
		bounds = self.canvas.bbox("all")
		p = 600
		bounds = (bounds[0]-p,bounds[1]-p,bounds[2]+p,bounds[3]+p,)
		self.canvas.config(scrollregion=bounds)


	#scroll and zoom

	def _on_mousewheel(self, event):#TODO implement zoom instead of scroll
		self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

	def _on_mc_press(self, event):
		self.canvas.scan_mark(event.x, event.y)
	def _on_mc_motion(self, event):
		self.canvas.scan_dragto(event.x, event.y, gain=1)


	#clicking/dragging atoms and connections
	def _on_atom_press(self, event):
		x,y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
		self._drag_data["item"] = self.canvas.gettags(self.canvas.find_withtag("current"))[1] #id is tags[1]
		self._dragged = False
		for item in self.canvas.find_withtag(self._drag_data["item"]):
			c = self.canvas.coords(item)
			output = []
			xySelect = True
			for i in c:
				output.append(i-(x if xySelect else y))
				xySelect = not xySelect
			self._drag_data["relPos"][item] = output

	def _on_atom_motion(self, event):
		self._dragged = True
		eX,eY = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
		xOff, yOff = eX-event.x, eY-event.y
		idNum = int(self._drag_data["item"][2:])
		rPos = self._drag_data["relPos"][self.canvas.find_withtag(self._drag_data["item"]+"&&case")[0]]
		w = rPos[2]-rPos[0]
		h = rPos[3]-rPos[1]
		x = min(max(0+xOff,eX+rPos[0]), self.canvas.winfo_width()-w+xOff)
		y = min(max(0+yOff,eY+rPos[1]), self.canvas.winfo_height()-h+yOff)
		if len(self.portList) > idNum:
			for i in range(len(self.portList[idNum])): #redraw incoming connections
				inport = self.portList[idNum][i]
				if inport != None:
					name = str(idNum) + ':' + str(i) + ',' + str(inport[0]) + ':' + str(inport[1])
					#print("i", name)
					current = self.canvas.coords(name)
					dist = min(abs(current[0] - current[6])/4,75) #for curvature
					newC = (x, y + PORT_OFF*(i)+TOTAL_OFF)
					self.canvas.coords(name, current[0], current[1], current[0]+dist, current[1], newC[0]-dist, newC[1], newC[0], newC[1])
		if len(self.RortList) > idNum:
			for o in range(len(self.RortList[idNum])): #redraw outgoing connections
				outportList = self.RortList[idNum][o]
				if outportList:
					for outport in outportList:
						if outport != None:
							name = str(outport[0]) + ':' + str(outport[1]) + ',' + str(idNum) + ':' + str(o)
							#print("o", name)
							current = self.canvas.coords(name)
							dist = min(abs(current[0] - current[6])/4,75) #for curvature
							newC = (x + w, y + PORT_OFF*(o)+TOTAL_OFF)
							self.canvas.coords(name, newC[0], newC[1], newC[0]+dist, newC[1], current[6]-dist, current[7], current[6], current[7])
		for item in self.canvas.find_withtag(self._drag_data["item"]): #redraw cell
			tag = self.canvas.gettags(item)[2]
			localr = self._drag_data["relPos"][item]
			newC = []
			xySelect = True
			for i in localr:
				newC.append((x-rPos[0] if xySelect else y-rPos[1])+i)
				xySelect = not xySelect
			self.canvas.coords(item, *newC)

	def _on_atom_release(self, event):
		if self._dragged:
			#add layer correction (atoms with a smaller y position should be on a lower canvas layer)
			rPos = self._drag_data["relPos"][self.canvas.find_withtag(self._drag_data["item"]+"&&case")[0]]
			idNum = int(self._drag_data["item"][2:])
			atomX, atomY = self.canvas.canvasx(event.x)+rPos[0], self.canvas.canvasy(event.y)+rPos[1]
			self.atomList[self.atomList[self.atomList[idNum].fields["settings(6194)"].id].fields["desktop_settings(612)"].id].fields["y(18)"] = int(atomX/H_MULT)
			self.atomList[self.atomList[self.atomList[idNum].fields["settings(6194)"].id].fields["desktop_settings(612)"].id].fields["x(17)"] = int(atomY/V_MULT)
		else:
			id = int(self._drag_data["item"][2:])
			self._draw_inspector(self.atomList[id], event.x, event.y)
			#print("clicked")
		self._drag_data["item"] = None
		self._drag_data["x"] = 0
		self._drag_data["y"] = 0

	def on_conn_press(self, event): #deletes the connection that is currently being clicked on
		x,y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
		tags = self.canvas.gettags(self.canvas.find_withtag("current"))
		if "conn" in tags:
			#delete drawn connection
			lineIndex = tags[1]
			self.canvas.delete(tags[1])

			#delete from port list
			connData = [int(x) for x in lineIndex.replace(':',',').split(',')]
			self.delConn(*connData)
			self.atomList[self.atomList[self.atomList[connData[0]].fields["settings(6194)"].id].fields["inport_connections(614)"][connData[1]].id].fields["source_component(248)"] = None
			self.atomList[self.atomList[self.atomList[connData[0]].fields["settings(6194)"].id].fields["inport_connections(614)"][connData[1]].id].fields["outport_index(249)"] = 0

	def on_port_press(self, event): #begins or completes a connection TODO simplify this a little
		x,y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
		if self._currentlyConnecting:
			end = self.canvas.find_closest(x, y)
			drainTags = self.canvas.gettags(*end)
			if 'port' in drainTags:
				#set variables
				typeE = drainTags[4]
				portE = drainTags[5]

				#check to ensure ports go from in to out
				if self._new_conn_data['typeS'] == typeE:
					return

				#set all my source and drain variables
				sID, dID = int(self.canvas.gettags(*self._new_conn_data['start'])[1][2:]), int(drainTags[1][2:])
				sPort, dPort = int(self._new_conn_data['portS']), int(portE)
				sPos, dPos = self.canvas.coords(self._new_conn_data['start']), self.canvas.coords(end)
				if self._new_conn_data['typeS'] == 'in':
					sID, dID = dID, sID
					sPort, dPort = dPort, sPort
					sPos, dPos = dPos, sPos

				if len(self.portList) > dID:
					if len(self.portList[dID]) > dPort:
						if self.portList[dID][dPort]: #check to make sure only one in connection per port
							return

				#draw new connection
				self.canvas.delete("connecting")
				sX, sY, dX, dY = (sPos[0] + sPos[2]) / 2, (sPos[1] + sPos[3]) / 2,   (dPos[0] + dPos[2]) / 2, (dPos[1] + dPos[3]) / 2
				dist = min(abs(sX - dX)/4,75) #for curvature
				name = str(dID) + ':' + str(dPort) + ',' + str(sID) + ':' + str(sPort)
				self.canvas.tag_lower(self.canvas.create_line(sX, sY, sX+dist, sY, dX-dist, dY, dX, dY,
												activefill = "white", width = LINE_WID, fill = LINE_COL, smooth=True, tags=('grapheditor', name, "conn")))

				self.addConn(dID,dPort,sID,sPort)

				while len(self.atomList[self.atomList[dID].fields["settings(6194)"].id].fields["inport_connections(614)"]) < dPort+1: #add empty inport connections
					self.atomList[self.atomList[dID].fields["settings(6194)"].id].fields["inport_connections(614)"].append(atoms.Reference(self.addAtom('float_core.inport_connection(105)')))
				self.atomList[self.atomList[self.atomList[dID].fields["settings(6194)"].id].fields["inport_connections(614)"][dPort].id].fields["source_component(248)"] = atoms.Reference(sID)
				self.atomList[self.atomList[self.atomList[dID].fields["settings(6194)"].id].fields["inport_connections(614)"][dPort].id].fields["outport_index(249)"] = sPort
				self._currentlyConnecting = False
		else:
			self._new_conn_data['start'] = self.canvas.find_closest(x, y)
			tags = self.canvas.gettags(*self._new_conn_data['start'])
			if tags[3] == 'port':
				#set variables
				self._new_conn_data['typeS'] = tags[4]
				self._new_conn_data['portS'] = tags[5]

				#find coords
				c = self.canvas.coords(self._new_conn_data['start'])
				nX, nY = (c[0] + c[2]) / 2, (c[1] + c[3]) / 2
				mX, mY = x, y
				if self._new_conn_data['typeS'] == 'in':
					nX, nY, mX, mY = mX, mY, nX, nY

				#draw pending connection
				dist = min(abs(nX - mX)/4,75) #for curvature
				self.canvas.tag_lower(self.canvas.create_line(nX, nY, nX+dist, nY, mX-dist, mY, mX, mY,
												width=LINE_WID, fill='white', smooth=True, tags=('grapheditor', 'connecting')))

				self._currentlyConnecting = True

	def on_move(self, event): #redraws pending connection
		x,y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
		if (self._currentlyConnecting):
			#find coords
			c = self.canvas.coords(self._new_conn_data['start'])
			nX, nY = (c[0] + c[2]) / 2, (c[1] + c[3]) / 2
			mX, mY = x, y

			#move pending connection
			dist = min(abs(c[0] - mX)/4,75) #for curvature
			if self._new_conn_data['typeS'] == 'in':
				nX, nY, mX, mY = mX, mY, nX, nY
			self.canvas.coords("connecting", nX, nY, nX+dist, nY, mX-dist, mY, mX, mY)

	def on_click(self, event):
		x,y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
		clickedOn = self.canvas.find_withtag("current")
		if self._currentlyConnecting:
			tags = self.canvas.gettags(*clickedOn)
			if len(clickedOn) == 1 and "port" not in tags:
				self.canvas.delete("connecting")
				self._currentlyConnecting = False
		if clickedOn:
			return
		if self._inspector_active:
			self.canvas.delete("inspector")
			self.canvas.delete("input")
			self._inspector_active = False
		if self._manager_active:
			self.canvas.delete("manager")
			self._manager_active = False
		if self._browser_active:
			self.canvas.delete("browser")
			self._browser_active = False


	#menus TODO limit menu positions to inside of the window

	#inspector
	def _draw_inspector(self, obj, eX,eY, overwrite = True):
		clickedOn = self.canvas.find_withtag("current")
		currentTags = self.canvas.gettags(clickedOn)
		if overwrite:
			self.canvas.delete("inspector")
			self.listList = []
			self.listNum = 0
		self.canvas.delete("manager")
		self._manager_active = False
		self._inspector_active = True
		x,y = self.canvas.canvasx(eX), self.canvas.canvasy(eY)
		maxWidth = 5
		if "n_list" in currentTags:
			fieldOffset = 0
			iterate = range(len(obj))
			id = currentTags[4]
			inspWind = self.canvas.create_rectangle(x, y, x+10, y+10, outline=LINE_COL, fill=BASECOL, tags=("grapheditor","id"+str(id), "4pt", "inspwind", "inspector"))
		else:
			fieldOffset = 1
			name = obj.classname.split('.', maxsplit = 1)
			name = name[-1] + " id: " + str(obj.id)
			id = obj.id
			inspWind = self.canvas.create_rectangle(x, y, x+10, y+10, outline=LINE_COL, fill=BASECOL, tags=("grapheditor","id"+str(id), "4pt", "inspwind", "inspector"))
			canvasText = self.canvas.create_text(x+BORDER,y+BORDER+BOL_FONT[1],fill="white",font=BOL_FONT, text=name, anchor="w", tags=("grapheditor","id"+str(id), "2pt", "text", "inspector",))
			textBounds = self.canvas.bbox(canvasText)
			maxWidth = max(textBounds[2] - textBounds[0], maxWidth)
			iterate = obj.fields
		for fields in iterate: #TODO clean this up
			tags = ("grapheditor","id"+str(id), "2pt", "text",)
			if isinstance(obj, atoms.Atom):
				item = obj.fields[fields]
			else:
				item = obj[fields]
			if type(item) in (int, str, float, bool, None,):
				if fields == "code(6264)":
					text = "{" + str(fields) + "}"
				elif fields in enums.usesEnums:
					text = str(fields) + ": " + str(enums.usesEnums[fields][item])
				else:
					text = str(fields) + ": " + str(item)
				tags += ("variable", fields)
			elif type(item) in (atoms.Atom, atoms.Reference):
				text = "<" + str(fields) + ">"
				tags+=(item.id, "nestedInsp",)
			elif type(item) in (list,):
				text = "[" + str(fields) + "]"
				self.listList.append(item)
				tags+=(str(self.listNum), "nestedInsp", "n_list",)
				self.listNum+=1
			else:
				text = fields + ": invalid"
			tags+=("inspector",)
			text = self.canvas.create_text(x+BORDER,y+BORDER+MED_FONT[1]*2*fieldOffset+MED_FONT[1],fill="white",font=MED_FONT, text=text, anchor="w", tags=tags)
			textBounds = self.canvas.bbox(text)
			maxWidth = max(textBounds[2] - textBounds[0], maxWidth)
			fieldOffset += 1
		c = self.canvas.coords(inspWind)
		self.canvas.coords(inspWind, c[0], c[1], x+maxWidth+BORDER*2, y+fieldOffset*2*MED_FONT[1] + BORDER + MED_FONT[1])

	def on_inspector_click(self, event):
		clickedOn = self.canvas.find_withtag("current")
		tags = self.canvas.gettags(clickedOn)
		if "variable" in tags:
			x,y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
			id = int(tags[1][2:])
			field = tags[5]
			self._draw_modifier(id, x, y, field)
			self._input_active = True
		elif "nestedInsp" in tags:
			if "n_list" in tags:
				self._draw_inspector(self.listList[int(tags[4])], event.x, event.y, False)
			else:
				self._draw_inspector(self.atomList[int(tags[4])], event.x, event.y, False)

	def _draw_modifier(self, id, x, y, field,):
		self.canvas.delete("input")
		self._input = tk.Entry(self.canvas)
		self.canvas.create_window(x, y, window = self._input, anchor = "nw", tags = ("grapheditor","id"+str(id), "2pt", "input",))
		self._input_data = (id, field,)

	def _on_enter(self, event):
		print("enter")
		if self._input_active:
			#parse the input
			fieldNum = int(''.join([s for s in self._input_data[1] if s.isdigit()]))
			#print(fieldNum)
			type = typeLists.fieldList[fieldNum]
			if type == 1:
				if self._input.get().isdigit():
					self.atomList[self._input_data[0]].fields[self._input_data[1]] = int(self._input.get())
				elif self._input_data[1] in enums.usesEnums:
					if self._input.get() in enums.usesEnums[self._input_data[1]]:
						self.atomList[self._input_data[0]].fields[self._input_data[1]] = enums.usesEnums[self._input_data[1]].index(self._input.get())
			elif type == 5:
				if self._input.get().lower() in ('0','f','false'):
					self.atomList[self._input_data[0]].fields[self._input_data[1]] = False
				elif self._input.get().lower() in ('1','t','true'):
					self.atomList[self._input_data[0]].fields[self._input_data[1]] = True
			elif type == 6 or type == 7:
				self.atomList[self._input_data[0]].fields[self._input_data[1]] = float(self._input.get())
			elif type == 8:
				self.atomList[self._input_data[0]].fields[self._input_data[1]] = str(self._input.get())
			else:
				print("modification of this parameter is not yet permitted")
			self.canvas.delete("input")
			self._input_active = False
			#TODO redraw inspector?

	#rc menu
	def on_atom_rc_press(self, event):
		rclicked = self.canvas.find_withtag("current")
		self._rclicked = rclicked
		print(rclicked)

	def on_atom_rc_release(self, event):
		rclicked = self.canvas.find_withtag("current")
		if rclicked == self._rclicked:
			id = int(self.canvas.gettags(rclicked)[1][2:])
			self._draw_manager(self.atomList[id], event.x, event.y)
		self._rclicked = None
		print(rclicked)

	def _draw_manager(self, obj, eX,eY,):#probably unnecessary once hotkeys are in place
		clickedOn = self.canvas.find_withtag("current")
		currentTags = self.canvas.gettags(clickedOn)
		id = int(currentTags[1][2:])
		self.canvas.delete("manager")
		self.canvas.delete("inspector")
		self._manager_active = True
		self._inspector_active = True
		self._currently_managed = True
		x,y = self.canvas.canvasx(eX), self.canvas.canvasy(eY)
		manaWind = self.canvas.create_rectangle(x, y, x+10, y+10, outline=ACCCOL3, fill=BASECOL, tags=("grapheditor","id"+str(id), "4pt", "manawind", "manager")) #id might be problematic for lists
		maxWidth = 5
		fieldOffset = 0

		'''#add name
		name = obj.classname
		i = 0
		while i < len(name):
			if name[i] == '.':
				break
			i+=1
		else:
			i = -1;
		name = name[i+1:] + " id: " + str(obj.id)
		canvasText = self.canvas.create_text(x+BORDER,y+BORDER+BOL_FONT[1],fill="white",font=BOL_FONT, text=name, anchor="w",
															tags=("grapheditor","id"+str(id), "2pt", "text", "manager",))
		textBounds = self.canvas.bbox(canvasText)
		maxWidth = max(textBounds[2] - textBounds[0], maxWidth)'''

		#add delete
		if obj.classname != "float_core.proxy_in_port_component(154)":
			text = self.canvas.create_text(x+BORDER,y+MED_FONT[1]*2*fieldOffset+BOL_FONT[1]+BORDER,fill="white",font=MED_FONT, text="DELETE ATOM", anchor="w",
																tags=("grapheditor","id"+str(id), "2pt", "text", "delete", "manager",))
			textBounds = self.canvas.bbox(text)
			maxWidth = max(textBounds[2] - textBounds[0], maxWidth)
			fieldOffset += 1

		#add code export for nitro
		if obj.classname == 'float_common_atoms.nitro_atom(1721)':
			text = self.canvas.create_text(x+BORDER,y+MED_FONT[1]*2*fieldOffset+BOL_FONT[1]+BORDER,fill="white",font=MED_FONT, text="Export nitro code", anchor="w",
																tags=("grapheditor","id"+str(id), "2pt", "text", "exportnitro", "manager",))
			textBounds = self.canvas.bbox(text)
			maxWidth = max(textBounds[2] - textBounds[0], maxWidth)
			fieldOffset += 1

		text = self.canvas.create_text(x+BORDER,y+MED_FONT[1]*2*fieldOffset+BOL_FONT[1]+BORDER,fill="white",font=MED_FONT, text="Refresh atom", anchor="w",
																tags=("grapheditor","id"+str(id), "2pt", "text", "refresh", "manager",))
		textBounds = self.canvas.bbox(text)
		maxWidth = max(textBounds[2] - textBounds[0], maxWidth)
		fieldOffset += 1

		#resize manager window to text
		c = self.canvas.coords(manaWind)
		self.canvas.coords(manaWind, c[0], c[1], x+maxWidth+BORDER*2, y+fieldOffset*2*MED_FONT[1] + 2*BORDER + BOL_FONT[1])
		#print(id)
		#print(self.data_info[id])

	def _on_del_press(self, event):
		x,y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
		clicked = self.canvas.find_closest(x, y)
		self._deleting = clicked

	def _on_del_release(self, event):
		x,y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
		clicked = self.canvas.find_closest(x, y)
		if clicked == self._deleting:
			id = int(self.canvas.gettags(clicked)[1][2:])
			self.delAtom(id)
		self._deleting = None

	def _on_refresh_press(self, event):
		x,y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
		clicked = self.canvas.find_closest(x, y)
		self._refreshing = clicked

	def _on_refresh_release(self, event):
		x,y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
		clicked = self.canvas.find_closest(x, y)
		if clicked == self._refreshing:
			self.refresh(clicked)
		self._refreshing = None

	def refresh(self, clicked = 0):
		id = int(self.canvas.gettags(clicked)[1][2:])
		self.canvas.delete(self.canvas.gettags(clicked)[1])
		self._draw_atom(self.atomList[id])
		print(self.atomList[id].stringify())
		print("refreshing")

	def _on_export_nitro_press(self, event):
		x,y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
		clicked = self.canvas.find_closest(x, y)
		self._exporting_nitro = clicked

	def _on_export_nitro_release(self, event):
		x,y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
		clicked = self.canvas.find_closest(x, y)
		if clicked == self._exporting_nitro:
			id = int(self.canvas.gettags(clicked)[1][2:])
			output = self.atomList[id].fields["code(6264)"].replace('\\n','\n')
			with tk.filedialog.asksaveasfile(mode='w', defaultextension=".nitro") as f:
				if f is None: #in case of cancel
					self._exporting_nitro = None
					return
				f.write(output)
		self._exporting_nitro = None

	#browser
	def _on_2c_press(self, event):
		if not self.canvas.find_withtag("current"):
			self._draw_browser(event.x, event.y)

	def _draw_browser(self, eX,eY,):
		x,y = self.canvas.canvasx(eX), self.canvas.canvasy(eY)
		self.canvas.delete("browser")
		self._browser_active = True
		self._browser = tk.Frame(self.canvas)
		self._browser_canvas = tk.Canvas(self._browser, bg=BASECOL)
		self._browser_canvas.config(height = 400, width = 200)
		self.vbar=tk.Scrollbar(self._browser,orient='vertical')
		self.vbar.pack(side='right',fill='y')
		self.vbar.config(command=self._browser_canvas.yview)
		self._browser_canvas.config(yscrollcommand=self.vbar.set)
		self._browser_canvas.pack(side = 'left', fill="both", expand=True)
		self._browser_position = (x,y,)

		offset=0
		for i in nodes.list:
			self._browser_canvas.create_text(5+BORDER,5+BORDER+MED_FONT[1]*2*offset,fill="white",font=MED_FONT, text=nodes.list[i]['name'], anchor="w",
																tags=("grapheditor", i, "text", "browser",))
			offset +=1

		self._browser.update()
		self._browser_canvas.config(scrollregion=self._browser_canvas.bbox("all"))
		self.canvas.create_window(x, y, window = self._browser, anchor = "nw", tags = ("grapheditor","id"+str(id), "2pt", "browser",))

		self._browser_canvas.tag_bind("browser", "<ButtonPress-1>", self._on_browser_press)
		self._browser_canvas.tag_bind("browser", "<ButtonRelease-1>", self._on_browser_release)

	def _on_browser_press(self, event):
		x,y = self._browser_canvas.canvasx(event.x), self._browser_canvas.canvasy(event.y)
		self._browser_clicked = self._browser_canvas.find_closest(x, y)
		#tags = self.canvas.gettags(clicked)

	def _on_browser_release(self, event):
		x,y = self._browser_canvas.canvasx(event.x), self._browser_canvas.canvasy(event.y)
		clicked = self._browser_canvas.find_closest(x, y)
		if clicked and self._browser_clicked == clicked:
			tags = self._browser_canvas.gettags(clicked)
			self.addAtom(tags[1])
			self.canvas.delete("browser")
			self._browser_active = False
		pass

	def drawKids(self, child,):
		if isinstance(child, atoms.Atom):
			if "settings(6194)" in child.fields:#if its a regular atom
				self._draw_atom(child)
				kid = self.atomList[child.fields["settings(6194)"].id].fields["inport_connections(614)"]
				inportCount = 0
				for i in kid:
					inportConn = self.atomList[i.id]
					if inportConn.fields["source_component(248)"]:
						obj = self.atomList[inportConn.fields["source_component(248)"].id]
						if isinstance(obj, atoms.Atom):
							if "settings(6194)" in obj.fields:
								self.addConn(child.id, inportCount, obj.id, inportConn.fields["outport_index(249)"])
					inportCount += 1

	def addConn(self, dID,dPort, sID,sPort,): #d is drain, s is source
		listLengths = max(sID+1,dID+1)
		while len(self.portList) < listLengths:
			self.portList.append([])
		while len(self.portList[dID]) < dPort+1:
			self.portList[dID].append(None)
		self.portList[dID][dPort] = (sID, sPort)

		while len(self.RortList) < listLengths:
			self.RortList.append([])
		while len(self.RortList[sID]) < sPort+1:
			self.RortList[sID].append([])
		self.RortList[sID][sPort].append((dID, dPort))

	def delConn(self, dID,dPort, sID,sPort,): #d is drain, s is source
		#print('b: d -',self.portList[dID], 's -', self.RortList[sID])
		if len(self.portList[dID]) >= dPort+1:
			if self.portList[dID][dPort] == (sID,sPort):
				self.portList[dID][dPort] = None
			else:
				print("jerror: source doesn't match drain. (401)")
		else:
			print("inport doesn't exist (400)")
		for i in range(len(self.portList[dID]),0,-1):#get rid of trailing empty arrays
			if self.portList[dID][i-1] == None:
				del self.portList[dID][i-1]
			else:
				break

		index = -1
		try:
			index = self.RortList[sID][sPort].index((dID,dPort))
		except:
			print("jerror: source doesn't match drain. (402)")
		else:
			del self.RortList[sID][sPort][index]
			for i in range(len(self.RortList[sID]),0,-1):#get rid of trailing 'None's
				#print('i:',self.RortList[sID][i-1])
				if len(self.RortList[sID][i-1]) == 0:
					del self.RortList[sID][i-1]
				else:
					break

		self.canvas.delete(str(dID) +':'+ str(dPort) +','+ str(sID) +':'+ str(sPort))
		#print('a: d -',self.portList[dID], 's -', self.RortList[sID])

	def addAtom(self, name,):
		#print(name,x,y,)
		fields = {}
		num = int(name.replace(')', ' ').replace('(', ' ').split()[-1])
		currentIndex = len(self.atomList)
		self.atomList.append(atoms.Atom(name))

		#add fields
		for i in typeLists.classList[num]: #i is a field id
			val = 0
			if i in names.params:
				fieldName = names.params[i] + '(' + str(i) + ')'
			else:
				fieldName = names.params[i]
			type = typeLists.fieldList[i]
			if type == 0x01:
				if i == 17:
					val = int(self._browser_position[1]/V_MULT)
				elif i == 18:
					val = int(self._browser_position[0]/H_MULT)
				else:
					val = int(0)
			elif type == 0x05:
				val = bool(0)
			elif type in (0x06, 0x07):
				val = float(0)
			elif type == 0x08:
				val = 'placeholder'
			elif type == 0x12:
				val = []
				print("objlist:", i)
				#if i == 614:
				#	val = self.addAtom('float_core.inport_connection(105)')
			elif type == 0x19:
				val = ['placeholder0','placeholder1',]
			elif type == 0x16:
				print("val is a color")
				val = atoms.Color(0.5,0.5,0.5,1.0)
			elif type == 0x09:
				if i == 702:
					if name == 'float_core.decimal_value_atom(289)':
						objNum = 123
					elif name == 'float_core.boolean_value_atom(87)':
						objNum = 198
					elif name == 'float_core.indexed_value_atom(180)':
						objNum = 155
					elif name == 'float_core.integer_value_atom(394)':
						objNum = 143
					else:
						print("add thisi:", name)
						objNum = -1
				elif i == 248:
					fields[fieldName] = None
					continue
				elif i in fieldAtoms.fa:
					objNum = fieldAtoms.fa[i]
				else:
					print("add this:", i)
					objNum = -1
				className = names.objs[objNum] + '(' + str(objNum) + ')'
				atomId = self.addAtom(className)
				val = atoms.Reference(atomId)
			else:
				print("modification of this parameter is not yet permitted", hex(type))
			fields[fieldName] = val
		self.atomList[currentIndex].set_fields(fields)

		#draw atom
		if 6194 in typeLists.classList[num]:
			self._draw_atom(self.atomList[currentIndex])
			print("drawn")

		print(self.atomList[currentIndex].id)
		return self.atomList[currentIndex].id

	def delAtom(self, id,):
		#delete the ports
		#print(self.RortList)
		if len(self.portList) > id+1:
			for port in range(len(self.portList[id])):
				if self.portList[id][port]:
					#print(self.portList[id][port])
					self.delConn(id, port, *self.portList[id][port])
		if len(self.RortList) > id+1:
			for port in range(len(self.RortList[id])):
				if self.RortList[id][port]:
					for conn in range(len(self.RortList[id][port])):
						if self.RortList[id][port][conn]:
							#print(self.RortList[id][port][conn])
							rConn = self.atomList[self.atomList[self.RortList[id][port][conn][0]].fields["settings(6194)"].id].fields["inport_connections(614)"][self.RortList[id][port][conn][1]]
							self.atomList[rConn.id].fields["source_component(248)"] = None
							#print(self.RortList[id][port])
							self.delConn(*self.RortList[id][port][conn], id, port,)

		#delete and erase the atom
		self.atomList[id] = None
		self.canvas.delete("id"+str(id))

		#delete panel mappings
		if len(self.panelMap) > id:#fix this (not working for delay-2's vumeters)
			for i in self.panelMap[id]:
				self.atomList[i].fields["data_model(6220)"] = None

		#delete inport source components ?what does this mean ? why did i write this?

		#close manager
		self.canvas.delete("manager")
		#print("delete")

	def addPanel(self, name,):
		fields = {}
		num = int(name.replace(')', ' ').replace('(', ' ').split()[-1])
		currentIndex = len(self.atomList)
		self.atomList.append(atoms.Atom(name))
		if 6226 in typeLists.classList[num]:
			self._draw_panel(self.atomList[currentIndex])
		pass

	def drawConnections(self):
		for dID in range(len(self.portList)):
			atoms = self.portList[dID]
			if atoms:
				for dPort in range(len(atoms)):
					inports = atoms[dPort]
					if inports:
						sID = inports[0]
						sPort = inports[1]
						fr = self.canvas.coords("id"+str(sID))
						to = self.canvas.coords("id"+str(dID))
						if not fr or not to: #ignores nonexistent nodes
							print("skipped:",dID,sID)
							continue
						name = str(dID) + ':' + str(dPort) + ',' + str(sID) + ':' + str(sPort)
						sCoord = (fr[2], fr[1] + PORT_OFF*(sPort)+TOTAL_OFF)
						dCoord = (to[0], to[1] + PORT_OFF*(dPort)+TOTAL_OFF)
						dist = min(abs(fr[2] - to[0])/4,75) #for curvature
						self.canvas.tag_lower(self.canvas.create_line(sCoord[0], sCoord[1], sCoord[0]+dist, sCoord[1], dCoord[0]-dist, dCoord[1], dCoord[0], dCoord[1],
														activefill = "white", width = LINE_WID, fill = LINE_COL, tags=("grapheditor", name, "conn"), smooth = True))
		return
		for i in range(self.size):
			for j in range(self.size):
				if self.adjList[i][j]: #only the top right triangular half of the matrix
					fr = self.canvas.coords("id"+str(i))
					to = self.canvas.coords("id"+str(j))
					if not fr or not to: #ignores nonexistent nodes
						self.adjList[i][j] = None
						print("skipped:",i,j)
						break
					#print("conn:",i,j)
					w = fr[1]-fr[3]
					portName = str(i) + ',' + str(j)
					inport = (fr[2], fr[1] + PORT_OFF*(self.linePorts[portName][1])+TOTAL_OFF)
					outport = (to[0], to[1] + PORT_OFF*(self.linePorts[portName][0])+TOTAL_OFF)
					dist = min(abs(fr[2] - to[0])/4,75) #for curvature
					self.canvas.tag_lower(self.canvas.create_line(inport[0], inport[1], inport[0]+dist, inport[1], outport[0]-dist, outport[1], outport[0], outport[1],
													activefill = "white", width = LINE_WID, fill = LINE_COL, tags=("grapheditor", self.adjList[i][j], "conn"), smooth = True))

	def _draw_atom(self, obj, x=None, y=None):
		id = obj.id
		#print("id:",id)
		x = H_MULT*self.atomList[self.atomList[obj.fields["settings(6194)"].id].fields["desktop_settings(612)"].id].fields["y(18)"]
		y = V_MULT*self.atomList[self.atomList[obj.fields["settings(6194)"].id].fields["desktop_settings(612)"].id].fields["x(17)"]
		(nodesI, nodesO) = (0,0)
		(w,h) = (50,50)
		v_offset = TOTAL_OFF
		b = BORDER
		className = obj.classname

		#values
		if className ==  'float_core.decimal_value_atom(289)':
			name = obj.fields["name(374)"]
			(w,h) = (4*b + 8*len(name),32+4*b+MED_FONT[1])
			#val = str(self.atomList[obj.fields["value_type(702)"].id].fields["default_value(891)"])[:7]
			val = str(obj.fields["value(712)"])[:7]
			self.makeRect(className, x, y, id, name=name, h=h, val=val, deco=True)
			#self.canvas.create_text(x+b+DOT_SIZE,y+(2*b+MED_FONT[1]+h)/2,fill="white",font=THK_FONT, text=str(val), anchor="w", tags=("grapheditor","id"+str(id), "2pt", "value"))
			return
		elif className == 'float_core.boolean_value_atom(87)':
			name = obj.fields["name(374)"]
			(w,h) = (4*b + 8*len(name),32+4*b+MED_FONT[1])
			#val = self.atomList[obj.fields["value_type(702)"].id].fields["default_value(6957)"]
			val = obj.fields["value(210)"]
			self.makeRect(className, x, y, id, name=name, h=h, val=val, deco=True)
			#self.canvas.create_text(x+b+DOT_SIZE,y+(2*b+MED_FONT[1]+h)/2,fill="white",font=THK_FONT, text=str(val), anchor="w", tags=("grapheditor","id"+str(id), "2pt", "value"))
			return
		elif className == 'float_core.indexed_value_atom(180)':
			name = obj.fields["name(374)"]
			(w,h) = (4*b + 8*len(name),32+4*b+MED_FONT[1])
			val = obj.fields["value(457)"]
			self.makeRect(className, x, y, id, name=name, h=h, val=val, deco=True)
			vals = self.atomList[obj.fields["value_type(702)"].id].fields["items(393)"]
			#self.canvas.create_text(x+b+DOT_SIZE,y+(2*b+MED_FONT[1]+h)/2,fill="white",font=THK_FONT, text=str(val), anchor="w", tags=("grapheditor","id"+str(id), "2pt", "value"))
			return
		elif className == 'float_core.integer_value_atom(394)':
			name = obj.fields["name(374)"]
			(w,h) = (4*b + 8*len(name),32+4*b+MED_FONT[1])
			val = obj.fields["value(828)"]
			self.makeRect(className, x, y, id, name=name, h=h, val=val, deco=True)
			self.canvas.create_text(x+b+DOT_SIZE,y+(2*b+MED_FONT[1]+h)/2,fill="white",font=THK_FONT, text=str(val), anchor="w", tags=("grapheditor","id"+str(id), "2pt", "value"))
			return
		elif className == 'float_common_atoms.bipolar_toggleable_decimal_value_atom(1763)':
			name = obj.fields["name(374)"]
			(w,h) = (4*b + 8*len(name),32+4*b+MED_FONT[1])
			val = str(obj.fields["value(712)"])[:7]
			self.makeRect(className, x, y, id, name=name, h=h, val=val, deco=True)
			return

		#constant values
		elif className == 'float_common_atoms.constant_value_atom(314)':
			val = str(obj.fields["constant_value(750)"])[:5]
			self.makeRect(className, x, y, id, h=50+MED_FONT[1], val=val)
			return
		elif className == 'float_common_atoms.constant_integer_value_atom(298)':
			val = str(obj.fields["constant_value(720)"])
			self.makeRect(className, x, y, id, h=50+MED_FONT[1], val=val)
			return
		elif className == 'constant_boolean_value_atom(635)':
			val = str(obj.fields["constant_value(2738)"])
			self.makeRect(className, x, y, id, h=50+MED_FONT[1], val=val)
			return

		#atoms
		elif className == 'float_common_atoms.nitro_atom(1721)':
			val = nitro.getName(obj.fields["code(6264)"])
			nodesI, nodesO = nitro.countIOs(obj.fields["code(6264)"])
			#val = obj.fields["code(6264)"][:20]
			#w = 4*b + 8*len(name)
			self.makeRect(className, x, y, id, nodesI=nodesI, nodesO=nodesO, deco=True)
			self.canvas.create_text(x+b+DOT_SIZE,y+4*b+MED_FONT[1],fill="white",font=CODEFONT, text=str(val), anchor="nw",
											tags=("grapheditor","id"+str(id), "2pt", "value"))
			return
		elif className == 'float_common_atoms.note_delay_compensation_atom(1435)':
			self.makeRect(className, x, y, id, name='',)

			self.canvas.create_oval(x+9,y+10,x+23,y+24, outline="#FAA", fill="#FAA",
											tags=("grapheditor", "id"+str(id), "4pt", "deco"))
			self.canvas.create_oval(x+41,y+10,x+27,y+24, outline="#FAA", fill="#FAA",
											tags=("grapheditor", "id"+str(id), "4pt", "deco"))
			self.canvas.create_oval(x+18,y+26,x+32,y+40, outline="#FAA", fill="#FAA",
											tags=("grapheditor", "id"+str(id), "4pt", "deco"))
			return
		elif className == 'float_common_atoms.delay_compensation_atom(1371)':
			self.makeRect(className, x, y, id, name='',)

			self.canvas.create_oval(x+9,y+10,x+23,y+24, outline="#FFF", fill="#FFF",
											tags=("grapheditor", "id"+str(id), "4pt", "deco"))
			self.canvas.create_oval(x+41,y+10,x+27,y+24, outline="#FFF", fill="#FFF",
											tags=("grapheditor", "id"+str(id), "4pt", "deco"))
			self.canvas.create_oval(x+18,y+26,x+32,y+40, outline="#FFF", fill="#FFF",
											tags=("grapheditor", "id"+str(id), "4pt", "deco"))
			return
		elif className == 'float_core.modulation_source_atom(766)':
			name = obj.fields["name(3639)"] + '\no->'
			(w,h) = (15 + 6*(len(name)-4),50+MED_FONT[1])
			self.makeRect(className, x, y, id, name=name, w=w, h=h)
		elif className == 'float_core.value_led_atom(189)':
			self.makeRect(className, x, y, id, name='')
			w,h = nodes.list[className]['w'],nodes.list[className]['h']
			self.canvas.create_rectangle(x+b, y+b, x+w-b, y+h-b , outline="#ed5", fill="#ed5",
													tags=("grapheditor","id"+str(id), "4pt", "deco"))
			return
		elif className == 'float_common_atoms.multiplexer_atom(1188)':
			nodesI = obj.fields["inputs(4763)"]+1
			self.makeRect(className, x, y, id, nodesI=nodesI)

		#other atoms
		elif className == 'float_common_atoms.decimal_event_filter_atom(400)':
			comparisons = ['<','>','=']
			val = comparisons[obj.fields["comparison(842)"]]
			val += str(obj.fields["comparison_value(843)"])[:5]
			self.makeRect(className, x, y, id, val=val)
		elif className == 'float_common_atoms.indexed_lookup_table_atom(344)': #TODO make a lookup table ui
			'''vals = obj.fields["row_data(744)"]
			length = obj.fields["row_count(743)"]
			name += '\n'
			for i in range(length):
				name += str(vals[i].fields["cells(726)"][0].fields["value(739)"]) + '|'
			width = 6*(len(name)-6)
			print("dothis.editor.238934")'''
			self.makeRect(className, x, y, id, nodesO=obj.fields["column_count(742)"])

		#math
		elif className in ('float_common_atoms.constant_add_atom(308)', 'float_common_atoms.constant_multiply_atom(303)',):
			val = str(obj.fields["constant_value(750)"])[:5]
			self.makeRect(className, x, y, id, val=val)
			return
		elif className == 'float_common_atoms.multiply_add_atom(304)':
			nodesI = obj.fields["multiplier_pairs(724)"]*2 + 1
			self.makeRect(className, x, y, id, nodesI=nodesI)
			return
		elif className == 'float_common_atoms.sum_atom(305)':
			nodesI = obj.fields["inputs(725)"]
			self.makeRect(className, x, y, id, nodesI=nodesI)
			return
			name =  str(val)

		#Buffers
		elif className in ('float_common_atoms.buffer_reader_atom(331)','float_common_atoms.buffer_writer_atom(364)'):
			w = nodes.list[className]['w']
			self.makeRect(className, x, y, id)
			self.canvas.create_text(x+w/2,y+h/2,fill="Yellow",font=THK_FONT, text='B', anchor="n", tags=("grapheditor","id"+str(id), "2pt", "name"))
			return

		#components
		elif className == 'float_core.proxy_in_port_component(154)':
			self.makeRect(className, x, y, id, name='',)
			w = nodes.list[className]['w']
			h = nodes.list[className]['h']
			name = self.atomList[obj.fields["port(301)"].id].fields["decorated_name(499)"]
			self.canvas.create_text(x+w/2,y+h/2,fill="white",font=THK_FONT, text=name[:2], anchor="center", tags=("grapheditor","id"+str(id), "2pt", "name"))
			self.canvas.create_polygon(x+10, y+v_offset, x, y+v_offset-7, x, y+v_offset+7, outline="#eee", fill="#eee",
												tags=("grapheditor","id"+str(id), "6pt", "deco"))
			return
			#val = obj.fields["port(301)"].fields["decorated_name(499)"]
			#name += '\n' + val
		elif className == 'float_core.proxy_out_port_component(50)':
			self.makeRect(className, x, y, id, name='',)
			w = nodes.list[className]['w']
			h = nodes.list[className]['h']
			name = self.atomList[obj.fields["port(301)"].id].fields["decorated_name(499)"]
			self.canvas.create_text(x+w/2,y+h/2,fill="white",font=THK_FONT, text=name[:2], anchor="center", tags=("grapheditor","id"+str(id), "2pt", "name"))
			self.canvas.create_polygon(x+w-10, y+v_offset, x+w, y+v_offset-7, x+w, y+v_offset+7, outline="#eee", fill="#eee",
												tags=("grapheditor","id"+str(id), "6pt", "deco"))
			return
			#val = obj.fields["port(301)"].fields["decorated_name(499)"]
			#name += '\n' + val
		elif className == 'float_core.nested_device_chain_slot(587)':
			name = obj.fields["name(835)"]
			b = BORDER
			(w,h) = (75,40)
			self.canvas.create_rectangle(x, y, x+w, y+h, activeoutline = "white" , outline=BASECOL, fill=BASECOL, tags=("grapheditor","id"+str(id), "4pt", "case"))
			self.canvas.create_rectangle(x+b, y+b, x+w-b, y+h-b , outline="#333", fill="#333", tags=("grapheditor","id"+str(id), "4pt", "deco"))
			self.canvas.create_text(x+b+DOT_SIZE,y+2*b,fill="white",font=THK_FONT, text=name, anchor="nw", tags=("grapheditor","id"+str(id), "2pt", "name"))
			nodesI = nodes.list[className]['i']
			nodesO = nodes.list[className]['o']
		elif className in nodes.list:
			self.makeRect(className, x, y, id)
			return
		else:
			color = "#"+("%06x"%random.randint(0,16777215))
			(w,h) = (100,50)
			self.canvas.create_rectangle(x, y, x+w, y+h, activeoutline = "white" , outline=color, fill=color, tags=("grapheditor","id"+str(id), "4pt", "case"))
			self.canvas.create_text(x+3+DOT_SIZE,y+3,fill="white",font=MED_FONT, text=className+" id:"+str(id), anchor="nw", tags=("grapheditor","id"+str(id), "2pt", "name"))
		for inports in range(nodesI):
			self.canvas.create_oval(x-DOT_SIZE, y+(PORT_OFF)*(inports)-DOT_SIZE+v_offset, x+DOT_SIZE, y+(PORT_OFF)*(inports)+DOT_SIZE+v_offset, activeoutline = "black" , outline=NODECOL, fill=NODECOL ,tags=("grapheditor","id"+str(id), "4pt", "port", "in", str(inports)))
		for outports in range(nodesO):
			self.canvas.create_oval(x+w-DOT_SIZE, y+(PORT_OFF)*(outports)-DOT_SIZE+v_offset, x+w+DOT_SIZE, y+(PORT_OFF)*(outports)+DOT_SIZE+v_offset, activeoutline = "black" , outline=NODECOL, fill=NODECOL ,tags=("grapheditor","id"+str(id), "4pt", "port", "out", str(outports)))
		doth = (PORT_OFF)*(max(nodesI,nodesO))+v_offset #whichever type of port there are more of
		if doth > h:
			current = self.canvas.coords("id"+str(id)+"&&case")
			self.canvas.coords("id"+str(id)+"&&case", current[0], current[1], current[2], y+doth)

	def _draw_panel(self, obj, x=None, y=None, xOff=0, yOff=0):
		id = obj.id
		#print("id:",id)
		if "layout_settings(6226)" in obj.fields and obj.fields["layout_settings(6226)"]:
			if obj.fields["layout_settings(6226)"].classname == "float_core.grid_panel_item_layout_settings(1694)":
				x = UI_H_MULT*obj.fields["layout_settings(6226)"].fields["x(6215)"]+xOff
				y = UI_V_MULT*obj.fields["layout_settings(6226)"].fields["y(6216)"]+yOff
				w = UI_H_MULT*obj.fields["layout_settings(6226)"].fields["width(6217)"]
				h = UI_V_MULT*obj.fields["layout_settings(6226)"].fields["height(6218)"]
				randcol = '#%006x' % random.randrange(16**6)
				self.pCanvas.create_rectangle(x, y, x+w, y+h, activeoutline = "white" , outline=BASECOL, fill=randcol, tags=("uieditor","id"+str(id), "4pt", "slider"))
			#elif obj.fields["layout_settings(6226)"].classname == "float_core.stack_panel_item_layout_settings(1803)":
			#	pass
			else:
				print("panel type unknown")
		if "data_model(6220)" in obj.fields and obj.fields["data_model(6220)"]:#if it depends on a control
			id = obj.fields["data_model(6220)"].id
			while len(self.panelMap) < id+1:
				self.panelMap.append([])
			self.panelMap[id].append(obj.id)
		if x == None:
			x = xOff
		if y == None:
			y = yOff
		if "items(6221)" in obj.fields and obj.fields["items(6221)"]:
			for subItem in obj.fields["items(6221)"]:
				self._draw_panel(subItem, xOff = x, yOff = y)
		if "root_item(6212)" in obj.fields and obj.fields["root_item(6212)"]:
			self._draw_panel(obj.fields["root_item(6212)"], xOff = x, yOff = y)

	def makeRect(self, className, x, y, id, name = None, w = None, h = None, nodesI = None, nodesO = None, b = BORDER, v_offset = TOTAL_OFF, val = None, vertical = False, center = False, deco = False):
		if "vertical" in nodes.list[className]:
			vertical = True
		if "center" in nodes.list[className]:
			center = True
		if nodesI == None:
			nodesI = nodes.list[className]['i']
			if isinstance(nodesI, list):
				nodesI = len(nodesI)
		if nodesO == None:
			nodesO = nodes.list[className]['o']
			if isinstance(nodesO, list):
				nodesO = len(nodesO)
		if w == None:
			if vertical:
				w = 30
			elif 'w' in nodes.list[className]:
				w = nodes.list[className]['w']
			else:
				w = 2*(b+DOT_SIZE)
		if h == None:
			if vertical:
				ports = max(nodesI, nodesO)
				h = (PORT_OFF)*(ports-1)+2*v_offset
			else:
				try:
					h = nodes.list[className]['h']
				except:
					ports = max(nodesI, nodesO)
					h = (PORT_OFF)*(ports-1)+2*v_offset
		if name == None:
			if "name" in nodes.list[className]:
				name = nodes.list[className]["name"]

		#the actual drawing part
		if name:
			if vertical:
				drawnName = self.canvas.create_text(x+w/2,y+h/2,fill="white",font=MED_FONT, text=name, angle=90, tags=("grapheditor","id"+str(id), "2pt", "name"))
			elif center:
				drawnName = self.canvas.create_text(x+w/2,y+h/2,fill="white",font=MED_FONT, text=name, tags=("grapheditor","id"+str(id), "2pt", "name"))
			else:
				drawnName = self.canvas.create_text(x+b+DOT_SIZE,y+b,fill="white",font=MED_FONT, text=name, anchor="nw", tags=("grapheditor","id"+str(id), "2pt", "name"))
				bb = self.canvas.bbox(drawnName)
				nameWidth = bb[2]-bb[0] + 2*(b+DOT_SIZE)
				w = max(nameWidth, w)
		if val != None and str(val) != '':
			drawnVal = self.canvas.create_text(x+b+DOT_SIZE,y+(2*b+MED_FONT[1]+h)/2,fill="white",font=THK_FONT, text=str(val), anchor="w", tags=("grapheditor","id"+str(id), "2pt", "value"))
		if deco:
			drawnDeco = self.canvas.create_rectangle(x+b, y+3*b+MED_FONT[1], x+w-b, y+h-b , outline=ACCCOL2, fill=ACCCOL2, tags=("grapheditor","id"+str(id), "4pt", "deco"))
		if "shape" in nodes.list[className]: #doesnt work yet
			if nodes.list[className]['shape'] == "hex":
				hexOff = round(w/2/1.73205)
				case = self.canvas.create_polygon(x,y+h/2, x+hexOff,y, x+w-hexOff,y, x+w,y+h/2, x+w-hexOff,y+h, x+hexOff,y+h, activeoutline = "white" , outline=ACCCOL1, fill=ACCCOL1, tags=("grapheditor","id"+str(id), "6pt", "case"))
		else:
			case = self.canvas.create_rectangle(x, y, x+w, y+h, activeoutline = "white" , outline=ACCCOL1, fill=ACCCOL1, tags=("grapheditor","id"+str(id), "4pt", "case"))

		self.canvas.tag_raise("id"+str(id) + '&&deco')
		self.canvas.tag_raise("id"+str(id) + '&&value')
		self.canvas.tag_raise("id"+str(id) + '&&name')
		for inports in range(nodesI):
			self.canvas.create_oval(x-DOT_SIZE, y+(PORT_OFF)*(inports)-DOT_SIZE+v_offset, x+DOT_SIZE, y+(PORT_OFF)*(inports)+DOT_SIZE+v_offset, activeoutline = "black" , outline=NODECOL, fill=NODECOL ,tags=("grapheditor","id"+str(id), "4pt", "port", "in", str(inports)))
		for outports in range(nodesO):
			self.canvas.create_oval(x+w-DOT_SIZE, y+(PORT_OFF)*(outports)-DOT_SIZE+v_offset, x+w+DOT_SIZE, y+(PORT_OFF)*(outports)+DOT_SIZE+v_offset, activeoutline = "black" , outline=NODECOL, fill=NODECOL ,tags=("grapheditor","id"+str(id), "4pt", "port", "out", str(outports)))

Application().mainloop()
