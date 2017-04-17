import math

#===== Utility Functions =====#
def dist(l1,l2):
    return math.sqrt( (l1[0]-l2[0])**2 + (l1[1]-l2[1])**2 )

def add(l,m):
    return (l[0]+m[0],l[1]+m[1])

def evaluate(node,target):
    return(node.dist + dist(node.location,target))

#===== Classes =====#
class Node:
    NEITHER,OPEN,CLOSED = range(3)
    neighbors = ( (1,0),(0,1),(-1,0),(0,-1) )
    def __init__(self,*args):
        if(len(args) == 1): #tuple init
            self.location = args[0]
            self.x,self.y = args[0]
        elif(len(args) == 2): #'literal' init
            self.location = args
            self.x,self.y = args
        self.dist = math.inf
        self.state = NEITHER
        
    def distanceTo(self,node):
        return(dist(self.location,node.location))
    
    def __str__(self):
        return('Location {}'.format(self.location))
    
    def __repr__(self):
        return('Node({})'.format(self.location))
    
    
class NodeContainer:
    def __init__(self,nodeLst):
        self._nodes = nodeLst
        
    def _searchLocation(self,location):
        for node in self._nodes:
            if(node.location == location):
                return(node)
        return(None)

    def at(self,*args): #objects are passed by reference in Python
        if(len(args) == 1):
            return(self._searchLocation(*args))
        elif(len(args) == 2):
            return(self._searchLocation(args))
        
    def size(self):
        x,y = 0,0
        for node in self._nodes:
            if(node.x > x): x = node.x
            if(node.y > y): y = node.y
        return((x,y))

    def allOpen(self):
        final = []
        for node in self._nodes:
            if(node.state == OPEN):
                final.append(node)
        return(final)

    def best(self,target):
        openNodes = self.allOpen()
        greatest = openNodes[0]
        for node in openNodes:
            if(evaluate(node,target) > evaluate(greatest,target)):
                greatest = node
        return(greatest.location)

    def neighbors(self,location):
        node = self.at(location)
        final = []
        for direction in node.neighbors:
            test = add(location,direction)
            if(self.at(test) is not None):
                final.append(self.at(test).location)
        return(final)

#===== Conversion =====#    
def nodes(maze): #True = open, false = closed
    final = []
    for y,row in enumerate(maze):
        for x,value in enumerate(row):
            if(value):
                final.append(Node(x,y))
    return(NodeContainer(final))

def maze(nodes):
    final = []
    size = nodes.size()
    for y in range(size[1] + 1):
        final.append([])
        for x in range(size[0] + 1):
            final[y].append(int(bool(nodes.at(x,y))))
    return(final)

#===== Solver ====="
def solve(start,end,nodes):
    nodes.at(start).dist = 0
    nodes.at(start).state = OPEN
    nodes.at(start).parent = None
    while(nodes.allOpen() != []):
        current = nodes.best(end)
        if(current == end):
            final = [] 
            while(True):
                final.append(current)
                if(current == start):
                    return(list(reversed(final)))
                current = nodes.at(current).parent

        nodes.at(current).state = CLOSED #closes current node

        for neighbor in nodes.neighbors(current):
            if(nodes.at(neighbor).state == CLOSED):
                continue

            if(nodes.at(neighbor).state == NEITHER):
                nodes.at(neighbor).state = OPEN
                
            if(nodes.at(current).dist + 1 < nodes.at(neighbor).dist):
                nodes.at(neighbor).dist = nodes.at(current).dist + 1
            else:
                continue

            nodes.at(neighbor).parent = current
