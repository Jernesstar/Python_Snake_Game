from random import randrange
import pygame
from pygame import QUIT, KEYDOWN
from pygame import (
    K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_s, K_a, K_d
)
from snake import Snake

pygame.init()

class Game_Mode(object):

    snake: Snake
    clock: pygame.time.Clock
    game_display: pygame.Surface

    display_width, display_height = 700, 500

    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    orange = (255, 165, 0)

    message_font = pygame.font.SysFont("arial", 30)
    score_font = pygame.font.SysFont("arial", 20)

    def __init__(
        self, 
        game
    ):
        self.snake = game.snake_1
        self.clock = game.clock
        self.game_display = game.game_display
        self.display_width = game.snake_1.display_width
        self.display_height = game.snake_1.display_height
    
    def run(self):
        pass

    def play(self):
        self.run()
        self.end()

    def update(self):
        pygame.display.update()
    
    def end(self):
        pygame.display.quit()
        pygame.quit()
        quit()
    
    def check_for_out_of_bounds(self):
        if self.snake.head_x >= self.display_width:
            self.snake.head_x = 0
        elif self.snake.head_x <= -10:
            self.snake.head_x = self.display_width
        elif self.snake.head_y >= self.display_height:
            self.snake.head_y = 0
        elif self.snake.head_y <= -10:
            self.snake.head_y = self.display_height

    def show_scores(self):
        text_1 = self.score_font.render(
            f"{self.snake.name}'s score: {self.snake.score}",
            True, self.orange
        )
        self.game_display.blit(text_1, [0, 0])

    def draw_snake(self):
        for x, y, in self.snake.pixels:
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
        
    def rand_x_y(self):
        rand_x = randrange(10, (self.display_width - 10) / 10.0) * 10.0
        rand_y = randrange(10, (self.display_height - 10) / 10.0) * 10.0
        if (rand_x, rand_y) not in self.snake.pixels and \
            (rand_x, rand_y) != (self.snake.head_x, self.snake.head_y):
            return (rand_x, rand_y)
        else:
            return self.rand_x_y()

class OnePlayer_Classic_Snake(Game_Mode):

    def game_over_screen(self):
        message = f"Game Over! Score: {self.snake.score}"
        text = self.score_font.render(message, True, self.orange)

        game_close = False
        while game_close == False:
            for event in pygame.event.get():
                if event.type == QUIT:
                    game_close = True
            self.game_display.fill(self.white)
            self.game_display.blit(
                text, 
                [(self.display_width // 2) - 100, 
                (self.display_height // 2) - 20]
            )
            self.update()

    def run(self):
        game_over, game_close = False, False  
        
        (self.snake.head_x, self.snake.head_y) = self.rand_x_y()
            
        delta_x, delta_y = 0, 0
        
        food_x_y = self.rand_x_y()
        
        while (game_over, game_close) == (False, False):
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.end()
                # If one snake, allow for KEYS or WASD
                elif event.type == KEYDOWN:
                    (delta_x, delta_y) = self.snake.get_directions_keys(
                        event, delta_x, delta_y)
                    (delta_x, delta_y) = self.snake.get_directions_wasd(
                        event, delta_x, delta_y)

            (food_eaten, game_over) = self.snake.move(
                delta_x, delta_y, food_x_y)
            self.check_for_out_of_bounds()

            if food_eaten:
                food_x_y = self.rand_x_y()
 
            self.game_display.fill(self.white)
            self.draw_snake()
            self.draw_fruit(food_x_y)
            self.show_scores()
            self.clock.tick(self.snake.speed)
            self.update()

        self.game_over_screen()


class TwoPlayer_Timed_Snake(Game_Mode):

    snake_1: Snake
    snake_2: Snake

    def __init__(
        self, 
        game
    ):
        self.snake_1 = game.snake_1
        self.snake_2 = game.snake_2
        self.clock = game.clock
        self.game_display = game.game_display
        self.display_width = game.width
        self.display_height = game.height

    def rand_x_y(self):
        rand_x = randrange(10, (self.display_width - 10) / 10.0) * 10.0
        rand_y = randrange(10, (self.display_height - 10) / 10.0) * 10.0
        if (rand_x, rand_y) not in self.snake_1.pixels and \
            (rand_x, rand_y) not in self.snake_2.pixels:
            return (rand_x, rand_y)

    def draw_snakes(self):
        for x, y, in self.snake_2.pixels:
            pygame.draw.rect(self.game_display, self.black, [x, y, 10, 10])
        for x, y, in self.snake_2.pixels:
            pygame.draw.rect(self.game_display, self.black, [x, y, 10, 10])
        
    def draw_fruits(self, coordinates):
        for x, y in coordinates:
            pygame.draw.rect(self.game_display, self.orange, [x, y, 10, 10])
            
    def show_scores(self):
        text_1 = self.score_font.render(
            f"{self.snake_1.name}'s score: {self.snake_1.score}",
            True, self.orange
        )
        text_2 = self.score_font.render(
            f"{self.snake_2.name}'s score: {self.snake_2.score}",
            True, self.orange
        )
        self.game_display.blit(text_1, [0, 0])
        self.game_display.blit(text_2, [0, 25])
        
    def run(self):
        game_over, game_close = False, False  
        
        (self.snake_1.head_x, self.snake_1.head_y) = (140, 220)
        (self.snake_2.head_x, self.snake_2.head_y) = (120, 250)
            
        delta_x_1, delta_y_1 = 0, 0
        delta_x_2, delta_y_2 = 0, 0
        
        foods = [self.rand_x_y() for _ in range(5)]
        
        while (game_over, game_close) == (False, False):
            for event in pygame.event.get():
                if event.type == QUIT:
                    game_close = True
                if event.type == KEYDOWN:
                    (delta_x_1, delta_y_1) = self.snake_1.get_directions_keys(
                        event, delta_x_1, delta_y_1)
                    (delta_x_2, delta_y_2) = self.snake_2.get_directions_wasd(
                        event, delta_x_2, delta_y_2)

            (i, _) = self.snake_1.move(
                delta_x_1, delta_y_1, foods)

            (j, _) = self.snake_2.move(
                delta_x_2, delta_y_2, foods)

            print(f"Snake 1 {self.snake_1.pixels}, Snake 2 {self.snake_2.pixels}")

            if i != -1:
                # If fruit at i eaten, replace      
                foods.pop(i) 
                foods.append(self.rand_x_y()) 
            if j != -1:
                # If fruit at j eaten, replace      
                foods.pop(j) 
                foods.append(self.rand_x_y()) 

            self.game_display.fill(self.white)

            self.draw_snakes()
            self.draw_fruits(foods)
            self.show_scores()

            self.clock.tick(self.snake_1.speed)
            self.update()