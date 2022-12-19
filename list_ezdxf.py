import dxfwrite

import dxfwrite
from dxfwrite import DXFEngine as dxf
from dxfwrite.const import CENTER, MIDDLE

name="rectangle.dxf"
drawing = dxf.drawing(name)

drawing.add(dxf.rectangle((0,0),5,5,halign= "CENTER",valign  = "MIDLE"))
drawing.add(dxf.text('aligned Text',insert = (2.5,2.5),alignpoint =(2.5,2.5) ,halign=CENTER,valign = MIDDLE))
drawing.save()
print("drawing '%s' created.\n" % name)
