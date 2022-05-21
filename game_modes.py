from random import randrange, choice
from functools import singledispatchmethod

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

    def run(self, **kwargs):
        raise NotImplementedError("Child classes should implement this method")

    def update(self):
        pygame.display.update()
    
    def end(self):
        pygame.display.quit()
        pygame.quit()
        quit()

    def get_fruit_positions(self, number: int):
        old_x = self.snake_1.head_x
        old_y = self.snake_1.head_y
        if number == 1:
            return self.rand_x_y(old_x, old_y)
        return [self.rand_x_y(old_x, old_y) for _ in range(number)]

    def tile_background(self):
        colors = [self.light_green, self.dark_green]
        tile_count_even = (self.display_width // self.snake_1.size) % 2 == 0

        for x in range(0, self.display_width, self.snake_1.size):
            for y in range(0, self.display_height, self.snake_1.size):
                pygame.draw.rect(
                    self.game_display,
                    colors[0],
                    [x, y, self.snake_1.size, self.snake_1.size]
                )
                colors.reverse()
            if tile_count_even:
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
        if isinstance(coordinates, tuple):
            (x, y) = coordinates
            pygame.draw.rect(
                self.game_display, 
                self.orange, 
                [x, y, self.snake_1.size, self.snake_1.size]
            )
        elif isinstance(coordinates, list):
            for x, y in coordinates:
                pygame.draw.rect(
                    self.game_display, 
                    self.orange, 
                    [x, y, self.snake_1.size, self.snake_1.size]
                )

    def pause_screen(self):
        message = "Paused. Press return key to continue"
        text = self.message_font.render(
            message, True, self.red
        )

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.end()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        return

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

    def run(self, **kwargs):
        game_over = False
        paused = False  

        (self.snake_1.head_x, self.snake_1.head_y) = self.rand_x_y(250, 250) 

        delta_x, delta_y = 0, 0

        try:
            food_x_y = self.get_fruit_positions(kwargs["fruit_count"])
        except:
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
                    # Since only one snake, allow for KEYS or WASD    
                    (delta_x, delta_y) = self.snake_1.get_directions_keys(
                        event, delta_x, delta_y)
                    (delta_x, delta_y) = self.snake_1.get_directions_wasd(
                        event, delta_x, delta_y)
            if paused:
                self.pause_screen()
            
            food_eaten = self.snake_1.move(delta_x, delta_y, food_x_y)
            game_over = self.snake_1.check_for_game_over(game_over)
            
            if isinstance(food_eaten, bool):
                if food_eaten:
                    food_x_y = self.rand_x_y(*food_x_y)
            
            elif isinstance(food_eaten, int):
                print(food_eaten)
                if food_eaten != -1:
                    x_y = food_x_y.pop(food_eaten)
                    food_x_y.append(self.rand_x_y(*x_y))
                    pass

            self.tile_background()

            self.draw_fruit(food_x_y)
            self.draw_snake(self.snake_1.pixels)
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

    def pause_screen(self):
        message = "Paused. Press any key to continue"
        text = self.message_font.render(message, True, self.red)
        self.tile_background()
        self.draw_snakes(self.snake_1.pixels, self.snake_2.pixels)
        self.game_display.blit(
            text, 
            [(self.display_width // 2) - 200, 
            (self.display_height // 2) - self.score_font.get_height()]
        )

    def rand_x_y(self, old_x, old_y):
        (rand_x, rand_y) = super().rand_x_y(old_x, old_y)
        if (rand_x, rand_y) not in self.snake_2.pixels:
            return (rand_x, rand_y)
        else:
            return self.rand_x_y(old_x, old_y)

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
    
    def winner_screen(self, snake_1_game_over: bool):
        (winner_name, winner_score) = (
            self.snake_1.name if not snake_1_game_over else self.snake_2.name,
            self.snake_1.score if not snake_1_game_over else self.snake_2.score
        )
        message = f"{winner_name} wins, score {winner_score}"
        message_2 = "Press return to continue"

        text = self.message_font.render(message, True, self.red)
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
        
    def run(self, **kwargs):        
        (self.snake_1.head_x, self.snake_1.head_y) = self.rand_x_y(250, 250)
        (self.snake_2.head_x, self.snake_2.head_y) = self.rand_x_y(250, 250)
            
        delta_x_1, delta_y_1 = 0, 0
        delta_x_2, delta_y_2 = 0, 0

        game_over_1 = False
        game_over_2 = False
        paused = False

        try:
            food_x_y = self.get_fruit_positions(kwargs["fruit_count"])
        except:
            food_x_y = self.rand_x_y(0, 0)

        while (game_over_1, game_over_2) == (False, False):
            for event in pygame.event.get():
                if event.type == QUIT:
                    return True
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return True
                    if event.key == K_RETURN:
                        paused = self.check_for_pause(paused, event)
                    (delta_x_1, delta_y_1) = self.snake_1.directions(
                        event, delta_x_1, delta_y_1)
                    (delta_x_2, delta_y_2) = self.snake_2.directions(
                        event, delta_x_2, delta_y_2)
            if paused:
                self.pause_screen()

            i = self.snake_1.move(delta_x_1, delta_y_1, food_x_y)
            j = self.snake_2.move(delta_x_2, delta_y_2, food_x_y)

            game_over_1 = self.snake_1.check_for_game_over(game_over_1)
            game_over_2 = self.snake_2.check_for_game_over(game_over_2)

            if isinstance(i, bool):
                if i or j:
                    food_x_y = self.rand_x_y(*food_x_y)
            
            elif isinstance(i, int):
                if i != -1:
                    x_y = food_x_y.pop(i)
                    food_x_y.append(self.rand_x_y(*x_y))
                if j != -1:
                    x_y = food_x_y.pop(j)
                    food_x_y.append(self.rand_x_y(*x_y))

            self.tile_background()

            self.draw_fruit(food_x_y)
            self.draw_snakes(self.snake_1.pixels, self.snake_2.pixels)
            self.show_scores()

            self.clock.tick(self.snake_1.speed)
            self.update()

        return self.winner_screen(snake_1_game_over=game_over_1)