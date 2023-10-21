
class Event:
   def __init__(self, type, bubbles=False, cancelable=False):
      pass

class IEventDispatcher:
   def __init__(self):
      self.eventobjects = {}
   def addEventListener(type, listener, useCapture=False, priority=0, useWeakReference=False):
      pass
   def dispatchEvent(event):
      pass
   def hasEventListener(type):
      pass
   def removeEventListener(type, listener, useCapture=False):
      pass
   def willTrigger(type):
      pass