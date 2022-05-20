from random import randrange, choice

import pygame
from pygame import (
    K_ESCAPE, K_RETURN, QUIT, KEYDOWN,
    K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_s, K_a, K_d
)

from snake import Snake

pygame.init()

class Game_Mode():

    snake_1: Snake
    clock: pygame.time.Clock
    game_display: pygame.Surface

    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    orange = (255, 165, 0)
    light_green = (0, 250, 0)
    dark_green = (0, 130, 0)
    
    message_font = pygame.font.Font("resources\\pixel_font.ttf", 25)
    score_font = pygame.font.Font("resources\\pixel_font.ttf", 20)

    def __init__(self, game):
        self.snake_1 = game.snake_1
        self.clock = game.clock
        self.game_display = game.game_display
        self.display_width = game.width
        self.display_height = game.height

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

    def tile_background(self):
        colors = [self.light_green, self.dark_green]
        size_divides_height = (self.display_height // 10) % self.snake_1.size == 0
        height_is_even = (self.display_height // 10) % 2 == 0
        size_is_even = self.snake_1.size % 2 == 0

        for x in range(0, self.display_width, self.snake_1.size):
            for y in range(0, self.display_height, self.snake_1.size):
                pygame.draw.rect(
                    self.game_display,
                    colors[0],
                    [x, y, self.snake_1.size, self.snake_1.size]
                )
                colors.reverse()
            if not size_is_even:   
                colors.reverse()
            elif not height_is_even:
                colors.reverse()
            elif size_divides_height:
                colors.reverse()

    def show_scores(self):
        message = f"{self.snake_1.name}'s score: {self.snake_1.score}"
        text_1 = self.score_font.render(
            message,
            True, self.white
        )
        self.game_display.blit(text_1, [3, 0])

    def draw_snake(self, pixels):
        for x, y, in pixels:
            pygame.draw.rect(
                self.game_display,
                self.black,
                [x, y, self.snake_1.size, self.snake_1.size]
            )

    def draw_fruit(self, coordinates):
        (x, y) = coordinates
        pygame.draw.rect(
            self.game_display, 
            self.orange, 
            [x, y, self.snake_1.size, self.snake_1.size]
        )

    def pause_screen(self):
        message = "Paused. Press any key to continue"
        text = self.message_font.render(
            message, True, self.red
        )
        self.tile_background()
        self.draw_snake(self.snake_1.pixels)

        self.game_display.blit(
            text, 
            [(self.display_width // 2) - 200, 
            (self.display_height // 2) - self.score_font.get_height()]
        )
    
    def check_for_pause(self, paused, event: pygame.event):
        if event.key == K_RETURN:
            return True if paused == False else False

    def check_end_game(self, event):
        if event.type == KEYDOWN:
            if event.key not in (K_UP, K_DOWN, K_LEFT, K_RIGHT) \
            and event.key not in (K_w, K_s, K_a, K_d):
                return True
        return False
        
    def check_for_out_of_bounds(self, game_over):
        if game_over:
            return True
        if self.snake_1.head_x >= self.display_width:
            return True
        elif self.snake_1.head_x <= -self.snake_1.size:
            return True
        elif self.snake_1.head_y >= self.display_height:
            return True
        elif self.snake_1.head_y <= -self.snake_1.size:
            return True
        return False
        
    def rand_x_y(self, old_x, old_y):
        size = self.snake_1.size
        
        rand_x = randrange(0, (self.snake_1.display_width) // size) * size
        rand_y = randrange(0, (self.snake_1.display_height) // size) * size
        
        if (rand_x, rand_y) not in self.snake_1.pixels and \
            (rand_x, rand_y) != (old_x, old_y):
            return (rand_x, rand_y)
        else:
            return self.rand_x_y(old_x, old_y)

class OnePlayer_Classic_Snake(Game_Mode):

    def game_over_screen(self):
        message_1 = f"Game Over! Score: {self.snake_1.score}"
        message_2 = "Press return to play again"

        text_1 = self.message_font.render(message_1, True, self.red)
        text_2 = self.message_font.render(message_2, True, self.red)
    
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return True
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return True
                    if event.key == K_RETURN:
                        return False
            self.tile_background()

            self.game_display.blit(
                text_1, 
                [(self.display_width // 2) - 150, 
                (self.display_height // 2) - self.message_font.get_height()]
            )
            
            self.game_display.blit(
                text_2,
                [(self.display_width // 2) - 120, 
                (self.display_height // 2)]
            )
            self.update()

    def run(self):
        game_over = False
        paused = False  

        (self.snake_1.head_x, self.snake_1.head_y) = self.rand_x_y(250, 250) 
        delta_x, delta_y = 0, 0

        food_x_y = self.rand_x_y(0, 0)

        while game_over == False:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return True 
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return True
                    if event.key == K_RETURN:
                        paused = self.check_for_pause(paused, event)
                    # If one snake, allow for KEYS or WASD    
                    (delta_x, delta_y) = self.snake_1.get_directions_keys(
                        event, delta_x, delta_y)
                    (delta_x, delta_y) = self.snake_1.get_directions_wasd(
                        event, delta_x, delta_y)
            if paused:
                self.pause_screen()
            else:
                (food_eaten, game_over) = self.snake_1.move(
                    delta_x, delta_y, food_x_y)

                game_over = self.check_for_out_of_bounds(game_over)

                if food_eaten:
                    food_x_y = self.rand_x_y(*food_x_y)
                    
                self.tile_background()

                self.draw_snake(self.snake_1.pixels)
                self.draw_fruit(food_x_y)
                self.show_scores()
                self.clock.tick(self.snake_1.speed)

            self.update()
            
        return self.game_over_screen()


class TwoPlayer_Snake(Game_Mode):

    snake_1: Snake
    snake_2: Snake

    def __init__(self, game):
        self.snake_1 = game.snake_1
        self.snake_2 = game.snake_2
        self.clock = game.clock
        self.game_display = game.game_display
        self.display_width = game.width
        self.display_height = game.height

    def rand_x_y(self, old_x, old_y):
        (rand_x, rand_y) = super().rand_x_y(old_x, old_y)
        if (rand_x, rand_y) not in self.snake_2.pixels:
            return (rand_x, rand_y)
        else:
            return self.rand_x_y()

    def draw_snakes(self, pixels_1, pixels_2):
        for x, y, in pixels_1:
            pygame.draw.rect(
                self.game_display, 
                self.black, 
                [x, y, self.snake_1.size, self.snake_1.size]
            )
        for x, y, in pixels_2:
            pygame.draw.rect(
                self.game_display, 
                self.red, 
                [x, y, self.snake_2.size, self.snake_2.size]
            )
        
    def draw_fruits(self, coordinates):
        for x, y in coordinates:
            pygame.draw.rect(
                self.game_display, 
                self.orange, 
                [x, y, self.snake_1.size, self.snake_1.size]
            )

    def show_scores(self):
        text_1 = self.score_font.render(
            f"{self.snake_1.name}'s score: {self.snake_1.score}",
            True, self.black
        )
        text_2 = self.score_font.render(
            f"{self.snake_2.name}'s score: {self.snake_2.score}",
            True, self.red
        )
        self.game_display.blit(text_1, [3, 0])
        self.game_display.blit(text_2, [3, self.score_font.get_height()])
    
    def check_for_out_of_bounds(self):
        _left_1 = self.snake_1.head_x <= -10
        _right_1 = self.snake_1.head_x >= self.display_width
        _up_1 = self.snake_1.head_y <= -10
        _down_1 = self.snake_1.head_y >= self.display_height

        _left_2 = self.snake_2.head_x >= self.display_width
        _right_2 = self.snake_2.head_x <= -10
        _up_2 = self.snake_2.head_y >= self.display_height
        _down_2 = self.snake_2.head_y <= -10

        if _left_1 or _right_1 or _up_1 or _down_1:
            return (True, False) # Player_1 lose is True
        if _left_2 or _right_2 or _up_2 or _down_2:
            return (False, True) # Player_1 lose is True
        return (False, False) # No one has gone out of bounds

    def check_for_game_over(self, game_over_1, game_over_2):
        if (game_over_1, game_over_2) != (False, False):
            return (game_over_1, game_over_2)
        return self.check_for_out_of_bounds()
    
    def winner_screen(self, snake_1_game_over: bool):
        (winner_name, winner_score) = (
            self.snake_1.name if not snake_1_game_over else self.snake_2.name,
            self.snake_2.score if not snake_1_game_over else self.snake_2.score
        )
        message = f"{winner_name} wins, score {winner_score}"
        message_2 = "Press any key to continue"

        text = self.message_font.render(message, True, self.red)
        text_2 = self.message_font.render(message_2, True, self.red)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return True
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        return False
                        
            self.tile_background()

            self.game_display.blit(
                text, 
                [(self.display_width // 2) - 150, 
                (self.display_height // 2) - 40]
            )
            
            self.game_display.blit(
                text_2,
                [(self.display_width // 2) - 120, 
                (self.display_height // 2)]
            )
            self.update()
        
    def run(self):        
        (self.snake_1.head_x, self.snake_1.head_y) = self.rand_x_y(250, 250)
        (self.snake_2.head_x, self.snake_2.head_y) = self.rand_x_y(250, 250)
            
        delta_x_1, delta_y_1 = 0, 0
        delta_x_2, delta_y_2 = 0, 0

        game_over_1 = False
        game_over_2 = False
        paused = False

        foods = [self.rand_x_y(0, 0) for _ in range(5)]
        
        while (game_over_1, game_over_2) == (False, False):
            for event in pygame.event.get():
                if event.type == QUIT:
                    return True
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        paused = self.check_for_pause(paused, event)
                    (delta_x_1, delta_y_1) = self.snake_1.directions(
                        event, delta_x_1, delta_y_1)

                    (delta_x_2, delta_y_2) = self.snake_2.directions(
                        event, delta_x_2, delta_y_2)

            if paused:
                self.pause_screen()
            else:
                (i, game_over_1) = self.snake_1.move(
                    delta_x_1, delta_y_1, foods)

                (j, game_over_2) = self.snake_2.move(
                    delta_x_2, delta_y_2, foods)

                (game_over_1, game_over_2) = self.check_for_game_over(
                    game_over_1, game_over_2)

                if i != -1:
                    # If fruit at i eaten, replace      
                    (old_x, old_y) = foods.pop(i) 
                    foods.append(self.rand_x_y(old_x, old_y)) 
                if j != -1:
                    # If fruit at j eaten, replace      
                    (old_x, old_y) = foods.pop(j) 
                    foods.append(self.rand_x_y(old_x, old_y)) 

                self.game_display.fill(self.white)
                self.tile_background()

                self.draw_snakes(self.snake_1.pixels, self.snake_2.pixels)
                self.draw_fruits(foods)
                self.show_scores()

                self.clock.tick(self.snake_1.speed)
            self.update()

        self.winner_screen(snake_1_game_over=game_over_1)