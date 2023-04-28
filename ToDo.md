Taking a little break and want to write down some notes for when I pick this back up.

    - New class for the player to be able to play the game again.
    - New class to let the player go head to head against a trained agent.
    - Graphing of training and how the neural network operates.
    - Work on GUI and make it more user friendly.
    - Output relavant information when training.
    - mutation(population): After generation 30 the model could be overfitted and need new genes to generate smarter snakes.
      Currently it overrides too many chromosomes so need to tinker.
    - trainGen(population, generation): Need to store the best n agents and return them.
    
    - Fixing the bugs.
    - Currently the bugs include:
        - A black screen showing up when training the AI agent.
        - Not good synergy between snake.py and AIagent.py with methods from one another needing to be used by both files.
        - Not displaying the final result correctly (runs for a bit then goes blank).
        - Only displaying 1 of 3 final snakes.
