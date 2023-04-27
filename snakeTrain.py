#!/usr/bin/python
import pygame
import random
import numpy as np

# Screen resolution.
res = (900, 800)

# Grid size.
blockSize = 20

# Screen width, height and center
width = res[0]
height = res[1]

# Keep track of what direction.
distance = 0

# Snake class
class Snake:

    def __init__(self, x, y, body):
        self.x = x
        self.y = y
        self.body = body

    def pos(self):
        return self.x, self.y


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

def MoveSnake(direction, snake):

    # Moves the head of the snake.
    if direction == "left":
        snake.x -= blockSize
    elif direction == "right":
        snake.x += blockSize
    elif direction == "up":
        snake.y -= blockSize
    elif direction == "down":
        snake.y += blockSize

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

    # Update the head in the body list.
    snake.body[0].x = snake.x
    snake.body[0].y = snake.y

def SnakeGame(player, lastMove, fruit):

    ## Global variables.
    global fruits
    global score
    global distance

    if len(player.body) < 1:

        # Draws the grid for the game and the fruit.
        fruits = fruit
        fruits.generateFruit()
        distance = 0

        # Head of snake.
        player.body.append(pygame.Rect(player.x, player.y, blockSize, blockSize))

        # Tail of snake.
        player.body.append(pygame.Rect(player.x, player.y, blockSize, blockSize))

        # Score variable.
        score = 0

    MoveSnake(lastMove, player)
    distance += 1

    # When you get a fruit it will replace it with another randomly generated fruit.
    # Then it will add one to the score and display it.
    if player.x == fruits.pos()[0] and player.y == fruits.pos()[1]:

        # Adds a part to the body.
        Grow(player, lastMove)

        # Generate a new fruit.
        fruits.generateFruit()

        # Increase score by one.
        score += 1

    # If the snake hit's itself.
    if len(player.body) > 2:
        for parts in player.body[1:]:
            if player.x == parts.x and player.y == parts.y:
                return score, distance, False

    if player.x < 20 or player.x > 860:
        return score, distance, False

    elif player.y < 20 or player.y > 700:
        return score, distance, False
    else:
        return score, distance, True