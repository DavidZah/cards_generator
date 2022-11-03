import math

import svgwrite

width = 512
heigth = 512
card_width = 100
card_heigth = 150
card_spacing = 10
text_fond = "fantasy"


def load_data(path="data.txt"):
    f = open(path, 'r')
    lst = []
    for i in f.readlines():
        lst.append(i)
    return lst


class Boards:
    def __init__(self, lst):
        self.lst = lst
        self.width = 512
        self.heigth = 512
        self.card_width = 100
        self.card_heigth = 50
        self.card_spacing = 10
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
        dwg_card = svgwrite.Drawing("zmenit", (self.width, self.heigth))
        dwg_text = svgwrite.Drawing("zmenit_text", (self.width, self.heigth))
        dwg_combined = svgwrite.Drawing("zmenit_combinace.svg", (self.width, self.heigth))
        for j in range(self.cards_per_colum):
            for i in range(self.cards_per_row):
                try:
                    txt = next(list_iter)
                except StopIteration:
                    break
                dwg_card.add(dwg_card.rect(insert=(self.card_spacing + i * (self.card_width + self.card_spacing),
                                                   self.card_spacing + j * (self.card_heigth + self.card_spacing)),
                                           size=(self.card_width, self.card_heigth), fill='white',
                                           stroke='black', stroke_width=3, rx=self.rx, ry=self.ry))
                dwg_text.add(
                    dwg_text.text(txt, (self.card_spacing + i * (self.card_width + self.card_spacing),
                                        self.card_spacing + j * (self.card_heigth + self.card_spacing)),
                                  font_family="fantasy", font_size='15', text_anchor='start', fill='black'))

                dwg_combined.add(
                    dwg_combined.rect(insert=(self.card_spacing + i * (self.card_width + self.card_spacing),
                                              self.card_spacing + j * (self.card_heigth + self.card_spacing)),
                                      size=(self.card_width, self.card_heigth), fill='white',
                                      stroke='black', stroke_width=3, rx=self.rx, ry=self.ry))
                dwg_combined.add(
                    dwg_combined.text(txt, (self.card_spacing + i * (self.card_width + self.card_spacing),
                                            self.card_spacing + j * (
                                                    self.card_heigth + self.card_spacing)),
                                      font_family="fantasy", font_size='15', text_anchor='start', fill='black'))

                dwg_combined.text()


        dwg_combined.save()


if __name__ == "__main__":
    lst = load_data()
    board = Boards(lst)
    board.boar_draw()
