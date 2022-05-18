from random import randrange
from typing import Any

import pygame
from pygame import KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT

from snake import Snake, Control
from game_modes import (
    OnePlayer_Classic_Snake,
    TwoPlayer_Snake
)

pygame.init()
pygame.display.set_caption("Snake Game")


class SnakeGame:

    snake: Snake
    snake_2: Snake

    width, height = 1000, 600
    
    black = (0, 0, 0)
    white = (255, 255, 255)

    message_font = pygame.font.SysFont("arial", 30)
    
    def __init__(self, name_1, name_2 = ""):
        self.clock = pygame.time.Clock()
        self.game_display = pygame.display.set_mode((self.width, self.height))
        pygame.display.update()
        
        self.snake_1 = Snake(game=self, name=name_1, controls=Control.KEYS)
        self.snake_1.size = 40
    
        if name_2 != "":
            self.snake_2 = Snake(game=self, name=name_2, controls=Control.WASD)
            self.snake_2.size = 50
            self.two_player_snake = TwoPlayer_Snake(game=self)
            
        self.classic_snake = OnePlayer_Classic_Snake(game=self)

    def start_screen(self):
        message = "Welcome to the snake game!"
        message_2 = "Press any key to continue"

        text = self.message_font.render(message, True, self.black)
        text_2 = self.message_font.render(message_2, True, self.black)

        background = pygame.image.load("resources\\start_bg.png").convert()
        background = pygame.transform.scale(
            background, (self.width, self.height))
       
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.end()
                if event.type == KEYDOWN:
                    return
            self.game_display.blit(background, [0, 0])
            self.game_display.blit(
                text, 
                [(self.width // 2) - 170, 
                (self.height // 2) - 25]
            )
            self.game_display.blit(
                text_2, 
                [(self.width // 2) - 150, 
                (self.height // 2)]
            )
            pygame.display.update()
                
    def end(self):
        pygame.display.quit()
        pygame.quit()
        quit()

    def play(self):
        self.start_screen()
        self.classic_snake.run()
        # self.two_player_snake.run()
        self.end()