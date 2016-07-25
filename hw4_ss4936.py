#!/usr/bin/env python
#coding:utf-8
import ac3solver
import backtrack
import time

ROW = "ABCDEFGHI";
COL = "123456789";
file1 = open('output_ss4936.txt','w')
file2 = open('Results_ss4936.txt','w')

# utility function to print each sudoku
def printSudoku(sudoku):
        file1.write("-----------------\n")
        for i in ROW:
                for j in COL:
                        file1.write(str(sudoku[i + j]))
                file1.write('\n')        

# Reading of sudoku list from file
try:
    f = open("su.txt", "r")
    sudokuList = f.read()
except:
        print "Error in reading the sudoku file."
        exit()
t1 = time.time()
# 1.5 count number of sudokus solved by AC-3
num_ac3_solved = 0
ac3solved_indexes = []
num = 1
for line in sudokuList.split("\n"):
        if line == "":
                continue
        # Parse sudokuList to individual sudoku in dict, e.g. sudoku["A2"] = 1
        sudoku = {ROW[i] + COL[j]: int(line[9*i+j]) for i in range(9) for j in range(9)}
        # write your AC3 algorithms here, update num_ac3_solved

        if ac3solver.ac3solver(sudoku):
                ac3solved_indexes.append(num)
                num_ac3_solved += 1
        num += 1
t2 = time.time()
# 1.6 solve all sudokus by backtracking
num_bt_solved = 0
for line in sudokuList.split("\n"):
        if line == "":
                continue
        # Parse sudokuList to individual sudoku in dict, e.g. sudoku["A2"] = 1
        sudoku = {ROW[i] + COL[j]: int(line[9*i+j]) for i in range(9) for j in range(9)}
        if backtrack.backtrack(sudoku):
                num_bt_solved += 1
                printSudoku(sudoku)
        # write your backtracking algorithms here
t3 = time.time()
file2.write('Number of puzzles solved by AC3: '+str(num_ac3_solved)+'\nTime taken by AC3: '+str(t2 - t1))
file2.write('\nAll puzzles solved by AC3 are:\n')
for a in ac3solved_indexes:
        file2.write(str(a)+ '\t')
file2.write('\n\nNumber of puzzles solved by backtracking algorithm: '+str(num_bt_solved))
file2.write('\nTime taken by backtracking algorithm: '+str(t3 - t2))

file1.close()
file2.close()
