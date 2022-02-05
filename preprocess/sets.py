# Python3 program to implement Disjoint Set Data
# Structure.

import numpy as np 
from typing import List

class Point:
    MAX_PIXEL = 548

    def __init__(self, y, x, white):
        self.x = x
        self.y = y
        self.white = white

    def getPoint(self):
        return [self.y, self.x]

    def getRight(self):
        if self.x + 1 <= Point.MAX_PIXEL:
            return [self.y, self.x + 1]
        return None

    def getLeft(self):
        if self.x - 1 >= 0:
            return [self.y, self.x - 1]
        return None
    
    def getDown(self):
        if self.y + 1 <= Point.MAX_PIXEL:
            return [self.y + 1, self.x] 
        return None

    def getUp(self):
        if self.y - 1 >= 0:
            return [self.y - 1, self.x]
        return None

    def getNeighborhood(self) -> List[int]:
        neighborhood = list()
        if self.getDown():
            neighborhood.append(self.getDown())
        if self.getLeft():
            neighborhood.append(self.getLeft())
        if self.getRight():
            neighborhood.append(self.getRight())
        if self.getUp():
            neighborhood.append(self.getUp())
        return neighborhood

class DisjSet:
    def __init__(self, parent: List[Point]):
        # Constructor to create and
        # initialize sets of n items
        self.rank = [1] * len(parent)
        self.parent = parent
  
    # Finds set of given item x
    def find(self, x):
          
        # Finds the representative of the set
        # that x is an element of
        if (self.parent[x] != x):
              
            # if x is not the parent of itself
            # Then x is not the representative of
            # its set,
            self.parent[x] = self.find(self.parent[x])
              
            # so we recursively call Find on its parent
            # and move i's node directly under the
            # representative of this set
  
        return self.parent[x]
  
    # Do union of two sets represented
    # by x and y.
    def union(self, x, y):
          
        # Find current sets of x and y
        xset = self.find(x)
        yset = self.find(y)
  
        # If they are already in same set
        if xset == yset:
            return
  
        # Put smaller ranked item under
        # bigger ranked item if ranks are
        # different
        if self.rank[xset] < self.rank[yset]:
            self.parent[xset] = yset
  
        elif self.rank[xset] > self.rank[yset]:
            self.parent[yset] = xset
  
        # If ranks are same, then move y under
        # x (doesn't matter which one goes where)
        # and increment rank of x's tree
        else:
            self.parent[yset] = xset
            self.rank[xset] = self.rank[xset] + 1
  
    def isReachable(self, x, y):
        return self.find(x) == self.find(y)

    def getPoint(self, x, y) -> Point:
        for point in self.parent: 
            if point.x == x and point.y == y:
                return point

    def preprocessMaze(self, maze: np.array):
        for i in range(maze.shape[0]):
            for j in range(maze.shape[1]):
                cell: Point = self.getPoint(i, j)
                if cell.white != 0:
                    for neigh in cell.getNeighborhood():
                        point = self.getPoint(neigh[0], neigh[1])
                        if point.white != 0:
                            self.union(cell, point)




if __name__ == "__main__":
    # Driver code
    obj = DisjSet(5)
    obj.union(0, 2)
    obj.union(4, 2)
    obj.union(3, 1)
    if obj.find(4) == obj.find(0):
        print('Yes')
    else:
        print('No')
    if obj.find(1) == obj.find(0):
        print('Yes')
    else:
        print('No')
    
    # This code is contributed by ng24_7.