
from random import randrange
import pygame
from pygame import KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT

from snake import Snake, Controls
from game_modes import OnePlayer_Classic_Snake

pygame.init()
pygame.display.set_caption("Snake Game")


class SnakeGame:

    width, height = 700, 500
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

    def update(self):
        pygame.display.update()
        
        if self.player_count == 2:
            text_2 = self.score_font.render(
                f"{self.snake_2.name}'s score: {self.snake_2.score}",
                True, self.orange
            )
            self.game_display.blit(text_2, [0, 25])

    def draw_snakes(self):
        self.game_display.fill(self.white)

        if self.player_count == 2:
            for x, y, in self.snake_1.pixels:
                pygame.draw.rect(
                    self.game_display,
                    self.black,
                    [x, y, 10, 10]
                )
            for x, y in self.snake_2.pixels:
                pygame.draw.rect(
                    self.game_display,
                    self.black,
                    [x, y, 10, 10]
                    )
        else:
            for x, y, in self.snake_1.pixels:
                pygame.draw.rect(
                    self.game_display,
                    self.black,
                    [x, y, 10, 10]
                )
                    
    def draw_fruits(self, coordinates):
        for x, y in coordinates:
            pygame.draw.rect(
                self.game_display, 
                self.orange, 
                [x, y, 10, 10]
            )

    def rand_x_y(self):
        rand_x = randrange(10, (self.width - 10) / 10.0) * 10.0
        rand_y = randrange(10, (self.height - 10) / 10.0) * 10.0
        return (rand_x, rand_y)

    def game_over_screen(self):
        message = f"Game Over! Score: {self.snake_1.score}"
        text = self.score_font.render(message, True, self.orange)
        game_close = False
        while game_close == False:
            for event in pygame.event.get():
                if event.type == QUIT:
                    game_close = True
            self.game_display.fill(self.white)
            self.game_display.blit(
                text, 
                [(self.width // 2) - 130, (self.height // 2) - 20]
            )
            self.update()

    def winner_screen(self):
        pass
             
    def end(self):
        pygame.display.quit()
        pygame.quit()
        quit()

    def play(self):
        self.classic_snake.run()
        self.end()
