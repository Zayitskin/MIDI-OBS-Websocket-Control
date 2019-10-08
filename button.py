import pygame

class Button():

    def __init__(self, loc, size, text = None, font = None):
        self.image = pygame.Surface((size))
        self.image.fill([100, 100, 100])
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, [0, 0, 0], self.rect, 3)
        self.rect.x, self.rect.y = loc[0], loc[1]
        self.text = text
        if font == None:
            font = pygame.font.SysFont("comicsans", 24)
        if text != None:
            render = font.render(text, False, [0, 0, 0])
            self.image.blit(render,
                            (self.image.get_width() // 2 - render.get_width() // 2,
                             self.image.get_height() // 2 - render.get_height() // 2))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

def buildButtonArray(stringlist, font = None, startx = 0, endx = 1600, starty = 0, endy = 900):
    out = []
    x, y = startx, starty
    for string in stringlist:
        out.append(Button((x, y), (100, 100), string, font))
        x += 100
        if x >= endx:
            x = startx
            y += 100
    return out
