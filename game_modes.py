import pygame
from pygame import QUIT, KEYDOWN
from snake import Snake

class Game_Mode:

    game_display: pygame.Surface

    def update(self):
        pygame.display.update()
    
    def end(self):
        pygame.display.quit()
        pygame.quit()
        quit()

    def play(self):
        self.run()
        self.end()

    def draw_snake(self):
        for x, y, in self.snake_1.pixels:
            pygame.draw.rect(
                self.game_display,
                self.black,
                [x, y, 10, 10]
            )

    def draw_fruit(self, coordinates):
        (x, y) = coordinates
        pygame.draw.rect(
            self.game_display, 
            self.orange, 
            [x, y, 10, 10]
        )

class Classic_Snake(Game_Mode):
    pass


