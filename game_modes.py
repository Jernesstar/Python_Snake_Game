from random import randrange

import pygame
from pygame import (
    QUIT, KEYDOWN,
    K_ESCAPE, K_RETURN, K_SPACE,
    K_UP, K_DOWN, K_LEFT, K_RIGHT, 
    K_w, K_s, K_a, K_d
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

    def run(self, options):
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
        size = self.snake_1.size
        for x in range(self.display_width // size):
            for y in range(self.display_height // size):
                pygame.draw.rect(
                    self.game_display,
                    colors[y % 2],
                    [x * size, y * size, size, size]
                )
            colors.reverse()

    def show_scores(self):
        message = f"{self.snake_1.name}'s score: {self.snake_1.score}"
        text_1 = self.score_font.render(
            message,
            True, self.white
        )
        self.game_display.blit(text_1, [3, 0])

    def draw_snake(self):
        for x, y, in self.snake_1.pixels:
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
        message_2 = "Press space to return to menu screen"

        text = self.message_font.render(message, True, self.red)
        text_2 = self.message_font.render(message_2, True, self.red)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.end()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        return False
                    if event.key == K_ESCAPE:
                        self.end()
                    if event.key == K_SPACE:
                        return True
            self.tile_background()
            self.draw_snake()
            self.game_display.blit(
                text, 
                [(self.display_width // 2) - 220, 
                (self.display_height // 2) - 40]
            )
            self.game_display.blit(
                text_2, 
                [(self.display_width // 2) - 220, 
                (self.display_height // 2)]
            )
            self.update()
        
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
                    return (True, False)
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return (True, False)
                    if event.key == K_RETURN:
                        return (False, False)
                    if event.key == K_SPACE:
                        return (False, True)
            self.tile_background()

            self.game_display.blit(
                text_1, 
                [(self.display_width // 2) - 125, 
                (self.display_height // 2) - 40]
            )
            
            self.game_display.blit(
                text_2,
                [(self.display_width // 2) - 155, 
                (self.display_height // 2)]
            )
            self.update()

    def run(self, options):
        (self.snake_1.head_x, self.snake_1.head_y) = self.rand_x_y(250, 250)

        game_over, paused, see_menu = False, False, False 
        delta_x, delta_y = 0, 0
        try:
            food_x_y = self.get_fruit_positions(options["fruit_count"])
            speed = options["speed"]
        except:
            food_x_y = self.rand_x_y(0, 0)
            speed = 10

        while game_over == False:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return (True, False)
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return (True, False)
                    if event.key == K_RETURN:
                        paused = self.check_for_pause(paused, event)
                    # Since only one snake, allow for KEYS or WASD    
                    (delta_x, delta_y) = self.snake_1.get_directions_keys(
                        event, delta_x, delta_y)
                    (delta_x, delta_y) = self.snake_1.get_directions_wasd(
                        event, delta_x, delta_y)  
            if paused:
                see_menu = self.pause_screen()
            if see_menu:
                return (False, True)
            paused = False
            food_eaten = self.snake_1.move(delta_x, delta_y, food_x_y)
            game_over = self.snake_1.check_for_game_over(game_over)
            
            if isinstance(food_eaten, bool):
                if food_eaten:
                    food_x_y = self.rand_x_y(*food_x_y)
            elif isinstance(food_eaten, int):
                if food_eaten != -1:
                    x_y = food_x_y.pop(food_eaten)
                    food_x_y.append(self.rand_x_y(*x_y))

            self.tile_background()

            self.draw_fruit(food_x_y)
            self.draw_snake()
            self.show_scores()

            self.clock.tick(speed)
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
            return self.rand_x_y(old_x, old_y)

    def draw_snake(self):
        for x, y, in self.snake_1.pixels:
            pygame.draw.rect(
                self.game_display, 
                self.black, 
                [x, y, self.snake_1.size, self.snake_1.size]
            )
        for x, y, in self.snake_2.pixels:
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
        message_2 = "Press return to play again"

        text = self.message_font.render(message, True, self.red)
        text_2 = self.message_font.render(message_2, True, self.red)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return (True, False)
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return (True, False)
                    if event.key == K_RETURN:
                        return (False, False)
                    if event.key == K_SPACE:
                        return (False, True)
                        
            self.tile_background()

            self.game_display.blit(
                text, 
                [(self.display_width // 2) - 120, 
                (self.display_height // 2) - 40]
            )
            self.game_display.blit(
                text_2,
                [(self.display_width // 2) - 155, 
                (self.display_height // 2)]
            )
            self.update()
        
    def run(self, options):        
        (self.snake_1.head_x, self.snake_1.head_y) = self.rand_x_y(250, 250)
        (self.snake_2.head_x, self.snake_2.head_y) = self.rand_x_y(250, 250)
     
        delta_x_1, delta_y_1 = 0, 0
        delta_x_2, delta_y_2 = 0, 0

        paused, game_over_1, game_over_2, see_menu = False, False, False, False
        try:
            food_x_y = self.get_fruit_positions(options["fruit_count"])
            speed = options["speed"]
        except:
            food_x_y = self.rand_x_y(0, 0)
            speed = 10

        while (game_over_1, game_over_2) == (False, False):
            for event in pygame.event.get():
                if event.type == QUIT:
                    return (True, False)
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return (True, False)
                    if event.key == K_RETURN:
                        paused = self.check_for_pause(paused, event)
                    (delta_x_1, delta_y_1) = self.snake_1.directions(
                        event, delta_x_1, delta_y_1)
                    (delta_x_2, delta_y_2) = self.snake_2.directions(
                        event, delta_x_2, delta_y_2)
            if paused:
                see_menu = self.pause_screen()
            if see_menu:
                return (False, True)
            paused = False
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
            self.draw_snake()
            self.show_scores()

            self.clock.tick(speed)
            self.update()
            
        return self.winner_screen(snake_1_game_over=game_over_1)