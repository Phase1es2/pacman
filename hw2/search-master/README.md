# search
DFS BFS, UCS, A*:
pseudocode
Function TREE-SEARCH(problem, strategy) returns a solution, or failure
    initialize the search tree using the initial state of problem
    loop do 
        if there are no candidates for expansion then return failure
        choose a leaf node for expansion according to strategy
        if the node contian a goal state then return the corresponding solution
        else expan the node and add the resulting nodes to the search tree
    end
All four code are very similar, each code we need tuple to keep track the visited node.
For DFS we need to use Stack to expand the node successor which is to expand a deepest 
node first and fringe is a FIFO stack, and how the node transfer to the next node.
For BFS we need to use Queue to expand the node successor which is to expand a shallowest node first
and fringe is FIFO queue, and how the node transfer to the next node.
UCS: the strategy for UCS is expand a cheatpest node first, and the fringe is a priority queue.
for UCS there are cost for different node(path), after adding each successor to the priority queue, we set the cost from current node add cost to next node the prioprit of the node. 
A*: A star search is similar as UCS, the different is that we using the heuristic, which is the total cost from start position to the current state add the heuristic from current state to the goal position.

Question 5: Findind All the Corners
There are 3 functions we need to complete:
the first one is that getStartState(), we need to return the starting state of the pacman, which I used a tuple to conatain the starting position and the four croners for the problem.
isGoalState() check if the current state is a goal state, which is a state taht there are no corners left to visited
getSuccessors() which is the function generate all possible successor of given state. It checks all 4 directions, if the next position in any direction is not a wall and is a remaining corner, htat norner is removed from the remaining corners list. Each successor state, action to get there, and cost is appended to a lis of successor, which is returned at the end of the fucntion. 

usese the maximum Manhattan distance from teh current state to the remaining corners as a heuristic.it check if there are no corneres left in the state, if true it return a heuristic value of 0 becuase it's already at the goal.
If there are still corners left, it computes the Manhattan distance from the current position to each remaining corner. 
The heuristic is the maximum of theese distances, which is the fartherst corner

Question 7: Eating All The Dots
The first time I implement this code, I calculate the Manhattan distance from the current position to all pieces of the food return the maximum of the distance. However, after run the code, I find out Path found with total cost of 60 in 2.6 seconds
Search nodes expanded: 9551
Pacman emerges victorious! Score: 570
Average Score: 570.0
Scores:        570.0
Win Rate:      1/1 (1.00)
Record:        Win

To deceast the number of expanded nodes, I see that there are mazeDistance in the searchAgents.py file. which is a better way to find a more informed heuristic for the A* search which decrease the expanded nodes. 

Question *: suboptimal Search
isGoalState(): return self.food[x][y]
returns true if there is food at pacman;s current position

For the findPathToClosestDot()
I called different search algorithm from search.py that I implement before. And I find out the UCS, A*, and BFS only cost 350, but BFS cost 5324.