import pygame
import random
import numpy as np

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN1 = (0, 200, 0)
GREEN2 = (100, 200, 100)

BLOCK_SIZE = 20
SPEED = 60

icon = pygame.image.load('icon.png')

class SnakeGame:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.direction = pygame.K_RIGHT
        self.head = [self.w / 2, self.h / 2]
        self.snake = [self.head,
                      [self.head[0] - BLOCK_SIZE, self.head[1]],
                      [self.head[0] - (2 * BLOCK_SIZE), self.head[1]]]
        self.score = 0
        self.food = None
        self.place_food()
        self.frame_iteration = 0

    def place_food(self):
        while True:
            x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            self.food = [x, y]
            if self.food not in self.snake:
                break

    def step(self, action):
        self.frame_iteration += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self.move(action)
        self.snake.insert(0, self.head)

        game_over = False
        reward = 0

        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        if self.head == self.food:
            self.score += 1
            reward = 10
            self.place_food()
        else:
            self.snake.pop()

        self.render()

        return reward, game_over, self.score

    def move(self, action):
        clock_wise = [pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT, pygame.K_UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            self.direction = clock_wise[idx]
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            self.direction = clock_wise[next_idx]
        elif np.array_equal(action, [0, 0, 1]):
            next_idx = (idx - 1) % 4
            self.direction = clock_wise[next_idx]

        x = self.head[0]
        y = self.head[1]

        if self.direction == pygame.K_RIGHT:
            x += BLOCK_SIZE
        elif self.direction == pygame.K_LEFT:
            x -= BLOCK_SIZE
        elif self.direction == pygame.K_DOWN:
            y += BLOCK_SIZE
        elif self.direction == pygame.K_UP:
            y -= BLOCK_SIZE

        self.head = [x,y]

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head

        if pt in self.snake[1:]:
            return True

        if not (0 <= pt[0] < self.w) or not (0 <= pt[1] < self.h):
            return True

        return False

    def render(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, GREEN1, pygame.Rect(pt[0], pt[1], BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, GREEN2, pygame.Rect(pt[0] + 4, pt[1] + 4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food[0], self.food[1], BLOCK_SIZE, BLOCK_SIZE))

        font = pygame.font.SysFont('Garamond', 25)
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [8, 5])
        pygame.display.flip()

        self.clock.tick(SPEED)

def random_moves():
    env = SnakeGame()

    while True:
        action = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        reward, game_over, score = env.step(action[random.randint(0, 2)])

        if game_over:
            break

    print('Final Score', score)

    pygame.quit()