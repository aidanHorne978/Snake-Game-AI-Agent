# Snake-Game-AI-Agent

snake.py:
  - A simple snake game made in Python using the PyGame library. Currently has user control stripped but will be adding back soon.

AIagent.py:
  - A genetic algorithm that uses snake.py to train 50 agents over 100 generations. Currently it takes a long time to train so looking at ways to improve efficiency
  - Currently, the agent has a 14 neuron input layer, 3 hidden layers of 120 neurons, and a 4 output neuron layer that contains the probability for each direction.
  - The inputs are relative x and y position of food (2 inputs). Direction of food (4 inputs). Current direction the snake is going (4 inputs). If there is a wall in any direction (4 inputs).

AIagent(multiprocessing).py
  - By using multiprocessing, I could speed up each generation to take 35 seconds with 10 worker processes, 38 seconds with 5 worker processes. instead of 85 seconds with 1 process.
  - Currently uses the multiprocessing library and Pool() which creates worker processes. I've tried 5, 10, 2 worker processes with 5 seeming to be the best.
  - The downside to this is that when we do crossover, the population size to select the best candidates is only 5 snakes instead of the full 50.

AIAgent(multiprocessing).py without visuals:
  - WIthout visuals it improved the time for a single process to 12 seconds and with 10 worker processes it improved it down to 2 seconds.
  - It can run the 100 generations in 171 seconds with the 10 worker processes.
  - The problem is as I feared. There isn't enough crossover and that means that we don't improve enough to get good results.
  - Will retire this file for now and maybe come back to it later and implement multiprocessing where they can talk to each other but I feel this will be a lot more work than it's worth.

Sites that helped:
  - https://davideliu.com/2020/02/03/teaching-ai-to-play-snake-with-genetic-algorithm/
  - https://www.sitepoint.com/python-multiprocessing-parallel-programming/
