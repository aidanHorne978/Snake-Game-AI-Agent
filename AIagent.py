#!/usr/bin/python
import pygame
import random
import numpy as np
import snake
import time

# Basically wanna make a genetic algorithm that will have a bunch of chromosomes and will make its way to the fruit.
# It's allowed to know where the fruit is but not how to get to it. It has to learn that

# Need to be aware that i need to be able to run multiple AIagent's with multithreading processing so it doesn't take years to learn.


class Player:

    def __init__(self, chromosome, hScore, deaths, penalties, avg_steps):
        chromosome = np.zeros(70)
        self.chromosome = chromosome
        self.hScore = hScore
        self.deaths = deaths
        self.penalties = penalties
        self.avg_steps = avg_steps

    def insert(self, value, index):
        self.chromosome[index] = value

    def createPopulation(self):
        self.chromosome = np.random.uniform(-1, 1, 70)
    
    def displayPopulation(self):
        return print("{}".format(self.chromosome))

    def chromosomeSet(self):
        return self.chromosome

    def setHigh(self, score):
        self.hScore = score

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def make_prediction(input_vector, weights):
    layer1 = np.dot(input_vector[1:], weights) + input_vector[0]
    layer2 = sigmoid(layer1)
    return layer2

def makeMove(newPop, snake, lastMove):

    # Input nodes.

    # Relative position of food to the head of the snake.
    posFood = [0, 0, 0, 0]
    # If food is up and left
    if snake.x < fruit.x and snake.y < fruit.y:
        posFood[0] = 1
        posFood[2] = 1
    # if food is down and left
    elif snake.x < fruit.x and snake.y > fruit.y:
        posFood[0] = 1
        posFood[3] = 1
    # if food is up and right
    elif snake.x > fruit.x and snake.y < fruit.y:
        posFood[1] = 1
        posFood[2] = 1
    # if food is down and right
    else:
        posFood[1] = 1
        posFood[3] = 1
    
    # Distance from head of snake to food.
    distFood = (snake.x - fruit.x, snake.y - fruit.y)

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
    else:
        wall[3] = 1
    
    currdirection = [0, 0, 0, 0]
    if lastMove == "left":
        currdirection[0] = 1
    elif lastMove == "right":
        currdirection[1] = 1
    elif lastMove == "up":
        currdirection[2] = 1
    else:
        currdirection[3] = 1

    input_vector = np.array(3)

    for i in range(4):
        input_vector = np.append(input_vector, wall[i])
        input_vector = np.append(input_vector, currdirection[i])
        input_vector = np.append(input_vector, posFood[i])

    input_vector = np.append(input_vector, int(distFood[0]))
    input_vector = np.append(input_vector, int(distFood[1]))

    left = make_prediction(input_vector, newPop.chromosomeSet()[0:14])
    right = make_prediction(input_vector, newPop.chromosomeSet()[15:29])
    up = make_prediction(input_vector, newPop.chromosomeSet()[30:44])
    down = make_prediction(input_vector, newPop.chromosomeSet()[45:59])

    move = left, right, up, down

    return move

def runGame(player, gen, lastMove):

    steps = 0
    deaths = 0
    oldScore = 0
    penalty = False

    global agent
    global fruit

    while True:
        
        # If the snake dies it then gets reset
        if agent.x < 20 or agent.x > 860:
            agent = snake.Snake(width / 2 - 30, height / 2 - 60, [])
        elif agent.y < 20 or agent.y > 700:
            agent = snake.Snake(width / 2 - 30, height / 2 - 60, [])

        move = makeMove(player, agent, lastMove)

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

        score = player.hScore * 5000 - player.deaths * 50 - player.avg_steps * 10 - player.penalties * 100

        if score > 0:
            fitness = score
        else:
            fitness = 0 + player.hScore * 20 + player.avg_steps
        
        scores.append(fitness)
    
    return scores

def crossover(population):

    mother = population[0:int(len(population) / 2 - 1)]
    father = population[int(len(population) / 2):int(len(population) - 1)]

    newGeneration = []
    while len(newGeneration) != 50:

        child = Player(np.array(mother[0].chromosomeSet()[0]), 0, 0, 0, 0)
        for j in range(1, len(mother) - 1):
            
            gene = random.randint(0, int(len(mother) / 2))
            coin = random.uniform(0, 1)

            if coin < 0.5:
                child.insert(mother[gene].chromosomeSet()[j], j)
            else:
                child.insert(father[gene].chromosomeSet()[j], j)

        newGeneration.append(child)

    return newGeneration

def mutation(population):

    for i in range(len(population)):

        for j in range(5):
            population[i].chromosomeSet()[random.randint(0, 49)] = random.randint(-1, 1)
    
    return population

# Creating a population of chromosomes for the AIagent.
population = []
for i in range(50):
    population.append(Player(np.zeros(0), 0, 0, 0, 0))
    population[i].createPopulation()

# Initilizing variables.
screen = snake.screen
width = snake.width
height = snake.height
lastMove = "left"
generation = 0

# Run the main menu.
# snake.MainMenu()


while True:
    
    print("Generation: {}".format(generation))
    if generation == 100:
        exit()
    results = []
    newGeneration = []
    currentScores = []
    for i in range(49):
        agent = snake.Snake(width / 2 - 30, height / 2 - 60, [])
        fruit = snake.Fruit(0,0)

        # Output is (score, distance, death, avg_steps, penalties)
        try:
            score = runGame(population[i], generation, lastMove)
        except IndexError:
            print(len(population))

        if population[i].hScore != 0:
            population[i].avg_steps = int(population[i].avg_steps / population[i].hScore)

        if population[i].hScore < score[0]:
            population[i].setHigh(score[0])

    # Selection process of the 24 best agents to make children.
    x = 0
    currentFitness = fitness(population)
    print(currentFitness)
    print()
    time.sleep(5)
    while len(newGeneration) != 12:

        if x > 50 - len(newGeneration) - 1:
            x = 0

        if currentFitness[x] == max(currentFitness):
            newGeneration.append(population[x])
            currentFitness.remove(currentFitness[x])
    
        x += 1

    population = crossover(newGeneration)
    population = mutation(population)

    generation += 1


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