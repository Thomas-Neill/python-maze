#!/usr/bin/env python3
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

#===== ALGORITHMS =====#

#=== Helpers ===#

delta = {N:location(0,-1),E:location(1,0),S:location(0,1),W:location(-1,0)}

opposite = {N:S,S:N,E:W,W:E}

def add(loc1,loc2,bounds):
    newX = loc1.x + loc2.x
    newY = loc1.y + loc2.y
    if(-1 < newX < bounds.x and -1 < newY < bounds.y):
        return location(newX,newY)

def addFlag(loc,flag,bounds):
    return add(loc,delta[flag],bounds)

def setSet(flags,setNo):
    return (flags & 15) | (setNo << 4)

def getSet(flags):
    return (flags & ~15) >> 4

#=== Recursive Backtracking ===#

def recursiveBacktrack(x=20,y=20,maze=None,start=location(0,0)):
    if(maze is None):
        maze = empty(x,y)
    directions = [N,E,S,W]
    random.shuffle(directions)
    for direction in directions:
        new = addFlag(start,direction, location(len(maze[0]),len(maze)))
        if(new is not None):
            if(maze[new.y][new.x] == CLOSED):
                maze[start.y][start.x] |= direction
                maze[new.y][new.x] |= opposite[direction]
                recursiveBacktrack(maze=maze,start=new)
    return maze

#=== Eller's Algorithm ===#

def setInds(row):
    ret = {}
    for ind,item in enumerate(row):
        try:
            ret[getSet(item)].append(ind)
        except KeyError:
            ret[getSet(item)] = [ind]
    return list(ret.values())
        
def ellerStep(previous,rowLen,last_alloc,joinBias,last=False):
    ret = [CLOSED] * rowLen
    for x in range(rowLen): #we connect to the upper cells and initialize sets
        if(previous[x] & S):
            ret[x] |= N
            ret[x] = setSet(ret[x],getSet(previous[x]))
        else:
            last_alloc += 1
            ret[x] = setSet(ret[x],last_alloc)
            
    for x in range(rowLen-1): #now we may or may not join adjacent cells of different sets
        if(getSet(ret[x+1]) != getSet(ret[x])):
            if(random.random() < joinBias or last):
                ret[x] |= E
                ret[x+1] |= W
                ret[x+1] = setSet(ret[x+1],getSet(ret[x]))

    if(last):
        return ret
    
    sets = setInds(ret)
    for group in sets:
        amount = random.randint(0,len(group)-1) + 1
        already = [-1]
        for r in range(amount):
            index = -1
            while(index in already):
                index = random.choice(group)
            already.append(index)
            ret[index] |= S

    return last_alloc,ret
  
def runEllers(x,y=None,joinBias=0.5):
    last_alloc,first = ellerStep([CLOSED]*x,x,0,joinBias)
    ret = [first]
    if(y):
        for i in range(y-2):
            last_alloc,new = ellerStep(ret[i],x,last_alloc,joinBias)
            ret.append(new)
        ret.append(ellerStep(ret[-1],x,last_alloc,joinBias,True))
        return ret
    else: #infinite loop
        print('_'*(1+x*2))
        try:
            while(True):
                last_alloc,first = ellerStep(first,x,last_alloc,joinBias)
                printRow(first)
        except:
            print('\r',end='')
            printRow(first)
            last = ellerStep(first,x,last_alloc,joinBias,True)
            printRow(last)
            
#=== Kruskal's Algorithm ===#
Edge = namedtuple("Edge",['fst','snd'])

def genEdges(x,y):
    ret = []
    for iX in range(x-1):
        for iY in range(y):
            ret.append(Edge(location(iX,iY),location(iX+1,iY)))
    for iY in range(y-1):
        for iX in range(x):
            ret.append(Edge(location(iX,iY),location(iX,iY+1)))
    return ret

def joinSets(maze,target,changee):
    for y,row in enumerate(maze):
        for x,cell in enumerate(row):
            if(getSet(cell) == changee):
                maze[y][x] = setSet(maze[y][x],target)
                
def kruskalAlg(x,y):
    maze = empty(x,y)
    counter = 0
    for iX in range(x):
        for iY in range(y):
            maze[iY][iX] = setSet(CLOSED,counter)
            counter += 1
    edges = genEdges(x,y)
    while(edges):
        current = edges.pop(random.randint(0,len(edges)-1))
        fst,snd = current
        if(getSet(maze[fst.y][fst.x]) != getSet(maze[snd.y][snd.x])):
            if(snd.y > fst.y): #we carve downwards
                maze[fst.y][fst.x] |= S
                maze[snd.y][snd.x] |= N
            else:
                maze[fst.y][fst.x] |= E
                maze[snd.y][snd.x] |= W
            joinSets(maze,getSet(maze[fst.y][fst.x]),getSet(maze[snd.y][snd.x]))
    return maze
            
#=== Prim's Algorithm ===#

CLOSED,FRONTIER,OPEN = range(3)

def getFrontier(maze):
    ret = []
    for y,row in enumerate(maze):
        for x,cell in enumerate(row):
            if(getSet(cell) == FRONTIER):
                ret.append(location(x,y))
    return ret

def openFrontier(maze,location,size):
    maze[location.y][location.x] = setSet(maze[location.y][location.x],OPEN)
    for direction in [N,E,S,W]:
        test = add(delta[direction],location,size)
        if(test):
            if(getSet(maze[test.y][test.x]) == CLOSED):
                maze[test.y][test.x] = setSet(maze[test.y][test.x],FRONTIER)
    
def primsAlg(x,y):
    maze = empty(x,y)
    dims = location(x,y)
    openFrontier(maze,location(random.randint(0,x-1),random.randint(0,y-1)),dims)
    while(getFrontier(maze)):
        target = random.choice(getFrontier(maze))
        openFrontier(maze,target,dims)
        directions = [N,E,S,W]
        random.shuffle(directions)
        for direction in directions:
            new = add(target,delta[direction],dims)
            if(new):
                if(getSet(maze[new.y][new.x]) == OPEN):
                    maze[target.y][target.x] |= direction
                    maze[new.y][new.x] |= opposite[direction]
                    break
    return maze
    
#===== OUTPUT =====#

def printRow(row):
    print('|',end='')
    for tile in row:
        print(' ' if tile & S else '_',end='')
        print((' ' if tile & S else '_') if tile & E else '|',end='')
    print()
    
def putMaze(maze):
    print('_' * (1+len(maze[0])*2))
    for row in maze:
        printRow(row)
        
#===== MAIN FUNCTIONALITY =====#
if(__name__ == "__main__"):
    args = get_args()
    random.seed(args.s)
    putMaze(primsAlg(args.x,args.y))
