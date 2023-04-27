# Snake-Game-AI-Agent

snake.py:
  - A simple snake game made in Python using the PyGame library. Currently has user control stripped but will be adding back soon.

AIagent.py:
  - A genetic algorithm that uses snake.py to train 50 agents over 100 generations. Currently it takes a long time to train so looking at ways to improve efficiency
  - Currently, the agent has a 14 neuron input layer, 3 hidden layers of 120 neurons, and a 4 output neuron layer that contains the probability for each direction.
  - The inputs are relative x and y position of food (2 inputs). Direction of food (4 inputs). Current direction the snake is going (4 inputs). If there is a wall in any direction (4 inputs).]
  - 




Sites that helped:
  - https://davideliu.com/2020/02/03/teaching-ai-to-play-snake-with-genetic-algorithm/
  - https://www.sitepoint.com/python-multiprocessing-parallel-programming/
