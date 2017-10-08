from mp1_1 import *
import sys


""" Maze Class """
class Maze_Multiple_Dot(Maze_One_Dot):
    """ Maze class for multiple dot """
    def __init__(self,maze):
        self.maze = maze 
        self.size = [self.getHeight(maze),self.getWidth(maze)] 
        self.start = []
        self.dots = []                                # List of all dots
        self.find_dots(self.maze)                     # FInd all dots


    def find_first_start(self,maze):
        """ The function to find the starting state and return a list of coordinates"""
        x_ind = 0;
        y_ind = 0;
        for line in maze:
            x_ind = 0;
            for char in line:
                if char == 'P':
                    return [y_ind,x_ind]
                x_ind += 1;
            y_ind += 1;

    def find_dots(self,maze):
        """ The function to find all the dots and return a list of coordinates"""
        x_ind = 0
        y_ind = 0
        for line in maze:
            x_ind = 0;
            for char in line:
                if char == '.':
                    self.dots.append([y_ind,x_ind,False])
                x_ind += 1
            y_ind += 1

    def is_goal(self,state):                 
        """ Goal of the 1.1 """
        if self.no_of_remain_dots() == 0:
            return True

    def no_of_remain_dots(self):             # Find No. of reamining dots not explored yet
        length = 0
        for dot in self.dots:
            if dot[2] == False:
                length += 1
        return length



"""" All the search classes """
class DFS_Search_Maze_Multiple(DFS_Search_Maze_Unique): 
    def __init__ (self,maze):
        self.frontier = []
        self.maze = Maze_Multiple_Dot(maze)
        self.start = []
        self.frontier.append(self.start)
        self.explored = []
        self.end = []
        self.parent = {}
        self.draw_no = 1
        self.cost = 0

    def is_end(self,state):
        if state[0] == self.end[0] and state[1] == self.end[1]:
            return True

    def is_empty(self):
        if len(self.frontier) == 0:
            return True;
        else:
            return False;

    def next_nodes(self):
        return self.frontier.pop();


    def next_dot(self,next_state):
        remain_dots = []
        print('#101 self.maze.dots =',self.maze.dots)
        for dots in self.maze.dots:
            if dots[2] == False:
                if dots[0] != next_state[0] and dots[1] != next_state[1]:
                    heuristic_cost = abs(dots[0]-self.start[0])+abs(dots[1]-self.start[1])
                    dots.append(heuristic_cost)
                    print('107 dots =',dots)
                    remain_dots.append(dots)
        print('#107 remain dots =',remain_dots)
        state = min(remain_dots,key=lambda x:x[3]);
        return state[0:3]


    def expand(self,state):
        new_state = list(state)

        i = 0
        for dot in self.maze.dots:
            if (new_state[0] == dot[0] and new_state[1] == dot[1]):
                self.maze.dots[i][2] = True
                break
            i += 1


        new_state = list(state)
        new_state[0] -= 1
        print('UP',new_state[1],new_state[0])
        if(self.maze.is_legal(new_state)):
            if new_state not in self.explored:
                self.explored.append(new_state)
                self.frontier.append(new_state)
                self.parent[','.join(str(v) for v in new_state)] = state

        new_state = list(state)
        new_state[0] += 1
        print('DOWN',new_state[1],new_state[0])
        if(self.maze.is_legal(new_state)):
            if new_state not in self.explored:
                self.explored.append(new_state)
                self.frontier.append(new_state)
                self.parent[','.join(str(v) for v in new_state)] = state

        new_state = list(state)
        new_state[1] -= 1
        print('LEFT',new_state[1],new_state[0])
        if(self.maze.is_legal(new_state)):
            if new_state not in self.explored:
                self.explored.append(new_state)
                self.frontier.append(new_state)
                self.parent[','.join(str(v) for v in new_state)] = state

        new_state = list(state)
        new_state[1] += 1
        print('RIGHT',new_state[1],new_state[0])
        if(self.maze.is_legal(new_state)):
            if new_state not in self.explored:
                self.explored.append(new_state)
                self.frontier.append(new_state)
                self.parent[','.join(str(v) for v in new_state)] = state


    def draw_path(self,end): 
        if end == self.start[0:2]:
            return 
        self.maze.draw(end,'*')    
        self.draw_path(self.parent[','.join(str(v) for v in end)])

    def display(self):
        return self.maze.display()



""" The general search top level """
def general_search_multiple(maze):
    """ Top-level search """
    next_state = []
    search = DFS_Search_Maze_Multiple(maze)
    temp_start = search.maze.find_first_start(maze)
    no_of_remain_dots = search.maze.no_of_remain_dots()
    print('no_of_remain_dots =',no_of_remain_dots)
    nodes_explored = 0
    cost = 0

    while no_of_remain_dots != 0:
        search = DFS_Search_Maze_Multiple(maze)
        search.start = temp_start
        print('#199 search.start =',search.start)
        search.frontier.append(search.start)
        search.end = search.next_dot(search.start)
        cost += abs(search.end[0]-search.start[0])+abs(search.end[1]-search.start[1])
        print('#199 search.end =',search.end[0:2])
        while(search.is_empty()==False):
            print('#201 not empty')
            next_state = search.next_nodes()
            print('#203 next state =',next_state)
            nodes_explored += 1
            if(search.is_end(next_state)):
                break
            search.expand(next_state)
        temp_start = next_state

        i = 0
        while(search.maze.dots[i][0] != next_state[0] and search.maze.dots[i][1] != next_state[1]):
            i += 1
        search.maze.dots[i][2] = True
        no_of_remain_dots -= 1
        print('#218 no_of_remain_dots =',no_of_remain_dots)
        maze = search.maze.maze 
        print('#223 maze =',maze)

    search.display()
    print('nodes explored =',nodes_explored)
    print('cost =',cost)
    

""" Read the maze """
maze = [];
indY = 0;
indX = 0;
with open(sys.argv[1]) as f_maze:
    for line in f_maze:
        maze.append([]);
        indX = 0;
        for char in line:
            if char != '\n':
                maze[indY].append(char);
                indX+=1;
        indY+=1;
general_search_multiple(maze)





