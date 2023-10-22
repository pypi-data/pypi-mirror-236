import pygame as pg
from . import font_finder


def load_font(font):
    font_size = font[0]
    font_args = font[1:]

    font_path = font_finder.find_font(*font_args)

    if font_path == None:
        font = pg.font.SysFont(None, font_size)
    else:
        font = pg.font.Font(font_path, font_size)

    return font
