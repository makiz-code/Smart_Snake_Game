import pygame
import random
import torch
import numpy as np
from collections import deque
from game import SnakeGame
from model import DQN, DQNTrainer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.n_food = 0
        self.epsilon = 0  # exploration factor
        self.gamma = 0.9  # discount factor
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = DQN(11, 256, 3)
        self.trainer = DQNTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        head = game.snake[0]
        point_l = [head[0] - 20, head[1]]
        point_r = [head[0] + 20, head[1]]
        point_u = [head[0], head[1] - 20]
        point_d = [head[0], head[1] + 20]

        dir_l = game.direction == pygame.K_LEFT
        dir_r = game.direction == pygame.K_RIGHT
        dir_u = game.direction == pygame.K_UP
        dir_d = game.direction == pygame.K_DOWN

        state = [
            # Danger straight
            (dir_r and game.is_collision(point_r)) or
            (dir_l and game.is_collision(point_l)) or
            (dir_u and game.is_collision(point_u)) or
            (dir_d and game.is_collision(point_d)),

            # Danger right
            (dir_u and game.is_collision(point_r)) or
            (dir_d and game.is_collision(point_l)) or
            (dir_l and game.is_collision(point_u)) or
            (dir_r and game.is_collision(point_d)),

            # Danger left
            (dir_d and game.is_collision(point_r)) or
            (dir_u and game.is_collision(point_l)) or
            (dir_r and game.is_collision(point_u)) or
            (dir_l and game.is_collision(point_d)),

            # Move direction
            dir_l, dir_r, dir_u, dir_d,

            # Food location
            game.food[0] < game.head[0],  # food left
            game.food[0] > game.head[0],  # food right
            game.food[1] < game.head[1],  # food up
            game.food[1] > game.head[1]  # food down
        ]

        return np.array(state, dtype=int)

    def get_action(self, state):
        # tradeoff exploration / exploitation
        self.epsilon = 100 - self.n_games
        action = [0, 0, 0]
        if self.n_food < self.epsilon & random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            action[move] = 1
        else:
            state = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state)
            move = torch.argmax(prediction).item()
            action[move] = 1

        return action

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))  # popleft if MAX_MEMORY is reached

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        for state, action, reward, next_state, done in mini_sample:
            self.trainer.train_step(state, action, reward, next_state, done)


def train():
    record = 0

    agent = Agent()
    env = SnakeGame()

    while True:
        state_old = agent.get_state(env)
        action = agent.get_action(state_old)
        reward, done, score = env.step(action)
        state_new = agent.get_state(env)

        agent.train_short_memory(state_old, action, reward, state_new, done)
        agent.remember(state_old, action, reward, state_new, done)

        if done:
            env.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game :', agent.n_games, '-- Score :', score, '-- Record :', record)
            agent.n_food += score

if __name__ == '__main__':
    train()