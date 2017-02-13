import random, time


class MazeNode:  # just a dumb data class to wrap some attributes
    def __init__(self, north=True, east=True, south=True, west=True):
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.unused = True  # this value is used for most algorithms
        self.moreData = None  # this is more data for more algorithm fun (mainly wilson's algorithm though)


class MazeCompiler:
    def __init__(self, x = 100, y = 100):
        self.setUpMaze(x, y)

    def setUpMaze(self, x, y):
        self.board = []
        for i in range(y):
            self.board.append([])
            for j in range(x):
                self.board[i].append(MazeNode())

    def compileMaze(self):
        returnMaze = []
        for y in self.board:  # sets up empty board
            returnMaze.append([1] * len(y) * 3)
            returnMaze.append([1] * len(y) * 3)
            returnMaze.append([1] * len(y) * 3)
        for ykey, y in enumerate(self.board):
            for xkey, x in enumerate(y):
                returnMaze[ykey * 3][xkey * 3 + 2] = 0
                returnMaze[ykey * 3][xkey * 3] = 0
                returnMaze[ykey * 3 + 2][xkey * 3] = 0
                returnMaze[ykey * 3 + 2][xkey * 3 + 2] = 0
                if (x.north):
                    returnMaze[ykey * 3][xkey * 3 + 1] = 0
                if (x.east):
                    returnMaze[ykey * 3 + 1][xkey * 3 + 2] = 0
                if (x.south):
                    returnMaze[ykey * 3 + 2][xkey * 3 + 1] = 0
                if (x.west):
                    returnMaze[ykey * 3 + 1][xkey * 3] = 0
        return (returnMaze)

    def open(self, node, side):
        x, y = node
        if (side == 0):
            self.board[y][x].north = False
        if (side == 1):
            self.board[y][x].east = False
        if (side == 2):
            self.board[y][x].south = False
        if (side == 3):
            self.board[y][x].west = False

    def connectCells(self, node1, node2):
        x1, y1 = node1
        x2, y2 = node2
        if (abs(x1 - x2) == 1):
            if (x1 > x2):
                self.open((x1, y1), 3)
                self.open((x2, y2), 1)
            else:
                self.open((x1, y1), 1)
                self.open((x2, y2), 3)
        elif (abs(y1 - y2) == 1):
            if (y1 > y2):
                self.open((x1, y1), 0)
                self.open((x2, y2), 2)
            else:
                self.open((x1, y1), 2)
                self.open((x2, y2), 0)
        else:
            raise IOError

    def listOpenNeighbors(self, node):
        x, y = node
        rLst = []
        if (len(self.board[0]) - 1 > x):
            if (self.board[y][x + 1].unused):
                rLst.append((x + 1, y))
        if (x > 0):
            if (self.board[y][x - 1].unused):
                rLst.append((x - 1, y))
        if ((len(self.board) - 1 > y)):
            if (self.board[y + 1][x].unused):
                rLst.append((x, y + 1))
        if (y > 0):
            if (self.board[y - 1][x].unused):
                rLst.append((x, y - 1))
        return (rLst)


def printMaze(maze):
    for line in maze:
        print(' '.join([str(i) for i in line]))


def saveMaze(filename, maze):
    with open(filename, 'w') as file:
        for line in maze:
            file.write(''.join([str(i) for i in line]))
            file.write('\n')


def recursiveBacktracker(size):
    maze = MazeCompiler(size, size)
    path = []
    done = False
    cursor = (0, 0)
    while (not done):
        if (maze.board[cursor[1]][cursor[0]].unused):
            maze.board[cursor[1]][cursor[0]].unused = False
            path.append(cursor)
        choices = maze.listOpenNeighbors(cursor)
        if (choices != []):
            newCursor = random.choice(choices)
            maze.connectCells(newCursor, cursor)
            cursor = newCursor
        elif (path == []):
            done = True
        else:
            path.pop(-1)
            if (path != []):
                cursor = path[-1]
    return (maze.compileMaze())


def checkABDone(maze):
    formattedMaze = [j for i in maze for j in i]
    for i in formattedMaze:
        if (i.unused):
            return (False)
    else:
        return (True)


def alodusBroder(size):
    maze = MazeCompiler(size, size)
    done = False
    cursor = (0, 0)
    while (not done):
        maze.board[cursor[1]][cursor[0]].unused = False
        choices = maze.listOpenNeighbors(cursor)
        noChoice = True
        while (noChoice):
            choice = random.randint(0, 3)
            if ((choice == 0 and cursor[1] != 0) or (choice == 3 and cursor[0] != 0) or (
                    choice == 2 and cursor[1] < len(maze.board) - 1) or (
                    choice == 1 and cursor[0] < len(maze.board[1]) - 1)):  # sanity check
                noChoice = False
        if (choice == 0):
            newCursor = (cursor[0], cursor[1] - 1)
        elif (choice == 1):
            newCursor = (cursor[0] + 1, cursor[1])
        elif (choice == 2):
            newCursor = (cursor[0], cursor[1] + 1)
        elif (choice == 3):
            newCursor = (cursor[0] - 1, cursor[1])
        if (maze.board[newCursor[1]][newCursor[0]].unused):
            maze.connectCells(newCursor, cursor)
        cursor = newCursor
        done = checkABDone(maze.board)
    return (maze.compileMaze())


maze = recursiveBacktracker(int(input('Maze size:\n')))
printMaze(maze)
saveMaze(input('Filename to save to:\n'), maze)
