import pygame
from pygame import K_ESCAPE, KEYDOWN, QUIT
from pygame.constants import K_LEFT, K_RETURN, K_RIGHT

from snake import Snake, Control

from game_modes import (
    OnePlayer_Classic_Snake,
    TwoPlayer_Snake
)

pygame.init()
pygame.display.set_caption("Snake Game 2.0")


class SnakeGame:

    snake_1: Snake
    snake_2: Snake

    width, height = 1000, 500
    
    black = (0, 0, 0)
    white = (255, 255, 255)

    message_font = pygame.font.Font("resources\\pixel_font.ttf", 40)
    option_font = pygame.font.Font("resources\\pixel_font.ttf", 30)

    def __init__(self, name_1, name_2 = ""):
        self.clock = pygame.time.Clock()
        
        self.snake_1 = Snake(game=self, name=name_1, controls=Control.KEYS)
        self.snake_1.size = 40
    
        if name_2 != "":
            self.snake_2 = Snake(game=self, name=name_2, controls=Control.WASD)
            self.snake_2.size = 40
            
        self.width += self.width % self.snake_1.size
        self.height += self.height % self.snake_1.size
        
        self.game_display = pygame.display.set_mode((self.width, self.height))

        self.background = pygame.image.load(
            "resources\\start_bg.png").convert()
        self.background = pygame.transform.scale(self.background, 
            (self.width, self.height))
        
        self.classic_snake = OnePlayer_Classic_Snake(game=self)
        if name_2 != "":
            self.two_player = TwoPlayer_Snake(game=self)

    def start_screen(self):
        message = "Snake 2.0"
        message_2 = "Press any key to continue"

        text_2 = self.message_font.render(message_2, True, self.white)
       
        colors = [self.black, self.white]
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.end()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.end()
                    else:
                        return
            text = self.message_font.render(message, True, colors[0])
        
            self.game_display.blit(self.background, [0, 0])
            self.game_display.blit(
                text, 
                [(self.width // 2) - 150, 
                (self.height // 2) - self.message_font.get_height()]
            )
            self.game_display.blit(
                text_2, 
                [(self.width // 2) - 250, 
                (self.height // 2)]
            )
            self.clock.tick(self.snake_1.speed)
            self.clock.tick(2)
            colors.reverse()
            pygame.display.update()

    def menu_screen(self):
        x_1 = self.width // 2 - 220
        y = self.height // 2
        x_2 = self.width // 2 + 30

        message = "Choose a game mode to play"
        option_1 = "One Player"
        option_2 = "Two Player"
        
        text = self.message_font.render(message, True, self.white)

        square = pygame.rect.Rect(x_1, y, 170, 50)
        square_2 = pygame.rect.Rect(x_2, y, 170, 50)

        colors = [self.white, self.black]
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.end()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.end()
                    if event.key in (K_LEFT, K_RIGHT):
                        colors.reverse()
                    if event.key == K_RETURN:
                        if colors[0] == self.white:
                            return self.classic_snake
                        if colors[1] == self.white:
                            return self.two_player
     
            self.game_display.blit(self.background, [0, 0])

            pygame.draw.rect(self.game_display, colors[0], square, 3)
            pygame.draw.rect(self.game_display, colors[1], square_2, 3)

            text_1 = self.option_font.render(option_1, True, colors[0])
            text_2 = self.option_font.render(option_2, True, colors[1])

            self.game_display.blit(
                text, 
                [(self.width // 2) - 250, 
                (self.height // 2) - self.message_font.get_height() - 50]
            )
            self.game_display.blit(
                text_1, 
                (square.center[0] - 72, square.center[1] - 12)
            )
            self.game_display.blit(
                text_2, 
                (square_2.center[0] - 74, square_2.center[1] - 12)
            )
            
            pygame.display.update()
                    
    def end(self):
        pygame.display.quit()
        pygame.quit()
        quit()

    def play(self):
        self.start_screen()
        stop = False
        
        while stop == False:
            game_mode = self.menu_screen()
            self.snake_1.reset()
            self.snake_2.reset()
            stop = game_mode.run()

        self.end()