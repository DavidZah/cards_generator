import ezdxf
from ezdxf.addons import text2path
from ezdxf.enums import TextEntityAlignment
from ezdxf.math import ConstructionArc
from ezdxf.gfxattribs import GfxAttribs
import pathlib
import ezdxf
from ezdxf import path, zoom, units
from ezdxf.tools import fonts
from ezdxf.addons import text2path
from ezdxf.enums import TextEntityAlignment



def get_rect(msp,width,heigth,radius,set_point= (0,0)):
    msp.add_line((set_point[0]+radius,set_point[1]), (set_point[0]+width-radius, set_point[1]))
    x = (set_point[0]+width-radius,set_point[1])
    y = (set_point[0] + width, set_point[1] - radius)
    arc = ConstructionArc.from_2p_radius(
        start_point=x, end_point=y, radius=radius, ccw=False
    )
    arc.add_to_layout(msp, dxfattribs=attribs)




    msp.add_line((set_point[0]+width, set_point[1]-radius), (set_point[0]+width,set_point[1]-heigth+radius))
    x = (set_point[0]+width,set_point[1]-heigth+radius)
    y = (set_point[0]+width-radius, set_point[1] - heigth)
    arc = ConstructionArc.from_2p_radius(
        start_point=x, end_point=y,
        radius=radius, ccw=False
    )
    arc.add_to_layout(msp, dxfattribs=attribs)



    msp.add_line((set_point[0]+radius,set_point[1]-heigth), (set_point[0]+width-radius, set_point[1]-heigth))
    x = (set_point[0] + radius, set_point[1]-heigth)
    y = (set_point[0], set_point[1]-heigth + radius)
    arc = ConstructionArc.from_2p_radius(
        start_point=x,
        end_point=y,
        radius=radius, ccw=False
    )
    arc.add_to_layout(msp, dxfattribs=attribs)



    msp.add_line((set_point[0] , set_point[1]-radius), (set_point[0], set_point[1]-heigth + radius))
    x = (set_point[0] , set_point[1]-radius)
    y = (set_point[0]+radius,set_point[1])

    arc = ConstructionArc.from_2p_radius(
        start_point=x,
        end_point=y,
        radius=radius, ccw=False
    )
    arc.add_to_layout(msp, dxfattribs=attribs)

    return msp

doc = ezdxf.new("R2010", setup=True)
doc.units = units.CM
msp = doc.modelspace()
attribs = GfxAttribs(layer="ENTITY")


def add_text(msp,text,pos,length = 1):
    z = ezdxf.math.Matrix44()
    z = z.translate(pos[0],pos[1],0)
    attr = {"layer": "OUTLINE", "color": 1}
    ff = fonts.FontFace(family="OpenSans")
    s = text
    align = TextEntityAlignment.ALIGNED
    path.render_splines_and_polylines(
    msp, text2path.make_paths_from_str(s, ff, align=align,m = z,length = length), dxfattribs=attr
    )

    attr["layer"] = "FILLING"
    attr["color"] = 2
    for hatch in text2path.make_hatches_from_str(
            s, ff, align=align, dxfattribs=attr
    ):
        msp.add_entity(hatch)
    return msp

get_rect(msp,7,4,0.5)
add_text(msp,"David",(3.5,-3),length = 7*0.95)
doc.saveas("test.dxf")