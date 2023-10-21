from as3lib import toplevel as as3
from as3lib import flash.net as fn
from typing import Union
import binascii

def clearInterval():
   pass
def clearTimeout():
   pass
def describeType():
   pass
def escapeMultiByte():
   pass
def getDefinitionByName():
   pass
def getQualifiedClassName():
   pass
def getQualifiedSuperclassName():
   pass
def getTimer():
   pass
def setInterval():
   pass
def setTimeout():
   pass
def unescapeMultiByte():
   pass

class IDataInput:
   pass
class IDataOutput:
   pass

class ByteArray:
   def __init__(self):
      self.bytesAvailable = ""
      self.defaultObjectEncoding = fn.ObjectEncoding.AMF3
      self.endian = Endian.BIG_ENDIAN
      self.objectEncoding = ""
      self.position = 0
      self.shareable = ""
      self.byteArray = {"bin":"","hex":""}
   def __len__(self):
      return len(self.byteArray)
   def _postition(self, pos):
      self.position = pos
      self.bytesAvailable = len(self.byteArray) - pos
   def length(self):
      return len(self.byteArray)
   def loadBytes(self, filepath="", bytestring=""):
      if filepath == bytestring == "":
         pass
      elif filepath != "" and bytestring != "":
         as3.trace("ByteArray Error","loadBytes; Both filepath and bytestring provided.",isError=True)
      else:
         if filepath != "":
            with open(filepath, "rb") as a:
               self.byteArray["hex"] = f"{binascii.hexlify(a.read())}".replace("b'","").replace("'","")
            self.byteArray["bin"] = bin(int(self.byteArray["hex"], 16))[2:].zfill(len(self.byteArray["hex"]) * 4)
         else:
            pass
   def atomicCompareAndSwapIntAt():
      pass
   def atomicCompareAndSwapLengthAt():
      pass
   def clear(self):
      self.byteArray = bytearray()
      self.length = 0
      self._postition(0)
   def compress():
      pass
   def deflate():
      pass
   def inflate():
      pass
   def readBoolean():
      pass
   def readByte():
      pass
   def readBytes():
      pass
   def readDouble():
      pass
   def readInt():
      pass
   def readMultiByte():
      pass
   def readObject():
      pass
   def readShort():
      pass
   def readUnsignedByte():
      pass
   def readUnsignedInt():
      pass
   def readUnsignedShort():
      pass
   def readUTF():
      pass
   def readUTFBytes():
      pass
   def toJSON():
      pass
   def toString():
      pass
   def uncompress():
      pass
   def writeBoolean():
      pass
   def writeByte():
      pass
   def writeBytes():
      pass
   def writeDouble():
      pass
   def writeFloat():
      pass
   def writeInt():
      pass
   def writeMultiByte():
      pass
   def writeObject():
      pass
   def writeShort():
      pass
   def writeUnsignedInt():
      pass
   def writeUTF():
      pass
   def writeUTFBytes():
      pass
class CompressionAlgorithm:
   DEFLATE = "deflate"
   LZMA = "lzma"
   ZLIB = "zlib"
class Dictionary:
   pass
class Endian:
   BIG_ENDIAN = "bigEndian"
   LITTLE_ENDIAN = "littleEndian"
class Timer:
   pass