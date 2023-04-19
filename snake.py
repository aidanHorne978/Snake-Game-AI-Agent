import pygame
import random

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

def MoveSnake(direction, snake, fruit):

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

            pygame.draw.rect(screen, BLACK, snake.body[j])

            # Draw's the background and grid back.
            pygame.draw.rect(screen, pygame.Color(GRASS), snake.body[-1])
            pygame.draw.rect(screen, BLACK, snake.body[-1], 1)

    # Update the head in the body list.
    snake.body[0].x = snake.x
    snake.body[0].y = snake.y

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

    # Drawing the grid.
    DrawGrid(screen)

    # Draws the grid for the game and the fruit.
    fruit = Fruit(0,0)
    fruit.generateFruit()
    snake = Snake(width / 2 - 30, height / 2 - 60, [])
    pygame.draw.rect(screen, BLACK, snake.draw())
    fruit.drawFruit()

    # Head of snake.
    snake.body.append(pygame.Rect(snake.x, snake.y, blockSize, blockSize))

    # Tail of snake.
    snake.body.append(pygame.Rect(snake.x, snake.y, blockSize, blockSize))

    # Score variable.
    score = 0
    scoreTitle = smallfont.render('score:' , True , BLACK)
    scoreValue = smallfont.render(str(score), True, BLACK)
    screen.blit(scoreTitle, (center[0] - 75, center[1] + 330))
    screen.blit(scoreValue, (center[0] + 15, center[1] + 330))

    while True:
        
        pygame.display.update()

        # If the snake hit's itself.
        if len(snake.body) > 2:
            for parts in snake.body[1:]:
                if snake.x == parts.x and snake.y == parts.y:
                    GameOver()

        if snake.x < 20 or snake.x > 860:
            GameOver()

        if snake.y < 20 or snake.y > 700:
            GameOver()


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
            MoveSnake(lastMove, snake, fruit)
            pygame.display.update()

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
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and startButton:
                SnakeGame()

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

# Runs the main menu.
MainMenu()

# Once user clicks "start", the main menu will close and the code then runs the game
# and will keep running until the user closes the game.
SnakeGame()