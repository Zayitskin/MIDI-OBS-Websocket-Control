import pygame, sys
from button import Button, buildButtonArray

class Tool:

    def __init__(self, queue = None):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        self.queue = queue
        
        buttons = []
        for i in range(1, 29):
            buttons.append("note_on " + str(i))
            buttons.append("note_off " + str(i))
            
        self.buttons = buildButtonArray(buttons, None, 0, 800, 0, 800)

    def eventHandler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.queue.put("SHUTDOWN")
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.rect.collidepoint(pos):
                        if self.queue != None:
                            self.queue.put(button.text)
                        else:
                            print(button.text)

    def run(self):
        self.eventHandler()
        for button in self.buttons:
            button.draw(self.screen)
        pygame.display.flip()

def toolLoop(queue):
    tool = Tool(queue)
    while True:
        tool.run()

if __name__ == "__main__":
    tool = Tool()
    while True:
        tool.run()
