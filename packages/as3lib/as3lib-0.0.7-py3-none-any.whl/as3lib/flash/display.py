from as3lib import configmodule, toplevel
from typing import Union

class as3totk:
   def anchors(flashalign:Union[str, toplevel.String]):
      match flashalign:
         case "B":
            return "s"
         case "BL":
            return "sw"
         case "BR":
            return "se"
         case "L":
            return "w"
         case "R":
            return "e"
         case "T":
            return "n"
         case "TL":
            return "nw"
         case "TR":
            return "ne"

class ActionScriptVersion:
   ACTIONSCRIPT2 = 2
   ACTIONSCRIPT3 = 3
class AVLoader:
   pass
class AVM1Movie:
   pass
class Bitmap:
   pass
class BitmapData:
   pass
class BitmapDataChannel:
   pass
class BitmapEncodingColorSpace:
   COLORSPACE_4_2_0 = "4:2:0"
   COLORSPACE_4_2_2 = "4:2:2"
   COLORSPACE_4_4_4 = "4:4:4"
   COLORSPACE_AUTO = "auto"
class BlendMode:
   ADD = "add"
   ALPHA = "alpha"
   DARKEN = "darken"
   DIFFERENCE = "difference"
   ERASE = "erase"
   HARDLIGHT = "hardlight"
   INVERT = "invert"
   LAYER = "layer"
   LIGHTEN = "lighten"
   MULTIPLY = "multiply"
   NORMAL = "normal"
   OVERLAY = "overlay"
   SCREEN = "screen"
   SHADER = "shader"
   SUBTRACT = "subtract"
class CapsStyle:
   NONE = "none"
   ROUND = "round"
   SQUARE = "square"
class ColorCorrection:
   DEFAULR = "default"
   OFF = "off"
   ON = "on"
class ColorCorrectionSupport:
   DEFAULT_OFF = "defaultOff"
   DEFAULT_ON = "defualtOn"
   UNSUPPORTED = "unsupported"
class DisplayObject:
   pass
class DisplayObjectContainer:
   pass
class FocusDirection:
   BOTTOM = "bottom"
   NONE = "none"
   TOP = "top"
class FrameLabel:
   pass
class GradientType:
   LINEAR = "linear"
   RADIAL = "radial"
class Graphics:
   pass
class GraphicsBitmapFill:
   pass
class GraphicsEndFill:
   pass
class GraphicsGradientFill:
   pass
class GraphicsPath:
   pass
class GraphicsPathCommand:
   pass
class GraphicsPathWinding:
   pass
class GraphicsShaderFill:
   pass
class GraphicsSolidFill:
   pass
class GraphicsStroke:
   pass
class GraphicsTrianglePath:
   pass
class GraphicsObject:
   pass
class InterpolationMethod:
   LINEAR_RGB = "linearRGB"
   RGB = "rgb"
class JointStyle:
   BEVEL = "bevel"
   MITER = "miter"
   ROUND = "round"
class JPEGEncoderOptions:
   pass
class JPEGCREncoderOptions:
   pass
class LineScaleMode:
   HORIZONTAL = "horizontal"
   NONE = "none"
   NORMAL = "normal"
   VERTICAL = "vertical"
class Loader:
   pass
class LoderInfo:
   pass
class MorphShape:
   pass
class MovieClip:
   pass
class NativeMenu:
   pass
class NativeMenuItem:
   pass
class NativeWindow:
   pass
class NativeWindowDisplayState:
   MAXIMIZED = "maximized"
   MINIMIZED = "minimized"
   NORMAL = "normal"
class NativeWindowInitOptions:
   pass
class NativeWindowRenderMode:
   AUTO = "auto"
   CPU = "cpu"
   DIRECT = "direct"
   GPU = "gpu"
class NativeWindowResize:
   BOTTOM = "B"
   BOTTOM_LEFT = "BL"
   BOTTOM_RIGHT = "BR"
   LEFT = "L"
   RIGHT = "R"
   TOP = "T"
   TOP_LEFT = "TL"
   TOP_RIGHT = "TR"
class NativeWindowSystemChrome:
   ALTERNATE = "alternate"
   NONE = "none"
   STANDARD = "standard"
class NativeWindowType:
   LIGHTWEIGHT = "lightweight"
   NORMAL = "normal"
   UTILITY = "utility"
class PixelSnapping:
   ALWAYS = "always"
   AUTO = "auto"
   NEVER = "never"
class PNGEncoderOptions:
   pass
class Scene:
   pass
class SceneMode:
   pass
class Screen:
   pass
class ScreenMode:
   colorDepth = configmodule.colordepth
   height = configmodule.height
   refreshRate = configmodule.refreshrate
   width = configmodule.width
class Shader:
   pass
class ShaderData:
   pass
class ShaderInput:
   pass
class ShaderJob:
   pass
class ShaderParameter:
   pass
class ShaderParameterType:
   BOOL = "bool"
   BOOL2 = "bool2"
   BOOL3 = "bool3"
   BOOL4 = "bool4"
   FLOAT = "float"
   FLOAT2 = "float2"
   FLOAT3 = "float3"
   FLOAT4 = "float4"
   INT = "int"
   INT2 = "int2"
   INT3 = "int3"
   INT4 = "int4"
   MATRIX2X2 = "matrix2x2"
   MATRIX3X3 = "matrix3x3"
   MATRIX4X4 = "matrix4x4"
class ShaderPrecision:
   FAST = "fast"
   FULL = "full"
class Shape:
   pass
class SimpleButtom:
   pass
class SpreadMethod:
   PAD = "pad"
   REFLECT = "reflect"
   REPEAT = "repeat"
class Sprite:
   pass
class Stage:
   pass
class Stage3D:
   pass
class StageAlign:
   BOTTOM = "B"
   BOTTOM_LEFT = "BL"
   BOTTOM_RIGHT = "BR"
   LEFT = "L"
   RIGHT = "R"
   TOP = "T"
   TOP_LEFT = "TL"
   TOP_RIGHT = "TR"
class StageAspectRatio:
   ANY = "any"
   LANDSCAPE = "landscape"
   PORTRAIT = "portrait"
class StageDisplayState:
   FULL_SCREEN = "fullScreen"
   FULL_SCREEN_INTERACTIVE = "fullScreenInteractive"
   NORMAL = "normal"
class StageOrientation:
   DEFAULT = "default"
   ROTATED_LEFT = "rotatedLeft"
   ROTATED_RIGHT = "rotatedRight"
   UNKNOWN = "unknown"
   UPSIDE_DOWN = "upsideDown"
class StageQuality:
   BEST = "best"
   HIGH = "high"
   HIGH_16X16 = "16x16"
   HIGH_16X16_LINEAR = "16x16linear"
   HIGH_8X8 = "8x8"
   HIGH_8X8_LINEAR = "8x8linear"
   LOW = "low"
   MEDIUM = "medium"
class StageScaleMode:
   EXACT_FIT = "exactFit"
   NO_BORDER = "noBorder"
   NO_SCALE = "noScale"
   SHOW_ALL = "showAll"
class SWFVersion:
   FLASH1 = 1
   FLASH2 = 2
   FLASH3 = 3
   FLASH4 = 4
   FLASH5 = 5
   FLASH6 = 6
   FLASH7 = 7
   FLASH8 = 8
   FLASH9 = 9
   FLASH10 = 10
   FLASH11 = 11
class TriangleCulling:
   NEGATIVE = "negative"
   NONE = "none"
   POSITIVE = "positive"
