import pygame as pg
from ..tools import load_font


class Text():

    def __init__(
        self,
        text,
        font=(20, None),
        antialias=True,
        foreground='#000000',
        background=None,
        shadow=None # ('#000000', (-2, 2))
    ):
        self.text = str(text)
        self.font = load_font(font)
        self.antialias = antialias
        self.foreground = foreground
        self.background = background
        self.shadow = shadow

        self.render()

    def render(self):
        self.text_surf = self.font.render()

    def draw(self, screen=None):
        screen = pg.display.get_surface() if screen == None else screen
