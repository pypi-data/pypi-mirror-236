<h1>python-as3lib</h1>
A python implementation of some of the ActionScript3 functions and classes. They are as close as I could get them with my knowledge and the very limited documentation that adobe provides. Once I learn how to make python c modules, I plan on offloading some of this stuff to c or c++ modules to speed things up. If I can figure out how to do it in this context, I might implement the interface in OpenGL or Vulkan to make it work better and more customizable.
<br><br>Please note that versions containing the configmodule before 0.0.6 are broken on windows becuase I forgot to escape the file paths and the imports were broken.
<br><br><b>If you are using wayland, this module will have a first time init message because wayland does not support fetching some values automatically.</b> These values are stored in &lt;library-directory&gt;/wayland.cfg. They are only needed if you are using any of the graphical elements of this library.
<br><br>I have no way as of current to test the accuracy of these functions as I can't find a compiler for actionscript that I could get to work so if anything doesn't work or there is undocumented functionality please let me know on the github issues page. DO NOT EMAIL ME, I will not respond and nothing will get fixed.
<h3>Requirements</h3>
Built-in:
<br>tkinter, re, math, io, platform, subprocess, random, time, datetime, os, pwd (linux), pathlib, configparser, webbrowser, textwrap, typing
<br>External:
<br><a href="https://pypi.org/project/numpy">numpy</a>, <a href="https://pypi.org/project/Pillow">Pillow</a>, <a href="https://pypi.org/project/tkhtmlview">tkhtmlview</a>
<h3>Modules</h3>
There are currently 13 modules in this library, toplevel, interface_tk, keyConversions, configmodule, initconfig, com.adobe, flash.ui, flash.display, flash.filesystem, flash.utils, flash.events, flash.display3D, and flash.net.
<h4>toplevel</h4>
Most of the functions and classes are implemented but there are some things missing. The inherited properties of many of the classes would be a pain to implement so I left them out for now.
<br><br>As of version 0.0.7 I reimplemented the Array and String class as extensions of the their conterparts from python instead of how I was doing it. I also implemented creating an array to a specified size in the constructor and implemented the length assignment feature (length is a function now not a property). Array.toSize has been merged into length and no longer exists. Unfortunately I can't implement length assignment into an override for the built in __len__ function because it can only take one arguement no matter what. I also added the ability to specify what to fill the empty slots with when using length assignment (not in actionscript).
<br><br>I implemented the type conversions inside a separate function in some of the dataclasses (ex: String._String(exression)). These are used as part of the constructor (__init__ function) but are separate in case they need to be used multiple times or the people using this library want to use it separately. They return values in python types instead of in the types of this module because they are meant to be used internally.
<br><br>For functions that needed a placeholder value for input(s) that aren't easily definable, like multiple possible types or they relied on other factors to be set, I use an empty dictionary as a placeholder. The values that these empty dictionaries represent aren't actually dictionaries, I just used something that would never be used in these functions so that I could detect it.
<h4>interface_tk</h4> 
Unlike the toplevel module, this one has completely different syntax than actionscript had. This module implements dynamic scaling and other things like the adobe flash projector. I will try to make one with similar syntax to actionscript later (no promises).
<h4>keyConversions</h4>
This module is a module that includes cross-platform key conversion functions for tkinter events, javascript (actionscript) keycodes, and mouse buttons (currently only supports united states standard keyboard on linux and windows).
<h4>configmodule</h4>
The module that holds all of the things that this module needs globally or that need to be used many times so I only have to fetch them once (this includes things like the platform and screen resolution).
<h4>initconfig</h4>
The module that is called when this module initializes and its only purpose is to set the variables in configmodule.
<h4>com.adobe, flash.ui, flash.display, flash.filesystem, flash.utils, flash.events, flash.display3D, and flash.net</h4>
These modules contain things from their respective actionscript modules. None of them are complete yet since many actionscript modules rely on each other to function. I have to go back and forth between modules coding things here and there so these are taking much longer than previous modules.
<h3>Config Files</h3>
&lt;library-directory&gt;/mm.cfg - this file is the same as it was in actionscript with the same options as defined <a href="https://web.archive.org/web/20180227100916/helpx.adobe.com/flash-player/kb/configure-debugger-version-flash-player.html">here</a> with the exception of "ClearLogsOnStartup" which I added to configure what it says. Its defualt value is 1 to match the behavior in actionscript.
<br>&lt;library-directory&gt;/configmodule.py - this file "stores" all of the variables needed by many modules while the program is running. It is also used to optimize things by calculating them once and then storing them instead of calculating over and over.
<br>&lt;library-directory&gt;/initconfig.py - initializes the configmodule with the required information. This information includes the current platform, the module directory, the config for the trace function, and details about the screen (width, hight, refresh rate, and color depth) for the display module. Note: use of multiple displays has not been tested yet.
<br>&lt;library-directory&gt;/wayland.cfg - generated on the first use of this module if you are using wayland. Stores all of the values that can't be fetch automatically so you only have to input them once.
