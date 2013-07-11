from Geometry import *
from math import pi, sin, cos

class Neighbor(object): #each Cell has a list of neighbor objects--these correspond to which cells can be neighbors on routes
    def __init__(self, index, junction): ###Possibility: eliminate this class and use a dict. with {index: junction}
        self.index = index #The index of the neighboring cell
        self.junction = junction #the point of junction that the route will follow from one cell to the other
        
class Route(object):
    """Routes are the paths that connect same-colored dots"""
    def __init__(self, routeIdx, startIdx, endIdx, container, colors):
        self.routeIndex = routeIdx #the RouteGroup getRoute() method uses this attribute to return a route
        self.startIndex = startIdx #the index of the cell that starts this route -- use RouteGroup.cells[index]
        self.endIndex = endIdx
        self.connected = False #used for keeping score, and for preventing further expansion after completion
        self.dragging = False #not currently used
        self.empty = True #not currently used
        self.orderedSteps = [] #list of cell indices that the route goes through
        self.startsAtEnd = False #determines the base of an active route. then we know which endpoint to test for for completion
        self.container = container #refers to the frame object used in the Stripes module. used for event binding
        self.getColor(self.routeIndex, colors) #color of endpoints. this function also sets bg color
        self.lines = {}
        
    def pointCoords(self, center, up, right):
        """Gets the coordinates of a pseudo-circular polygon that marcates the endpoint of a route"""
        numPoints = 12 #arbitrary. increase for more circular circles; decrease for faster rendering
        coords = []
        for i in range(numPoints):
            theta = 2.0 * pi * (float(i) / float(numPoints))
            coords.append(center.translateByVector(right.unit().scalarMultiply(cos(theta) * 0.5)).translateByVector(up.unit().scalarMultiply(sin(theta) * 0.5)))
        return coords
        
    def getLines(self, cells, indx, camera, width, height, options):
        if options == 'to':
            point1 = cells.cells[self.orderedSteps[indx]].position
            point2 = cells.cells[self.orderedSteps[indx]].getNeighbor(self.orderedSteps[indx+1]).junction
            normal = cells.cells[self.orderedSteps[indx]].normal
        elif options == 'from':
            point2 = cells.cells[self.orderedSteps[indx]].getNeighbor(self.orderedSteps[indx+1]).junction
            point1 = cells.cells[self.orderedSteps[indx+1]].position
            normal = cells.cells[self.orderedSteps[indx+1]].normal
        parallel = Vector(point1, point2).unit().scalarMultiply(0.25)
        side = parallel.cross(normal).unit().scalarMultiply(0.25)
        
        numPoints = 4
        coords = ()
        for i in range(numPoints):
            coords = coords + point1.translateByVector(side.scalarMultiply(cos((pi * i) / (numPoints - 1)))).translateByVector(parallel.scalarMultiply(sin((pi * i) / (1 - numPoints)))).flatten(camera, width, height)
        coords = coords + point2.translateByVector(side.scalarMultiply(-1)).flatten(camera, width, height) + point2.translateByVector(side).flatten(camera,width,height)
        
        return coords
        
    def clip(self, index, *options):
        """Shortens the orderedSteps of a given route to a given index"""
        i = 0
        for step in range(len(self.orderedSteps)):
            if self.orderedSteps[step] == index:
                i = step
                break
        if 'before' not in options: #'before' lets us clip down before an index, rather than on it
            i += 1
        if i < 1: i = 1
        self.redraw = True
        self.orderedSteps = self.orderedSteps[:i]
        
    def overlappedBy(self, other):
        return len([i for i in self.orderedSteps + other.orderedSteps if i in self.orderedSteps and i in other.orderedSteps]) > 0
        
    def startCellEntered(self, event, canvas):
        self.container.setIndex(self.startIndex)
    def endCellEntered(self, event):
        self.container.setIndex(self.endIndex)
       
    def getColor(self, index, colors):
        
        if index <= len(colors):
            color = colors[index-1]
        else:
            color = colors[len(colors)-1]
            
        blue = color % 0x100
        green = (color >> 8) % 0x100
        red = (color >> 16)
        
        dullColor = []
        brightColor = []
        regColor = []
        
        dullColor.append(round(red * 0.3))
        dullColor.append(round(green * 0.3))
        dullColor.append(round(blue * 0.3))
        
        regColor.append(red)
        regColor.append(green)
        regColor.append(blue)
        
        brightColor.append(min(0xff,round(red*0.6)))
        brightColor.append(min(0xff,round(green*0.6)))
        brightColor.append(min(0xff,round(blue*0.6)))
        
        def toString(nums):
            strs = []
            for num in nums:
                num = str(hex(int(num))[2:])
                while len(num) < 2:
                    num = '0' + num
                strs.append(num)
            return strs
            
        regColor = toString(regColor)
        dullColor = toString(dullColor)
        brightColor = toString(brightColor)
        
        self.dullColor = '#'
        for col in dullColor: self.dullColor += col
        self.lightColor = '#'
        for col in brightColor: self.lightColor += col
        self.color = '#'
        for col in regColor: self.color += col

class Cell(object):
    def __init__(self, index, position, normal, up, neighborIdxs, neighborJunctions, numSides, container):
        self.index = index
        self.position = position
        self.normal = normal
        self.up = up
        self.neighbors = []
        self.container = container
        
        for i, j in zip(neighborIdxs, neighborJunctions):
            self.neighbors.append(Neighbor(i, j))
        numSides = numSides
        
        self.corners = []
        if numSides == 4:
            v = normal.cross(up)
            self.corners.append(self.position.translateByVector(up.unit().addVector(v.unit())))
            self.corners.append(self.position.translateByVector(up.unit().scalarMultiply(-1).addVector(v.unit())))
            self.corners.append(self.position.translateByVector(up.unit().scalarMultiply(-1).addVector(v.unit().scalarMultiply(-1))))
            self.corners.append(self.position.translateByVector(up.unit().addVector(v.unit().scalarMultiply(-1))))
            self.corners.append(self.position.translateByVector(up.unit().addVector(v.unit())))
            
    def getNeighbor(self, index):
        for neighbor in self.neighbors:
            if neighbor.index == index:
                return neighbor
        
    def containsEndPoint(self, routes):
        index = 0
        for r in routes:
            if r.startIndex == self.index:
                index = r.routeIndex
                break
            elif r.endIndex == self.index:
                index = r.routeIndex * -1
                break;
        return index
    
    def containsRoutePoint(self, routes, excluding):
        index = 0
        found = False
        for r in routes:
            if not r.empty:
                for i in r.orderedSteps:
                    if self.index == i and r.routeIndex != excluding:
                        index = r.routeIndex
                        found = True
                        break
                if found:
                    break
        return index
        
    def canvasCoords(self, camera, width, height):
        if len(self.corners) == 5:
            points = (self.corners[0].flatten(camera, width, height), self.corners[1].flatten(camera,width,height), self.corners[2].flatten(camera,width,height), self.corners[3].flatten(camera,width,height))
            return (points[0][0], points[0][1], points[1][0], points[1][1], points[2][0], points[2][1], points[3][0], points[3][1])
            
    def isNeighbor(self, index):
        for neighbor in self.neighbors:
            if neighbor.index == index:
                return True
                break
        else:
            return False
            
    def containsPoint(self, x, y, camera, width, height):
        right = self.up.cross(self.normal).unit()
        cornerVector = right.addVector(self.up.unit())
        cornerVector2 = right.addVector(self.up.unit().scalarMultiply(-1))
        corners = []
        corners.append(Locus(self.position.translateByVector(cornerVector).flatten(camera, width, height) + tuple([0])))
        corners.append(Locus(self.position.translateByVector(cornerVector2.scalarMultiply(-1)).flatten(camera, width, height) + tuple([0])))
        corners.append(Locus(self.position.translateByVector(cornerVector.scalarMultiply(-1)).flatten(camera, width, height) + tuple([0])))
        corners.append(Locus(self.position.translateByVector(cornerVector2).flatten(camera, width, height) + tuple([0])))
        
        for i in range(len(corners) - 1):
            prev = i - 1
            if prev == -1:
                prev = len(corners) - 1
            cursor = Vector(x - corners[i].x, y - corners[i].y, 0)
            prevVect = Vector(corners[prev].x - corners[i].x, corners[prev].y - corners[i].y, 0)
            nextVect = Vector(corners[i+1].x - corners[i].x, corners[i+1].y - corners[i].y, 0)
            
            if prevVect.angleBetween(cursor) > prevVect.angleBetween(nextVect) or nextVect.angleBetween(cursor) > nextVect.angleBetween(prevVect):
                break
        else:
            return True
        return False

class Camera(object):
    def __init__(self, zoom, fieldOfVision):
        self.zoom = zoom
        self.fieldOfVision = fieldOfVision
        self.position = Locus(zoom, zoom / 3, zoom / 2)
        self.origin = Locus(0,0,0)
        self.position = self.position.vectorFrom(self.origin).unit().scalarMultiply(zoom).getLocus()
        self.view = self.position.vectorTo(self.origin).unit()
        self.up = Vector(0, 0, -1)
        self.up = self.up.subtractVector(self.up.project(self.view)).unit()
        self.xOff = 0
        self.yOff = 0
    def rotate(self, x, y):
        right = self.view.cross(self.up)
        self.position = self.position.translateByVector(self.up.scalarMultiply(self.zoom * 0.007 * y))
        self.view = self.position.vectorTo(self.origin)
        self.position = (self.origin.vectorTo(self.position).unit().scalarMultiply(self.zoom)).getLocus()
        self.up = right.cross(self.view).unit().scalarMultiply(self.up.magnitude())
        self.position = self.position.translateByVector(right.unit().scalarMultiply(self.up.magnitude() * self.zoom * 0.007 * x))
        self.position = (self.origin.vectorTo(self.position).unit().scalarMultiply(self.zoom)).getLocus()
        self.view = self.position.vectorTo(self.origin)
        self.up = right.cross(self.view).unit().scalarMultiply(self.up.magnitude())
    def resize(self, delta):
        self.zoom *= 1 + (delta * 0.02)
        self.position = (self.origin.vectorTo(self.position).unit().scalarMultiply(self.zoom)).getLocus()
        self.view = self.position.vectorTo(self.origin)
