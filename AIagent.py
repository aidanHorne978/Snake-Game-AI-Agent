#!/usr/bin/python
import pygame
import random
import numpy as np
import snake
import time
from multiprocessing import Pool
from functools import partial


""" 

To do list:


    - Need to be aware that i need to be able to run multiple AIagent's with multithreading processing so it doesn't take years to learn.
      Might not be more efficient but will have to test.
      Could move it all into snake.py and then use Pool() to make multiple instances of the snake.py file running 10 Player's at once. Then it will return it's best
      Agent and those 5 agents can be used to vs the player. Will make training time quicker but not sure if it's possible to implement.


    - New class for the player to be able to play the game again.
    - New class to let the player go head to head against a trained agent.
    - Graphing of training and how the neural network operates.
    - Work on GUI and make it more user friendly.

    - mutation(population): After generation 30 the model could be overfitted and need new genes to generate smarter snakes.
      Currently it overrides too many chromosomes so need to tinker.
    - trainGen(population, generation): Need to store the best n agents and return them.
    
"""

class Player:

    def __init__(self, hScore, deaths, penalties, avg_steps, distance):
        
        # Initilizing with the size of the chromosomes.
        self.chromosome = np.zeros(45243)

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
        self.chromosome = np.random.uniform(-1, 1, 45243)
    
    # Prints the population for debugging.
    def displayPopulation(self):
        return print("{}".format(self.chromosome))

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
    wall = [0, 0, 0, 0]

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
    
    # relative pos of food:
    relativePosx = (fruit.x - snake.x) / res[0]
    relativePosy = (fruit.y - snake.y) / res[1]

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

    for i in range(1, 3):
        input_vector = np.append(input_vector, wall[i])

    for i in range(4):
        input_vector = np.append(input_vector, currdirection[i])
        input_vector = np.append(input_vector, posFood[i])

    input_vector = np.append(input_vector, relativePosx)
    input_vector = np.append(input_vector, relativePosy)

    # Chromosomes split.
    input_to_layer1 = newPop.chromosome[0:1560].reshape(13, 120)
    input_to_layer1[:, 0] = input_vector
    layer1_to_layer2 = newPop.chromosome[1561:15961].reshape(120, 120)
    layer2_to_layer3 = newPop.chromosome[15962:30362].reshape(120, 120)
    layer3_to_layer4 = newPop.chromosome[30362:44762].reshape(120, 120)
    layer3_to_output = newPop.chromosome[44763:45243].reshape(120, 4)

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

        # Runs the neural network to decide which direction to move.
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

        if steps == 1000:
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
        
        # Fitness function.
        score = player.hScore * 10000 - player.deaths * 150 - player.avg_steps * 100 - player.penalties * 1000
        scores.append((score, player))

    return scores

def crossover(population):

    # Split the n best from last generation into mother and father.
    mother = population[0:5]
    father = population[6:11]

    newGeneration = []

    for i in range(3):
        newGeneration.append(population[i])

    # population is sorted by highest fitness so we append the first 3 for the next generation (Elitism).
    while len(newGeneration) < 50:
        child = Player(0, 0, 0, 0, 0)
        parent = random.randint(0, len(mother) - 1)
        for j in range(46122):
            
            coin = random.getrandbits(1)

            if coin == 0:
                child.insert(mother[parent].chromosome[j], j)
            else:
                child.insert(father[parent].chromosome[j], j)

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

def trainGen(population):

    bestAgents = []
    generation = 0
    while True:
        
        # How many generations it's going to train for.
        if generation == 100:
            break

        # Priting out the current generation.
        print("Generation: {}".format(generation))
        if generation == 100:
            exit()
        
        newGeneration = []
        
        # Running the game for every agent in the generation.
        for i in range(49):
            agent = snake.Snake(width / 2 - 30, height / 2 - 60, [])
            fruit = snake.Fruit(0,0)

            # Output is (score, distance, death, avg_steps, penalties)
            score = runGame(population[i], generation, lastMove, agent, fruit)

            if population[i].hScore < score[0]:
                population[i].hScore = score[0]

        currentFitness = fitness(population)
        currentFitness = sorted(currentFitness, key=lambda x: x[0], reverse=True)

        # To initilize best agents list with best 3 from first run.
        if generation == 0:
            for i in range(3):
                bestAgents.append(currentFitness[i])

        # We will compare the best agents from the last generation and see if we did better this time.
        for i in range(3):
            if bestAgents[i][0] < currentFitness[i][0]:
                bestAgents[i] = currentFitness[i]

        cFitness = []
        for x in currentFitness:
            cFitness.append(x[0])
            
        print(cFitness)
        print()
        print("Current Max: {}".format(currentFitness[0][0]))
        print()

        # Selection process of the 24 best agents to make children.
        for i in range(12):
            newGeneration.append(currentFitness[i][1])
        
        population = crossover(newGeneration)

        generation += 1

    return bestAgents

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
res = snake.res

# Run the main menu.
# snake.MainMenu()

# Train the population and will return the 3 best agents.
start = time.time()
results = trainGen(population)
end = time.time()

print(end - start)
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