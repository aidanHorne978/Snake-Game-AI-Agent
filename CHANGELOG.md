# Snake-Game-AI-Agent

## 15 May 2023:
 - Finished the project on the 12th of May and have taken a few days off. I dove into this head first and ended up spending 6+ hours a day on it but enjoyed every second.
 - I changed the small, medium and large buttons to reflect steps instead of generations. This is because it usually takes around 75 generations regardsless of steps to train the generation so doing more / fewer was pointless. This makes it train faster with being a couple seconds for small (1500 steps/generation) and 5 - 6 seconds for large (10,000 steps/generation).
 - Added in deathmatch which allows you to vs the Agent in the same arena, both fighting for the same fruit. Win conditions are first to make the other run into their body or if one hits the wall they lose.
 - The current run time isn't too bad with the smaller steps being around 3 minutes and the larger being around 7.
 - A big problem is how intense it is on my system. It uses all avaliable CPU sometimes maxing out and while talking to a friend on discord he said my voice was cutting out while it was running. I also had Subnautica open while trying to train a generation and it crashed at around generation 30.
 - The graphics and colour scheme of the project isn't the best, but I don't see myself as the most creative person and definetly had more fun building the genetic algorithm then colouring / positioning buttons.
 - The actual program is working and I'm happy with it but I might do some research on processes and threads and see if I can get it more responsive in the training process.

## 9th May 2023:

### snake-game.py
 - I've now integrated the genetic algorithm and player controls into one file which is now the main file.
 - Sadly, I can't call an instance of AIAgentmultiprocessing.py because I can't share variables and return from one file to another since it's a whole different process and it becomes messy quick.
 - Have implemented a menu system where you can always go back and forth between the two options in the inital menu. This is so it's a smooth program to run.
 - Once the user has pressed "Start (with AI agent)" The code then creates another process for the training which is very computationally heavy. On the main process, it displays to the user information about the training process and once finished it allows the user to select from a range of options and gamemodes.
 - Have also implemented graphing while the population is training. There are two graphs, one for the current generation's fitness and another for max fitness in each generation. These are displayed to the user while the population trains. Also shows the user the generation number but is a bit laggy because of the sheer amount of computations happening in the background.
 - Training time is still 5 - 6 seconds with 2500 steps per generation and now has a variety of options to do after training is complete like:
     - Retrain if the agent for any reason.
     - View the agent playing the snake game.
     - Go head to head in a normal game of snake competing for the highest score.
     - --------------------------------------------------------- Not implemented yet ---------------------------------------------------------------
         * Will have a deathmatch gamemode where you and the agent are both in the same game fighting to hit each other and get the highest score.

## 4th May 2023:

Have recreated the game with the user controlls working and is in repository Snake-Game (https://github.com/aidanHorne978/Snake-Game).
      
### AIAgentmultiprocessing.py
 - Run's the same AI agent as AIagent.py but uses multiprocessing to speed up the generations.
 - Currently, I'm using a desktop with a AMD Ryzen 7 3700X 8-Core Processor 3.60 GHz CPU and I am running 50 Agents in a generation that each do 2,500 steps before returning. I've divided the population into 10 groups  of 5 which takes between 5 - 6 seconds to train a generation.
 - Comparing the 5 - 6 seconds with 2500 steps per generation to the 14 - 15 seconds it takes just using one process in AIagent.py, it is much more efficient and takes way less time (10 minutes instead of 25 minutes).
 - In my previous version, I was dividing the population then training. In this version, I've kept the population together but divide them off to run the game and then bring them all back together when assessing fitness and doing the crossover / mutation functions.
 - **This is now the main file.**

### AIagent.py:
 - A genetic algorithm that uses components from snake.py to train 50 agents over 100 generations. 
 - I've improved efficiency by stripping away the visual components for training and it now trains in 15 minutes for 1000 steps and 50 agents.
 - Currently, the agent has a 12 neuron input layer, 1 hidden layers of 120 neurons, and a 4 output neuron layer that contains the probability for each direction.
 - The inputs are the position of the food (4 inputs). Current direction the snake is going (4 inputs). If there is a wall in any direction (4 inputs).
 - Will be working on having an input that has information on the body of the snake so it knows when it's long and turning around to avoid itself.

      
## April 27th 2023:

#### AIagent(multiprocessing).py
 - By using multiprocessing, I could speed up each generation to take 35 seconds with 10 worker processes, 38 seconds with 5 worker processes. instead of 85 seconds with 1 process.
 - Currently uses the multiprocessing library and Pool() which creates worker processes. I've tried 5, 10, 2 worker processes with 5 seeming to be the best.
 - The downside to this is that when we do crossover, the population size to select the best candidates is only 5 snakes instead of the full 50.

#### AIAgent(multiprocessing).py without visuals:
 - WIthout visuals it improved the time for a single process to 12 seconds and with 10 worker processes it improved it down to 2 seconds.
 - It can run the 100 generations in 171 seconds with the 10 worker processes.
 - The problem is as I feared. There isn't enough crossover and that means that we don't improve enough to get good results.
 - Will retire this file for now and maybe come back to it later and implement multiprocessing where they can talk to each other but I feel this will be a lot more work than it's worth.

 ## Before April 27th 2023:
  - I wasn't sure I could finish this project so I never made a changelog but I started the project around the start of April.
  - I started by creating the snake game which took about 2 weeks. The major challenges I had was working with PyGame for the first time and getting each segment of the snake to follow the last.
  - I then started tackling the AI and had a lot of issues with the input nodes not working correctly.
  - Then had issues with the snake getting around the (if left, you can't go right). This was because I was moving around methods to different files and trying to make concise code before it even worked.
  - Also had problems with the fitness function not rewarding scoring and snakes would flattening out at 0 fitness and not learn how to score they would just value survival. The reason this happened was that the input nodes weren't giving the correct direction of the food and after fixing that the algorithm could connect the input nodes to food position and started working.
  - I'm writing this on the 15th May 2023, so I don't remember all my challenges but these ones stick out in my mind.

Sites that helped:
 - ChatGPT. (Had a lot of conversations with the AI but never copied chunks of code just used it more for the maths).
 - https://davideliu.com/2020/02/03/teaching-ai-to-play-snake-with-genetic-algorithm/
 - https://www.sitepoint.com/python-multiprocessing-parallel-programming/
 - https://www.fontspace.com/snake-holiday-font-f87373
