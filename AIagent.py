#!/usr/bin/python
import pygame
import random
import numpy as np
import snake

nPercepts = 75
nActions = 4

class AIPlayer:

    def __init__(self):
        self.chromosome = np.random.rand(nPercepts * nActions)
    
    def AgentFunction(self):
        actions = np.zeros(5)
        count = 0
        all_percepts = self.chromosome
        responses = np.zeros(375)
        for j in range(5):
            for percept in all_percepts:
                responses[count] = self.chromosome[count] * percept
                count += 1
                print(responses)

        count = 0
        for i in range(375):
            actions[count - 1] += responses[i]
            if i % 75 == 0:
                count += 1

        return actions

trainingSchedule = [("random", 1000), ("self", 1)]

x = AIPlayer()

print(x.AgentFunction())

# screen = snake.screen
# width = snake.width
# height = snake.height

# snake.MainMenu()

# player = snake.Snake(width / 2 - 30, height / 2 - 60, [])

# while True:
#     snake.SnakeGame(player)
#     print(player.body)

