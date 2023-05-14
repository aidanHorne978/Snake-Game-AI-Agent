#!/usr/bin/python
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random
import numpy as np
import time as timer
from multiprocessing import Pool, Process, Pipe
from threading import Thread
import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab

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
    def drawFruit(self, screen):
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

def MainMenu():

    # Creating the screen.
    background_colour = pygame.Color("#8fcb9e")
    screen = pygame.display.set_mode(res)
    pygame.display.set_caption('Snake Game')
    screen.fill(background_colour)

    smallerfont = pygame.font.SysFont('Corbel', 20)
    smallfont = pygame.font.SysFont('Corbel',35)
    bigfont = pygame.font.SysFont('Corbel',70)

    quit = smallfont.render('quit' , True , color)
    start = bigfont.render('start' , True , color)
    withAI = smallerfont.render('(with AI agent)', True, color)
    withoutAI = smallerfont.render('(normal snake)', True, color)

    screen.blit(pygame.image.load('images/logo.png').convert_alpha(), (center[0] - 230, center[1] - 350))

    pygame.display.update()

    while 1:

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

def MoveSnake(screen, direction, snake, fruit, draw, color):

    if draw:
        fruit.drawFruit(screen)

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
        pygame.draw.rect(screen, color, snake.draw())

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
                pygame.draw.rect(screen, color, snake.body[j])
                pygame.draw.rect(screen, pygame.Color(GRASS), snake.body[-1])
                pygame.draw.rect(screen, BLACK, snake.body[-1], 1)

    # Update the head in the body list.
    snake.body[0].x = snake.x
    snake.body[0].y = snake.y

def PlayerSnakeGame(display):

    background_colour = pygame.Color("#8fcb9e")
    screen = pygame.display.set_mode(res)
    pygame.display.set_caption('Snake Game')
    screen.fill(background_colour)

    # Drawing the grid.
    DrawGrid(screen)

    snake = Snake(random.randrange(40, 840, 20), random.randrange(40, 680, 20), [])
    fruit = Fruit(0, 0)
    pygame.draw.rect(screen, BLACK, snake.draw())
    fruit.generateFruit()
    fruit.drawFruit(screen)

    # Head of snake.
    snake.body.append(pygame.Rect(snake.x, snake.y, blockSize, blockSize))

    # Tail of snake.
    snake.body.append(pygame.Rect(snake.x, snake.y, blockSize, blockSize))
    
    score = 0
    switch = True
    wait = True
    lastMove = ""

    s = pygame.Surface(res)
    s.fill(BLACK)
    s.set_alpha(200)
    screen.blit(s, (0,0))
    screen.blit(pygame.image.load('images/press-any-key.png').convert_alpha(), (center[0] - 325, center[1] - 200))

    pygame.display.update()

    while wait:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    lastMove = "left"
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    lastMove = "right"
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    lastMove = "up"
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    lastMove = "down"
                else:
                    lastMove = "left"

                wait = False
        
    background_colour = pygame.Color("#8fcb9e")
    screen = pygame.display.set_mode(res)
    pygame.display.set_caption('Snake Game')
    screen.fill(background_colour)
    fruit.drawFruit(screen)
    DrawGrid(screen)

    pygame.display.update()

    while 1:

        if display == 2:

            if switch == True:
                pygame.display.update(screen.blit(pygame.image.load('images/player.png').convert_alpha(), (center[0] - 50, center[1] + 370)))
                switch = False
            else:
                pygame.display.update(screen.blit(pygame.image.load('images/player2.png').convert_alpha(), (center[0] - 50, center[1] + 370)))
                switch = True

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
        if clock.tick(8):
            MoveSnake(screen, lastMove, snake, fruit, True, BLACK)

        # If the snake hit's itself.
        if len(snake.body) > 2:
            for parts in snake.body[1:]:
                if snake.x == parts.x and snake.y == parts.y:
                    if display != 2:
                        GameOverPSG(screen)
                    else:
                        return score

        if snake.x < 20 or snake.x > 860:
            if display != 2:
                GameOverPSG(screen)
            else:
                return score

        if snake.y < 20 or snake.y > 700:
            if display != 2:
                GameOverPSG(screen)
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
        
def GameOverPSG(screen):

    s = pygame.Surface(res)
    s.fill(BLACK)
    s.set_alpha(200)
    pygame.display.update(screen.blit(s, (0,0)))

    quit = smallfont.render('back' , True , color)
    start = bigfont.render('play again' , True , color)

    while 1:

        # Close screen if user clicks quit or the red arrow in the top right corner.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and backButton:
                return MainMenu()
            if event.type == pygame.MOUSEBUTTONDOWN and startButton:
                PlayerSnakeGame(0)

        # To find where the mouse is at all times.
        mouse = pygame.mouse.get_pos()

        # Coordinates of the quitButton for hit registering and drawing the quit button.
        backButton = width / 2 - 102 <= mouse[0] <= width / 2 + 78 and height / 2 + 42 <= mouse[1] <= height / 2 + 102

        # Coordinates of the start button for hit registering and drawing the quit button.
        startButton = width / 2 - 190 <= mouse[0] <= width / 2 + 170 and height / 2 - 100 <= mouse[1] <= height / 2 + 20

        # Draws quit button as lit up if mouse is hovering, otherwise draws it normally.
        if backButton:
            pygame.draw.rect(screen,color_light,pygame.Rect(width/2 - 102,height/2 + 45, 180, 60)) 
        else: 
            pygame.draw.rect(screen,color_dark,pygame.Rect(width/2 - 102,height/2 + 45, 180, 60)) 

        # Draws the start button as lit up if mouse is hovering, otherwise draws it normally.
        if startButton:
            pygame.draw.rect(screen,color_light,pygame.Rect(width/2 - 190,height/2 - 100, 360, 120)) 
        else: 
            pygame.draw.rect(screen,color_dark,pygame.Rect(width/2 - 190,height/2 - 100, 360, 120)) 

        # Draws the "quit" and "start" text.
        pygame.display.update(screen.blit(quit, (center[0] - 45, center[1] + 60)))
        pygame.display.update(screen.blit(start, (center[0] - 150, center[1] - 75)))
        
        # Puts the "snake" logo onto the screen.
        logo = pygame.image.load('images/game-over.png').convert_alpha()
        pygame.display.update(screen.blit(logo, (center[0] - 230, center[1] - 350)))

        # updates the frames of the game 
         
def SnakeGame(agent, lastMove, fruit):

    scored = False
    BLACK = [0, 0, 0]
    temp = 0
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
    MoveSnake(temp, lastMove, agent, fruit, False, BLACK)

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

    smallerfont = pygame.font.SysFont('Corbel', 20)
    smallfont = pygame.font.SysFont('Corbel',35)
    clock = pygame.time.Clock()

    DrawGrid(screen)

    # Drawing the snake's head.
    pygame.draw.rect(screen, BLACK, snake.draw())

    # Generating and drawing the fruit.
    fruit.generateFruit()
    fruit.drawFruit(screen)

    # Head of snake.
    snake.body.append(pygame.Rect(snake.x, snake.y, blockSize, blockSize))

    # Tail of snake.
    snake.body.append(pygame.Rect(snake.x, snake.y, blockSize, blockSize))
    
    score = 0
    switch = True

    pygame.display.update()

    while 1:

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
                screen.blit(pygame.image.load('images/agent.png').convert_alpha(), (center[0] - 50, center[1] + 370))
                switch = False
            else:
                screen.blit(pygame.image.load('images/agent2.png').convert_alpha(), (center[0] - 50, center[1] + 370))
                switch = True
            
        # This is so the user can close the window anytime when displaying.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if display == 0:
                if event.type == pygame.MOUSEBUTTONDOWN and backButton:
                    return
                
        # Score variable.
        scoreTitle = smallfont.render('score:' , True , BLACK)
        scoreValue = smallfont.render(str(score), True, BLACK)
        screen.blit(scoreTitle, (center[0] - 75, center[1] + 330))
        screen.blit(scoreValue, (center[0] + 15, center[1] + 330))

        # This moves the snake at a certain time interval.
        if clock.tick(8):

            # Uses the trained agent to play the game with it's neural network. (Set to true for debugging).
            move = makeMove(agent, snake, lastMove, fruit)

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

            MoveSnake(screen, lastMove, snake, fruit, True, BLACK)

        # When the agent gets a fruit it will replace it with another randomly generated fruit.
        # Then it will add one to the score and display it.
        if snake.x == fruit.x and snake.y == fruit.y:

            # Adds a part to the body.
            Grow(snake, lastMove)

            # Generate a new fruit.
            fruit.generateFruit()
            fruit.drawFruit(screen)

            # Increase score by one.
            score += 1

            # Erase the old score and put in the new score.
            scoreValue = smallfont.render(str(score), True, BLACK)
            screen.fill(background_colour, (center[0] + 15, center[1] + 330, 100, 100))
            screen.blit(scoreValue, (center[0] + 15, center[1] + 330))
        
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

        pygame.display.update()

def sigmoid(x):
    
    # Activation function.
    return 1 / (1 + np.exp(-x))

def make_prediction(input_vector, input_to_layer1, layer1_to_layer2, layer2_to_output, bias):

    # Neural network for the agent to make decisions.
    layer1 = np.dot(input_vector, input_to_layer1)
    layer2 = sigmoid(np.dot(layer1, layer1_to_layer2) + bias)
    output_layer = np.dot(layer2, layer2_to_output) + bias
    return output_layer

def makeMove(agent, snake, lastMove, fruit):

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

    # Neural network's structure is an input layer (12 -> 120) values, hidden layer (120 -> 120) values and an output layer (120 -> 4) values.
    input_to_layer1 = agent.chromosome[0:1440].reshape(12, 120)
    input_to_layer1[:, 0] = input_vector
    layer1_to_layer2 = agent.chromosome[1441:15841].reshape(120, 120)
    layer2_to_output = agent.chromosome[15841:16321].reshape(120, 4)

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

def runAgentSmall(agent):

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
    while 1:

        # If the snake dies it then gets reset
        if aiSnake.x < 20 or aiSnake.x > 860:
            aiSnake = respawn()
            penalty = True
        elif aiSnake.y < 20 or aiSnake.y > 700:
            aiSnake = respawn()
            penalty = True

        # Runs the neural network to decide which direction to move.
        move = makeMove(agent, aiSnake, lastMove, fruit)

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

def runAgentMedium(agent):

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
    while 1:

        # If the snake dies it then gets reset
        if aiSnake.x < 20 or aiSnake.x > 860:
            aiSnake = respawn()
            penalty = True
        elif aiSnake.y < 20 or aiSnake.y > 700:
            aiSnake = respawn()
            penalty = True

        # Runs the neural network to decide which direction to move.
        move = makeMove(agent, aiSnake, lastMove, fruit)

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
        if steps == 2500:
            return agent
            
        steps += 1

def runAgentLarge(agent):

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
    while 1:

        # If the snake dies it then gets reset
        if aiSnake.x < 20 or aiSnake.x > 860:
            aiSnake = respawn()
            penalty = True
        elif aiSnake.y < 20 or aiSnake.y > 700:
            aiSnake = respawn()
            penalty = True

        # Runs the neural network to decide which direction to move.
        move = makeMove(agent, aiSnake, lastMove, fruit)

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
        if steps == 5000:
            return agent
            
        steps += 1

def trainGen(connection, steps):

    # 15 groups of 2 is best atm with 15 processes.

    generation = 0
    group = 2
    size = group * 20
    counter = 0

    # Creating a population of agents.
    population = []
    for i in range(40):
        population.append(Agent(0, 0, 0, []))
        population[i].createPopulation()

    # Train the n number of agents for x number of generations.
    while 1:

        newGeneration = []
        
        # Running the game for every agent in the generation. Run's the agents in size of group with 10 processes.
        newPop = []

        with Pool() as pool:
            if steps == 1000:
                result = pool.map_async(runAgentSmall, population)
            elif steps == 2500:
                result = pool.map_async(runAgentMedium, population)
            else:
                result = pool.map_async(runAgentLarge, population)
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

        if currentFitness[0][0] > steps * 200:
            counter += 1
            if counter >= 5:
                connection.send(1)
                connection.send(currentFitness)
                return
        else:
            counter = 0

        # # Adding the best 12 agents to the next generation for crossover and mutation.
        for i in range(12):
            newGeneration.append(currentFitness[i][1])

        population = crossover(newGeneration, size)
        population = mutation(population, size)
    
        # # How many generations it's going to train for.
        if generation == 75:
            connection.send(currentFitness)
            return 
    
        generation += 1

def gamemodeGameOver(screen, mode, AIscore, playerScore, agent):
    
    middlefont = pygame.font.SysFont('Corbel', 55)

    s = pygame.Surface(res)
    s.fill(BLACK)
    s.set_alpha(200)
    pygame.display.update(screen.blit(s, (0,0)))

    while 1:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and playAgainButton:
                if mode == "score":
                    return gamemodeScore(agent)
                elif mode == "dm":
                    return gamemodeDeathmatch(agent)
            if event.type == pygame.MOUSEBUTTONDOWN and backButton:
                return 

        if AIscore > playerScore:
            screen.blit(pygame.image.load('images/agent-wins.png').convert_alpha(), (center[0] - 300, center[1] - 270))
        elif playerScore > AIscore:
            screen.blit(pygame.image.load('images/player-wins.png').convert_alpha(), (center[0] - 300, center[1] - 270))
        else:
            screen.blit(pygame.image.load('images/draw.png').convert_alpha(), (center[0] - 220, center[1] - 300))

        mouse = pygame.mouse.get_pos()

        playAgain = middlefont.render('play again', True, color)
        back = smallfont.render('back' , True , color)

        playAgainButton = width / 2 - 140 <= mouse[0] <= width / 2 + 120 and height / 2 - 50 <= mouse[1] <= height / 2 + 70
        backButton = width / 2 - 102 <= mouse[0] <= width / 2 + 78 and height / 2 + 80 <= mouse[1] <= height / 2 + 140

        if playAgainButton:
            pygame.draw.rect(screen,color_light,pygame.Rect(width/2 - 140,height/2 - 70, 260, 120))
        else:
            pygame.draw.rect(screen,color_dark,pygame.Rect(width/2 - 140,height/2 - 70, 260, 120))
        
        if backButton:
            pygame.draw.rect(screen,color_light,pygame.Rect(width/2 - 102,height/2 + 80, 180, 60))
        else: 
            pygame.draw.rect(screen,color_dark,pygame.Rect(width/2 - 102,height/2 + 80, 180, 60)) 

        screen.blit(playAgain, (center[0] - 120, center[1] - 35))
        screen.blit(back, (center[0] - 45, center[1] + 95))

        pygame.display.update()

def gamemodeScore(agent):

    # Screen resolution.
    screen = pygame.display.set_mode(res)
    background_colour = pygame.Color("#8fcb9e")
    pygame.display.set_caption('Snake Game')
    screen.fill(background_colour)

    # Colours used.
    BLACK = [0, 0, 0]
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

    while menu:

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

        backButton = width / 2 - 102 <= mouse[0] <= width / 2 + 78 and height / 2 + 42 <= mouse[1] <= height / 2 + 102
        readyButton = width / 2 - 140 <= mouse[0] <= width / 2 + 120 and height / 2 - 100 <= mouse[1] <= height / 2 + 20

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
        screen.blit(pygame.image.load('images/press-ready-to-see.png').convert_alpha(), (center[0] - 330, center[1] - 350))
        screen.blit(pygame.image.load('images/the-agent.png').convert_alpha(), (center[0] - 180, center[1] - 245))

        pygame.display.update()
    
    # Run the AI.
    AIscore = displayGame("left", agent, Fruit(0, 0), 1)
    menu = True

    s = pygame.Surface(res)
    s.fill(BLACK)
    s.set_alpha(200)
    pygame.display.update(screen.blit(s, (0,0)))

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
        pygame.display.update(screen.blit(pygame.image.load('images/press-ready-to-play.png').convert_alpha(), (center[0] - 330, center[1] - 300)))

        backButton = width / 2 - 102 <= mouse[0] <= width / 2 + 78 and height / 2 + 42 <= mouse[1] <= height / 2 + 102
        readyButton = width / 2 - 140 <= mouse[0] <= width / 2 + 120 and height / 2 - 100 <= mouse[1] <= height / 2 + 20

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

        pygame.display.update()

    playerScore = PlayerSnakeGame(2)

    gamemodeGameOver(screen, "score", AIscore, playerScore, agent)

def gamemodeDeathmatch(agent):

    # Screen resolution.
    screen = pygame.display.set_mode(res)
    background_colour = pygame.Color("#8fcb9e")
    pygame.display.set_caption('Snake Game')
    screen.fill(background_colour)
    DrawGrid(screen)
    
    # Colours used.
    BLACK = [0, 0, 0]
    color_dark = (100,100,100) 

    # Fonts used.
    bigfont = pygame.font.SysFont('Corbel',70)

    # Screen width, height and center
    width = res[0]
    height = res[1]
    center = (int(width / 2), int(height / 2))

    fruit = Fruit(0, 0)
    fruit.generateFruit()
    fruit.drawFruit(screen)
    agentLastMove = "left"
    playerLastMove = ""
    playerScore = 0
    agentScore = 0

    s = pygame.Surface(res)
    s.fill(BLACK)
    s.set_alpha(200)
    pygame.display.update(screen.blit(pygame.image.load('images/press-any-key.png').convert_alpha(), (center[0] - 325, center[1] - 200)))
    screen.blit(s, (0,0))

    pygame.display.update()

    wait = True

    # -------------------------- Player --------------------------

    playerSnake = Snake(random.randrange(40, 840, 20), random.randrange(40, 680, 20), [])
    pygame.draw.rect(screen, BLACK, playerSnake.draw())

    # Head of snake.
    playerSnake.body.append(pygame.Rect(playerSnake.x, playerSnake.y, blockSize, blockSize))

    # Tail of snake.
    playerSnake.body.append(pygame.Rect(playerSnake.x, playerSnake.y, blockSize, blockSize))

    # -------------------------- Agent --------------------------

    agentSnake = Snake(random.randrange(40, 840, 20), random.randrange(40, 680, 20), [])
    pygame.draw.rect(screen, color_dark, agentSnake.draw())

    # Head of snake.
    agentSnake.body.append(pygame.Rect(agentSnake.x, agentSnake.y, blockSize, blockSize))

    # Tail of snake.
    agentSnake.body.append(pygame.Rect(agentSnake.x, agentSnake.y, blockSize, blockSize))

    pygame.display.update()

    while wait:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    playerLastMove = "left"
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    playerLastMove = "right"
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    playerLastMove = "up"
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    playerLastMove = "down"
                else:
                    playerLastMove = "left"

                wait = False
        
    background_colour = pygame.Color("#8fcb9e")
    screen = pygame.display.set_mode(res)
    pygame.display.set_caption('Snake Game')
    screen.fill(background_colour)
    DrawGrid(screen)
    pygame.display.update()

    switch = True
    game = True

    while game:

        # This is so the user can close the window anytime when displaying.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if playerLastMove != "right":
                        playerLastMove = "left"
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if playerLastMove != "left":
                        playerLastMove = "right"
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if playerLastMove != "down":
                        playerLastMove = "up"
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if playerLastMove != "up":
                        playerLastMove = "down"


        if switch:
            screen.blit(pygame.image.load('images/player-colon2.png').convert_alpha(), (center[0] - 200, center[1] + 330))
            screen.blit(pygame.image.load('images/agent-colon2.png').convert_alpha(), (center[0] + 75, center[1] + 330))
            screen.fill(background_colour, (center[0] - 75, center[1] + 330, 100, 100))
            screen.fill(background_colour, (center[0] + 225, center[1] + 330, 100, 100))
            agentScoreTitle = bigfont.render(str(agentScore), True, BLACK)
            playerScoreTitle = bigfont.render(str(playerScore), True, BLACK)
            switch = False
        else:
            screen.blit(pygame.image.load('images/player-colon.png').convert_alpha(), (center[0] - 200, center[1] + 330))
            screen.blit(pygame.image.load('images/agent-colon.png').convert_alpha(), (center[0] + 75, center[1] + 330))
            screen.fill(background_colour, (center[0] - 75, center[1] + 330, 100, 100))
            screen.fill(background_colour, (center[0] + 225, center[1] + 330, 100, 100))
            agentScoreTitle = bigfont.render(str(agentScore), True, color_dark)
            playerScoreTitle = bigfont.render(str(playerScore), True, color_dark)

            switch = True

        screen.blit(playerScoreTitle, (center[0] - 75, center[1] + 330))
        screen.blit(agentScoreTitle, (center[0] + 225, center[1] + 325))        

        # This moves the snake at a certain time interval.
        if clock.tick(8):

            move = makeMove(agent, agentSnake, agentLastMove, fruit)

            if move[0] == max(move):
                if agentLastMove != "right":
                    agentLastMove = "left"
            if move[1] == max(move):
                if agentLastMove != "left":
                    agentLastMove = "right"
            if move[2] == max(move):
                if agentLastMove != "down":
                    agentLastMove = "up"
            if move[3] == max(move):
                if agentLastMove != "up":
                    agentLastMove = "down"

            MoveSnake(screen, agentLastMove, agentSnake, fruit, True, color_dark)
            MoveSnake(screen, playerLastMove, playerSnake, fruit, True, BLACK)
            

        # If the snake hit's itself.
        if len(agentSnake.body) > 2:
            for parts in agentSnake.body[1:]:
                if agentSnake.x == parts.x and agentSnake.y == parts.y:
                    game = False

        if len(agentSnake.body) > 2:
            for parts in playerSnake.body[1:]:
                if agentSnake.x == parts.x and agentSnake.y == parts.y:
                    agentScore = 0
                    playerScore = 1
                    game = False

        if agentSnake.x == playerSnake.x and agentSnake.y == playerSnake.y:
            agentScore = 0
            playerScore = 0
            game = False

        if agentSnake.x < 20 or agentSnake.x > 860:
            agentScore = 0
            playerScore = 1
            game = False

        if agentSnake.y < 20 or agentSnake.y > 700:
            agentScore = 0
            playerScore = 1
            game = False

        # If the snake hit's itself.
        if len(playerSnake.body) > 2:
            for parts in playerSnake.body[1:]:
                if playerSnake.x == parts.x and playerSnake.y == parts.y:
                    game = False
        
        if len(playerSnake.body) > 2:
            for parts in agentSnake.body[1:]:
                if playerSnake.x == parts.x and playerSnake.y == parts.y:
                    agentScore = 1
                    playerScore = 0
                    game = False

        if playerSnake.x < 20 or playerSnake.x > 860:
            agentScore = 1
            playerScore = 0
            game = False

        if playerSnake.y < 20 or playerSnake.y > 700:
            agentScore = 1
            playerScore = 0
            game = False

        # When you get a fruit it will replace it with another randomly generated fruit.
        # Then it will add one to the score and display it.
        if playerSnake.x == fruit.pos()[0] and playerSnake.y == fruit.pos()[1]:

            # Adds a part to the body.
            Grow(playerSnake, lastMove)

            # Generate a new fruit.
            fruit.generateFruit()

            # Increase score by one.
            playerScore += 1

        # When you get a fruit it will replace it with another randomly generated fruit.
        # Then it will add one to the score and display it.
        if agentSnake.x == fruit.pos()[0] and agentSnake.y == fruit.pos()[1]:

            # Adds a part to the body.
            Grow(agentSnake, lastMove)

            # Generate a new fruit.
            fruit.generateFruit()

            # Increase score by one.
            agentScore += 1
        
        pygame.display.update()


    gamemodeGameOver(screen, "dm", agentScore, playerScore, agent)

def AIMenu():
    
    # Fonts used.
    screen = pygame.display.set_mode(res)
    pygame.display.set_caption('Snake Game')

    bigfont = pygame.font.SysFont('Corbel',70)
    smallfont = pygame.font.SysFont('Corbel',35)
    smallerfont = pygame.font.SysFont('Corbel', 20)
    middlefont = pygame.font.SysFont('Corbel', 55)

    background_colour = pygame.Color("#8fcb9e")
    color = (255,255,255) 
    color_light = (128,128,128) 
    color_dark = (100,100,100)

    # Screen width, height and center
    width = res[0]
    height = res[1]
    center = (int(width / 2), int(height / 2)) 

    counter = 0
    choice = True

    global numSteps

    screen.fill(background_colour)
    pygame.display.update(screen.blit(pygame.image.load('images/logo.png').convert_alpha(), (center[0] - 230, center[1] - 350)))
    pygame.display.flip()

    while choice:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and smallButton:
                numSteps = 1000
                choice = False
            if event.type == pygame.MOUSEBUTTONDOWN and mediumButton:
                numSteps = 2500
                choice = False
            if event.type == pygame.MOUSEBUTTONDOWN and largeButton:
                numSteps = 5000
                choice = False
            if event.type == pygame.MOUSEBUTTONDOWN and backButton:
                return MainMenu()
            
        mouse = pygame.mouse.get_pos()

        smallButton = width / 2 - 240 <= mouse[0] <= width / 2 + 60 and height / 2 - 140 <= mouse[1] <= height / 2 - 20
        mediumButton = width / 2 - 200 <= mouse[0] <= width / 2 + 60 and height / 2 - 10 <= mouse[1] <= height / 2 + 110
        largeButton = width / 2 - 200 <= mouse[0] <= width / 2 + 60 and height / 2 + 120 <= mouse[1] <= height / 2 + 240
        backButton = width / 2 - 160 <= mouse[0] <= width / 2 + 20 and height / 2 + 250 <= mouse[1] <= height / 2 + 310

        if smallButton:
            pygame.draw.rect(screen,color_light,pygame.Rect(width/2 - 200,height/2 - 140, 260, 120))
        else:
            pygame.draw.rect(screen,color_dark,pygame.Rect(width/2 - 200,height/2 - 140, 260, 120))

        if mediumButton:
            pygame.draw.rect(screen,color_light,pygame.Rect(width/2 - 200,height/2 - 10, 260, 120))
        else:
            pygame.draw.rect(screen,color_dark,pygame.Rect(width/2 - 200,height/2  - 10, 260, 120))

        if largeButton:
            pygame.draw.rect(screen,color_light,pygame.Rect(width/2 - 200,height/2 + 120, 260, 120))
        else:
            pygame.draw.rect(screen,color_dark,pygame.Rect(width/2 - 200,height/2 + 120, 260, 120))

        if backButton:
            pygame.draw.rect(screen,color_light,pygame.Rect(width/2 - 160,height/2 + 250, 180, 60))
        else: 
            pygame.draw.rect(screen,color_dark,pygame.Rect(width/2 - 160,height/2 + 250, 180, 60)) 

        small = middlefont.render('small', True, color)
        medium = middlefont.render('medium', True, color)
        large = middlefont.render('large', True, color)
        back = smallfont.render('back', True, color)
        smallTime = smallerfont.render('Small: 5 - 6 minute train time.', True, BLACK)
        mediumTime = smallerfont.render('Medium: 7 - 8 minute train time.', True, BLACK)
        largeTime = smallerfont.render('Large: 10 - 11 minute train time.', True, BLACK)
        disclaimer = smallerfont.render('Times are estimates from my machine (AMD Ryzen 7 3700X 8-Core Processor 3.60 GHz)', True, BLACK)

        screen.blit(small, (center[0] - 130, center[1] - 105))
        screen.blit(medium, (center[0] - 160, center[1] + 25))
        screen.blit(large, (center[0] - 130, center[1] + 155))
        screen.blit(back, (center[0] - 105, center[1] + 265))
        screen.blit(smallTime, (center[0] + 80, center[1] - 90))
        screen.blit(mediumTime, (center[0] + 80, center[1] + 40))
        screen.blit(largeTime, (center[0] + 80, center[1] + 170))
        screen.blit(disclaimer, (center[0] - 360, center[1] + 340))

        pygame.display.flip()

    pygame.display.quit()
    screen = pygame.display.set_mode((res[0] + 350, res[1] + 100))
    img1 = pygame.image.load("images/training1.png").convert_alpha()
    img2 = pygame.image.load("images/training2.png").convert_alpha()
    img3 = pygame.image.load("images/training3.png").convert_alpha()

    trainingText = [img1, img2, img3]
    screen.fill(background_colour)
    screen.blit(pygame.image.load('images/loading3.png').convert_alpha(), (center[0] - 30, center[1] - 70))

    pygame.display.update()

    flick = False
    highest = []
    generation = 0

    conn1, conn2  = Pipe(duplex = False)
    # p1 = Thread(target = trainGen, args=(conn2, numSteps,))
    p1 = Process(target = trainGen, args=(conn2, numSteps,))
    p1.start()

    start = timer.time()
    # Training loop
    while 1:

        # Close screen if user clicks quit or the red arrow in the top right corner.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if generation == 76:
            break

        if generation <= 75:
            fitness = conn1.recv()

            if fitness == 1:
                break

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
                screen.blit(trainingText[counter], (center[0] - 50, center[1] - 390))
                flick = False

            else:
                screen.fill(background_colour)
                screen.blit(trainingText[counter], (center[0] - 50, center[1] - 390))
                flick = True

            screen.blit(pygame.image.load('images/current-generation.png').convert_alpha(), (center[0] - 70, center[1] + 330))
            generationCount = bigfont.render(str(generation), True, BLACK)
            screen.blit(generationCount, (center[0] + 240, center[1] + 340))
            size = canvas.get_width_height()
            allGens = pygame.image.fromstring(raw_data2, size, "RGB")
            screen.blit(allGens, (center[0] + 185, center[1] - 220))
            currentGen = pygame.image.fromstring(raw_data, size, "RGB")
            screen.blit(currentGen, (center[0] - 435, center[1] - 220))
            

            matplotlib.pyplot.close('all')
            pygame.display.update()

            counter += 1
            generation += 1

    finalGeneration = conn1.recv()
    conn1.close()
    conn2.close()
    p1.join()
    p1.close()
    end = timer.time()

    # Finished Training loop.
    while 1:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and menuButton:
                pygame.display.quit()
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
                gamemodeDeathmatch(finalGeneration[0][1])
                screen = pygame.display.set_mode((res[0] + 350, res[1] + 100))
        
        screen.fill(background_colour)
        screen.blit(pygame.image.load('images/training-complete.png').convert_alpha(), (center[0] - 80, center[1] - 380))
        screen.blit(pygame.image.load('images/time-elapsed.png').convert_alpha(), (center[0] + 380, center[0] + 380))
        totalTime = smallerfont.render(timer.strftime("%H:%M:%S.{}".format(str(end - start % 1)[2:])[:8], timer.gmtime(end - start)), True, BLACK)
        screen.blit(totalTime, (center[0] + 530, center[1] + 450))

        size = canvas.get_width_height()
        allGens = pygame.image.fromstring(raw_data2, size, "RGB")
        screen.blit(allGens, (center[0] + 185, center[1] - 250))
        currentGen = pygame.image.fromstring(raw_data, size, "RGB")
        screen.blit(currentGen, (center[0] - 435, center[1] - 250))

        screen.blit(pygame.image.load('images/select-a-gamemode.png').convert_alpha(), (center[0] + 305, center[1] + 255))
        screen.blit(pygame.image.load('images/select-an-option.png').convert_alpha(), (center[0] - 305, center[1] + 255))
        
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
        
        
        matplotlib.pyplot.close('all')
        pygame.display.update()

# Grid size.
blockSize = 20
res = (900, 800)    
amountOfChromosomes = 16321

if __name__ == '__main__':

    # # Initilizing
    pygame.init()

    smallerfont = pygame.font.SysFont('Corbel', 20)
    smallfont = pygame.font.SysFont('Corbel',35)
    bigfont = pygame.font.SysFont('Corbel',70)

    # Colours used.
    BLACK = [0, 0, 0]
    RED = [255, 0, 0]
    GRASS = ("#7EC984")
    color = (255,255,255) 
    color_light = (170,170,170) 
    color_dark = (100,100,100) 

    # Screen width, height and center
    width = res[0]
    height = res[1]
    center = (int(width / 2), int(height / 2))

    # Keep track of what direction and when the snake should move.
    clock = pygame.time.Clock()

    lastMove = "left"

    # Runs the main menu.
    MainMenu()