#!/usr/bin/python
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random
import numpy as np
import time as timer
from multiprocessing import Pool, Process, Pipe, Queue
from multiprocessing.managers import BaseManager
import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab
from matplotlib import style

# Snake class
class Snake:

    def __init__(self, x, y, body):
        self.x = x
        self.y = y
        self.body = body

    def pos(self):
        return self.x, self.y

    def draw(self):
        return pygame.Rect(self.x, self.y, blockSize, blockSize)

class Fruit:

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def pos(self):
        return self.x, self.y

    # Range is so it fits in the grid of the game.
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


    # nothing
    pass

def MainMenu():

    # Creating the screen.
    background_colour = pygame.Color("#8fcb9e")
    screen = pygame.display.set_mode(res)
    pygame.display.set_caption('Snake Game')
    screen.fill(background_colour)
    pygame.display.flip()

    quit = smallfont.render('quit' , True , color)
    start = bigfont.render('start' , True , color)
    withAI = smallerfont.render('(with AI agent)', True, color)
    withoutAI = smallerfont.render('(normal snake)', True, color)

    while True:

        # Close screen if user clicks quit or the red arrow in the top right corner.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and quitButton:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and startButton:
                return PlayerSnakeGame(0)
            if event.type == pygame.MOUSEBUTTONDOWN and startAIbutton:
                pygame.display.quit()
                return AIMenu()

        # To find where the mouse is at all times.
        mouse = pygame.mouse.get_pos()

        # Coordinates of the quitButton for hit registering.
        quitButton = width / 2 - 102 <= mouse[0] <= width / 2 + 78 and height / 2 + 42 <= mouse[1] <= height / 2 + 102
        startAIbutton = width / 2 - 290 <= mouse[0] <= width / 2 - 30 and height / 2 - 100 <= mouse[1] <= height / 2 + 20
        startButton = width / 2 <= mouse[0] <= width / 2 + 260 and height / 2 - 100 <= mouse[1] <= height / 2 + 20

        # Draws the start buttons as lit up if mouse is hovering, otherwise draws them normally.
        if startAIbutton:
            pygame.draw.rect(screen,color_light,pygame.Rect(width/2 - 290,height/2 - 100, 260, 120)) 
        else: 
            pygame.draw.rect(screen,color_dark,pygame.Rect(width/2 - 290,height/2 - 100, 260, 120))
        
        if startButton:
            pygame.draw.rect(screen,color_light,pygame.Rect(width/2,height/2 - 100, 260, 120))
        else:
            pygame.draw.rect(screen,color_dark,pygame.Rect(width/2,height/2 - 100, 260, 120))

        # Draws quit button as lit up if mouse is hovering, otherwise draws it normally.
        if quitButton:
            pygame.draw.rect(screen,color_light,pygame.Rect(width/2 - 102,height/2 + 45, 180, 60)) 
        else: 
            pygame.draw.rect(screen,color_dark,pygame.Rect(width/2 - 102,height/2 + 45, 180, 60)) 



        # Draws the "quit" button.
        screen.blit(quit, (center[0] - 40, center[1] + 56)) 

        # Draws the start with AI button.
        screen.blit(start, (center[0] - 227, center[1] - 85))
        screen.blit(withAI, (center[0] - 220, center[1] - 15))

        # Draws the normal start button.
        screen.blit(start, (center[0] + 65, center[1] - 85))
        screen.blit(withoutAI, (center[0] + 65, center[1] - 15))
        
        # Puts the "snake" logo onto the screen.
        logo = pygame.image.load('images/logo.png')
        screen.blit(logo, (center[0] - 230, center[1] - 350))


        # updates the frames of the game 
        pygame.display.update() 

def DrawGrid(screen):

    # Drawing the grid.
    for x in range(blockSize, res[0] - 20, blockSize):
        for y in range(blockSize, res[1] - 80, blockSize):
            pygame.draw.rect(screen, pygame.Color(GRASS), pygame.Rect(x, y, blockSize, blockSize))
            pygame.draw.rect(screen, BLACK, pygame.Rect(x, y, blockSize, blockSize), 1)

def Grow(snake, direction):

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

def MoveSnake(direction, snake, fruit, draw):

    if draw:
        fruit.drawFruit()

    # Moves the head of the snake.
    if direction == "left":
        snake.x -= blockSize
    elif direction == "right":
        snake.x += blockSize
    elif direction == "up":
        snake.y -= blockSize
    elif direction == "down":
        snake.y += blockSize

    if draw:
        pygame.draw.rect(screen, BLACK, snake.draw())

    # Code for the body.
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

            if draw:
                pygame.draw.rect(screen, BLACK, snake.body[j])
                pygame.draw.rect(screen, pygame.Color(GRASS), snake.body[-1])
                pygame.draw.rect(screen, BLACK, snake.body[-1], 1)

    # Update the head in the body list.
    snake.body[0].x = snake.x
    snake.body[0].y = snake.y

def PlayerSnakeGame(display):

    # Creating the screen.
    background_colour = pygame.Color("#8fcb9e")
    res = (900, 800)
    screen = pygame.display.set_mode(res)
    pygame.display.set_caption('Snake Game')
    screen.fill(background_colour)
    pygame.display.flip()

    # Drawing the grid.
    DrawGrid(screen)

    snake = Snake(random.randrange(40, 840, 20), random.randrange(40, 680, 20), [])
    fruit = Fruit(0, 0)
    pygame.draw.rect(screen, BLACK, snake.draw())
    fruit.generateFruit()
    fruit.drawFruit()

    # Head of snake.
    snake.body.append(pygame.Rect(snake.x, snake.y, blockSize, blockSize))

    # Tail of snake.
    snake.body.append(pygame.Rect(snake.x, snake.y, blockSize, blockSize))
    
    score = 0
    lastMove = "left"
    switch = True

    while True:

        if display == 2:

            if switch == True:
                title = smallerfont.render('Player.', True, (128,128,128))
                switch = False
            else:
                title = smallerfont.render('Player.', True, (16,16,16))
                switch = True
            
            screen.blit(title, (center[0] - 50, center[1] + 370))

        # Score variable.
        scoreTitle = smallfont.render('score:' , True , BLACK)
        scoreValue = smallfont.render(str(score), True, BLACK)
        screen.blit(scoreTitle, (center[0] - 75, center[1] + 330))
        screen.blit(scoreValue, (center[0] + 15, center[1] + 330))

        # If the user presses a key that is allowed it will remember the key for when the clock ticks and the snake is moved.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
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

        # This moves the snake at a certain time interval.
        if clock.tick(6):
            MoveSnake(lastMove, snake, fruit, True)
            pygame.display.update()

        # If the snake hit's itself.
        if len(snake.body) > 2:
            for parts in snake.body[1:]:
                if snake.x == parts.x and snake.y == parts.y:
                    if display != 2:
                        GameOver()
                    else:
                        return score

        if snake.x < 20 or snake.x > 860:
            if display != 2:
                GameOver()
            else:
                return score

        if snake.y < 20 or snake.y > 700:
            if display != 2:
                GameOver()
            else:
                return score

        # When you get a fruit it will replace it with another randomly generated fruit.
        # Then it will add one to the score and display it.
        if snake.x == fruit.pos()[0] and snake.y == fruit.pos()[1]:

            # Adds a part to the body.
            Grow(snake, lastMove)

            # Generate a new fruit.
            fruit.generateFruit()

            # Increase score by one.
            score += 1

            # Erase the old score and put in the new score.
            scoreValue = smallfont.render(str(score), True, BLACK)
            screen.fill(background_colour, (center[0] + 15, center[1] + 330, 100, 100))
            screen.blit(scoreValue, (center[0] + 15, center[1] + 330))
        
        pygame.display.update()

def GameOver():

    s = pygame.Surface(res)
    s.fill(BLACK)
    s.set_alpha(200)
    screen.blit(s, (0,0))
    pygame.display.flip()

    quit = smallfont.render('quit' , True , color)
    start = bigfont.render('play again' , True , color)

    while True:

        # Close screen if user clicks quit or the red arrow in the top right corner.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and quitButton:
                return MainMenu()
            if event.type == pygame.MOUSEBUTTONDOWN and startButton:
                PlayerSnakeGame(0)

        # To find where the mouse is at all times.
        mouse = pygame.mouse.get_pos()

        # Coordinates of the quitButton for hit registering and drawing the quit button.
        quitButton = width / 2 - 102 <= mouse[0] <= width / 2 + 78 and height / 2 + 42 <= mouse[1] <= height / 2 + 102

        # Coordinates of the start button for hit registering and drawing the quit button.
        startButton = width / 2 - 190 <= mouse[0] <= width / 2 + 170 and height / 2 - 100 <= mouse[1] <= height / 2 + 20

        # Draws quit button as lit up if mouse is hovering, otherwise draws it normally.
        if quitButton:
            pygame.draw.rect(screen,color_light,pygame.Rect(width/2 - 102,height/2 + 45, 180, 60)) 
        else: 
            pygame.draw.rect(screen,color_dark,pygame.Rect(width/2 - 102,height/2 + 45, 180, 60)) 

        # Draws the start button as lit up if mouse is hovering, otherwise draws it normally.
        if startButton:
            pygame.draw.rect(screen,color_light,pygame.Rect(width/2 - 190,height/2 - 100, 360, 120)) 
        else: 
            pygame.draw.rect(screen,color_dark,pygame.Rect(width/2 - 190,height/2 - 100, 360, 120)) 


        # Draws the "quit" and "start" text.
        screen.blit(quit, (center[0] - 40, center[1] + 56))
        screen.blit(start, (center[0] - 150, center[1] - 75))
        
        # Puts the "snake" logo onto the screen.
        logo = pygame.image.load('images/game-over.png')
        screen.blit(logo, (center[0] - 230, center[1] - 350))

        # updates the frames of the game 
        pygame.display.update() 

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
    MoveSnake(lastMove, agent, fruit, False)

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

def displayGame(lastMove, agent, fruit, display):

    # Creating the screen.
    global res
    global screen
    background_colour = pygame.Color("#8fcb9e")
    snake = Snake(random.randrange(40, 840, 20), random.randrange(40, 680, 20), [])
    res = (900, 800)
    screen = pygame.display.set_mode(res)
    pygame.display.set_caption('Snake Game')
    screen.fill(background_colour)
    pygame.display.flip()

    smallerfont = pygame.font.SysFont('Corbel', 20)
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
    switch = True

    while True:

        mouse = pygame.mouse.get_pos()

        if display == 0:

            back = smallerfont.render('back' , True , color)
            backButton = width / 2 + 260 <= mouse[0] <= width / 2 + 380 and height / 2 + 330 <= mouse[1] <= height / 2 + 360

            if backButton:
                pygame.draw.rect(screen,color_light,pygame.Rect(width/2 + 260,height/2 + 335, 120, 30))
            else: 
                pygame.draw.rect(screen,color_dark,pygame.Rect(width/2 + 260,height/2 + 335, 120, 30))
            
            screen.blit(back, (center[0] + 300, center[1] + 340))
        
        elif display == 1:

            if switch == True:
                title = smallerfont.render('AI agent.', True, (128,128,128))
                switch = False
            else:
                title = smallerfont.render('AI agent.', True, (16,16,16))
                switch = True
            
            screen.blit(title, (center[0] - 50, center[1] + 370))

        # This is so the user can close the window anytime when displaying.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and backButton:
                return

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

            MoveSnake(lastMove, snake, fruit, True)
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
                    return score

        # If the snake hits a wall on the horizontal axis.
        if snake.x < 20 or snake.x > 860:
            return score

        # If the snake hits a wall on the vertical axis.
        elif snake.y < 20 or snake.y > 700:
            return score

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
    
    return population

def runAgent(agent):

    # Initlizing variables needed for each individual agent.
    steps = 0
    firstFruit = 0
    first = True
    lastMove = "left"
    penalty = True

    fruit = Fruit(0, 0)
    aiSnake = Snake(random.randrange(40, 840, 20), random.randrange(40, 680, 20), [])
    fruit.generateFruit()

    # Creates a new snake in a random position with a new fruit aswell to promote dynamic behaviour.
    def respawn():
        newSnake = Snake(random.randrange(40, 840, 20), random.randrange(40, 680, 20), [])
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

def trainGen(numGens, connection):

    generation = 0
    group = 4
    size = group * 10
    global finalGeneration

    # Creating a population of agents.
    population = []
    for i in range(40):
        population.append(Agent(0, 0, 0, []))
        population[i].createPopulation()

    # Train the n number of agents for x number of generations.
    while True:

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

        cFitness = []
        for x in currentFitness:
            cFitness.append(x[0])

        connection.send(cFitness)
        currentFitness = sorted(currentFitness, key=lambda x: x[0], reverse=True)

        # # Adding the best 12 agents to the next generation for crossover and mutation.
        for i in range(12):
            newGeneration.append(currentFitness[i][1])

        population = crossover(newGeneration, size)
        population = mutation(population, size)
    
        # # How many generations it's going to train for.
        if generation == numGens:
            connection.send(currentFitness)
            return 
    
        generation += 1

def gamemodeScore(agent):

    # Screen resolution.
    screen = pygame.display.set_mode(res)
    background_colour = pygame.Color("#8fcb9e")
    pygame.display.set_caption('Snake Game')
    screen.fill(background_colour)

    # Colours used.
    BLACK = [0, 0, 0]
    RED = [255, 0, 0]
    GRASS = ("#7EC984")
    color = (255,255,255) 
    color_light = (170,170,170) 
    color_dark = (100,100,100) 

    # Fonts used.
    smallfont = pygame.font.SysFont('Corbel',35)
    bigfont = pygame.font.SysFont('Corbel',70)

    # Screen width, height and center
    width = res[0]
    height = res[1]
    center = (int(width / 2), int(height / 2))

    menu = True

    while menu == True:

        # Close screen if user clicks quit or the red arrow in the top right corner.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and backButton:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and readyButton:
                menu = False

        mouse = pygame.mouse.get_pos()

        back = smallfont.render('back' , True , color)
        ready = bigfont.render('ready' , True , color)
        title = bigfont.render('Press ready to see the', True, color_dark)
        title2 = bigfont.render(' Agent play.', True, color_dark)

        backButton = width / 2 - 102 <= mouse[0] <= width / 2 + 78 and height / 2 + 42 <= mouse[1] <= height / 2 + 102
        readyButton = width / 2 <= mouse[0] <= width / 2 + 260 and height / 2 - 100 <= mouse[1] <= height / 2 + 20

        if readyButton:
            pygame.draw.rect(screen,color_light,pygame.Rect(width/2 - 140,height/2 - 100, 260, 120))
        else:
            pygame.draw.rect(screen,color_dark,pygame.Rect(width/2 - 140,height/2 - 100, 260, 120))

        # Draws quit button as lit up if mouse is hovering, otherwise draws it normally.
        if backButton:
            pygame.draw.rect(screen,color_light,pygame.Rect(width/2 - 102,height/2 + 45, 180, 60))
        else: 
            pygame.draw.rect(screen,color_dark,pygame.Rect(width/2 - 102,height/2 + 45, 180, 60)) 

        screen.blit(ready, (center[0] - 85, center[1] - 75))
        screen.blit(back, (center[0] - 45, center[1] + 60))
        screen.blit(title, (center[0] - 330, center[1] - 280))
        screen.blit(title2, (center[0] - 180, center[1] - 205))

        pygame.display.flip()
    
    # Run the AI.
    AIscore = displayGame("left", agent, Fruit(0, 0), 1)
    menu = True

    s = pygame.Surface(res)
    s.fill(BLACK)
    s.set_alpha(200)
    screen.blit(s, (0,0))
    pygame.display.flip()

    while menu == True:
        # Close screen if user clicks quit or the red arrow in the top right corner.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and backButton:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and readyButton:
                menu = False

        mouse = pygame.mouse.get_pos()

        back = smallfont.render('back' , True , color)
        ready = bigfont.render('ready' , True , color)
        title = bigfont.render('Press ready to play', True, color_dark)

        backButton = width / 2 - 102 <= mouse[0] <= width / 2 + 78 and height / 2 + 42 <= mouse[1] <= height / 2 + 102
        readyButton = width / 2 <= mouse[0] <= width / 2 + 260 and height / 2 - 100 <= mouse[1] <= height / 2 + 20

        if readyButton:
            pygame.draw.rect(screen,color_light,pygame.Rect(width/2 - 140,height/2 - 100, 260, 120))
        else:
            pygame.draw.rect(screen,color_dark,pygame.Rect(width/2 - 140,height/2 - 100, 260, 120))

        # Draws quit button as lit up if mouse is hovering, otherwise draws it normally.
        if backButton:
            pygame.draw.rect(screen,color_light,pygame.Rect(width/2 - 102,height/2 + 45, 180, 60))
        else: 
            pygame.draw.rect(screen,color_dark,pygame.Rect(width/2 - 102,height/2 + 45, 180, 60)) 

        screen.blit(ready, (center[0] - 85, center[1] - 75))
        screen.blit(back, (center[0] - 45, center[1] + 60)) 
        screen.blit(title, (center[0] - 270, center[1] - 210))

        pygame.display.update()

    playerScore = PlayerSnakeGame(2)

def AIMenu():
    
    # Fonts used.
    screen = pygame.display.set_mode((res[0] + 350, res[1] + 100))
    bigfont = pygame.font.SysFont('Corbel',70)
    smallfont = pygame.font.SysFont('Corbel',35)
    smallerfont = pygame.font.SysFont('Corbel', 20)
    color = (255,255,255) 
    color_light = (128,128,128) 
    color_dark = (100,100,100)

    # Screen width, height and center
    width = res[0]
    height = res[1]
    center = (int(width / 2), int(height / 2)) 

    trainingText = ["Training.", "Training..", "Training..."]
    counter = 0

    # Creating the screen.
    background_colour = pygame.Color("#8fcb9e")
    pygame.display.set_caption('Snake Game')
    screen.fill(background_colour)
    
    trainText = bigfont.render(trainingText[0], True, color_dark)
    screen.fill(background_colour)
    screen.blit(trainText, (center[0] + 50, center[1] - 350))

    flick = False
    pygame.display.flip()

    highest = []
    generation = 0
    numGens = 0

    conn1, conn2  = Pipe(duplex = False)
    p1 = Process(target = trainGen, args=(numGens, conn2,))
    p1.start()

    # Training loop
    while True:

        # Close screen if user clicks quit or the red arrow in the top right corner.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if generation == numGens + 1:
            break

        if generation <= numGens:
            fitness = conn1.recv()
            highest.append(max(fitness))

            with matplotlib.pyplot.style.context('ggplot'):
                fig = pylab.figure(figsize = [6,5])
                fig2 = pylab.figure(figsize = [6,5])
                ax = fig.gca()
                ax2 = fig2.gca()
                ax.plot(fitness[::-1])
                ax.set_title("Fitness scores of the current generation.")
                ax.set_xlabel("Agent number.")
                ax.set_ylabel("Score.")
                ax.yaxis.set_label_position("right")
                ax2.plot(highest)
                ax2.set_title("Max score of each generation.")
                ax2.set_xlabel("Amount of generations.")
                ax2.set_ylabel("Score.")
                ax2.yaxis.set_label_position("right")
                ax2.set_xlim(1)

            canvas = agg.FigureCanvasAgg(fig)
            canvas2 = agg.FigureCanvasAgg(fig2)
            canvas.draw()
            canvas2.draw()
            renderer = canvas.get_renderer()
            renderer2 = canvas2.get_renderer()
            raw_data = renderer.tostring_rgb()
            raw_data2 = renderer2.tostring_rgb()
        
            if counter == 3:
                counter = 0

            if flick:
                screen.fill(background_colour)
                trainText = bigfont.render(trainingText[counter], True, color_light)
                screen.blit(trainText, (center[0] + 50, center[1] - 350))
                flick = False

            else:
                screen.fill(background_colour)
                trainText = bigfont.render(trainingText[counter], True, color_dark)
                screen.blit(trainText, (center[0] + 50, center[1] - 350))
                flick = True

            generationText = smallfont.render(f"Current generation: {generation}", True, color_dark)
            screen.blit(generationText, (center[0] + 20, center[1] + 285))

            size = canvas.get_width_height()
            allGens = pygame.image.fromstring(raw_data2, size, "RGB")
            screen.blit(allGens, (center[0] + 185, center[1] - 240))
            currentGen = pygame.image.fromstring(raw_data, size, "RGB")
            screen.blit(currentGen, (center[0] - 435, center[1] - 240))
            pygame.display.flip()

            matplotlib.pyplot.close('all')

            counter += 1
            generation += 1

    finalGeneration = conn1.recv()
    conn1.close()
    conn2.close()
    p1.join()

    # Finished Training loop.
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and menuButton:
                return MainMenu()
            if event.type == pygame.MOUSEBUTTONDOWN and retrainAgentButton:
                return AIMenu()
            if event.type == pygame.MOUSEBUTTONDOWN and viewAgentButton:
                displayGame(lastMove, finalGeneration[0][1], Fruit(0,0), 0)
                screen = pygame.display.set_mode((res[0] + 350, res[1] + 100))
            if event.type == pygame.MOUSEBUTTONDOWN and scoreButton:
                gamemodeScore(finalGeneration[0][1])
                screen = pygame.display.set_mode((res[0] + 350, res[1] + 100))
            if event.type == pygame.MOUSEBUTTONDOWN and deathmatchButton:
                return
        
        screen.fill(background_colour)
        trainText = bigfont.render("Training complete.", True, color_dark)
        screen.blit(trainText, (center[0] - 60, center[1] - 350))

        size = canvas.get_width_height()
        allGens = pygame.image.fromstring(raw_data2, size, "RGB")
        screen.blit(allGens, (center[0] + 185, center[1] - 250))
        currentGen = pygame.image.fromstring(raw_data, size, "RGB")
        screen.blit(currentGen, (center[0] - 435, center[1] - 250))

        gamemode = smallfont.render("Please select a gamemode.", True, color_dark)
        screen.blit(gamemode, (center[0] + 305, center[1] + 270))

        option = smallfont.render("Please select an option.", True, color_dark)
        screen.blit(option, (center[0] - 300, center[1] + 270))
        
        mouse = pygame.mouse.get_pos()

        menu = smallerfont.render('menu' , True , color)
        deathmatch = smallfont.render('deathmatch' , True , color)
        score = smallfont.render('high score', True, color)
        viewAgent = smallfont.render('view agent', True, color)
        retrain = smallfont.render('retrain', True, color)

        deathmatchButton = width / 2 + 240 <= mouse[0] <= width / 2 + 470 and height / 2 + 320 <= mouse[1] <= height / 2 + 410
        scoreButton = width / 2 + 500 <= mouse[0] <= width / 2 + 730 and height / 2 + 320 <= mouse[1] <= height / 2 + 410
        viewAgentButton = width / 2 - 130 <= mouse[0] <= width / 2 + 100 and height / 2 + 320 <= mouse[1] <= height / 2 + 410
        retrainAgentButton = width / 2 - 390 <= mouse[0] <= width / 2 - 160 and height / 2 + 320 <= mouse[1] <= height / 2 + 410
        menuButton = width / 2 + 90 <= mouse[0] <= width / 2 + 250 and height / 2 + 430 <= mouse[1] <= height / 2 + 470

        if deathmatchButton:
            pygame.draw.rect(screen,color_light,pygame.Rect(width/2 + 240,height/2 + 320, 230, 90)) 
        else: 
            pygame.draw.rect(screen,color_dark,pygame.Rect(width/2 + 240,height/2 + 320, 230, 90))
        
        if scoreButton:
            pygame.draw.rect(screen,color_light,pygame.Rect(width/2 + 500,height/2 + 320, 230, 90))
        else:
            pygame.draw.rect(screen,color_dark,pygame.Rect(width/2 + 500,height/2 + 320, 230, 90))
        
        if viewAgentButton:
            pygame.draw.rect(screen,color_light,pygame.Rect(width/2 - 130,height/2 + 320, 230, 90)) 
        else:
            pygame.draw.rect(screen,color_dark,pygame.Rect(width/2 - 130,height/2 + 320, 230, 90))
        
        if retrainAgentButton:
            pygame.draw.rect(screen,color_light,pygame.Rect(width/2 - 390,height/2 + 320, 230, 90)) 
        else:
            pygame.draw.rect(screen,color_dark,pygame.Rect(width/2 - 390,height/2 + 320, 230, 90))

        # Draws quit button as lit up if mouse is hovering, otherwise draws it normally.
        if menuButton:
            pygame.draw.rect(screen,color_light,pygame.Rect(width/2 + 90,height/2 + 430, 160, 40))
        else: 
            pygame.draw.rect(screen,color_dark,pygame.Rect(width/2 + 90,height/2 + 430, 160, 40)) 
        
        screen.blit(menu, (center[0] + 150, center[1] + 440))
        screen.blit(deathmatch, (center[0] + 265, center[1] + 350))
        screen.blit(score, (center[0] + 545, center[1] + 350))
        screen.blit(viewAgent, (center[0] - 90, center[1] + 350))
        screen.blit(retrain, (center[0] - 325, center[1] + 350))
        
        pygame.display.flip()
        matplotlib.pyplot.close(fig)
        matplotlib.pyplot.close(fig2)


# Grid size.
blockSize = 20
res = (900, 800)    
amountOfChromosomes = 16321


if __name__ == '__main__':

    # Initilizing
    pygame.init()

    # Screen resolution.
    screen = pygame.display.set_mode(res)

    # Colours used.
    BLACK = [0, 0, 0]
    RED = [255, 0, 0]
    GRASS = ("#7EC984")
    color = (255,255,255) 
    color_light = (170,170,170) 
    color_dark = (100,100,100) 

    # Fonts used.
    smallerfont = pygame.font.SysFont('Corbel', 20)
    smallfont = pygame.font.SysFont('Corbel',35)
    bigfont = pygame.font.SysFont('Corbel',70)

    # Screen width, height and center
    width = res[0]
    height = res[1]
    center = (int(width / 2), int(height / 2))

    # Keep track of what direction and when the snake should move.
    clock = pygame.time.Clock()

    lastMove = "left"

    # Runs the main menu.
    MainMenu()