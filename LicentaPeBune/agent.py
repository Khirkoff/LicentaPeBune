import torch
import random
import numpy as np
from collections import deque
from training import Linear_QNet, QTrainer
from AIplayed import Game
from plothelper import plot
from Gameproperties import Properties
import pygame
import math

MAX_MEMORY = 1000_000
BATCH_SIZE = 1000
LR = 0.0005

class Agent:

    def __init__(self):
        Properties.n_games = 0
        self.epsilon = 300 # randomness
        self.gamma = 0.98 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(1, 2, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def metoda(self, PT1 , Blocks0 ):
        return PT1.pos.x - Blocks0.pos.x
        if (PT1.pos.x - Blocks0.pos.x) == 0:
            return 0
        if (PT1.pos.y - Blocks0.pos.y) == 0:
            if (PT1.pos.x - Blocks0.pos.x) > 0:
                return 2
            return -2
        return np.arctan((PT1.pos.x - Blocks0.pos.x) / (PT1.pos.y - Blocks0.pos.y))
    def get_state(self, game):
        state = [
            self.metoda(game.PT1, game.Blocks0)
        ]
        return state

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            return
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # Epsilon-greedy strategy

        if random.randint(0, 200) < self.epsilon:
            # Explore: select a random action
            final_move = random.choice([0, 1, 2])
        else:
            # Exploit: select the action with max value (greedy)
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            final_move = torch.argmax(prediction).item()
        self.epsilon = self.epsilon * 0.9999
        print("Epsilon: ", self.epsilon)
        return final_move

    def train(self):
        plot_scores = []
        plot_mean_scores = []
        total_score = 0
        game = Game()
        game.loadgrafic()
        game.blocksgroup.add(game.Blocks0)
        game.all_sprites.add(game.PT1)
        game.all_sprites.add(game.Blocks0)

        while Properties.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Properties.running = False
            if Properties.running == False:
                break
            state_old = self.get_state(game)
            final_move = self.get_action(state_old)
            reward, done, score = game.play_step(final_move)
            state_new = self.get_state(game)
            self.train_short_memory(state_old, final_move, reward, state_new, done)
            self.remember(state_old, final_move, reward, state_new, done)

            if Properties.running == False:
                Properties.running=True
                game.reset()
                Properties.n_games += 1
                self.train_long_memory()

                if score > Properties.maxscore:
                    Properties.maxscore = score
                    self.model.save()
                    print("saved")

                plot_scores.append(score)
                total_score += score
                mean_score = total_score / Properties.n_games
                plot_mean_scores.append(mean_score)
                plot(plot_scores, plot_mean_scores)

                print('Game', Properties.n_games, 'Score', score, 'Record:', Properties.maxscore)

if __name__ == "__main__":

    agent = Agent()
    agent.train()