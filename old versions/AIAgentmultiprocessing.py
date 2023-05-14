#!/usr/bin/python
import random
import numpy as np
import time
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from multiprocessing import Pool

class Agent:

    def __init__(self, hScore, deaths, penalties, avg_steps):
        
        # Initilizing with the size of the player's chromosomes.
        self.chromosome = np.zeros(amountOfChromosomes)

        # Player's highest score in training.
        self.hScore = hScore

        # Amount of deaths in training.
        self.deaths = deaths

        # Penalties received during training.
        self.penalties = penalties

        # Average steps during training.
        self.avg_steps = avg_steps

    # Insert a chromosome at a certain index.
    def insert(self, value, index):
        self.chromosome[index] = value

    # Initilizes the chromosomes for a player.
    def createPopulation(self):
        self.chromosome = np.random.uniform(-1, 1, amountOfChromosomes)

class Snake:

    # Initilizes the snake with it's heads x, y value and body which is a list.
    def __init__(self, x, y, body):
        self.x = x
        self.y = y
        self.body = body

    # Draws the snake's body.
    def draw(self):
        return pygame.Rect(self.x, self.y, blockSize, blockSize)

class Fruit:

    # Initilizes the fruit object and which has an x and y coordinate.
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Generates a fruit with a range so it fits inside grid of the game.
    def generateFruit(self):
        newx = random.randrange(blockSize, res[0] - blockSize, blockSize)
        newy = random.randrange(blockSize, res[1] - blockSize - 100, blockSize)
        self.x = newx
        self.y = newy
        return self.x, self.y

    # Draw's the fruit on the grid.
    def drawFruit(self):
        rect = pygame.Rect(self.x, self.y, blockSize, blockSize)
        return pygame.draw.rect(screen, RED, rect)

def Grow(snake, direction):

    # Will create the new segment on the tile the snake's head just left.
    if direction == "left":
        segment = pygame.Rect(snake.body[-1].x + blockSize, snake.body[-1].y, blockSize, blockSize)
        snake.body.insert(len(snake.body), segment)
    if direction == "right":
        segment = pygame.Rect(snake.body[-1].x - blockSize, snake.body[-1].y, blockSize, blockSize)
        snake.body.insert(len(snake.body), segment)    
    if direction == "up":
        segment = pygame.Rect(snake.body[-1].x, snake.body[-1].y + blockSize, blockSize, blockSize)
        snake.body.insert(len(snake.body), segment)   
    if direction == "down":
        segment = pygame.Rect(snake.body[-1].x, snake.body[-1].y - blockSize, blockSize, blockSize)
        snake.body.insert(len(snake.body), segment)

def MoveSnake(direction, snake, draw):

    # Moves the head of the snake.
    if direction == "left":
        snake.x -= blockSize
    elif direction == "right":
        snake.x += blockSize
    elif direction == "up":
        snake.y -= blockSize
    elif direction == "down":
        snake.y += blockSize

    # If we are displaying to the user we draw it to the screen.
    if draw:
        pygame.draw.rect(screen, BLACK, snake.draw())

    # This moves the body in the way a snake does, by following the segment before it.
    if len(snake.body) > 1:

        for j in reversed(range(1, len(snake.body))):

            if snake.body[j - 1] == snake.x:
                snake.body[j].x = snake.x
            else:
                snake.body[j].x = snake.body[j - 1].x

            if snake.body[j - 1] == snake.y:
                snake.body[j].y = snake.y
            else:
                snake.body[j].y = snake.body[j - 1].y

            # If we are displaying to the user we draw it to the screen.
            if draw:
                pygame.draw.rect(screen, BLACK, snake.body[j])
                pygame.draw.rect(screen, pygame.Color(GRASS), snake.body[-1])
                pygame.draw.rect(screen, BLACK, snake.body[-1], 1)

    # Update the head in the body list.
    snake.body[0].x = snake.x
    snake.body[0].y = snake.y

def SnakeGame(agent, lastMove, fruit):

    scored = False

    # If this is the first run through for the current agent we initilize some variables.
    if len(agent.body) < 1:

        global score
        score = 0

        # Head of snake.
        agent.body.append(pygame.Rect(agent.x, agent.y, blockSize, blockSize))

        # Tail of snake.
        agent.body.append(pygame.Rect(agent.x, agent.y, blockSize, blockSize))

        # Score variable.
        score = 0

    # Move the snake in a direction picked by the neural network.
    MoveSnake(lastMove, agent, False)

    # When you get a fruit it will replace it with another randomly generated fruit.
    # Then it will add one to the score and display it.
    if agent.x == fruit.x and agent.y == fruit.y:

        # Adds a part to the body.
        Grow(agent, lastMove)

        # Increase score by one.
        score += 1
        scored = True

    # If the snake hit's itself.
    if len(agent.body) > 2:
        for parts in agent.body[1:]:
            if agent.x == parts.x and agent.y == parts.y:
                return score, scored, False

    # If the snake hit's the horizontal barrier we return with False which indicates a death.
    if agent.x < 20 or agent.x > 860:
        return score, scored, False

    # If the snake hit's the vertical barrier we return with False which indicates a death.
    if agent.y < 20 or agent.y > 700:
        return score, scored, False
    else:

        # If the snake didn't die then we return the score, whether they scored or not and True indicating it's still alive.
        return score, scored, True

def sigmoid(x):
    
    # Activation function.
    return 1 / (1 + np.exp(-x))

def make_prediction(input_vector, input_to_layer1, layer1_to_layer2, layer2_to_output, bias):

    # Neural network for the agent to make decisions.
    layer1 = np.dot(input_vector, input_to_layer1)
    layer2 = sigmoid(np.dot(layer1, layer1_to_layer2) + bias)
    output_layer = np.dot(layer2, layer2_to_output) + bias
    return output_layer

def makeMove(agent, snake, lastMove, fruit, debug):

    # --------------------------------- DEBUGGING ---------------------------------

    # print("Snake x: {}\tSnake y: {}\tFruit x: {}\tFruit y: {}".format(snake.x, snake.y, fruit.x, fruit.y))

    # --------------------------------- DEBUGGING ---------------------------------

    ## Input nodes ##

    # Orientation is Left, Right, Up, Down in the lists.

    # Read's a 1 if the food is in that direction, else 0. Will have 2 1's unless the snake is on the correct horizontal or vertical axis.
    posFood = [0, 0, 0, 0]
    if snake.x != fruit.x:
        if snake.x > fruit.x:
            posFood[0] = 1
        elif snake.x < fruit.x:
            posFood[1] = 1
    if snake.y != fruit.y:
        if snake.y > fruit.y:
            posFood[2] = 1
        elif snake.y < fruit.y:
            posFood[3] = 1

    # Read's 1 if there is a wall in that direction, else 0.
    wall = [0, 0, 0, 0]
    if snake.x == 20:
        wall[0] = 1
    if snake.x == 860:
        wall[1] = 1
    if snake.y == 20:
        wall[2] = 1
    if snake.y == 700:
        wall[3] = 1

    # Gives the relative position of the food like posFood. Index 0 will have -1 if food is left, else 0. Index 1 will have -1 if food is right, else 0.
    # Index 2 will have -1 if food is up, else 0, Index 3 will have -1 if food is down, else 0.
    # relativePos = [0, 0, 0, 0]
    # if fruit.x < snake.x:
    #     relativePos[0] = -1
    # elif fruit.x > snake.x:
    #     relativePos[1] = 1
        
    # if fruit.y < snake.y:
    #     relativePos[2] = -1
    # elif fruit.y > snake.y:
    #     relativePos[3] = 1

    # Current direction the snake is moving aka lastMove variable.
    currdirection = [0, 0, 0, 0]
    if lastMove == "left":
        currdirection[0] = 1
    if lastMove == "right":
        currdirection[1] = 1
    if lastMove == "up":
        currdirection[2] = 1
    if lastMove == "down":
        currdirection[3] = 1

    # Putting the input nodes into an array.
    input_vector = np.array(posFood[0])

    for i in range(4):
        if i > 0:
            input_vector = np.append(input_vector, posFood[i])
        input_vector = np.append(input_vector, wall[i])
        input_vector = np.append(input_vector, currdirection[i])
        # input_vector = np.append(input_vector, relativePos[i])


    # Neural network's structure is an input layer (12 -> 120) values, hidden layer (120 -> 120) values and an output layer (120 -> 4) values.
    input_to_layer1 = agent.chromosome[0:1440].reshape(12, 120)
    input_to_layer1[:, 0] = input_vector
    layer1_to_layer2 = agent.chromosome[1441:15841].reshape(120, 120)
    layer2_to_output = agent.chromosome[15841:16321].reshape(120, 4)

    # --------------------------------- DEBUGGING ---------------------------------
    # 14 input nodes.
    # input_to_layer1 = agent.chromosome[0:1680].reshape(14, 120)
    # input_to_layer1[:, 0] = input_vector
    # layer1_to_layer2 = agent.chromosome[1681:16081].reshape(120, 120)
    # layer2_to_layer3 = agent.chromosome[16082:30482].reshape(120, 120)
    # layer3_to_output = agent.chromosome[30483:30963].reshape(120, 4)

    # 16 input nodes
    # input_to_layer1 = agent.chromosome[0:1920].reshape(16, 120)
    # input_to_layer1[:, 0] = input_vector
    # layer1_to_layer2 = agent.chromosome[1921:16321].reshape(120, 120)
    # layer2_to_output = agent.chromosome[16321:16801].reshape(120, 4)

    if debug:
        return move, [wall, currdirection, posFood]

    # --------------------------------- DEBUGGING ---------------------------------

    # Return's a numpy array of 4 numbers with the highest being the best move.
    move = make_prediction(input_vector, input_to_layer1, layer1_to_layer2, layer2_to_output, 0)

    # Convert to list.
    move = move.tolist()
    return move

def fitness(population):

    scores = []
    # Review how the agent performed in that generation and return it's score.
    for agent in population:
        if agent.hScore > 0:
            score = agent.hScore * 5000  - agent.deaths * 150 - int(sum(agent.avg_steps) / len(agent.avg_steps) * 100) - agent.penalties * 1000
        else:
            score = agent.hScore * 5000  - agent.deaths * 150 - agent.penalties * 1000
        scores.append((score, agent))
    return scores

def crossover(population, size):

    # Split the 12 best from last generation into 2 lists so we don't crossover from the same parent.
    mother = population[0:5]
    father = population[6:11]
    newGeneration = []

    # Will crossover from the best 12 agents in the previous generation to create the next generation.
    while len(newGeneration) < size:
        child = Agent(0, 0, 0, [])
        for j in range(amountOfChromosomes - 1):

            coin = random.getrandbits(1)
            parent = random.randint(0, len(mother) - 1)

            if coin == 0:
                child.insert(mother[parent].chromosome[j], j)
            else:
                child.insert(father[parent].chromosome[j], j)

        newGeneration.append(child)

    return newGeneration

def mutation(population, size):

    prob = random.randint(0, 100)

    # Mutate the next generation at random to promote diversity and try avoid the local minima.
    if prob % 48 == 0:
        for j in range(random.randint(0, int(size / 2 - 1)), random.randint(int(size / 2), size - 1)):
            for i in range(len(population[j].chromosome)):
                population[j].chromosome[i] = population[j].chromosome[i] + random.uniform(-1, 1)
        print("mutated")
    
    return population

def runAgent(agent):

    # Initlizing variables needed for each individual agent.
    steps = 0
    firstFruit = 0
    first = True
    lastMove = "left"
    penalty = True

    fruit = Fruit(0, 0)
    aiSnake = Snake(random.randrange(20, 860, 20), random.randrange(20, 700, 20), [])
    fruit.generateFruit()

    # Creates a new snake in a random position with a new fruit aswell to promote dynamic behaviour.
    def respawn():
        newSnake = Snake(random.randrange(20, 860, 20), random.randrange(20, 700, 20), [])
        fruit = Fruit(0, 0)
        fruit.generateFruit()
        return newSnake

    # Train the agent for n number of steps.
    while True:
        
        # If the snake dies it then gets reset
        if aiSnake.x < 20 or aiSnake.x > 860:
            aiSnake = respawn()
            penalty = True
        elif aiSnake.y < 20 or aiSnake.y > 700:
            aiSnake = respawn()
            penalty = True

        # Runs the neural network to decide which direction to move.
        move = makeMove(agent, aiSnake, lastMove, fruit, False)

        # The highest value is the move the neural network thinks is the best.
        if move[0] == max(move):
            if lastMove != "right":
                lastMove = "left"
        elif move[1] == max(move):
            if lastMove != "left":
                lastMove = "right"
        elif move[2] == max(move):
            if lastMove != "down":
                lastMove = "up"
        elif move[3] == max(move):
            if lastMove != "up":
                lastMove = "down"

        # Run's the code for the snake game.
        evaluation = SnakeGame(aiSnake, lastMove, fruit)

        # To counter-act spinning by killing the snake if it spins and spawning in a new one.
        if steps % 200 == 0 and steps != 0 and penalty == True:
            if penalty == True:
                agent.penalties += 1
            agent.deaths += 1
            aiSnake = respawn()
            penalty = True

        # If the snake gets a fruit then we start counting steps.
        if evaluation[1]:
            if first:
                firstFruit = steps
                first = False
            fruit = Fruit(0, 0)
            fruit.generateFruit()
            agent.avg_steps.append(steps - firstFruit)
            firstFruit = steps
            penalty = False

        # Keeps track of deaths.
        if evaluation[2] == False:
            if evaluation[0] > agent.hScore:
                agent.hScore = evaluation[0]
            agent.deaths += 1
            first = True


        # Return the agent after training.
        if steps == 1000:
            return agent
            
        steps += 1

def trainGen(numGens):

    generation = 0
    group = 5
    size = group * 10

    # Creating a population of agents.
    population = []
    for i in range(50):
        population.append(Agent(0, 0, 0, []))
        population[i].createPopulation()

    # Train the n number of agents for x number of generations.
    while True:

        # Record how long each generation takes for debugging and efficiency purposes.
        start = time.time()

        # Priting out the current generation.
        print(f"Generation: {generation}")

        newGeneration = []
        
        # Running the game for every agent in the generation. Run's the agents in size of group with 10 processes.
        sublists = [population[i:i+group] for i in range(0, len(population), group)]
        newPop = []
        with Pool(10) as pool:
            for sublist in sublists:
                result = pool.map_async(runAgent, sublist)
                for result in result.get():
                    newPop.append(result)
        population = newPop

        # Finding the fitness for the generation and sorting by score to find best agents.
        currentFitness = fitness(population)
        currentFitness = sorted(currentFitness, key=lambda x: x[0], reverse=True)

        if generation % 33 == 0 and generation > 0 and len(population) > 21:
            group -= 1
            size = group * 10

        cFitness = []
        for x in currentFitness:
            cFitness.append(x[0])

        # If the generation isn't past 100,000 fitness by generation 74. Then it's an unlucky population and we should start again.
        # if generation % 49 == 0 and int(sum(cFitness) / 2) < 100000 and generation != 0:
        #     for agent in population:
        #         agent.createPopulation()
        #     numGens += 50
        #     group = 5
        #     size = group * 10

        #     print("\n\n\n\n")
        #     print("Bad population, Restarting")
        #     print("\n\n\n\n")



        # # Printing the generation's score and current maximum fitness score.
        print()
        print(cFitness)
        print()
        print("Current Max: {}".format(currentFitness[0][0]))
        print()
        print(f"Size of population: {len(population)}")
        print()

        # # --------------------------------- DEBUGGING ---------------------------------

        # # if generation > 90:
        # #     for i in range(3):
        # #         print("Score: {}".format(currentFitness[i][1].hScore))
        # #         print("Deaths: {}".format(currentFitness[i][1].deaths))
        # #         print("Penaltys: {}".format(currentFitness[i][1].penalties))
        # #         print("Average steps: {}".format(currentFitness[i][1].avg_steps))
        # #         print()
        # #         displayGame(Snake(random.randrange(20, 860, 20), random.randrange(20, 700, 20), []), "left", population[i], Fruit(0, 0))
        # #     pygame.quit()
        # #     input("Are you ready for the next run? ")

        # # --------------------------------- DEBUGGING ---------------------------------

        # # Adding the best 12 agents to the next generation for crossover and mutation.
        for i in range(12):
            newGeneration.append(currentFitness[i][1])

        population = crossover(newGeneration, size)
        population = mutation(population, size)

        generation += 1
        end = time.time()
    
        # # How many generations it's going to train for.
        if generation == numGens + 1:
            return currentFitness

        print("Time for generation: {}".format(end - start))
        print("-----------------------------------------------------")

def displayGame(snake, lastMove, agent, fruit):

    # Creating the screen.
    global res
    global screen
    background_colour = pygame.Color("#8fcb9e")
    res = (900, 800)
    screen = pygame.display.set_mode(res)
    pygame.display.set_caption('Snake Game')
    screen.fill(background_colour)
    pygame.display.flip()
    pygame.init()

    smallfont = pygame.font.SysFont('Corbel',35)
    clock = pygame.time.Clock()

    # Drawing the grid.
    for x in range(blockSize, res[0] - 20, blockSize):
        for y in range(blockSize, res[1] - 80, blockSize):
            pygame.draw.rect(screen, pygame.Color(GRASS), pygame.Rect(x, y, blockSize, blockSize))
            pygame.draw.rect(screen, BLACK, pygame.Rect(x, y, blockSize, blockSize), 1)

    # Drawing the snake's head.
    pygame.draw.rect(screen, BLACK, snake.draw())

    # Generating and drawing the fruit.
    fruit.generateFruit()
    fruit.drawFruit()

    # Head of snake.
    snake.body.append(pygame.Rect(snake.x, snake.y, blockSize, blockSize))

    # Tail of snake.
    snake.body.append(pygame.Rect(snake.x, snake.y, blockSize, blockSize))
    
    score = 0

    while True:

        # This is so the user can close the window anytime when displaying.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # --------------------------------- DEBUGGING ---------------------------------
        # if clock.tick(6):

        #     newEvent = pygame.event.wait()
        #     if newEvent.type == pygame.KEYDOWN:
                        
        #         MoveSnake(lastMove, snake, True)
        #         move = makeMove(agent, snake, lastMove, fruit, True)

        #         print("Snake x: {}\tSnake y: {}\tFruit x: {}\tFruit y: {}".format(snake.x, snake.y, fruit.x, fruit.y))
        #         print()
        #         print("Wall: {}".format(move[1][0]))
        #         print("Current Direction: {}".format(move[1][1]))
        #         print("Relative X and Y: {}".format(move[1][2]))

        #         if move[0][0] == max(move[0]):
        #             if lastMove != "right":
        #                 lastMove = "left"
        #         if move[0][1] == max(move[0]):
        #             if lastMove != "left":
        #                 lastMove = "right"
        #         if move[0][2] == max(move[0]):
        #             if lastMove != "down":
        #                 lastMove = "up"
        #         if move[0][3] == max(move[0]):
        #             if lastMove != "up":
        #                 lastMove = "down"

        #         pygame.display.update()

        # --------------------------------- DEBUGGING ---------------------------------


        # Score variable.
        scoreTitle = smallfont.render('score:' , True , BLACK)
        scoreValue = smallfont.render(str(score), True, BLACK)
        screen.blit(scoreTitle, (center[0] - 75, center[1] + 330))
        screen.blit(scoreValue, (center[0] + 15, center[1] + 330))

        # This moves the snake at a certain time interval.
        if clock.tick(6):

            # Uses the trained agent to play the game with it's neural network. (Set to true for debugging).
            move = makeMove(agent, snake, lastMove, fruit, False)

            if move[0] == max(move):
                if lastMove != "right":
                    lastMove = "left"
            if move[1] == max(move):
                if lastMove != "left":
                    lastMove = "right"
            if move[2] == max(move):
                if lastMove != "down":
                    lastMove = "up"
            if move[3] == max(move):
                if lastMove != "up":
                    lastMove = "down"

            MoveSnake(lastMove, snake, True)
            pygame.display.update()

        # When the agent gets a fruit it will replace it with another randomly generated fruit.
        # Then it will add one to the score and display it.
        if snake.x == fruit.x and snake.y == fruit.y:

            # Adds a part to the body.
            Grow(snake, lastMove)

            # Generate a new fruit.
            fruit.generateFruit()
            fruit.drawFruit()

            # Increase score by one.
            score += 1

            # Erase the old score and put in the new score.
            scoreValue = smallfont.render(str(score), True, BLACK)
            screen.fill(background_colour, (center[0] + 15, center[1] + 330, 100, 100))
            screen.blit(scoreValue, (center[0] + 15, center[1] + 330))
        
        pygame.display.update()

        # If the snake hit's itself.
        if len(snake.body) > 2:
            for parts in snake.body[1:]:
                if snake.x == parts.x and snake.y == parts.y:
                    return

        # If the snake hits a wall on the horizontal axis.
        if snake.x < 20 or snake.x > 860:
            return

        # If the snake hits a wall on the vertical axis.
        elif snake.y < 20 or snake.y > 700:
            return


blockSize = 20
res = (900, 800)

if __name__ == '__main__':
    # Initilizing variables.
    width = res[0]
    height = res[1]
    center = (int(width / 2), int(height / 2))
    lastMove = "left"

    BLACK = [0, 0, 0]
    RED = [255, 0, 0]
    GRASS = ("#7EC984")
    color = (255,255,255) 
    color_light = (170,170,170) 
    color_dark = (100,100,100)

    amountOfChromosomes = 16321 

    # Run the training.
    start = time.time()
    results = trainGen(50)
    end = time.time()
    print()
    print("Elapsed time: " + time.strftime("%H:%M:%S.{}".format(str(end - start % 1)[2:])[:15], time.gmtime(end - start)))

    # This is for when the training is completed it will wait for user input to display results.
    x = input("are you ready to see the results?")

    # Display the 20 best agents.
    # for i in range(20):
    #     print("Fitness: {}".format(results[i][0]))
    #     displayGame(Snake(random.randrange(20, 860, 20), random.randrange(20, 700, 20), []), "left", results[i][1], Fruit(0, 0))




