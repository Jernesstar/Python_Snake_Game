import pygame
from pygame import K_ESCAPE, KEYDOWN, QUIT

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

    width, height = 600, 300
    
    black = (0, 0, 0)
    white = (255, 255, 255)

    message_font = pygame.font.Font("resources\\pixel_font.ttf", 40)
    
    def __init__(self, name_1, name_2 = ""):
        self.clock = pygame.time.Clock()
        
        self.snake_1 = Snake(game=self, name=name_1, controls=Control.WASD)
        self.snake_1.size = 40
    
        if name_2 != "":
            self.snake_2 = Snake(game=self, name=name_2, controls=Control.WASD)
            self.snake_2.size = 40
            
        self.width += self.width % self.snake_1.size
        self.height += self.height % self.snake_1.size
        
        self.game_display = pygame.display.set_mode((self.width, self.height))
        
        self.classic_snake = OnePlayer_Classic_Snake(game=self)
        if name_2 != "":
            self.two_player = TwoPlayer_Snake(game=self)

    def start_screen(self):
        message = "Welcome to the snake game!"
        message_2 = "Press any key to continue"

        text = self.message_font.render(message, True, self.white)
        text_2 = self.message_font.render(message_2, True, self.white)

        background = pygame.image.load("resources\\start_bg.png").convert()
        background = pygame.transform.scale(
            background, (self.width, self.height))
       
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.end()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.end()
                    else:
                        return
            self.game_display.blit(background, [0, 0])
            self.game_display.blit(
                text, 
                [(self.width // 2) - 270, 
                (self.height // 2) - self.message_font.get_height()]
            )
            self.game_display.blit(
                text_2, 
                [(self.width // 2) - 250, 
                (self.height // 2)]
            )
            pygame.display.update()

    def menu_screen(self):
        pass
                
    def end(self):
        pygame.display.quit()
        pygame.quit()
        quit()

    def play(self):
        self.start_screen()

        stop = False
        while stop == False:
            self.snake_1.reset()
            self.snake_2.reset()
            stop = self.classic_snake.run()

        self.end()