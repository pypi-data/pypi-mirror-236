platform = "" #Windows, Linux, or Darwin
windowmanagertype = "" #linux only, x11 or wayland
wlcompositor = "" #wayland only, compositor name to identify which commands to use
moduledirectory = "" #full path to as3lib (this library)
pythonversion = ""

objects = {} #list of objects (testing, might not be here later)

#toplevel
as3DebugEnable = False #(True=enabled, False=disabled) state of debug mode
ErrorReportingEnable = 0 #(1=enabled, 0=disabled) state of error reporting
MaxWarnings = 100 #maximum number of warnings until they are suppressed
TraceOutputFileEnable = 0 #(1=file, 0=console) determines whether to output "trace" to a file or to the console
TraceOutputFileName = "" #file path where error messages are stored if TraceOutputFileEnable is set to "1"
CurrentWarnings = 0 #current number of warnings
MaxWarningsReached = False #(True=yes, False=no)tells if the maximum number of warnings has been reached
ClearLogsOnStartup = 1 #(1=yes, 0=no) if set, clears logs on startup. This is the default behavior in flash
defaultTraceFilePath = "" #default file path for trace output
defaultTraceFilePath_Flash = "" #default file path for trace output in flash

#display
width = "" #maximum width of the display window (not implemented yet), needs to be manually set on wayland
height = "" #maximum height of the display window (not implemented yet), needs to be manually set on wayland
refreshrate = "" #refresh rate of the display window (not implemented yet), needs to be manually set on wayland
colordepth = "" #color depth of the display window (not implemented yet), needs to be manually set on wayland

#initcheck
initdone = False #variable to make sure this module has initialized
initerror = [] #[{"errcode":errcode, "errdesc":errdesc},...]; errcode:int, errdesc:str
