from random import randrange
from pathlib import Path
import os

import pygame
from pygame import (
    QUIT, KEYDOWN,
    K_ESCAPE, K_RETURN, K_SPACE,
)
from pygame import sprite

from sprites import Block, Snake, Apple

pygame.init()

resources_path = Path(
        os.path.split(os.path.split(__file__)[0])[0]
    ) / "resources"

class Game_Mode:

    snake_1: Snake
    clock: pygame.time.Clock
    game_display: pygame.Surface

    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    orange = (255, 165, 0)
    light_green = (0, 250, 0)
    dark_green = (0, 130, 0)
    

    message_font = pygame.font.Font(f"{resources_path}\\pixel_font.ttf", 25)
    score_font = pygame.font.Font(f"{resources_path}\\pixel_font.ttf", 20)

    def __init__(self, game):
        self.snake_1 = game.snake_1
        self.clock = game.clock
        self.game_display = game.game_display
        self.display_width = game.width
        self.display_height = game.height
        self.size = game.square_size
        self.tiled_background = self.tile_background()
        self.apples: sprite.Group = game.apples

    def run(self, options):
        raise NotImplementedError("Child classes should implement this method")

    def update(self):
        pygame.display.update()
    
    def end(self):
        pygame.display.quit()
        pygame.quit()
        quit()

    def spawn_fruits(self, number: int):
        size = self.size
        if number == 1:
            Apple(size, self.rand_x_y())
        else:
            [Apple(size, self.rand_x_y()) for _ in range(number)]

    def tile_background(self) -> pygame.Surface:
        colors = [self.light_green, self.dark_green]
        size = self.size
        background = pygame.Surface([self.display_width, self.display_height])
        for x in range(self.display_width // size):
            for y in range(self.display_height // size):
                pygame.draw.rect(
                    background, colors[y % 2], [x * size, y * size, size, size]
                )
            colors.reverse()
        return background

    def show_scores(self):
        message = f"{self.snake_1.name}'s score: {self.snake_1.score}"
        text_1 = self.score_font.render(message,True, self.white)
        self.game_display.blit(text_1, [3, 0])

    def draw_snake(self):
        for block in self.snake_1.pixels:
            self.game_display.blit(block.image, block.rect.topleft) 
        pos_1 = self.snake_1.eye_rect_1.topleft
        pos_2 = self.snake_1.eye_rect_2.topleft
        self.game_display.blit(self.snake_1.eye, pos_1)
        self.game_display.blit(self.snake_1.eye, pos_2)

    def draw_fruit(self):
        self.apples.clear(self.game_display, self.tiled_background)
        # Returns what pixels have changed
        dirty = self.apples.draw(self.game_display) 
        pygame.display.update(dirty)

    def pause_screen(self):
        message = "Paused. Press return key to continue"
        message_2 = "Press space to return to menu screen"
        x = self.display_width / 2
        y = self.display_height / 2
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
            offset_1 = self.message_font.size(message)[0] / 2
            offset_2 = self.message_font.size(message_2)[0] / 2
            
            self.game_display.blit(self.tiled_background, [0, 0])
            self.draw_snake()
            self.game_display.blit(text, [x - offset_1, y - 40])
            self.game_display.blit(text_2, [x - offset_2, y])
            self.update()
        
    def check_for_pause(self, paused, event: pygame.event):
        if event.key == K_RETURN:
            return not paused # negates the current paused state

    def rand_x_y(self) -> tuple[int, int]:
        size = self.size
        rand_x = randrange(0, (self.display_width - size) // size) * size
        rand_y = randrange(0, (self.display_height - size) // size) * size
        if (rand_x, rand_y) not in (
            block.rect.topleft for block in self.snake_1.pixels):
            return (rand_x, rand_y)
        else:
            return self.rand_x_y()

    def check_for_fruit_collisions(self):
        # Check if the snake has eaten an apple
        for _ in sprite.spritecollide(self.snake_1, self.apples, 1):
            Apple(self.size, self.rand_x_y())
            self.snake_1.score += 1
            self.snake_1.length += 1


class OnePlayer_Classic_Snake(Game_Mode):

    def game_over_screen(self):
        message_1 = f"Game Over! Score: {self.snake_1.score}"
        message_2 = "Press return to play again"
        x = self.display_width / 2
        y = self.display_height / 2
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
            self.game_display.blit(self.tiled_background, [0, 0])

            offset_1 = self.message_font.size(message_1)[0] / 2
            offset_2 = self.message_font.size(message_2)[0] / 2

            self.game_display.blit(text_1, [x - offset_1, y - 40])
            self.game_display.blit(text_2,[x - offset_2, y])
            self.update()

    def run(self, options):
        (self.snake_1.head_x, self.snake_1.head_y) = (
            self.display_width / 2 - 5 * self.size, 
            self.display_height / 2
        )
        self.snake_1.rect.topleft = (self.snake_1.head_x, self.snake_1.head_y)
        
        for i in range(1, self.snake_1.length + 1):
            x = self.snake_1.head_x - ((self.snake_1.length - i) * self.size)
            block = Block(self.size, (x, self.snake_1.head_y))
            self.snake_1.pixels.append(block)

        game_over, paused, see_menu = False, False, False 
        delta_x, delta_y = 0, 0
        try:
            self.spawn_fruits(options["fruit_count"])
            speed = options["speed"]
        except:
            self.spawn_fruits(1)
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
                    # Since only one snake, allow for KEYS and WASD
                    (delta_x, delta_y) = self.snake_1.get_directions_keys(
                        event, delta_x, delta_y)
                    (delta_x, delta_y) = self.snake_1.get_directions_wasd(
                        event, delta_x, delta_y)
            if paused:
                see_menu = self.pause_screen()
            if see_menu:
                self.apples.empty()
                return (False, True)
            paused = False
            self.snake_1.move(delta_x, delta_y)
            game_over = self.snake_1.check_for_game_over(game_over)
            self.check_for_fruit_collisions()

            self.game_display.blit(self.tiled_background, [0, 0])
            self.draw_fruit()
            self.draw_snake()
            self.show_scores()

            self.clock.tick(speed)
            self.update()
        
        self.apples.empty()
        return self.game_over_screen()


class TwoPlayer_Snake(Game_Mode):

    snake_1: Snake
    snake_2: Snake

    def __init__(self, game):
        super().__init__(game)
        self.snake_2 = game.snake_2
        self.apples: sprite.Group = game.apples

    def rand_x_y(self):
        (rand_x, rand_y) = super().rand_x_y()
        if (rand_x, rand_y) not in (
            block.rect.topleft for block in self.snake_2.pixels):
            return (rand_x, rand_y)
        else:
            return self.rand_x_y()

    def draw_snake(self):
        super().draw_snake()
        for block in self.snake_2.pixels:
            self.game_display.blit(block.image, block.rect.topleft)
        pos_1 = self.snake_2.eye_rect_1.topleft
        pos_2 = self.snake_2.eye_rect_2.topleft
        self.game_display.blit(self.snake_2.eye, pos_1)
        self.game_display.blit(self.snake_2.eye, pos_2)

    def show_scores(self):
        super().show_scores()
        text_2 = self.score_font.render(
            f"{self.snake_2.name}'s score: {self.snake_2.score}",
            True, self.red
        )
        self.game_display.blit(text_2, [3, self.score_font.get_height()])

    def check_for_fruit_collisions(self):
        super().check_for_fruit_collisions()
        for _ in sprite.spritecollide(self.snake_2, self.apples, 1):
            Apple(self.size, self.rand_x_y())
            self.snake_2.score += 1
            self.snake_2.length += 1
    
    def winner_screen(self, snake_1_game_over: bool):
        (winner_name, winner_score) = (
            self.snake_1.name if not snake_1_game_over else self.snake_2.name,
            self.snake_1.score if not snake_1_game_over else self.snake_2.score
        )
        message = f"{winner_name} wins, score {winner_score}"
        message_2 = "Press return to play again"
        x = self.display_width / 2
        y = self.display_height / 2
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
            self.game_display.blit(self.tiled_background, [0, 0])
            self.game_display.blit(text, [x - 120, y - 40])
            self.game_display.blit(text_2, [x - 155, y])
            self.update()
        
    def run(self, options):        
        (self.snake_1.head_x, self.snake_1.head_y) = (
            self.display_width / 2 - 5 * self.size, 
            self.display_height / 2
        )
        (self.snake_2.head_x, self.snake_2.head_y) = (
            self.display_width / 2 + 4 * self.snake_2.size, 
            self.display_height / 2
        )
        self.snake_1.rect.topleft = (self.snake_1.head_x, self.snake_1.head_y)
        self.snake_2.rect.topleft = (self.snake_2.head_x, self.snake_2.head_y)
        
        for i in range(1, self.snake_1.length + 1):
            x = self.snake_1.head_x - ((self.snake_1.length - i) * self.size)
            block = Block(self.size, (x, self.display_height / 2))
            self.snake_1.pixels.append(block)
        for i in range(1, self.snake_2.length + 1):
            x = self.snake_2.head_x + ((self.snake_2.length - i) * self.size)
            block = Block(self.size, (x, self.display_height / 2))
            self.snake_2.pixels.append(block)

        delta_x_1, delta_y_1, delta_x_2, delta_y_2 = 0, 0, 0, 0
        paused, game_over_1, game_over_2, see_menu = False, False, False, False
        try:
            self.spawn_fruits(options["fruit_count"])
            speed = options["speed"]
        except:
            self.spawn_fruits(1)
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
                    (delta_x_1, delta_y_1) = self.snake_1.get_directions_keys(
                        event, delta_x_1, delta_y_1)
                    (delta_x_2, delta_y_2) = self.snake_2.get_directions_wasd(
                        event, delta_x_2, delta_y_2)
            if paused:
                see_menu = self.pause_screen()
            paused = False
            if see_menu:
                return (False, True)
            self.snake_1.move(delta_x_1, delta_y_1)
            self.snake_2.move(delta_x_2, delta_y_2)

            game_over_1 = self.snake_1.check_for_game_over(game_over_1)
            game_over_2 = self.snake_2.check_for_game_over(game_over_2)
            self.check_for_fruit_collisions()

            self.game_display.blit(self.tiled_background, [0, 0])
            self.draw_fruit()
            self.draw_snake()
            self.show_scores()

            self.clock.tick(speed)
            self.update()

        self.apples.empty()
        return self.winner_screen(snake_1_game_over=game_over_1)