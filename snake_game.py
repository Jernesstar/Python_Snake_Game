from random import randrange
import pygame
from pygame import KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT

from snake import Snake, Controls
from game_modes import (
    OnePlayer_Classic_Snake,
    TwoPlayer_Timed_Snake
)

pygame.init()
pygame.display.set_caption("Snake Game")


class SnakeGame:

    width, height = 300, 300
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    orange = (255, 165, 0)

    message_font = pygame.font.SysFont("arial", 30)
    score_font = pygame.font.SysFont("arial", 20)

    def __init__(self, name_1, name_2 = ""):
        self.clock = pygame.time.Clock()
        self.game_display = pygame.display.set_mode(
            (self.width, self.height)
        )
        self.game_display.fill(self.white)
        pygame.display.update()
        
        self.snake_1 = Snake(
            name_1, self.width, self.height, Controls.KEYS
        )
        if name_2 != "":
            self.snake_2 = Snake(
                name_2, self.width, self.height, Controls.WASD
            )
        self.player_count = 2 if name_2 != "" else 1

        self.classic_snake = OnePlayer_Classic_Snake(
            snake=self.snake_1, 
            clock=self.clock, 
            game_display=self.game_display  
        )
        self.two_player_timed_snake = TwoPlayer_Timed_Snake(
            snake_1=self.snake_1,
            snake_2=self.snake_2,
            clock=self.clock,
            game_display=self.game_display
        )
             
    def end(self):
        pygame.display.quit()
        pygame.quit()
        quit()

    def play(self):
        self.classic_snake.run()
        self.end()

