import platform, subprocess
from . import configmodule
import configparser
from pathlib import Path
from os.path import dirname

def defaultTraceFilePath():
   """
   Outputs the default file path for trace in this library
   """
   match configmodule.platform:
      case "Windows":
         path = fr"{configmodule.moduledirectory}\flashlog.txt"
      case "Linux" | "Darwin":
         path = f"{configmodule.moduledirectory}/flashlog.txt"
   return path
def defaultTraceFilePath_Flash(versionOverride:bool=False,overrideSystem:str=None,overrideVersion:str=None):
   """
   Outputs the defualt file path for trace as defined by https://web.archive.org/web/20180227100916/helpx.adobe.com/flash-player/kb/configure-debugger-version-flash-player.html
   Since anything earlier than Windows 7 isn't supported by python 3, you normally wouldn't be able to get the file path for these systems but I have included an optional parameter to force this function to return it.
   """
   match configmodule.platform:
      case "Linux" | "Darwin":
         from os import getuid
         from pwd import getpwuid
         username = getpwuid(getuid())[0]
      case "Windows":
         from os import getlogin
         username = getlogin()
   if versionOverride == True:
      match overrideSystem:
         case "Linux":
            return fr"/home/{username}/.macromedia/Flash_Player/Logs/flashlog.txt"
         case "Darwin":
            return fr"/Users/{username}/Library/Preferences/Macromedia/Flash Player/Logs/flashlog.txt"
         case "Windows ":
            match overrideVersion:
               case "95" | "98" | "ME" | "XP":
                  return fr"C:\Documents and Settings\{username}\Application Data\Macromedia\Flash Player\Logs\flashlog.txt"
               case "Vista" | "7" | "8" | "8.1" | "10" | "11":
                  return fr"C:\Users\{username}\AppData\Roaming\Macromedia\Flash Player\Logs\flashlog.txt"
   else:
      match configmodule.platform:
         case "Linux":
            return fr"/home/{username}/.macromedia/Flash_Player/Logs/flashlog.txt"
         case "Windows":
            return fr"C:\Users\{username}\AppData\Roaming\Macromedia\Flash Player\Logs\flashlog.txt"
         case "Darwin":
            return fr"/Users/{username}/Library/Preferences/Macromedia/Flash Player/Logs/flashlog.txt"

def sm_x11():
   """
   Gets and returns screen width, screen height, refresh rate, and color depth on x11
   """
   xr = str(subprocess.check_output("xrandr --current", shell=True)).split("\\n")
   for option in xr:
      if option.find("*") != -1:
         curop = option
         break
      else:
         continue
   curop = curop.split(" ")
   ops = []
   for i in curop:
      if i == "":
         continue
      else:
         ops.append(i)
   resandref = []
   resandref.append(ops.pop(0))
   for i in ops:
      if i.find("*") != -1:
         resandref.append(i)
      else:
         continue
   tempres = resandref[0].split("x")
   cdp = str(subprocess.check_output("xwininfo -root | grep Depth", shell=True)).replace("\\n","").replace("b'","").replace(" ","").replace("'","").split(":")[1]
   return int(tempres[0]),int(tempres[1]),float(resandref[1].replace("*","").replace("+","")),int(cdp)

def sm_wayland():
   configpath = configmodule.moduledirectory + "/wayland.cfg"
   if Path(configpath).exists() == True:
      with open(configpath, 'r') as f:
         configwithheader = f.read()
      config = configparser.ConfigParser()
      config.read_string(configwithheader)
      actual_config = config["Screen"]
      existing_options = ["screenwidth" in actual_config,"screenheight" in actual_config,"refreshrate" in actual_config,"colordepth" in actual_config]
      if existing_options[0] == True:
         sw = int(actual_config["screenwidth"])
      else:
         sw = 1600
      if existing_options[1] == True:
         sh = int(actual_config["screenheight"])
      else:
         sh = 900
      if existing_options[2] == True:
         rr = float(actual_config["refreshrate"])
      else:
         rr = 60.00
      if existing_options[3] == True:
         cd = int(actual_config["colordepth"])
      else:
         cd = 8
   else:
      print("(The things that these answers controls is not implemented yet) This seems to be your first time using the module as3lib. Since you are using wayland, some things could not be automatically detected. Please input them in the fields bellow. This information is a part of the flash display module, if you aren't planning to use that, you can put in whatever you want. This information can be configured later in the file <library directory>/wayland.cfg")
      sw = input("Maximum width (px), or -1 for no limit: ")
      sh = input("Maximum height (px), or -1 for no limit: ")
      rr = input("Refresh rate (Hz): ")
      cd = input("Color depth (bits): ")
      with open(f"{configmodule.moduledirectory}/wayland.cfg", "w") as cfg:
         cfg.write(f"['Screen']\nscreenwidth={int(sw)}\nscreenheight={int(sh)}\nrefreshrate={float(rr)}\ncolordepth={int(cd)}")
   return int(sw), int(sh), float(rr), int(cd)

def sm_windows():
   pass

def sm_darwin():
   pass

def indexOf_String(string:str, find:str):
   try:
      return string.index(find)
   except:
      return -1

def initconfig():
   #set up variables needed by mutiple modules
   configmodule.moduledirectory = dirname(__file__)
   configmodule.platform = platform.system()
   configmodule.defaultTraceFilePath = defaultTraceFilePath()
   configmodule.defaultTraceFilePath_Flash = defaultTraceFilePath_Flash()
   configmodule.pythonversion = platform.python_version()
   match configmodule.platform:
      case "Linux":
         dmtype = subprocess.check_output("loginctl show-session $(loginctl | grep $(whoami) | awk '{print $1}') -p Type", shell=True)
         dmtype = str(dmtype).split("=")[1]
         dmtype = dmtype.replace("\\n'","")
         configmodule.windowmanagertype = dmtype
         if dmtype == "wayland":
            comp = subprocess.check_output('lsof -t "${XDG_RUNTIME_DIR}/${WAYLAND_DISPLAY:-wayland-0}"', shell=True)
            compids = str(comp).replace("b'","").replace("'","").split("\\n")
            compids.remove("")
            psout = []
            for i in compids:
               temp = str(subprocess.check_output(f"ps {i}",shell=True)).split("\\n")[1].split(" ")
               temp2 = ""
               for i in temp:
                  try:
                     t = i.index("/bin/")
                     temp2 = i
                  except:
                     continue
               try:
                  t = temp2.index("xwayland")
               except:
                  psout.append(temp2)
            if indexOf_String(psout[0], "kwin") != -1:
               configmodule.wlcompositor = "kwin"
            elif indexOf_String(psout[0], "gnome-shell") != -1:
               configmodule.wlcompositor = "gnome"
            #elif indexOf_String(psout[0], "") != -1:
            #   pass
            else:
               configmodule.wlcompositor = "ERROR: COMPOSITOR NOT ACCOUNTED FOR"
               configmodule.initerror.append({"errcode":2,"errdesc":f"Error fetching compositor name; Linux, Wayland; Compositor {psout[0]} not implemented"})
         match configmodule.windowmanagertype:
            case "x11":
               temp = sm_x11()
               configmodule.width = temp[0]
               configmodule.height = temp[1]
               configmodule.refreshrate = temp[2]
               configmodule.colordepth = temp[3]
            case "wayland":
               temp = sm_wayland()
               configmodule.width = temp[0]
               configmodule.height = temp[1]
               configmodule.refreshrate = temp[2]
               configmodule.colordepth = temp[3]
      case "Windows":
         configmodule.initerror.append({"errcode":1,"errdesc":"Error fetching screen properties; Windows; Not Implemented Yet"})
         #configmodule.width = temp[0]
         #configmodule.height = temp[1]
         #configmodule.refreshrate = temp[2]
         #configmodule.colordepth = temp[3]
         pass
      case "Darwin":
         configmodule.initerror.append({"errcode":1,"errdesc":"Error fetching screen properties; Darwin; Not Implemented Yet"})
         #configmodule.width = temp[0]
         #configmodule.height = temp[1]
         #configmodule.refreshrate = temp[2]
         #configmodule.colordepth = temp[3]
         pass
   match configmodule.platform:
      case "Linux" | "Darwin":
         configpath = f"{configmodule.moduledirectory}/mm.cfg"
         if Path(configpath).exists() == True:
            with open(configpath, 'r') as f:
               configwithheader = '[dummy_section]\n' + f.read()
            config = configparser.ConfigParser()
            config.read_string(configwithheader)
            actual_config = config["dummy_section"]
            existing_options = ["ErrorReportingEnable" in actual_config,"MaxWarnings" in actual_config,"TraceOutputFileEnable" in actual_config,"TraceOutputFileName" in actual_config,"ClearLogsOnStartup" in actual_config]
            if existing_options[0] == True:
               configmodule.ErrorReportingEnable = int(actual_config["ErrorReportingEnable"])
            if existing_options[1] == True:
               configmodule.MaxWarnings = int(actual_config["MaxWarnings"])
            if existing_options[2] == True:
               configmodule.TraceOutputFileEnable = int(actual_config["TraceOutputFileEnable"])
            if existing_options[3] == True:
               configmodule.TraceOutputFileName = actual_config["TraceOutputFileName"]
            if existing_options[4] == True:
               configmodule.ClearLogsOnStartup = int(actual_config["ClearLogsOnStartup"])
      case "Windows":
         configpath = fr"{configmodule.moduledirectory}\mm.cfg"
         if Path(configpath).exists() == True:
            with open(configpath, 'r') as f:
               configwithheader = '[dummy_section]\n' + f.read()
            config = configparser.ConfigParser()
            config.read_string(configwithheader)
            actual_config = config["dummy_section"]
            existing_options = ["ErrorReportingEnable" in actual_config,"MaxWarnings" in actual_config,"TraceOutputFileEnable" in actual_config,"TraceOutputFileName" in actual_config,"ClearLogsOnStartup" in actual_config]
            if existing_options[0] == True:
               configmodule.ErrorReportingEnable = int(actual_config["ErrorReportingEnable"])
            if existing_options[1] == True:
               configmodule.MaxWarnings = int(actual_config["MaxWarnings"])
            if existing_options[2] == True:
               configmodule.TraceOutputFileEnable = int(actual_config["TraceOutputFileEnable"])
            if existing_options[3] == True:
               configmodule.TraceOutputFileName = actual_config["TraceOutputFileName"]
            if existing_options[4] == True:
               configmodule.ClearLogsOnStartup = int(actual_config["ClearLogsOnStartup"])
   if configmodule.TraceOutputFileName == "":
      configmodule.TraceOutputFileName = configmodule.defaultTraceFilePath
   if Path(configmodule.TraceOutputFileName).is_dir() == True:
      print("Path provided is a directory, writing to defualt location instead.")
      configmodule.TraceOutputFileName = configmodule.defaultTraceFilePath
   if configmodule.ClearLogsOnStartup == 1:
      if Path(configmodule.TraceOutputFileName).exists() == True:
         with open(configmodule.TraceOutputFileName, "w") as f: 
            f.write("")

   #Tell others that library has been initialized
   configmodule.initdone = True
