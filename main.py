from solver import *
from generator import *
#===== Text I/O ======#
def text(maze):
    final = []
    for row in maze:
        final.append([' ' if tile else 'X' for tile in row])
    return(final)

def printMaze(textMaze):
    decor = 'O' + '-' * (len(textMaze[0]) * 2 - 1) + 'O'
    print(decor)
    for row in textMaze:
        print('|'+' '.join(row)+'|')
    print(decor)

def overlaySolution(textMaze,solution):
    for point in solution:
        textMaze[point[1]][point[0]] = '@'
        

if(__name__ == '__main__'):
    pass
