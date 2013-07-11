from GamePieces import Route, Camera, Neighbor, Cell
from Geometry import Vector, Locus

def _abs(num): return ((2 * (num > 0)) - 1) * num #quick and dirty absolute value function

class RouteGroup(object):
    def __init__(self, initType, typeString, numSides, levelNum, cells, container, colors):
        if numSides == 4:
            if initType == 'grid':
                self.getRoutesForGrid(typeString, levelNum, container, colors)
            elif initType == 'cube':
                self.getRoutesForCube(typeString, levelNum, container, colors)
                
        for route in self.routes:
            route.startCoords = route.pointCoords(cells.cells[route.startIndex].position, cells.cells[route.startIndex].normal.cross(cells.cells[route.startIndex].up), cells.cells[route.startIndex].up)
            route.endCoords = route.pointCoords(cells.cells[route.endIndex].position, cells.cells[route.endIndex].normal.cross(cells.cells[route.endIndex].up), cells.cells[route.endIndex].up)
    def getRoutesForGrid(self, typeString, levelNum):
        pass
    def getRoutesForCube(self, typeString, levelNum, c, co):
        if typeString == '3':
            file = open('levels.txt', 'r')
            data = ''
            for i in range(levelNum + 2):
                data = file.readline()
            file.close()
            data = eval(data)
            routes = data[0]
            self.routes = []
            for i in range(1, len(routes)+1):
                self.routes.append(Route(i,routes[i-1][0],routes[i-1][1],c, co))
                
    def getRoute(self, index):
        for route in self.routes:
            if route.routeIndex == index:
                return route
                break
        else:
            return 0
    def clip(self, dom, cells):
        dom = self.getRoute(_abs(dom))
        for step in dom.orderedSteps:
            intersect = cells.cells[step].containsRoutePoint(self.routes, dom.routeIndex)
            if intersect:
                self.getRoute(intersect).clip(step, 'before')
                
    def complete(self):
        for route in self.routes:
            if not (route.startIndex in route.orderedSteps and route.endIndex in route.orderedSteps):
                return False
                break
        else:
            return True
                    
    def add(self, cells, cellIndex, routeIndex, *options):
        needsRedraw = False
        route = self.getRoute(_abs(routeIndex))
        
        isNew = True
        if len(route.orderedSteps) > 0:
            if route.orderedSteps[len(route.orderedSteps)-1] == cellIndex:
                isNew = False
        
        if isNew or 'reset' in options:
            if 'reset' in options:
                needsRedraw = True
                route.redraw = True
                route.empty = False
                route.orderedSteps = [cellIndex]
                if routeIndex < 0:
                    route.startsAtEnd = True
                else:
                    route.startsAtEnd = False
            
            if route.orderedSteps == []:
                if routeIndex < 0:
                    route.startsAtEnd = True
                    route.orderedSteps.append(route.endIndex)
                    route.empty = False
                else:
                    route.startsAtEnd = False
                    route.orderedSteps.append(route.startIndex)
                    route.empty = False
                needsRedraw = True
            else:
                if cellIndex in route.orderedSteps[:len(route.orderedSteps) - 1]:
                    route.clip(cellIndex, 'before')
                    needsRedraw = [routeIndex]
                if cells.cells[route.orderedSteps[len(route.orderedSteps) - 1]].isNeighbor(cellIndex):
                    end = cells.cells[cellIndex].containsEndPoint(self.routes)
                    if end == 0 or _abs(end) == _abs(routeIndex):
                        if route.endIndex not in route.orderedSteps or route.startIndex not in route.orderedSteps:
                            route.orderedSteps.append(cellIndex)
                        if needsRedraw != [routeIndex]:
                            needsRedraw = True
                        intersect = cells.cells[cellIndex].containsRoutePoint(self.routes, _abs(routeIndex))
                        if intersect:
                            return self.getRoute(intersect)
        return needsRedraw  

class CellGroup(object):
    def __init__(self, initType, typeString, numSides, container):
        if numSides == 4:
            if initType == 'grid':
                self.getCellsForGrid(typeString, container)
            elif initType == 'cube':
                self.getCellsForCube(typeString, container)
                
    def getCellsForGrid(self, typeString, container):
        x = int(typeString)
        y = int(typeString)
        cells = {}
        index = 1
        
        for j in range(y):
            for i in range(x):
                posX = -x + (2 * i) + 1
                posY = -y + (2 * j) + 1
                
                ints = []
                loci = []
                if i != 0:
                    ints.append(index - 1)
                    loci.append(Locus(posX - 1, posY, x))
                if j != 0:
                    ints.append(index - x)
                    loci.append(Locus(posX, posY - 1, x))
                if i != (x - 1):
                    ints.append(index + 1)
                    loci.append(Locus(posX + 1, posY, x))
                if j != (y - 1):
                    ints.append(index + x)
                    loci.append(Locus(posX, posY + 1, x))
                    
                cells[index] = Cell(index, Locus(posX, posY, x), Vector(0, 0, 1), Vector(1, 0, 0), ints, loci, 4, container)
                index += 1
        self.cells = cells
        
    def percent(self, routes):
        total = len(self.cells)
        numFilled = 0
        for key in self.cells:
            if self.cells[key].containsRoutePoint(routes, 0) != 0:
                numFilled += 1
        return int((100 * float(numFilled) / float(total)))

    def getCellsForCube(self, typeString, container):
        x = int(typeString)
        cells = {}
        index = 1
        for k in range(6):
            if k == 0:
                normal = Vector(1, 0, 0)
                up = Vector(0, 0, 1)
            elif k == 1:
                normal = Vector(0, 1, 0)
                up = Vector(0, 0, 1)
            elif k == 2:
                normal = Vector(0, 0, 1)
                up = Vector(1, 0, 0)
            elif k == 3:
                normal = Vector(-1, 0, 0)
                up = Vector(0, 0, 1)
            elif k == 4:
                normal = Vector(0, -1, 0)
                up = Vector(0, 0, 1)
            elif k == 5:
                normal = Vector(0, 0, -1)
                up = Vector(1, 0, 0)
            right = normal.cross(up).unit()
            for j in range(x):
                for i in range(x):
                    position = Locus(0,0,0).translateByVector(normal.scalarMultiply(x)).translateByVector(up.scalarMultiply(x - 1 - (2 * j))).translateByVector(right.scalarMultiply(x - 1 - (2 * i)))
                    neighborJunctions = []
                    
                    neighborJunctions.append(position.translateByVector(right))
                    neighborJunctions.append(position.translateByVector(right.scalarMultiply(-1)))
                    neighborJunctions.append(position.translateByVector(up))
                    neighborJunctions.append(position.translateByVector(up.scalarMultiply(-1)))
                    
                    cells[index] = Cell(index, position, normal, up, [1,1,1,1], neighborJunctions, 4, container)
                    index += 1
                    
        self.cells = cells
        self.generateNeighbors()
    def generateNeighbors(self):
        for cell in [self.cells[i] for i in self.cells]:
            for neighbor in cell.neighbors:
                found = False
                for other in [self.cells[i] for i in self.cells]:
                    if not other.position.isEqual(cell.position):
                        for nother in other.neighbors:
                            if neighbor.junction.isEqual(nother.junction):
                                neighbor.index = other.index
                                found = True
                                break
                        if found:
                            break;
    def canvasPoints(self, camera, width, height):
        polylines = []
        for cell in [self.cells[i] for i in self.cells]:
                polylines.append((cell, cell.canvasCoords(camera, width, height)))
        return polylines