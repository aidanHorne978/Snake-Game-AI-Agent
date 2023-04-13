import pygame
import random
import time

## Global Variables

# Initilizing
pygame.init()

# Screen resolution.
res = (900, 800)
screen = pygame.display.set_mode(res)

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

# Grid size.
blockSize = 20

# Screen width, height and center
width = screen.get_width()
height = screen.get_height()
center = screen.get_rect().center

class Snake:

    def __init__(self, x, y, body, size):
        self.x = x
        self.y = y
        self.body = body
        self.size = size

    def pos(self):
        return self.x, self.y

    def draw(self):
        return pygame.Rect(self.x, self.y, blockSize, blockSize)
    
def MainMenu():

    # Creating the screen.
    background_colour = pygame.Color("#8fcb9e")
    pygame.display.set_caption('Snake Game')
    screen.fill(background_colour)
    pygame.display.flip()

    quit = smallfont.render('quit' , True , color)
    start = bigfont.render('start' , True , color)

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
                return

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
        screen.blit(start, (center[0] - 75, center[1] - 75))
        
        # Puts the "snake" logo onto the screen.
        logo = pygame.image.load('images/logo.png')
        screen.blit(logo, (center[0] - 230, center[1] - 350))


        # updates the frames of the game 
        pygame.display.update() 

def DrawGrid(screen):

    # Drawing the grid.
    for x in range(20, res[0] - 20, blockSize):
        for y in range(20, res[1] - 80, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, pygame.Color(GRASS), rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

def Grow(snake, direction):
    if direction == "left":
        snake.body.append(pygame.draw.rect(screen, BLACK, pygame.Rect(snake.x, snake.y, blockSize, blockSize)))
    elif direction == "right":
        snake.body.append(pygame.draw.rect(screen, BLACK, pygame.Rect(snake.x, snake.y, blockSize, blockSize)))
    elif direction == "up":
        snake.body.append(pygame.draw.rect(screen, BLACK, pygame.Rect(snake.x, snake.y, blockSize, blockSize)))
    elif direction == "down":
        snake.body.append(pygame.draw.rect(screen, BLACK, pygame.Rect(snake.x, snake.y, blockSize, blockSize)))

def MoveSnake(direction, snake, lastDirection):

    # Draw's the background and grid back.
    pygame.draw.rect(screen, pygame.Color(GRASS), snake.draw())
    pygame.draw.rect(screen, BLACK, snake.draw(), 1)

    if direction == "left":
        if snake.x > 20:
            snake.x -= 20
    elif direction == "right":
        if snake.x < 850:
            snake.x += 20
    elif direction == "up":
        if snake.y > 20:
            snake.y -= 20
    elif direction == "down":
        if snake.y < 700:
            snake.y += 20

    pygame.draw.rect(screen, BLACK, snake.draw())

    i = 1
    for part in snake.body:
        pygame.draw.rect(screen, pygame.Color(GRASS), part)
        pygame.draw.rect(screen, BLACK, part, 1)

        # For when the snake changes direction.
        # This makes sure the snake flows properly and goes to the space it's segement before
        # Was on before changing direction.
        if direction != lastDirection:
            if lastDirection == "left":
                if part.x > 20:
                    if len(snake.body) <= 1:
                        part.x = snake.x
                    else:
                        part.x = snake.body[i].x
            elif lastDirection == "right":
                if part.x < 850:
                    if len(snake.body) <= 1:
                        part.x = snake.x
                    else:
                        part.x = snake.body[i].x
            elif lastDirection == "up":
                if snake.y > 20:
                    if len(snake.body) <= 1:
                        part.y = snake.y
                    else:
                        part.y = snake.body[i].y
            elif lastDirection == "down":
                if snake.y < 700:
                    if len(snake.body) <= 1:
                        part.y = snake.y
                    else:
                        part.y = snake.body[i].y

        # Changes directions of the segments of the body.
        if direction == "left":
            if part.x > 20:
                part.x = snake.x + 20 * i
        elif direction == "right":
            if part.x < 850:
                part.x = snake.x - 20 * i
        elif direction == "up":
            if snake.y > 20:
                part.y = snake.y + 20 * i
        elif direction == "down":
            if snake.y < 700:
                part.y = snake.y - 20 * i

        pygame.draw.rect(screen, BLACK, part)

        i += 1

        # print(snake.body)
        # print("Head x: {}".format(snake.x))
        # print("Body x: {}".format(snake.body[0].x))
        # print("Head y: {}".format(snake.y))
        # print("Body y: {}".format(snake.body[0].y))
        # print()
        # time.sleep(1)
    i = 1


        # print(part.x)
        # print(snake.body)
        # exit()
    # Draws where the snake moves.
    # pygame.draw.rect(screen, BLACK, snake.draw())
    # print(snake.body)

def Fruit():

    # Range is so it fits in the grid of the game.
    x = random.randrange(20, 860, 20)
    y = random.randrange(20, 700, 20)

    # Draw's the fruit on the grid.
    rect = pygame.Rect(x, y, blockSize, blockSize)
    pygame.draw.rect(screen, RED, rect)

    # Returns the position of the fruit.
    return x, y

def SnakeGame():

    # Creating the screen.
    background_colour = pygame.Color("#8fcb9e")
    res = (900, 800)
    screen = pygame.display.set_mode(res)
    pygame.display.set_caption('Snake Game')
    screen.fill(background_colour)
    pygame.display.flip()

    # Keep track of what direction and when the snake should move.
    clock = pygame.time.Clock()
    lastMove = "left"
    lastDirection = ""

    # Drawing the grid.
    DrawGrid(screen)

    # Draws the grid for the game, the initial snake and the fruit.
    snake = Snake(width / 2 - 30, height / 2 - 60, [], 1)
    pygame.draw.rect(screen, BLACK, snake.draw())
    fruit = Fruit()

    grow = False

    # Score variable.
    score = 0
    scoreTitle = smallfont.render('score:' , True , BLACK)
    scoreValue = smallfont.render(str(score), True, BLACK)
    screen.blit(scoreTitle, (center[0] - 125, center[1] + 330))
    screen.blit(scoreValue, (center[0] - 30, center[1] + 330))

    while True:

        pygame.display.update()
        
        lastDirection = lastMove

        # Close screen if user clicks quit or the red arrow in the top right corner.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            # If the user presses a key that is allowed it will remember the key for when the clock ticks and the snake is moved.
            if event.type == pygame.KEYDOWN:
                pygame.draw.rect(screen, pygame.Color(GRASS), snake.draw())
                pygame.draw.rect(screen, BLACK, snake.draw(), 1)
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    # snake.x -= 20
                    if lastMove != "right":
                        lastMove = "left"
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    # snake.x += 20
                    if lastMove != "left":
                        lastMove = "right"
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    # snake.y -= 20
                    if lastMove != "down":
                        lastMove = "up"
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    # snake.y += 20
                    if lastMove != "up":
                        lastMove = "down"
                # pygame.draw.rect(screen, BLACK, snake.draw())

        # When you get a fruit it will replace it with another randomly generated fruit.
        # Then it will add one to the score and display it.
        if snake.x == fruit[0] and snake.y == fruit[1]:

            # Generate a new fruit.
            fruit = Fruit()

            # Increase score by one and increase snake length.
            score += 1
            Grow(snake, lastMove)

            # Erase the old score and put in the new score.
            scoreValue = smallfont.render(str(score), True, BLACK)
            screen.fill(background_colour, (center[0] - 30, center[1] + 330, 100, 100))
            screen.blit(scoreValue, (center[0] - 30, center[1] + 330))

        # This moves the snake at a certain time interval.
        if clock.tick(6):
            MoveSnake(lastMove, snake, lastDirection)
            pygame.display.update()
    
# Runs the main menu.
MainMenu()

# Once user clicks "start", the main menu will close and the code then runs the game.
SnakeGame()