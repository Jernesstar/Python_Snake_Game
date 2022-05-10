
from random import randrange
import pygame
from pygame import KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT

from snake import Controls
from snake import Snake

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

    def update(self):
        pygame.display.update()

    def show_scores(self):
        text_1 = self.score_font.render(
            f"{self.snake_1.name}'s score: {self.snake_1.score}",
            True, self.orange
        )
        self.game_display.blit(text_1, [0, 0])
        
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

    def run(self):
        game_over, game_close = False, False  
        
        self.snake_1.head_x = 250
        self.snake_1.head_y = 250

        if self.player_count == 2:
            self.snake_2.pixels.append(
                (250, 250)
            )
            
        delta_x_1 = 0
        delta_x_2 = 0
        delta_y_1 = 0 
        delta_y_2 = 0
        
        foods = [self.rand_x_y() for _ in range(5)]
        
        while (game_over, game_close) == (False, False):
            for event in pygame.event.get():
                if event.type == QUIT:
                    game_close = True
                elif event.type == KEYDOWN:
                    if self.player_count == 2:
                        (delta_x_1, delta_y_1) = self.snake_1.directions(event)
                        (delta_x_2, delta_y_2) = self.snake_2.directions(event)
                    else:
                        (delta_x_1, delta_y_1) = self.snake_1.directions(event)

            if self.player_count == 2:
                (i, snake_1_game_over) = self.snake_1.move(
                    delta_x_1, delta_y_1, foods)

                (j, snake_2_game_over) = self.snake_2.move(
                    delta_x_2, delta_y_2, foods)

                if i != -1:
                    foods.pop(i)
                    foods.append(self.rand_x_y())
                if j != -1:
                    foods.pop(j)
                    foods.append(self.rand_x_y())
            else:
                (i, snake_1_game_over) = self.snake_1.move(
                    delta_x_1, delta_y_1, foods)
                    
                if i != -1:
                    foods.pop(i) 
                    foods.append(self.rand_x_y())
            
            self.draw_snakes()
            self.draw_fruits(foods)
            self.show_scores()
            self.clock.tick(self.snake_1.speed)
            self.update()
             
    def end(self):
        pygame.display.quit()
        pygame.quit()
        quit()

    def play(self):
        self.run()
        self.end()
