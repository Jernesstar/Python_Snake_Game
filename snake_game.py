from random import randrange
import pygame
from pygame import KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT

pygame.init()
pygame.display.set_caption("Snake Game")


class SnakeGame:

    snake_length = 1
    snake_size = 10
    snake_speed = 15
    snake_head_x = 0
    snake_head_y = 0
    snake_pixels: list[tuple] = []

    score = 0
    width, height = 700, 500
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    orange = (255, 165, 0)

    message_font = pygame.font.SysFont("arial", 30)
    score_font = pygame.font.SysFont("arial", 25)

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.game_display = pygame.display.set_mode((self.width, self.height))
        self.game_display.fill(self.white)
        pygame.display.update()

    def update(self):
        pygame.display.update()

    def print_score(self, score: int) -> None:
        text = self.score_font.render(f"Score: {score}", True, self.orange)
        self.game_display.blit(text, [0, 0])

    def print_time(self, time: int):
        text = self.score_font.render(f"Time: {time}", True, self.orange)
        self.game_display.blit(text, [30, 0])

    def draw_snake(self):
        for x, y in self.snake_pixels:
            pygame.draw.rect(
                self.game_display,
                self.black,
                [x, y, self.snake_size, self.snake_size],
            )

    def draw_fruits(self, coordinates: list[tuple[int, int]]):
        for x, y in coordinates:
            pygame.draw.rect(self.game_display, self.orange, [x, y, 10, 10])

    def rand_x_y(self):
        rand_x = randrange(10, (self.width - 20) / 10.0) * 10.0
        rand_y = randrange(10, (self.height - 20) / 10.0) * 10.0
        if (rand_x, rand_y) not in self.snake_pixels:
            return (rand_x, rand_y)
        else:
            return self.rand_x_y()

    def get_directions(self, event: pygame.event) -> tuple[int, int]:
        """
        This method returns the directions to go depending on the key
        press. It also makes sure that the player can not go directly
        opposite of the direction they are currently going.

        The following if-statement checks that the snake is longer than one
        pixel:
        >>> if len(self.snake_pixels) == 1

        as this will prevent an IndexError

        The following line checks if the snake is currently going left
        >>> self.snake_pixels[-2][0] - self.snake_pixels[-1][0] < 0

        since the current snake head position always will correspond to:

        >>> self.snake_pixels[-1]

        as it will always be the last positions to be appended to
        self.snake_pixels
        """
        delta_x, delta_y = 0, 0

        if len(self.snake_pixels) == 1:
            if event.key in (K_LEFT, K_RIGHT):
                delta_x = -10 if event.key == K_LEFT else 10
                delta_y = 0
            elif event.key in (K_UP, K_DOWN):
                delta_x = 0
                delta_y = -10 if event.key == K_UP else 10
            return (delta_x, delta_y)

        if event.key in (K_LEFT, K_RIGHT):
            """Snake is going left"""
            if (self.snake_pixels[-1][0] - self.snake_pixels[-2][0]) < 0:
                delta_x = -10
                delta_y = 0
                """
                Snake is currently moving up, so turning either direction
                is fine 
                """
            elif (self.snake_pixels[-1][0] - self.snake_pixels[-2][0]) == 0:
                delta_x = -10 if event.key == K_LEFT else 10
                delta_y = 0
            elif (self.snake_pixels[-1][0] - self.snake_pixels[-2][0]) > 0:
                delta_x = 10
                delta_y = 0

        elif event.key in (K_UP, K_DOWN):
            if (self.snake_pixels[-1][1] - self.snake_pixels[-2][1]) < 0:
                delta_x = 0
                delta_y = -10
            elif (self.snake_pixels[-1][1] - self.snake_pixels[-2][1]) == 0:
                delta_x = 0
                delta_y = -10 if event.key == K_UP else 10
            elif (self.snake_pixels[-1][1] - self.snake_pixels[-2][1]) > 0:
                delta_x = 0
                delta_y = 10
        else:
            delta_x = 0
            delta_y = 0
        return (delta_x, delta_y)

    def change_directions(self, delta_x, delta_y):
        self.snake_head_x += delta_x
        self.snake_head_y += delta_y

    def check_for_game_over(self, game_over):
        if game_over:
            return True
        if (self.snake_head_x, self.snake_head_y) in self.snake_pixels[:-1]:
            return True
        return False

    def when_eat_food(self, target_x, target_y):
        if (self.snake_head_x, self.snake_head_y) == (target_x, target_y):
            self.score += 1
            self.snake_length += 1
            return self.rand_x_y()
        return (target_x, target_y)

    def check_out_of_bounds(self, x, y):
        if x == -10:
            x = self.width - 10
        if x == self.width + 10:
            x = 10
        if y == -10:
            y = self.height - 10
        if y == self.height + 10:
            y = 10
        return (x, y)

    def game_over_screen(self):
        message = f"Game Over! Score: {self.score}"
        text = self.score_font.render(message, True, self.orange)
        game_close = False
        while game_close == False:
            for event in pygame.event.get():
                if event.type == QUIT:
                    game_close = True
            self.game_display.fill(self.white)
            self.game_display.blit(
                text, [(self.width // 2) - 130, (self.height // 2) - 20]
            )
            self.update()

    def run(self):
        game_over = False
        game_close = False

        self.snake_head_x = self.width // 2
        self.snake_head_y = self.height // 2

        delta_x = 0
        delta_y = 0

        (rand_x, rand_y) = self.rand_x_y()

        while (game_close, game_over) == (False, False):
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.end()
                elif event.type == KEYDOWN:
                    (delta_x, delta_y) = self.get_directions(event)

            self.change_directions(delta_x, delta_y)

            (self.snake_head_x, self.snake_head_y) = self.check_out_of_bounds(
                self.snake_head_x, self.snake_head_y
            )
            self.snake_pixels.append((self.snake_head_x, self.snake_head_y))

            if len(self.snake_pixels) > self.snake_length:
                self.snake_pixels.pop(0)

            game_over = self.check_for_game_over(game_over)

            (rand_x, rand_y) = self.when_eat_food(rand_x, rand_y)

            self.game_display.fill(self.white)
            self.draw_snake()
            self.draw_fruits([(rand_x, rand_y)])
            self.print_score(self.snake_length)
            self.clock.tick(self.snake_speed)
            self.update()

        self.game_over_screen()

    def end(self):
        pygame.display.quit()
        pygame.quit()
        quit()

    def play(self):
        self.run()
        self.end()
