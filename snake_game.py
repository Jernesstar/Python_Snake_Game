from random import randrange
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

    width, height = 500, 500
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    orange = (255, 165, 0)

    message_font = pygame.font.SysFont("arial", 30)
    score_font = pygame.font.SysFont("arial", 20)

    def __init__(self, name_1, name_2 = ""):
        self.clock = pygame.time.Clock()
        self.game_display = pygame.display.set_mode((self.width, self.height))
        self.game_display.fill(self.white)
        pygame.display.update()
        
        self.snake_1 = Snake(game=self, name=name_1, controls=Control.KEYS)
    
        if name_2 != "":
            self.snake_2 = Snake(game=self, name=name_2, controls=Control.WASD)
            self.two_player_snake = TwoPlayer_Snake(game=self)
            
        self.classic_snake = OnePlayer_Classic_Snake(game=self)
                
    def end(self):
        pygame.display.quit()
        pygame.quit()
        quit()

    def play(self):
        # self.classic_snake.run()
        self.two_player_snake.run()
        self.end()

