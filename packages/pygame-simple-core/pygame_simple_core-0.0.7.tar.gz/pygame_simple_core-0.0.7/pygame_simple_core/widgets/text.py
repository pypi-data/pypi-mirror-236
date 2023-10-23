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
        self.text_surf = self.font.render(
            self.text, self.antialias, self.foreground)
        self.text_rect = self.text_surf.get_rect()

        if self.shadow != None:
            shadow_color = self.shadow[0]
            shadow_pos_x = self.shadow[1][0]
            shadow_pos_y = self.shadow[1][1]

            self.shadow_surf = self.font.render(
                self.text, self.antialias, shadow_color)
            self.shadow_rect = self.shadow_surf.get_rect()

            if shadow_pos_x >= 0:
                self.shadow_rect.move_ip(shadow_pos_x, 0)
            else:
                self.text_rect.move_ip(-shadow_pos_x, 0)

            if shadow_pos_y >= 0:
                self.shadow_rect.move_ip(0, shadow_pos_y)
            else:
                self.text_rect.move_ip(0, -shadow_pos_y)

            left = min(self.shadow_rect.left, self.text_rect.left)
            right = max(self.shadow_rect.right, self.text_rect.right)
            top = min(self.shadow_rect.top, self.text_rect.top)
            bottom = max(self.shadow_rect.bottom, self.text_rect.bottom)
            width = right - left
            height = bottom - top

            self.surf = pg.Surface((width, height), pg.SRCALPHA)
            self.rect = self.surf.get_rect()

            if self.background != None:
                self.surf.fill(self.background)

            self.surf.blit(self.shadow_surf, self.shadow_rect)
            self.surf.blit(self.text_surf, self.text_rect)
        else:
            self.surf = self.text_surf
            self.rect = self.text_rect

    def draw(self, screen=None):
        screen = pg.display.get_surface() if screen == None else screen

        screen.blit(self.surf, self.rect)
