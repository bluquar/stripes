import math
from math import pi

class Vector:
    'Vectors have x, y, and z components. theta, phi and magnitude can be accessed via methods.'
    def __init__(self, *args):
        if len(args) == 3: #if we pass in three components
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]
        elif len(args) == 2: #if we pass in a tip locus and tail locus
            self.x = args[1].x - args[0].x
            self.y = args[1].y - args[0].y
            self.z = args[1].z - args[0].z       
    def hasComponents(self):
        return hasattr(self, 'x') and hasattr(self, 'y') and hasattr(self, 'z')
        
    def hasNonZeroComponents(self):
        if self.hasComponents():
            return self.x != 0 or self.y != 0 or self.z != 0
        else:
            return False
        
    def infoString(self): #for debugging. we can display components and magnitude in the console
        if self.hasComponents():
            return '<' + str(self.x) + ',' + str(self.y) + ',' + str(self.z) + '> Magnitude = ' + str(self.magnitude())    
        else:
            return 'missing component!'                
        
    def magnitude(self):
        'returns the magnitude of a vector'
        if self.hasComponents(): #make sure we aren't trying to access things that aren't there
            return (self.x**2 + self.y**2 + self.z**2)**0.5 #safe because any num. squared is > 0, so the sum will be non-negative
        else:
            return 0;
            
    def addVector(self, other):
        'returns the sum of self and other'
        if self.hasComponents() and other.hasComponents():
            return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            return Vector(0, 0, 0)
            
    def subtractVector(self, other):
        'returns the sum of self and negative other'
        return self.addVector(other.scalarMultiply(-1)) #safeties are not needed because they are already included in addvector
            
    def scalarMultiply(self, factor):
        if self.hasComponents():
            return Vector(self.x * factor, self.y * factor, self.z * factor)
        else:
            return Vector(0, 0, 0)
        
    def dot(self, other):
        'returns the dot product of this vector and another vector which must be passed in'
        if other.hasComponents() and self.hasComponents(): #make sure all necessary attributes exist
            return self.x * other.x + self.y * other.y + self.z * other.z
        else:
            return 0;
        
    def cross(self, other):
        'returns the cross product of SELF crossed with OTHER (in that order)'
        if other.hasComponents() and self.hasComponents(): #make sure all necessary attributes exist
            return Vector(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z, self.x * other.y - self.y * other.x)
        else:
            return Vector(0, 0, 0)
            
    def unit(self):
        'returns a vector with the same direction as self, but with magnitude 1'
        if self.hasNonZeroComponents():
            mag = self.magnitude()
            return Vector(self.x / mag, self.y / mag, self.z / mag)
        else:
            return Vector(0, 0, 0)
            
    def project(self, other):
        'returns the component of the SELF vector that is in the direction of the OTHER vector'
        if self.hasComponents() and other.hasNonZeroComponents():
            #the scale factor is
            scaleFactor = self.dot(other) / (other.x**2 + other.y**2 + other.z**2) #this is the two vectors dotted together, divided by the magnitude of other SQUARED (x^2 + y^2 + z^2 is equivalent to its square root squared). this takes the dot of self and other's unit, then adjusts for unitizing other once more since we are about to scalar multiply by it:
            return other.scalarMultiply(scaleFactor)
        else:
            return Vector(0, 0, 0)
            
    def isEqual(self, other):
        'returns true if the two vectors have identical components, and false otherwise'
        if self.hasComponents() and other.hasComponents():
            if self.x == other.x and self.y == other.y and self.z == other.z:
                return True
        return False
        
    def isNegation(self, other):
        'returns true if the two vectors added together are zero. i.e., they are antiparallel and equimagnitude'
        if self.hasComponents() and other.hasComponents():
            if self.scalarMultiply(-1).isEqual(other):
                return True
        return False
            
    def isParallel(self, other):
        'returns true if the vectors are parallel, and false otherwise'
        if self.hasComponents() and other.hasComponents():
            if self.unit().isEqual(other) or self.unit().isNegation(other):
                return True
        return False
        
    def isPerpendicular(self, other):
        'returns true if the vectors are orthogonal, and false otherwise'
        if self.hasComponents() and other.hasComponents():
            if self.dot(other) == 0:
                return True
        return False
        
    def angleBetween(self, other):
        'returns the angle between the two vectors.'
        if self.hasNonZeroComponents() and other.hasNonZeroComponents():
            return math.acos(self.dot(other) / (self.magnitude() * other.magnitude()))
            
    def getLocus(self, *args):
        return Locus(self.x, self.y, self.z)

class Locus:
    'a locus is a point in |R**3'
    def __init__(self, *args):
            if len(args) == 3:
                self.x = args[0]
                self.y = args[1]
                self.z = args[2]
            elif len(args) == 1:
                self.x = args[0][0]
                self.y = args[0][1]
                self.z = args[0][2]
    
    def hasCoordinates(self):
        return hasattr(self, 'x') and hasattr(self, 'y') and hasattr(self, 'z')
        
    def infoString(self):
        return '(' + str(self.x) + ',' + str(self.y) + ',' + str(self.z) + ')'
        
    def distanceFromOrigin(self):
        if self.hasCoordinates():
            return (self.x**2 + self.y**2 + self.z**2)**0.5
        else:
            return 0
            
    def distance(self, other):
        if self.hasCoordinates() and other.hasCoordinates():
            return ((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)**0.5
        else:
            return 0
            
    def vectorTo(self, other):
        'returns a vector with self as the tail and other as the tip'
        if self.hasCoordinates() and other.hasCoordinates():
            return Vector(self, other)
        else:
            return Vector(0, 0, 0)
            
    def vectorFrom(self, other):
        'returns a vector with other as the tail and self as the tip'
        if self.hasCoordinates() and other.hasCoordinates():
            return Vector(other, self)
        else:
            return Vector(0, 0, 0)
            
    def vectorFromOrigin(self):
        'returns the position vector for this locus'
        if self.hasCoordinates():
            return Vector(self.x, self.y, self.z)
        else:
            return Vector(0, 0, 0)
            
    def translateByVector(self, vector):
        if self.hasCoordinates() and vector.hasComponents():
            return Locus(self.x + vector.x, self.y + vector.y, self.z + vector.z)
        else:
            return Locus(0, 0, 0)
            
    def isEqual(self, other):
        if self.hasCoordinates() and other.hasCoordinates():
            if self.x == other.x and self.y == other.y and self.z == other.z:
                return True
        return False
        
    def flatten(self, camera, width, height):
#        print 'view = ' + camera.view.infoString()
#        print 'up = ' + camera.up.infoString()
#        print 'field of vision = %d' % (camera.fieldOfVision)
        cameraView = camera.view
        cameraUp = camera.up
        fieldOfVision = camera.fieldOfVision
        cameraLocus = camera.position
        
        rightVector = cameraUp.cross(cameraView)
        displacement = cameraLocus.vectorTo(self)
        horizontalVector = displacement.subtractVector(displacement.project(cameraUp))
        verticalVector = displacement.subtractVector(displacement.project(rightVector))
        forwardHoriz = horizontalVector.project(cameraView)
        rightEdge = forwardHoriz.addVector(rightVector.unit().scalarMultiply(horizontalVector.magnitude() * math.tan(fieldOfVision)))
        rightComp = rightEdge.subtractVector(forwardHoriz)
        horizComp = horizontalVector.subtractVector(forwardHoriz)
        isNegative = False
        if rightComp.dot(horizComp) < 0:
            isNegative = True
        ratio = horizComp.magnitude() / rightComp.magnitude()
        if isNegative:
            ratio *= -1
        length = min(width, height)
        xMid = width / 2;
        x = xMid + (ratio * length)
        
        forwardVertical = verticalVector.project(cameraView)
        topEdge = forwardVertical.addVector(cameraUp.unit().scalarMultiply(verticalVector.magnitude() * math.tan(fieldOfVision)))
        topComp = topEdge.subtractVector(forwardVertical);
        verticComp = verticalVector.subtractVector(forwardVertical);
        isNegative = False;
        if topComp.dot(verticComp) < 0:
            isNegative = True
        ratio = verticComp.magnitude() / topComp.magnitude();
        if isNegative:
            ratio *= -1

        yMid = height / 2
        y = yMid + (ratio * length)
        
#        print '(%d,%d)' % (x, y)

        return (x + camera.xOff, y + camera.yOff)
            
class Line:
    'a line has a locus (arbitrary) and a vector slope'
    def __init__(self, origin, slope):
        self.origin = origin
        self.slope = slope
    
    def initializeByTwoPoints(self, point1, point2):
        self.origin = point1
        if point1.isEqual(point2):
            print('!!attempted line initialization with identical anchor-points')
            self.slope = Vector(1, 1, 1)
        else:
            self.slope = point1.vectorTo(point2)
            
    def hasAttributes(self):
        if hasattr(self, 'origin') and hasattr(self, 'slope'):
            if isinstance(self.slope, Vector) and isinstance(self.origin, Locus):
                if self.slope.hasNonZeroComponents() and self.origin.hasCoordinates():
                    return True
        return False
        
    def infoString(self):
        if self.hasAttributes():
            return self.origin.infoString() + ' ' + self.slope.infoString()
        else:
            return 'invalid line'
        
    def distanceToPoint(self, point):
        if self.hasAttributes():
            return self.vectorToPoint(point).magnitude()
        else:
            print('Invalid line!')
            return 0
            
    def vectorToPoint(self, point):
        if self.hasAttributes() and point.hasCoordinates():
            return self.origin.vectorTo(point).subtractVector(self.origin.vectorTo(point).project(self.slope))
        else:
            print('Invalid line or point!')
            return Vector(0, 0, 0)          