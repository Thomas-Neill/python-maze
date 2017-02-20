import random
import argparse
import time
from collections import namedtuple
location = namedtuple("location",['x','y'])

#===== COMMAND-LINE ARGUMENTS =====#
def get_args():
    parser = argparse.ArgumentParser(
        description="A Python maze generator",
        epilog="Usage: generator.py [ARGS]"
        )
    parser.add_argument('-o',help="Output file",default=None)
    parser.add_argument('-x',help="Output width",type=int,default=20)
    parser.add_argument('-y',help="Output height",type=int,default=20)
    parser.add_argument('-s',help="Seed value",type=int,default=time.time())
    return parser.parse_args()

#===== CONSTANTS =====#
CLOSED,N,E,S,W = 0,1,2,4,8

#===== SETUP =====#
def empty(x,y):
    return [[CLOSED for rx in range(x)] for ry in range(y)]

#===== BITFLAG ARITHMETIC =====#
def check(flagset,flag):
    return flagset & flag

def on(flagset,flag):
    return flagset | flag

def off(flagset,flag):
    return flagset & ~flag

#===== ALGORITHMS =====#

#=== Helpers ===#
def direction(flag):
    if(flag == N):
        return location(0,-1)
    elif(flag == E):
        return location(1,0)
    elif(flag == S):
        return location(0,1)
    elif(flag == W):
        return location(-1,0)

def opposite(flag):
    return S if flag == N else W if flag == E else N if flag == S else E if flag == W else None

def add(loc1,loc2,bounds):
    newX = loc1.x + loc2.x
    newY = loc1.y + loc2.y
    if(-1 < newX < bounds.x and -1 < newY < bounds.y):
        return location(newX,newY)

def addFlag(loc,flag,bounds):
    return add(loc,direction(flag),bounds)

#=== Recursive Backtracking ====#

def recursiveBacktrack(maze=None,x=20,y=20,start=location(0,0),father=True):
    if(maze is None):
        maze = empty(x,y)
    directions = [N,E,S,W]
    random.shuffle(directions)
    for direction in directions:
        new = addFlag(start,direction, location(len(maze[0]),len(maze)) )
        if(new is not None):
            if(maze[new.y][new.x] == CLOSED):
                maze[start.y][start.x] |= direction
                maze[new.y][new.x] |= opposite(direction)
                recursiveBacktrack(maze=maze,start=new,father=False)
    return maze

#===== OUTPUT =====#

def putMaze(maze):
    print('_' * len(maze[0])*2)
    for row in maze:
        print('|',end='')
        for tile in row:
            print(' ' if tile & S else '_',end='')
            print((' ' if tile & S else '_') if tile & E else '|',end='')
        print()
        
#===== MAIN FUNCTIONALITY =====#
if __name__ == "__main__":
    args = get_args()
    random.seed(args.s)
    maze = recursiveBacktrack(x=args.x,y=args.y)
    putMaze(maze)
