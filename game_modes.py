from random import randrange
import pygame
from pygame import QUIT, KEYDOWN
from snake import Snake

pygame.init()

class Game_Mode:

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
        snake: Snake, 
        clock: pygame.time.Clock, 
        game_display: pygame.Surface
    ):
        self.snake = snake
        self.clock = clock
        self.game_display = game_display
        self.display_width = snake.display_width
        self.display_height = snake.display_height
    
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
        if (rand_x, rand_y) not in self.snake.pixels:
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
        
        self.snake.head_x = self.snake.display_width // 2
        self.snake.head_y = self.snake.display_height // 2
        self.snake.length = 80
            
        delta_x, delta_y = 10, 0
        
        food_x_y = self.rand_x_y()
        
        while (game_over, game_close) == (False, False):
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.end()
                elif event.type == KEYDOWN:
                    (delta_x, delta_y) = self.snake.directions(
                        event, delta_x, delta_y)

            (food_eaten, game_over) = self.snake.move(
                delta_x, delta_y, food_x_y)

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
        snake_1: Snake, 
        snake_2: Snake,
        clock: pygame.time.Clock, 
        game_display: pygame.Surface
    ):
        self.snake_1 = snake_1
        self.snake_2 = snake_2
        self.clock = clock
        self.game_display = game_display
        self.display_width = snake_1.display_width
        self.display_height = snake_1.display_height

    def draw_snakes(self):
        self.game_display.fill(self.white)
        for x, y, in self.snake_1.pixels:
            pygame.draw.rect(
                self.game_display,
                self.black,
                [x, y, 10, 10]
            )
        for x, y, in self.snake_2.pixels:
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
        
        self.snake_1.head_x = (self.display_width // 2)
        self.snake_1.head_y = (self.display_height // 2)
        
        self.snake_2.head_x = (self.display_width // 2) - 10
        self.snake_2.head_y = (self.display_height // 2) + 10
            
        delta_x_1, delta_y_1 = 0, 0
        delta_x_2, delta_y_2 = 0, 0
        
        foods = [self.rand_x_y() for _ in range(5)]
        
        while (game_over, game_close) == (False, False):
            for event in pygame.event.get():
                if event.type == QUIT:
                    game_close = True
                elif event.type == KEYDOWN:
                    (delta_x_1, delta_y_1) = self.snake_1.directions(
                        event, delta_x_1, delta_y_1)
                    (delta_x_2, delta_y_2) = self.snake_2.directions(
                        event, delta_x_2, delta_y_2)

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

            self.game_display.fill(self.white)
            self.draw_snakes()
            self.draw_fruits(foods)
            self.show_scores()
            self.clock.tick(15)
            self.update()