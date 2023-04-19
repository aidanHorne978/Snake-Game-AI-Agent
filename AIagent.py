#!/usr/bin/python
import pygame
import random
import numpy as np
import snake

screen = snake.screen
width = snake.width
height = snake.height

snake.MainMenu()

player = snake.Snake(width / 2 - 30, height / 2 - 60, [])

snake.SnakeGame(player)


