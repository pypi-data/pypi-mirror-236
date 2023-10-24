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
        shadow=None, # ('#000000', (-2, 2))
        spacement=0.1
    ):
        self.text = str(text)
        self.font = load_font(font)
        self.antialias = antialias
        self.foreground = foreground
        self.background = background
        self.shadow = shadow
        self.spacement = spacement
        self.lines = [self.render_line(line) for line in self.split_lines()]
        self.render()

    def split_lines(self):
        return self.text.split('\n')

    def render_line(self, text):
        background = self.background if self.shadow == None else None

        text_surf = self.font.render(
            text, self.antialias, self.foreground, background)
        text_rect = text_surf.get_rect()

        if self.shadow != None:
            shadow_color = self.shadow[0]
            shadow_pos_x = self.shadow[1][0]
            shadow_pos_y = self.shadow[1][1]

            shadow_surf = self.font.render(
                text, self.antialias, shadow_color)
            shadow_rect = shadow_surf.get_rect()

            if shadow_pos_x >= 0:
                shadow_rect.move_ip(shadow_pos_x, 0)
            else:
                text_rect.move_ip(-shadow_pos_x, 0)

            if shadow_pos_y >= 0:
                shadow_rect.move_ip(0, shadow_pos_y)
            else:
                text_rect.move_ip(0, -shadow_pos_y)

            left = min(shadow_rect.left, text_rect.left)
            right = max(shadow_rect.right, text_rect.right)
            top = min(shadow_rect.top, text_rect.top)
            bottom = max(shadow_rect.bottom, text_rect.bottom)
            width = right - left
            height = bottom - top

            surf = pg.Surface((width, height), pg.SRCALPHA)
            rect = surf.get_rect()

            if self.background != None:
                surf.fill(self.background)

            surf.blit(shadow_surf, shadow_rect)
            surf.blit(text_surf, text_rect)
        else:
            surf = text_surf
            rect = text_rect

        if self.background == None:
            surf = surf.convert_alpha()
        else:
            surf = surf.convert()

        return surf, rect

    def render(self):
        if len(self.lines) > 1:
            surfs = []
            rects = []

            for surf, rect in self.lines:
                surfs.append(surf)
                rects.append(rect)

            height = max([rect.height for rect in rects])
            spacement = height + height * self.spacement

            for i, rect in enumerate(rects):
                rect.move_ip(0, spacement * i)

            left = min([rect.left for rect in rects])
            right = max([rect.right for rect in rects])
            top = min([rect.top for rect in rects])
            bottom = max(rect.bottom for rect in rects)
            width = right - left
            height = bottom - top

            surf = pg.Surface((width, height), pg.SRCALPHA)
            rect = pg.Rect(left, right, width, height)

            if self.background:
                surf.fill(self.background)

            for s, r in zip(surfs, rects):
                surf.blit(s, r)

            if self.background == None:
                surf = surf.convert_alpha()
            else:
                surf = surf.convert()

            self.surf = surf
            self.rect = rect
        else:
            self.surf, self.rect = self.lines[0]

    def draw(self, screen=None):
        screen = pg.display.get_surface() if screen == None else screen

        screen.blit(self.surf, self.rect)
