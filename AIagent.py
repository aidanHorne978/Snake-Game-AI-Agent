#!/usr/bin/python
import pygame
import random
import numpy as np
import snake

# Basically wanna make a genetic algorithm that will have a bunch of chromosomes and will make its way to the fruit.
# It's allowed to know where the fruit is but not how to get to it. It has to learn that

# Need to be aware that i need to be able to run multiple AIagent's with multithreading processing so it doesn't take years to learn.


class Player:

    def __init__(self, chromosome):
        chromosome = np.zeros(400)
        self.chromosome = chromosome

    def createPopulation(self):
        self.chromosome = np.random.random(400)
    
    def displayPopulation(self):
        return print("{}".format(self.chromosome))

    def chromosomeSet(self):
        return self.chromosome


def dividePopulation(newPop):
    left = newPop.chromosomeSet()[0:99]
    right = newPop.chromosomeSet()[100:199]
    up = newPop.chromosomeSet()[200:299]
    down = newPop.chromosomeSet()[300:399]

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

def runGame(player):

    while True:

        move = dividePopulation(player)

        if move == 0:
            lastMove = "left"
        elif move == 1:
            lastMove = "right"
        elif move == 2:
            lastMove = "up"
        elif move == 3:
            lastMove = "down"

        # Run's the code for the snake game
        evaluation = snake.SnakeGame(agent, lastMove, fruit)
        if evaluation[2] == False:
            return evaluation[0], evaluation[1]

        # Close screen if user clicks quit or the red arrow in the top right corner.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
        # print("Snake position: {}\t Fruit position: {}".format(player.pos(), fruit.pos()))

        pygame.display.update()

def fitness(population):

    scores = []
    
    highestScore = max(population[0])
    highestDistance = max(population[1])

    avgScore = 0
    for score in population[0]:
        avgScore += score
    
    avgDistance = 0
    for distance in population[1]:
        avgDistance += distance
    
    avgScore = avgScore / len(population[0])
    avgDistance = avgDistance / len(population[1])

    for player in population:

        score = 0

        if player[0] > avgScore:
            score += 200
        
        if player[1] > avgDistance:
            score += 500
        
        if player[0] > highestScore:
            score += 1000
        
        if player[1] > highestDistance:
            score += 1000

        scores.append(score)
    
    return scores

def crossover(population):

    mother = population[0:11]
    father = population[12:23]

    newGeneration = []

    for i in range(24):

        child = []
        for j in range(len(population[0].chromosomeSet())):

            coin = random.randint(0, 1)
            if coin == 0:
                child.append(mother[i][j])
            else:
                child.append(father[i][j])
        
        newGeneration.append(child)

        print(child)
        print(population[0])
        exit()
# Creating a population of chromosomes for the AIagent.
population = []
for i in range(100):
    population.append(Player(np.zeros(0)))
    population[i].createPopulation()

# Initilizing variables.
screen = snake.screen
width = snake.width
height = snake.height
lastMove = "left"

# Run the main menu.
# snake.MainMenu()

while True:

    results = []
    for i in range(len(population)):
        agent = snake.Snake(width / 2 - 30, height / 2 - 60, [])
        fruit = snake.Fruit(0,0)
        results.append(runGame(population[i]))

    currentScores = fitness(results)
    newGeneration = []
    for i in range(100):

        if len(newGeneration) == 24:
            break

        if currentScores[i] > sum(currentScores) / len(currentScores):
            newGeneration.append(population[i])

    crossover(newGeneration)






# def UserControl():
    # If the user presses a key that is allowed it will remember the key for when the clock ticks and the snake is moved.
    # if event.type == pygame.KEYDOWN:
    #     if event.key == pygame.K_LEFT or event.key == pygame.K_a:
    #         if lastMove != "right":
    #             lastMove = "left"
    #     if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
    #         if lastMove != "left":
    #             lastMove = "right"
    #     if event.key == pygame.K_UP or event.key == pygame.K_w:
    #         if lastMove != "down":
    #             lastMove = "up"
    #     if event.key == pygame.K_DOWN or event.key == pygame.K_s:
    #         if lastMove != "up":
    #             lastMove = "down"