#!/usr/bin/python
import pygame
import random
import numpy as np
import snake

# Basically wanna make a genetic algorithm that will have a bunch of chromosomes and will make its way to the fruit.
# It's allowed to know where the fruit is but not how to get to it. It has to learn that

# Need to be aware that i need to be able to run multiple AIagent's with multithreading processing so it doesn't take years to learn.

# Creates the inital population.
class Population:

    def __init__(self, chromosome):
        self.chromosome = chromosome

    def createPopulation(self):
        self.chromosome = np.random.random(400)
    
    def displayPopulation(self):
        return print("{}".format(self.chromosome))

    def population(self):
        return self.chromosome


def dividePopulation(population):
    left = population.population()[0:99]
    right = population.population()[100:199]
    up = population.population()[200:299]
    down = population.population()[300:399]

    moves = [left, right, up, down]
    weights = []
    total = 0

    for move in moves:
        for value in move:
            total += value
        total / len(move)
        weights.append(total)
        total = 0

    direction = max(weights)
    index = weights.index(direction)

    return index


# Creating a population of chromosomes for the AIagent.
newPop = Population(np.zeros(400))
newPop.createPopulation()

# Initilizing variables.
screen = snake.screen
width = snake.width
height = snake.height
lastMove = "left"

# Run the main menu.
snake.MainMenu()

# A player and fruit object are passed through to snake.py now so we have access to the information of snake and fruit.
player = snake.Snake(width / 2 - 30, height / 2 - 60, [])
fruit = snake.Fruit(0,0)

# Running the game.
while True:

    index = dividePopulation(newPop)

    if index == 0:
        lastMove = "left"
    elif index == 1:
        lastMove = "right"
    elif index == 2:
        lastMove = "up"
    elif index == 3:
        lastMove = "down"

    # Run's the code for the snake game
    snake.SnakeGame(player, lastMove, fruit)

    # Close screen if user clicks quit or the red arrow in the top right corner.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        # If the user presses a key that is allowed it will remember the key for when the clock ticks and the snake is moved.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if lastMove != "right":
                    lastMove = "left"
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if lastMove != "left":
                    lastMove = "right"
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if lastMove != "down":
                    lastMove = "up"
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if lastMove != "up":
                    lastMove = "down"
        
    print("Snake position: {}\t Fruit position: {}".format(player.pos(), fruit.pos()))

    pygame.display.update()
