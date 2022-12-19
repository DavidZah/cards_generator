# -*- coding: utf-8 -*-
import math
import svgwrite
import dxfwrite
from dxfwrite import DXFEngine as dxf
from dxfwrite.const import CENTER, MIDDLE
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

width = 60
heigth = 60
card_width = 3
card_heigth = 2
card_spacing = 1
text_fond = "fantasy"


def load_data(path="data.txt"):
    f = open(path, 'r', encoding="utf-8")
    lst = []
    for i in f.readlines():
        lst.append(i)
    return lst


def get_rect(msp, width, heigth, radius, set_point=(0, 0)):
    msp.add_line((set_point[0] + radius, set_point[1]), (set_point[0] + width - radius, set_point[1]))
    x = (set_point[0] + width - radius, set_point[1])
    y = (set_point[0] + width, set_point[1] - radius)
    arc = ConstructionArc.from_2p_radius(
        start_point=x, end_point=y, radius=radius, ccw=False
    )
    arc.add_to_layout(msp, dxfattribs=attribs)

    msp.add_line((set_point[0] + width, set_point[1] - radius), (set_point[0] + width, set_point[1] - heigth + radius))
    x = (set_point[0] + width, set_point[1] - heigth + radius)
    y = (set_point[0] + width - radius, set_point[1] - heigth)
    arc = ConstructionArc.from_2p_radius(
        start_point=x, end_point=y,
        radius=radius, ccw=False
    )
    arc.add_to_layout(msp, dxfattribs=attribs)

    msp.add_line((set_point[0] + radius, set_point[1] - heigth), (set_point[0] + width - radius, set_point[1] - heigth))
    x = (set_point[0] + radius, set_point[1] - heigth)
    y = (set_point[0], set_point[1] - heigth + radius)
    arc = ConstructionArc.from_2p_radius(
        start_point=x,
        end_point=y,
        radius=radius, ccw=False
    )
    arc.add_to_layout(msp, dxfattribs=attribs)

    msp.add_line((set_point[0], set_point[1] - radius), (set_point[0], set_point[1] - heigth + radius))
    x = (set_point[0], set_point[1] - radius)
    y = (set_point[0] + radius, set_point[1])

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


def add_text(msp, text, pos, length=1):
    # MOVe later

    z = ezdxf.math.Matrix44()
    z = z.translate(pos[0], pos[1], 0)
    attr = {"layer": "OUTLINE", "color": 1}
    ff = fonts.FontFace(family="monospace")
    s = text
    align = TextEntityAlignment.MIDDLE_CENTER
    data = text2path.make_paths_from_str(s, ff, align=align, m=z, length=length, size=5)

    path.render_lwpolylines(
        msp, data, dxfattribs=attr
    )

    attr["layer"] = "FILLING"
    attr["color"] = 2
    for hatch in text2path.make_hatches_from_str(
            s, ff, align=align, dxfattribs=attr
    ):
        msp.add_entity(hatch)


    return msp


class Boards:
    def __init__(self, lst):
        self.lst = lst
        self.width = 330
        self.heigth = 500
        self.card_width = 70
        self.card_heigth = 40
        self.card_spacing = 2
        self.text_fond = "fantasy"
        self.calculate_num_of_cards()
        self.num_of_cards = len(lst)
        # ToDo change to better names
        self.rx = 1
        self.ry = 1

    def calculate_num_of_cards(self):
        cards_per_row = (self.width / (self.card_spacing + self.card_width))
        self.cards_per_row = math.floor(cards_per_row)
        cards_per_colum = self.heigth / (self.card_spacing + self.card_heigth)
        self.cards_per_colum = math.floor(cards_per_colum)
        self.cards_per_board = self.cards_per_colum * self.cards_per_row

    def boar_draw(self):
        list_iter = iter(self.lst)

        doc = ezdxf.new("R2010", setup=True)
        doc.units = units.CM

        dxf_card = ezdxf.new("R2010", setup=True)
        dxf_card.units = units.CM
        msp_card = dxf_card.modelspace()
        dxf_text = ezdxf.new("R2010", setup=True)
        dxf_text.units = units.CM
        msp_text = dxf_text.modelspace()
        dxf_combined = ezdxf.new("R2010", setup=True)
        dxf_combined.units = units.CM
        msp_combined = dxf_combined.modelspace()

        msp_text.add_circle((self.width+self.card_spacing/2,self.heigth-self.card_heigth+self.card_spacing),0.1)
        msp_card.add_circle((self.width+self.card_spacing/2,self.heigth-self.card_heigth+self.card_spacing),0.1)
        msp_combined.add_circle((self.width+self.card_spacing/2,self.heigth-self.card_heigth+self.card_spacing),0.1)
        for j in range(self.cards_per_colum):
            for i in range(self.cards_per_row):
                try:
                    txt = next(list_iter).rstrip()
                except StopIteration:
                    break
                msp_card = get_rect(msp_card, self.card_width, self.card_heigth, 5,
                                    (self.card_spacing + i * (self.card_width + self.card_spacing),
                                     self.card_spacing + j * (self.card_heigth + self.card_spacing)))

                msp_text = add_text(msp_text, txt, (
                    self.card_spacing + i * (self.card_width + self.card_spacing) + self.card_width / 2,
                    self.card_spacing + j * (self.card_heigth + self.card_spacing) - self.card_heigth / 2),
                                    length=self.card_width * 0.9)

                msp_combined = get_rect(msp_combined, self.card_width, self.card_heigth, 5,
                                        (self.card_spacing + i * (self.card_width + self.card_spacing),
                                         self.card_spacing + j * (self.card_heigth + self.card_spacing)))

                msp_combined = add_text(msp_combined, txt, (
                self.card_spacing + i * (self.card_width + self.card_spacing) + self.card_width / 2,
                self.card_spacing + j * (self.card_heigth + self.card_spacing) - self.card_heigth / 2),
                                        length=self.card_width * 0.9)
        dxf_card.saveas("card.dxf")
        dxf_text.saveas("text.dxf")
        dxf_combined.saveas("combined.dxf")


if __name__ == "__main__":
    lst = load_data()
    board = Boards(lst)
    board.boar_draw()
