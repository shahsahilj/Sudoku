import random
import numpy as np

ROW = "ABCDEFGHI";
COL = "123456789";
Rowgroups = ["ABC","DEF","GHI"]
Colgroups = ["123","456","789"]

##generates the neighbor list for a given i,j
def getNeighbors(i,j):
    neighbors = []
    for r in ROW:
        if r != i:
            neighbors.append(r+j)##same row elements
    for c in COL:
        if c != j:
            neighbors.append(i+c)##same column elements
    for r in Rowgroups:
        if i in r:
            rowbox = r
    for c in Colgroups:
        if j in c:
            colbox = c
    for r in rowbox:
        for c in colbox:
            if r+c not in neighbors and (r+c) != (i+j):
                neighbors.append(r+c)##same box elements
    return neighbors

##checks if length of all the domains is 1
def isSolved(Domains):
    for i in ROW:
        for j in COL:
            if len(Domains[i+j])>1:
                return False
    return True

##checks arc consistency for a pair of positions
def check_consistency(a,b,Domains):
    x_i = Domains[a]
    y_i = Domains[b]
    change = False
    ##for all x in x_i there should be at least one other value in y_i. If there is a conflict, x is removed from x_i
    for x in x_i:
        if x in y_i:
            if len(y_i) == 1:
                change = True
                x_i.remove(x)
    return change

##The main logic of the code
def ac3solver(sudoku):
    Domains = {} ##Domains store the possible values for the positions
    for i in ROW:
        for j in COL:
            if sudoku[i + j] == 0:
                Domains[i + j] = [k for k in range(1,10)]##If it was empty it can have any value(The constraints will be eliminated later)
            else:
                Domains[i + j] = [sudoku[i + j]]##If it was already assigned a value
    worklist = []
    ##A worklist of the constraints is created...Here all neighbors of all elements are added
    for i in ROW:
        for j in COL:
            neighbors = getNeighbors(i , j)
            for n in neighbors:
                worklist.append([n, i + j])
    ##For all the pairs in the worklist check the consistency, If there is a change then add all the neighbors of the changed element back to the worklist
    while len(worklist) != 0:
        [a,b] = worklist.pop()
        if check_consistency(a,b,Domains):
            if len(Domains[a]) == 0:
                return False
            [i,j] = a
            neighbors = getNeighbors(i , j)
            for n in neighbors:
                if [n,i+j] not in worklist:
                    worklist.append([n, i + j])
    ##If the problem is not solved using simple AC3, then keep assigning random values from domains with smallest length and check consistency again
    ##Smallest length is selected because that will have the maximum probability of being correct
    while not isSolved(Domains):
        smallest_len = np.inf
        [r,c] = [0,0]
        for i in ROW:
            for j in COL:
                l = len(Domains[i+j])
                if l < smallest_len and l != 1:
                    smallest_len = l
                    [r,c] = [i,j]
        Domains[r+c] = [random.choice(Domains[r+c])]##change domain of smallest possible
        neighbors = getNeighbors(r,c)##get neighbors
        worklist = []
        for n in neighbors:
            worklist.append([n, r+c])##add to worklist
        while len(worklist) != 0:
            [a,b] = worklist.pop()
            if check_consistency(a,b,Domains):##check consistency
                if len(Domains[a]) == 0:
                    return False
                [i,j] = a
                neighbors = getNeighbors(i , j)
                for n in neighbors:
                    if [n,i+j] not in worklist:
                        worklist.append([n, i + j])
    for i in ROW:
        for j in COL:
            sudoku[i+j] = Domains[i+j][0]##Assign the  solved domains to the sudoku puzzle
    return True
        


def main():
    f = open("sudokus.txt", "r")
    sudokuList = f.read()
    count = 0
    for line in sudokuList.split('\n'):
        sudoku = {ROW[i] + COL[j]: int(line[9*i+j]) for i in range(9) for j in range(9)}
        print ac3solver(sudoku)
##        if count == 0:
##            break

if __name__ == "__main__":
    main()
