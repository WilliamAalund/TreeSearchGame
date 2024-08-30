# TreeSearchGame

## This game is a recreation of Pokemon played entirely within the terminal, and powered completely by Python. 

The AI for wild creatures in the game is entirely random. However, trainer AI in the game is powered by the Monte Carlo Tree search algorithm (MTCS.) Information on the algorithm can be found here: https://en.wikipedia.org/wiki/Monte_Carlo_tree_search

The MTCS algorithm provides a way for the game to heuristically determine the best course of action given a particular situation. The reward structure has been tuned and balanced for the game itself, but the algorithm was implemented agnostic of the game mechanic implementations. 
This means that as the game mechanics change and develop, the algorithm will still be able to function, so long as the reward structure is accurate.
