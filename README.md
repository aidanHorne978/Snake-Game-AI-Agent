# Snake-Game-AI-Agent

4th May 2023:

    Have recreated the game with the user controlls working and is in repository Snake-Game (https://github.com/aidanHorne978/Snake-Game).

 **AIagent.py:**
      - A genetic algorithm that uses components from snake.py to train 50 agents over 100 generations. 
      - I've improved efficiency by stripping away the visual components for training and it now trains in 15 minutes for 1000 steps and 50 agents.
      - Currently, the agent has a 12 neuron input layer, 1 hidden layers of 120 neurons, and a 4 output neuron layer that contains the probability for each direction.
      - The inputs are the position of the food (4 inputs). Current direction the snake is going (4 inputs). If there is a wall in any direction (4 inputs).
      - Will be working on having an input that has information on the body of the snake so it knows when it's long and turning around to avoid itself.
      
**AIAgentmultiprocessing.py**
      - Run's the same AI agent as AIagent.py but uses multiprocessing to speed up the generations.
      - Currently, I'm using a desktop with a AMD Ryzen 7 3700X 8-Core Processor 3.60 GHz CPU and I am running 50 Agents in a generation that each do 2,500 steps before returning. I've divided the population into 10 groups  of 5 which takes between 5 - 6 seconds to train a generation.
      - Comparing the 5 - 6 seconds per generation to the 14 - 15 seconds it takes just using one process in AIagent.py, it is much more efficient and takes way less time (10 minutes instead of 25 minutes).
      - In my previous version, I was dividing the population then training. In this version, I've kept the population together but divide them off to run the game and then bring them all back together when assessing fitness and doing the crossover / mutation functions.
      
April 27th 2023:

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
