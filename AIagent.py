#!/usr/bin/python
import pygame
import random
import numpy as np
import snake
import time
from multiprocessing import Process

# Need to be aware that i need to be able to run multiple AIagent's with multithreading processing so it doesn't take years to learn.
# Might not be more efficient but will have to test.

class Player:

    def __init__(self, hScore, deaths, penalties, avg_steps, distance):
        
        # Initilizing with the size of the chromosomes.
        self.chromosome = np.zeros(46122)

        # Player's high score in training.
        self.hScore = hScore

        # Amount of deaths in training.
        self.deaths = deaths

        # Penalties received during training.
        self.penalties = penalties

        # Average steps during training.
        self.avg_steps = avg_steps

        # Distance travelled during training.
        self.distance = distance

    # Insert a chromosome at a certain index.
    def insert(self, value, index):
        self.chromosome[index] = value

    # Initilizes the chromosomes for a player.
    def createPopulation(self):
        self.chromosome = np.random.uniform(-1, 1, 46122)
    
    # Prints the population for debugging.
    def displayPopulation(self):
        return print("{}".format(self.chromosome))

    # Returns the players chromosome set.
    def chromosomeSet(self):
        return self.chromosome

    # Sets the highscore of a player.
    def setHigh(self, score):
        self.hScore = score

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def make_prediction(input_vector, input_to_layer1, layer1_to_layer2, layer2_to_layer3, layer3_to_layer4, layer3_to_output, bias):

    layer1 = np.dot(input_vector, input_to_layer1)
    layer2 = sigmoid(np.dot(layer1, layer1_to_layer2) + bias)
    layer3 = sigmoid(np.dot(layer2, layer2_to_layer3) + bias)
    layer4 = sigmoid(np.dot(layer3, layer3_to_layer4) + bias)
    output_layer = np.dot(layer4, layer3_to_output) + bias
    return output_layer

def makeMove(newPop, snake, lastMove, fruit):

    # Input nodes.

    # Relative position of food to the head of the snake.
    posFood = [0, 0, 0, 0]
    # If food is up and left
    if snake.x > fruit.x and snake.y < fruit.y:
        posFood[0] = 1
        posFood[2] = 1
    # if food is down and left
    elif snake.x > fruit.x and snake.y > fruit.y:
        posFood[0] = 1
        posFood[3] = 1
    # if food is up and right
    elif snake.x < fruit.x and snake.y < fruit.y:
        posFood[1] = 1
        posFood[2] = 1
    # if food is down and right
    elif snake.x < fruit.y and snake.y > fruit.y:
        posFood[1] = 1
        posFood[3] = 1

    # Current direction aka lastMove variable

    wall = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # wall on left
    if snake.x - 20 == 20:
        wall[0] = 1
    # wall on right
    elif snake.x + 20 == 860:
        wall[1] = 1
    # wall down
    elif snake.y - 20 == 20:
        wall[2] = 1
    # wall up
    elif snake.y + 20 == 700:
        wall[3] = 1

    # wall on left
    if snake.x - 40 == 20:
        wall[4] = 0.75
    # wall on right
    elif snake.x + 40 == 860:
        wall[5] = 0.75
    # wall down
    elif snake.y - 40 == 20:
        wall[6] = 0.75
    # wall up
    elif snake.y + 40 == 700:
        wall[7] = 0.75

    # wall on left
    if snake.x - 60 == 20:
        wall[8] = 0.5
    # wall on right
    elif snake.x + 60 == 860:
        wall[9] = 0.5
    # wall down
    elif snake.y - 60 == 20:
        wall[10] = 0.5
    # wall up
    elif snake.y + 60 == 700:
        wall[11] = 0.5
    
    currdirection = [0, 0, 0, 0]
    if lastMove == "left":
        currdirection[0] = 1
    elif lastMove == "right":
        currdirection[1] = 1
    elif lastMove == "up":
        currdirection[2] = 1
    else:
        currdirection[3] = 1

    input_vector = np.array(wall[0])

    for i in range(1, 10):
        input_vector = np.append(input_vector, wall[i])

    for i in range(4):
        input_vector = np.append(input_vector, currdirection[i])
        input_vector = np.append(input_vector, posFood[i])

    # Chromosomes split.
    input_to_layer1 = newPop.chromosome[0:2160].reshape(18, 120)
    input_to_layer1[:, 0] = input_vector
    layer1_to_layer2 = newPop.chromosome[2401:16801].reshape(120, 120)
    layer2_to_layer3 = newPop.chromosome[16841:31241].reshape(120, 120)
    layer3_to_layer4 = newPop.chromosome[31241:45641].reshape(120, 120)
    layer3_to_output = newPop.chromosome[45642:46122].reshape(120, 4)

    move = make_prediction(input_vector, input_to_layer1, layer1_to_layer2, layer2_to_layer3, layer3_to_layer4, layer3_to_output, 0.1)

    return move

def runGame(player, gen, lastMove, agent, fruit):

    steps = 0
    deaths = 0
    oldScore = 0
    penalty = False

    while True:
        
        # If the snake dies it then gets reset
        if agent.x < 20 or agent.x > 860:
            agent = snake.Snake(width / 2 - 30, height / 2 - 60, [])
        elif agent.y < 20 or agent.y > 700:
            agent = snake.Snake(width / 2 - 30, height / 2 - 60, [])

        move = makeMove(player, agent, lastMove, fruit)

        if move[0] == max(move):
            if lastMove != "right":
                lastMove = "left"
        elif move[1] == max(move):
            if lastMove != "left":
                lastMove = "right"
        elif move[2] == max(move):
            if lastMove != "down":
                lastMove = "up"
        else:
            lastMove = "down"

        # Run's the code for the snake game.
        evaluation = snake.SnakeGame(agent, lastMove, fruit, gen)

        # If the snake goes 200 steps without eating food.
        if steps % 200 == 0 and steps != 0 and penalty == True:
            player.penalties += 1

        # If the snake gets a fruit then we start counting steps.
        if player.hScore > oldScore:
            oldScore = player.hScore
            penalty = True
            player.avg_steps += steps

        # Keeps track of the players steps throughout training.
        player.distance += evaluation[1]

        # Keeps track of deaths.
        if evaluation[2] == False:
            player.deaths += 1

        # Keeps track of highest score.
        if evaluation[0] > player.hScore:
            player.hScore = evaluation[0]

        if steps == 2000:
            return evaluation[0], evaluation[1], deaths

        # Close screen if user clicks quit or the red arrow in the top right corner.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
        # print("Snake position: {}\t Fruit position: {}".format(player.pos(), fruit.pos()))
        pygame.display.update()
        steps += 1

def fitness(population):

    scores = []

    for player in population:
        score = player.hScore * 10000 - player.deaths * 150 - player.avg_steps * 100 - player.penalties * 1000
        scores.append(score)

    return scores

def crossover(population):

    mother = population[0:int(len(population) / 2 - 1)]
    father = population[int(len(population) / 2):int(len(population) - 1)]

    newGeneration = []

    for i in range(3):
        newGeneration.append(population[i])

    while len(newGeneration) != 50:

        child = Player(0, 0, 0, 0, 0)

        for j in range(0, len(population[0].chromosome)):
            
            coin = np.random.uniform(-1, 1, 1)
            gene = random.randint(0, len(mother) - 1)

            if coin < 0:
                child.insert(mother[gene].chromosomeSet()[j], j)
            else:
                child.insert(father[gene].chromosomeSet()[j], j)

        newGeneration.append(child)

    return newGeneration

def mutation(population):

    prob = random.randint(0, 100)

    if prob % 10 == 0:
        chromeRange = random.randint(0, len(population[0].chromosome) / 2), random.randint(len(population[0].chromosome) / 2, len(population[0].chromosome))
        for j in range(random.randint(0, 25)):
            population[j].chromosomeSet()[chromeRange[0]:chromeRange[1]] = random.randint(-1, 1)
        print("mutated", chromeRange)
        
    return population

def trainGen(population, generation):

    while True:
    
        if generation == 100:
            break

        print("Generation: {}".format(generation))
        if generation == 100:
            exit()
        
        newGeneration = []
        for i in range(49):
            agent = snake.Snake(width / 2 - 30, height / 2 - 60, [])
            fruit = snake.Fruit(0,0)

            # Output is (score, distance, death, avg_steps, penalties)
            score = runGame(population[i], generation, lastMove, agent, fruit)

            if population[i].hScore != 0:
                population[i].avg_steps = int(population[i].avg_steps / population[i].hScore)

            if population[i].hScore < score[0]:
                population[i].setHigh(score[0])

        # Selection process of the 24 best agents to make children.
        x = 0
        currentFitness = fitness(population)

        print(sorted(currentFitness))
        print()

        fitnessDict = dict()
        
        for player in population:
            if currentFitness[x] not in fitnessDict.keys():
                fitnessDict[currentFitness[x]] = player
            x += 1

        x = 0
        fitnessDict = sorted(fitnessDict.items(), reverse=True)
        fitnessDict = dict(fitnessDict)

        for i in range(12):
            
            newGeneration.append(list(fitnessDict.values())[i])
        
        population = crossover(newGeneration)
        # if generation > 30:
        #     population = mutation(population)

        generation += 1

    return population, currentFitness

# Creating a population of chromosomes for the AIagent.
population = []
for i in range(50):
    population.append(Player(0, 0, 0, 0, 0))
    population[i].createPopulation()

# Initilizing variables.
screen = snake.screen
width = snake.width
height = snake.height
lastMove = "left"
generation = 0

# Run the main menu.
# snake.MainMenu()

# Train the first generation.
results = trainGen(population, generation)

# Pick the best Player in the population
# print(results[0][1])
# bestAgent = results[0][2]

# Run game with best agent
# run = True
# while run == True:
#     runGame(bestAgent, 0, "left", agent = snake.Snake(width / 2 - 30, height / 2 - 60, []), fruit = snake.Fruit(0,0))
#     input = input("Do you want to play another?")
#     if input != "yes" or input != "y":
#         run = False

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