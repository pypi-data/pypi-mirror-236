import tkinter
import tkhtmlview
import re
import PIL
import math
from io import BytesIO as btio
"""
Temporary interface to get things working. A bit slow when too many things are defined. Even after this module is no longer needed, it will stay for compatibility purposes.
Notes:
- Canvas is not supported yet even though there is an option for it
- When setting commands, they must be accessible from the scope of where they are called
- When grouping windows together, the object that should be used is <windowobject>.root
Todo:
- Fix minimum size calculation
- Optimize refresh for HTMLScrolledText
- Properly support canvas mode
"""
#Adobe flash minimum size is 262x0 for a window that starts out at 1176x662

def help():
   print("If you are confused about how to use this module, please run this module by itself and look at the test code at the bottom.")

class _ScrolledListbox(tkinter.Listbox):
   #This code is a modification of the code from tkhtmlview
   def __init__(self, master=None, **kwargs):
      self.frame = tkinter.Frame(master)
      self.vbar = tkinter.Scrollbar(self.frame)

      kwargs["yscrollcommand"] = self.vbar.set
      self.vbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
      self.vbar["command"] = self.yview

      tkinter.Listbox.__init__(self, self.frame, **kwargs)
      self.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

      text_meths = vars(tkinter.Text).keys()
      methods = vars(tkinter.Pack).keys() | vars(tkinter.Grid).keys() | vars(tkinter.Place).keys()
      methods = methods.difference(text_meths)

      for m in methods:
         if m[0] != "_" and m != "config" and m != "configure":
            setattr(self, m, getattr(self.frame, m))
      def __str__(self):
         return str(self.frame)
class ScrolledListbox(_ScrolledListbox):
   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)

class window:
   def __init__(self, width, height, title="Python",_type="frame",color="#FFFFFF",mainwindow=True,defaultmenu=True):
      self.oldmult = 100
      self.aboutwindowtext = "placeholdertext"
      self.children = {}
      self.childproperties = {}
      self.imagedict = {} # "imagename":{"oimage":data,"rimage":data,"osize":[width,height]}
      self.hstproperties = {}
      self.sbsettings = {} # "name":[scalingenable:bool,defaultsize:int]
      self.fs = False
      if width < 262:
         width = 262
      self.startwidth = width
      self.startheight = height
      self.color = color
      self.mw = mainwindow
      if mainwindow == True:
         self.root = tkinter.Tk()
         self.root.minsize(262,int((262*self.startheight)/self.startwidth) + 28)
         if defaultmenu == True:
            self.menubar = tkinter.Menu(self.root, bd=1)
            self.filemenu = tkinter.Menu(self.menubar, tearoff=0)
            self.filemenu.add_command(label="Quit", font=("Terminal",8), command=self.endProcess)
            self.menubar.add_cascade(label="File", font=("Terminal",8), menu=self.filemenu)
            self.viewmenu = tkinter.Menu(self.menubar, tearoff=0)
            self.viewmenu.add_command(label="Full Screen", font=("Terminal",8), command=self.togglefullscreen)
            self.viewmenu.add_command(label="Reset Size", font=("Terminal",8), command=self.resetSize)
            self.menubar.add_cascade(label="View", font=("Terminal",8), menu=self.viewmenu)
            self.controlmenu = tkinter.Menu(self.menubar, tearoff=0)
            self.controlmenu.add_command(label="Controls", font=("Terminal",8))
            self.menubar.add_cascade(label="Control", font=("Terminal",8), menu=self.controlmenu)
            self.helpmenu = tkinter.Menu(self.menubar, tearoff=0)
            self.helpmenu.add_command(label="About", font=("Terminal",8), command=self.aboutwin)
            self.menubar.add_cascade(label="Help", font=("Terminal",8), menu=self.helpmenu)
            self.root.config(menu=self.menubar)
         else:
            self.menubar = tkinter.Menu(self.root, bd=1)
            self.root.config(menu=self.menubar)
      else:
         self.root = tkinter.Toplevel()
         self.root.minsize(262,int((262*self.startheight)/self.startwidth))
      self.root.title(title)
      self.root.geometry(f"{self.startwidth}x{self.startheight}")
      if _type == "canvas":
         self.display = tkinter.Canvas(self.root, background=self.color, confine=True)
         self.display.place(anchor="center", width=width, height=height, x=self.startwidth/2, y=self.startheight/2)
      elif _type == "frame":
         self.display = tkinter.Frame(self.root, background=self.color)
         self.display.place(anchor="center", width=width, height=height, x=self.startwidth/2, y=self.startheight/2)
      else:
         raise Exception("_type must be either frame or canvas.")
      self.root.bind("<Configure>",self.doResize)
      self.root.bind("<Escape>",self.outfullscreen)
   def __getattr__(self, key):
      return self.children[key]
   def resetSize(self):
      self.root.geometry(f"{self.startwidth}x{self.startheight}")
   def group(self, objectName:object):
      self.root.group(objectName)
   def toTop(self):
      self.root.lift()
   def forceFocus(self, child:str):
      self.children[child].focus_force()
   def round(self, num):
      tempList = str(num).split(".")
      tempList[1] = f".{tempList[1]}"
      if float(tempList[1]) >= 0.5: #0.85? 0.5? 1?
         return math.ceil(num)
      else:
         return math.floor(num)
   def minimumSize(self,_type:str="b",**kwargs):
      """
      _type must be either 'w','h',or 'b' (meaning width, height, or both). If nothing is passed, assumed to be 'b' (both)
      kwargs must include width, height, or both depending on what you chose for _type
      if 'w' or 'height' is chosen, the other will be assumed based on the ration of the original size
      """
      match _type:
         case "w":
            if self.mw == True:
               self.root.minsize(kwargs["width"],int((kwargs["width"]*self.startheight)/self.startwidth) + 28)
            else:
               self.root.minsize(kwargs["width"],int((kwargs["width"]*self.startheight)/self.startwidth))
         case "h":
            if self.mw == True:
               self.root.minsize(int((self.startwidth*kwargs["height"])/self.startheight) - 52,kwargs["height"])
            else:
               self.root.minsize(int((self.startwidth*kwargs["height"])/self.startheight),kwargs["height"])
         case "b":
            self.root.minsize(kwargs["width"],kwargs["height"])
         case _:
            print("Invalid type")
   def minimumSizeReset(self):
      if self.mw == True:
         self.root.minsize(262,int((262*self.startheight)/self.startwidth) + 28)
      else:
         self.root.minsize(262,int((262*self.startheight)/self.startwidth))
   def resizefont(self, font:tuple, mult):
      return (font[0],self.round(font[1]*mult/100))
   def _checkName(self, name:str):
      blacklist = ["(",")","{","}","[","]","!","@","#","$","%","^","&","*",",",".","<",">","/","\\","|","'","\"",":",";","-","+","=","~","`"]
      if name[0].isalpha():
         array = [i in name for i in blacklist]
         try:
            i = array.index(True)
            return False
         except:
            return True
      else:
         return False
   def mainloop(self):
      self.resizeChildren(100)
      self.root.mainloop()
   def enableResizing(self):
      self.root.resizable(True,True)
   def disableResizing(self):
      self.root.resizable(False,False)
   def endProcess(self):
      self.root.destroy()
   def togglefullscreen(self):
      if self.fs == False:
         self.gofullscreen()
      else:
         self.outfullscreen()
   def gofullscreen(self):
      self.fs = True
      self.root.attributes("-fullscreen", True)
   def outfullscreen(self, useless=""):
      self.fs = False
      self.root.attributes("-fullscreen", False)
   def setAboutWindowText(self, text):
      self.aboutwindowtext = text
   def aboutwin(self):
      self.aboutwindow = tkinter.Toplevel()
      self.aboutwindow.geometry("350x155")
      self.aboutwindow.resizable(False,False)
      self.aboutwindow.group(self.root)
      self.aboutwindow.configure(background=self.color)
      self.aboutlabel1 = tkinter.Label(self.aboutwindow, font=("TkTextFont",9), justify="left", text=self.aboutwindowtext, background=self.color)
      self.aboutlabel1.place(anchor="nw", x=7, y=9)
      self.aboutokbutton = tkinter.Button(self.aboutwindow, text="OK", command=self.closeabout, background=self.color)
      self.aboutokbutton.place(anchor="nw", width=29, height=29, x=299, y=115)
   def closeabout(self):
      self.aboutwindow.destroy()
   def addButton(self, master:str, name:str, x, y, width, height, font, anchor:str="nw"):
      if master == "root":
         master = "display"
      if self._checkName(master) == False:
         print("Invalid Master")
         pass
      elif self._checkName(name) == False:
         print("Invalid Name")
         pass
      else:
         if master == "display":
            self.children[name] = tkinter.Button(self.display)
         else:
            self.children[name] = tkinter.Button(self.children[master])
         self.children[name].place(x=x,y=y,width=width,height=height,anchor=anchor)
         self.childproperties[name] = [None,"Button",x,y,width,height,font,anchor]
         self.resizeChild(name, self.oldmult)
   def addLabel(self, master:str, name:str, x, y, width, height, font, anchor:str="nw"):
      if master == "root":
         master = "display"
      if self._checkName(master) == False:
         print("Invalid Master")
         pass
      elif self._checkName(name) == False:
         print("Invalid Name")
         pass
      else:
         if master == "display":
            self.children[name] = tkinter.Label(self.display)
         else:
            self.children[name] = tkinter.Label(self.children[master])
         self.children[name].place(x=x,y=y,width=width,height=height,anchor=anchor)
         self.childproperties[name] = [None,"Label",x,y,width,height,font,anchor]
         self.resizeChild(name, self.oldmult)
   def addnwhLabel(self, master:str, name:str, x, y, font, anchor:str="nw"):
      if master == "root":
         master = "display"
      if self._checkName(master) == False:
         print("Invalid Master")
         pass
      elif self._checkName(name) == False:
         print("Invalid Name")
         pass
      else:
         if master == "display":
            self.children[name] = tkinter.Label(self.display)
         else:
            self.children[name] = tkinter.Label(self.children[master])
         self.children[name].place(x=x,y=y,anchor=anchor)
         self.childproperties[name] = [None,"nwhLabel",x,y,None,None,font,anchor]
         self.resizeChild(name, self.oldmult)
   def addFrame(self, master:str, name:str, x, y, width, height, anchor:str="nw"):
      if master == "root":
         master = "display"
      if self._checkName(master) == False:
         print("Invalid Master")
         pass
      elif self._checkName(name) == False:
         print("Invalid Name")
         pass
      else:
         if master == "display":
            self.children[name] = tkinter.Frame(self.display)
         else:
            self.children[name] = tkinter.Frame(self.children[master])
         self.children[name].place(x=x,y=y,width=width,height=height,anchor=anchor)
         self.childproperties[name] = [None,"Frame",x,y,width,height,None,anchor]
         self.resizeChild(name, self.oldmult)
   def addHTMLScrolledText(self, master:str, name:str, x, y, width, height, font, anchor:str="nw", sbscaling:bool=True, sbwidth:int=12):
      if master == "root":
         master = "display"
      if self._checkName(master) == False:
         print("Invalid Master")
         pass
      elif self._checkName(name) == False:
         print("Invalid Name")
         pass
      else:
         if master == "display":
            self.children[name] = tkhtmlview.HTMLScrolledText(self.display)
         else:
            self.children[name] = tkhtmlview.HTMLScrolledText(self.children[master])
         self.children[name].place(x=x,y=y,width=width,height=height,anchor=anchor)
         self.hstproperties[name] = {"fg":'#000000',"bg":'#FFFFFF',"otext":"","ftext":"","fontbold":False,"sbsettings":[sbscaling,sbwidth]}
         self.childproperties[name] = [None,"HTMLScrolledText",x,y,width,height,font,anchor]
         self.resizeChild(name, self.oldmult)
   def prepareHTMLST(self, child:str, text:str):
      if self.hstproperties[f"{child}"]["otext"] == text:
         self.HTMLSTUpdateText(child, True)
      else:
         self.hstproperties[f"{child}"]["otext"] = text
         self.HTMLSTUpdateText(child)
   def HTMLSTUpdateText(self, child:str, rt=False):
      self.children[child]["state"] = "normal"
      font = self.childproperties[child][6]
      fontsize = font[1]
      if rt == False:
         self.hstproperties[f"{child}"]["ftext"] = re.sub("(\t)", "    ",self.hstproperties[f"{child}"]["otext"])
      text = self.hstproperties[f"{child}"]["ftext"]
      text = "<pre style=\"color: " + self.hstproperties[f"{child}"]["fg"] + "; background-color: " + self.hstproperties[f"{child}"]["bg"] + f"; font-size: {int(fontsize*self.oldmult/100)}px; font-family: {font[0]}\">{text}</pre>"
      if self.hstproperties[child]["fontbold"] == True:
         text = "<b>" + text + "</b>"
      self.children[child].set_html(text)
      self.children[child]["state"] = "disabled"
   def addImage(self, image_name:str, image_data, size:tuple=""):
      """
      size - the target (display) size of the image before resizing
      if size is not defined it is assumed to be the actual image size
      """
      self.imagedict[f"{image_name}"] = {}
      self.imagedict[f"{image_name}"]["oimage"] = image_data
      if size != "":
         self.imagedict[f"{image_name}"]["osize"] = [size[0],size[1]]
      else:
         ims = PIL.Image.open(btio(image_data)).size
         self.imagedict[f"{image_name}"]["osize"] = [ims[0],ims[1]]
   def addImageLabel(self, master:str, name:str, x, y, width, height, anchor:str="nw", image_name:str=""):
      if master == "root":
         master = "display"
      if self._checkName(master) == False:
         print("Invalid Master")
         pass
      elif self._checkName(name) == False:
         print("Invalid Name")
         pass
      else:
         self.resizeImage((width,height), image_name)
         if master == "display":
            self.children[name] = tkinter.Label(self.display)
         else:
            self.children[name] = tkinter.Label(self.children[master])
         self.children[name].place(x=x,y=y,width=width,height=height,anchor=anchor)
         if image_name == "":
            self.children[name]["image"] = ""
         else:
            self.children[name]["image"] = self.imagedict[f'{image_name}']["rimage"]
         self.childproperties[name] = [None,"ImageLabel",x,y,width,height,None,anchor,image_name]
         self.resizeChild(name, self.oldmult)
   def addScrolledListbox(self, master:str, name:str, x, y, width, height, font, anchor:str="nw", sbscaling:bool=True, sbwidth:int=12):
      if master == "root":
         master = "display"
      if self._checkName(master) == False:
         print("Invalid Master")
         pass
      elif self._checkName(name) == False:
         print("Invalid Name")
         pass
      else:
         self.sbsettings[name] = [sbscaling,sbwidth]
         if master == "display":
            self.children[name] = ScrolledListbox(self.display)
         else:
            self.children[name] = ScrolledListbox(self.children[master])
         self.children[name].place(x=x,y=y,width=width,height=height,anchor=anchor)
         self.childproperties[name] = [None,"ScrolledListbox",x,y,width,height,font,anchor]
         self.resizeChild(name, self.oldmult)
   def slb_Insert(self, child:str, position, item):
      self.children[child].insert(position,item)
   def slb_Delete(self, child:str, start, end):
      self.children[child].delete(start, end)
   def resizeImage(self, size:tuple, image_name):
      img = PIL.Image.open(btio(self.imagedict[f"{image_name}"]["oimage"]))
      img.thumbnail(size)
      self.imagedict[f"{image_name}"]["rimage"] = PIL.ImageTk.PhotoImage(img)
   def resizeChildren(self, mult):
      for i in self.imagedict:
         self.resizeImage((int(self.imagedict[i]["osize"][0]*mult/100),int(self.imagedict[i]["osize"][1]*mult/100)),i)
      for i in self.childproperties:
         cl = self.childproperties[i]
         match cl[1]:
            case "nwhLabel":
               self.children[i].place(x=cl[2]*mult/100,y=cl[3]*mult/100,anchor=cl[7])
            case _:
               self.children[i].place(x=cl[2]*mult/100,y=cl[3]*mult/100,width=cl[4]*mult/100,height=cl[5]*mult/100,anchor=cl[7])
         match cl[1]:
            case "HTMLScrolledText":
               if self.hstproperties[i]["sbsettings"][0] == True:
                  self.children[i].vbar["width"] = self.hstproperties[i]["sbsettings"][1]*mult/100
               self.HTMLSTUpdateText(i,True)
            case "ScrolledListbox":
               if self.sbsettings[i][0] == True:
                  self.children[i].vbar["width"] = self.sbsettings[i][1]*mult/100
               font = self.childproperties[i][6]
               self.children[i]["font"] = (font[0],int(font[1]*self.oldmult/100))
            case "ImageLabel":
               if cl[8] == "":
                  self.children[i]["image"] = ""
               else:
                  self.children[i]["image"] = self.imagedict[f"{cl[8]}"]["rimage"]
            case _:
               if cl[1] != "Frame":
                  f = cl[6]
                  self.children[i]["font"] = self.resizefont(f,mult)
   def resizeChild(self, child:str, mult):
      cl = self.childproperties[child]
      match cl[1]:
         case "nwhLabel":
            self.children[child].place(x=cl[2]*mult/100,y=cl[3]*mult/100,anchor=cl[7])
         case _:
            self.children[child].place(x=cl[2]*mult/100,y=cl[3]*mult/100,width=cl[4]*mult/100,height=cl[5]*mult/100,anchor=cl[7])
      match cl[1]:
         case "HTMLScrolledText":
            if self.hstproperties[child]["sbsettings"][0] == True:
               self.children[child].vbar["width"] = self.hstproperties[child]["sbsettings"][1]*mult/100
            self.HTMLSTUpdateText(child,True)
         case "ScrolledListbox":
            if self.sbsettings[child][0] == True:
               self.children[child].vbar["width"] = self.sbsettings[child][1]*mult/100
            font = self.childproperties[child][6]
            self.children[child]["font"] = (font[0],int(font[1]*self.oldmult/100))
         case "ImageLabel":
            if cl[8] == "":
               self.children[child]["image"] = ""
            else:
               self.resizeImage((int(cl[4]*mult/100),int(cl[5]*mult/100)),cl[8])
               self.children[child]["image"] = self.imagedict[f"{cl[8]}"]["rimage"]
         case _:
            if cl[1] != "Frame":
               f = cl[6]
               self.children[child]["font"] = self.resizefont(f,mult)
   def bindChild(self, child:str, tkevent, function):
      self.children[child].bind(tkevent, function)
   def configureChild(self, child:str, **args):
      k = []
      v = []
      for i in args.keys():
         k.append(i)
      for i in args.values():
         v.append(i)
      i = 0
      while i < len(k):
         match k[i]:
            case "x" | "y" | "width" | "height" | "font"| "anchor":
               newlist = self.childproperties[child]
               match k[i]:
                  case "x":
                     newlist[2] = v[i]
                  case "y":
                     newlist[3] = v[i]
                  case "width":
                     newlist[4] = v[i]
                  case "height":
                     newlist[5] = v[i]
                  case "font":
                     newlist[6] = v[i]
                  case "anchor":
                     newlist[7] = v[i]
               self.childproperties[child] = newlist
               self.resizeChild(child, self.oldmult)
            case "text" | "textadd":
               if self.childproperties[child][1] == "HTMLScrolledText":
                  if k[i] == "text":
                     text = v[i]
                  else:
                     text = self.hstproperties[f"{child}"]["otext"] + v[i]
                  self.prepareHTMLST(child, text)
               else:
                  self.children[child][k[i]] = v[i]
            case "background" | "foreground":
               if child == "display":
                  if k[i] == "background":
                     self.display["bg"] = v[i]
               elif self.childproperties[child][1] == "Frame":
                  if k[i] == "background":
                     self.children[child]["bg"] = v[i]
               elif self.childproperties[child][1] == "HTMLScrolledText":
                  self.children[child][k[i]] = v[i]
                  if k[i] == "background":
                     self.hstproperties[f"{child}"]["bg"] = v[i]
                  else:
                     self.hstproperties[f"{child}"]["fg"] = v[i]
                  self.prepareHTMLST(child, self.hstproperties[f"{child}"]["otext"])
               else:
                  self.children[child][k[i]] = v[i]
            case "image":
               self.childproperties[child][8] = v[i]
               self.resizeChildren(self.oldmult)
            case _:
               if k[i] == "stfontbold" and self.childproperties[child][1] == "HTMLScrolledText":
                  self.hstproperties[child]["fontbold"] = v[i]
                  self.prepareHTMLST(child, self.hstproperties[f"{child}"]["otext"])
               elif k[i] == "sbwidth":
                  if self.childproperties[child][1] == "HTMLScrolledText":
                     self.hstproperties[child]["sbsettings"][1] = int(v[i])
                  elif self.childproperties[child][1] == "HTMLScrolledText":
                     self.sbsettings[child][1] = int(v[i])
               else:
                  self.children[child][k[i]] = v[i]
         i += 1
   def destroyChild(self, child:str):
      temppref = self.childproperties.pop(child)
      match temppref[1]:
         case "HTMLScrolledText":
            self.hstproperties.pop(child)
         case "ScrolledListbox":
            self.sbsettings.pop(child)
      self.children[child].destroy()
      self.children.pop(child)
   def getChildAttribute(self, child:str, attribute:str):
      match child:
         case "display":
            return self.display.cget(attribute)
         case _:
            return self.children[child].cget(attribute)
   def getChildAttributes(self, child:str, *args:str):
      templist = {}
      for i in args:
         templist.append(getChildAttribute(child, i))
      return templist
   def doResize(self, event):
      if event.widget == self.root:
         mult = self.calculate()
         self.set_size(mult)
         if mult != self.oldmult:
            self.oldmult = mult
            self.resizeChildren(mult)
   def calculate(self):
      newwidth = self.root.winfo_width()
      newheight = self.root.winfo_height()
      xmult = (100*newwidth)/self.startwidth
      ymult = (100*newheight)/self.startheight
      if xmult > ymult:
         mult = ymult
      elif xmult < ymult:
         mult = xmult
      elif xmult == ymult:
         mult = xmult
      if self.oldmult == mult:
         return self.oldmult
      else:
         return mult
   def set_size(self, mult):
      newwidth = self.root.winfo_width()
      newheight = self.root.winfo_height()
      self.display.place(anchor="center", width=self.startwidth*mult/100, height=self.startheight*mult/100, x=math.floor(newwidth/2), y=math.floor(newheight/2))

if __name__ == "__main__":
   #Test
   from platform import python_version
   testcolor = 0
   fontBold = False
   def test_changebold():
      global fontBold
      if fontBold == True:
         fontBold = False
         return False
      elif fontBold == False:
         fontBold = True
         return True
   def test_cyclecolor():
      global testcolor
      testcolorlist = ["#FFFFFF","#8F2F9F","#AAAAAA"]
      testcolor += 1
      if testcolor >= 3:
         testcolor = 0
      return testcolorlist[testcolor]
   root = window(1176,662,title="Adobe Flash Projector-like Window Demo")
   root.setAboutWindowText(f"Adobe Flash Projector-like window demo.\n\nPython {python_version()}")
   root.addButton("root","testbutton1",130,0,130,30,("Times New Roman",12))
   root.configureChild("testbutton1",command=lambda: root.configureChild("testtext", background=test_cyclecolor()))
   root.addLabel("root","testlabel1",0,30,100,20,("Times New Roman",12))
   root.addHTMLScrolledText("root","testtext",0,50,600,400,("Times New Roman",12),anchor="nw")
   root.configureChild("testtext", text="TestTextpt1\n\nTestTextpt2", cursor="arrow", wrap="word")
   root.configureChild("testbutton1", text="st_colourtest")
   root.configureChild("testlabel1", text="TestLabel")
   secondwindow = window(400,400,title="Second Window",_type="frame",mainwindow=False)
   secondwindow.group(root.root)
   root.addButton("root","testbutton2",0,0,130,30,("Times New Roman",12))
   root.configureChild("testbutton2",command=lambda: secondwindow.toTop()) 
   root.configureChild("testbutton2", text="liftsecondwindow")
   root.addButton("root","testbutton3",260,0,130,30,("Times New Roman",12))
   root.configureChild("testbutton3",command=lambda: root.configureChild("testtext",stfontbold=test_changebold())) 
   root.configureChild("testbutton3", text="st_boldtest")
   root.addScrolledListbox("root","testslb",0,450,150,150,("Times New Roman",12))
   l1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
   for i in l1:
      root.slb_Insert("testslb", "end", i)
   root.mainloop()