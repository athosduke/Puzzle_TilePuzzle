import math
import random
import time
from queue import PriorityQueue
import copy

def create_tile_puzzle(rows, cols):
    board = []
    for i in range(rows):
        line =[]
        for j in range(1,cols+1):
            line.append(j+i*cols);
        board.append(line)
    board[rows-1][cols-1] = 0;
    return TilePuzzle(board)

class TilePuzzle(object):
    
    # Required
    def __init__(self, board):
        self.board = board
        cols = len(self.board[0])
        self.cols = cols
        self.rows = len(self.board)
        pindex = (sum(board,[])).index(0)
        self.prow = int(pindex/cols)
        self.pcol = pindex%cols
        
    def get_board(self):
        return (self.board)

    def elements(self):
        return sum(self.board,[])

    def h(self):
        elements = sum(self.board,[])
        count = 0
        for i in range(len(elements)-1):
            if elements[i] != i+1:
                irow = self.rows -1;
                icol = self.cols -1;
                if elements[i] != 0:   
                    irow = int((elements[i]-1)/self.cols);
                    icol = (elements[i]-1)%self.cols;
                count += abs(irow-int(i/self.cols)) + abs(icol-i%self.cols);
        last = elements[-1];
        if last != 0:
            count += abs(int(last/self.cols)-(self.cols-1))+abs(last%self.cols-(self.cols-1));
        return count

    def perform_move(self, direction):
        result = False
        prow = self.prow
        pcol = self.pcol
        if (direction == "up"):
            if (self.prow > 0):
                self.prow -= 1
                self.board[prow][pcol] = self.board[prow-1][pcol]
                self.board[prow-1][pcol] = 0 
                result = True
        elif (direction == "down"): 
            if (self.prow < self.rows-1):
                    self.prow += 1
                    self.board[prow][pcol] = self.board[prow+1][pcol]
                    self.board[prow+1][pcol] = 0 
                    result = True
        elif (direction == "left"): 
            if (self.pcol > 0):
                    self.pcol -= 1
                    self.board[prow][pcol] = self.board[prow][pcol-1]
                    self.board[prow][pcol-1] = 0 
                    result = True
        elif (direction == "right"): 
            if (self.pcol < self.cols-1):
                    self.pcol += 1
                    self.board[prow][pcol] = self.board[prow][pcol+1]
                    self.board[prow][pcol+1] = 0 
                    result = True
        return result

    def scramble(self, num_moves):
        directionlist = ["up","down","left","right"]
        i = 1
        while(i < num_move):
            direction = random.choice(directionlist)
            poss = self.perform_move(direction)
            if(poss):
                i+=1


    def is_solved(self):
        if (self.board[self.rows-1][self.cols-1] != 0):
            return False
        elements = sum(self.board,[])
        for i in range(len(elements)-1):
            if (elements[i]!=i+1):
                return False
        return True


    def copy(self):
        copy = []
        for i in self.board:
            line = []
            for j in i:
                line.append(j)
            copy.append(line)
        return TilePuzzle(copy)

    def successors(self):
        for d in ["up","down","left","right"]:
            newboard = self.copy()
            poss = newboard.perform_move(d)
            if(poss):
                yield d, newboard

    def helper_iddfs(self,limit,moves):
        for move,newpuzzle in self.successors():
            moves.append(move)
            if newpuzzle.is_solved():
                yield moves[:]
            if (len(moves)<limit):
                for i in newpuzzle.helper_iddfs(limit,moves):
                    yield i
            moves.pop()

    # Required
    def find_solutions_iddfs(self):
        #start_time = time.time()
        if self.is_solved():
            return []
        fit = False
        for i in range (100):
            for sol in self.helper_iddfs(i,[]):
                if sol is not None:
                    yield sol
                    fit = True
            if fit:
                #print("--- %s seconds ---" % (time.time() - start_time))
                break

    # Required
    def find_solution_a_star(self):
        #start_time = time.time()
        if self.is_solved():
            return []
        depth = 0
        knownboard = []
        knownboard.append(self.board)
        openlist = PriorityQueue()
        f = self.h() + depth
        #        score depth move newboard
        openlist.put((f,(depth,[],self)))
        while not openlist.empty():
            mytuple = openlist.get()
            #f = mytuple[0]
            depth = mytuple[1][0]
            moves = mytuple[1][1]
            newp = mytuple[1][2]
            for move,newpuzzle in newp.successors():
                if(newpuzzle.board) not in knownboard:
                    newmove = copy.copy(moves)
                    newmove.append(move)
                    if newpuzzle.is_solved():
                        #print("--- %s seconds ---" % (time.time() - start_time))
                        return newmove
                    knownboard.append(newpuzzle.board)
                    newdepth = depth+1
                    newf = newpuzzle.h()+ newdepth
                    new_p = newpuzzle.copy()
                    #print(newf,newmove,new_p.get_board(),newdepth)
                    openlist.put((newf,(newdepth,newmove,new_p)))
