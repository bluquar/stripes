from GamePieces import *

def drawCells(container):
    camera = container.camera
    cells = container.cells
    width = container.width
    height = container.height
    canvas = container.canvas
    for seg in cells.canvasPoints(camera, width, height):
        if not hasattr(seg[0], 'polygonId'):
            seg[0].polygonId = canvas.create_polygon(seg[1], width=2, outline='white', activefill='#333333', tags=str(seg[0].index))
        else:
            canvas.coords(seg[0].polygonId, seg[1])
        if seg[0].normal.dot(container.camera.view) < 0:
            canvas.itemconfig(seg[0].polygonId, state='normal')
            if hasattr(seg[0], 'textt'):
                if hasattr(seg[0], 'texts') and seg[0].texts == True:
                    canvas.coords(seg[0].textt, seg[0].position.flatten(camera, width, height))
                    canvas.itemconfig(seg[0].textt, state='normal')
            else:
                seg[0].textt = canvas.create_text(seg[0].position.flatten(camera, width, height), text=str(seg[0].index), fill='white')
        else:
            canvas.itemconfig(seg[0].polygonId, state='hidden')
            if hasattr(seg[0], 'textt'):
                canvas.itemconfig(seg[0].textt, state='hidden')
        if hasattr(seg[0], 'textt') and hasattr(seg[0], 'texts') and seg[0].texts == False:
            canvas.itemconfigure(seg[0].textt, state='hidden')
                
def drawRoutes(container):
    width = container.width
    height = container.height
    routes = container.routes
    camera = container.camera
    canvas = container.canvas
    cells = container.cells.cells
    
    for route in routes.routes:                
        coords = ()
        for point in route.startCoords:
            coords += point.flatten(camera, width, height)
        if hasattr(route, 'startPolygonId'):
            canvas.coords(route.startPolygonId, coords)
            canvas.tag_raise(route.startPolygonId)
        else:
            route.startPolygonId = canvas.create_polygon(coords, fill=route.color, outline=route.color, state='disabled')
        if cells[route.startIndex].normal.dot(camera.view) < 0:
            canvas.itemconfig(route.startPolygonId, state='disabled')
        else:
            canvas.itemconfig(route.startPolygonId, state='hidden')
            
        if len(route.orderedSteps) > 0:
            if hasattr(route, 'redraw') and hasattr(route, 'lines'):
                print 'redrawing route %d' % (route.routeIndex)
                for line in route.lines:
                    canvas.delete(route.lines[line])
                route.lines = {}
                del route.redraw
                
            for i in range(len(route.orderedSteps) - 1):
                coordsTo = route.getLines(container.cells, i, camera, width, height, 'to')
                coordsFrom = route.getLines(container.cells, i, camera, width, height, 'from')
                if cells[route.orderedSteps[i]] in route.lines:
                    canvas.coords(route.lines[cells[route.orderedSteps[i]]], coordsTo)
                else:
                    route.lines[cells[route.orderedSteps[i]]] = canvas.create_polygon(coordsTo, fill=route.color, state='disabled')
                if cells[route.orderedSteps[i]].getNeighbor(route.orderedSteps[i+1]) in route.lines:
                    canvas.coords(route.lines[cells[route.orderedSteps[i]].getNeighbor(route.orderedSteps[i+1])], coordsFrom)
                else:
                    route.lines[cells[route.orderedSteps[i]].getNeighbor(route.orderedSteps[i+1])] = canvas.create_polygon(coordsFrom, fill=route.color, state='disabled')
                
                if cells[route.orderedSteps[i]].normal.dot(camera.view) < 0 and not hasattr(route, 'hidden'):
                    canvas.itemconfig(route.lines[cells[route.orderedSteps[i]]], state='disabled')
                else:
                    canvas.itemconfig(route.lines[cells[route.orderedSteps[i]]], state='hidden')
                if cells[route.orderedSteps[i+1]].normal.dot(camera.view) < 0 and not hasattr(route, 'hidden'):
                    canvas.itemconfig(route.lines[cells[route.orderedSteps[i]].getNeighbor(route.orderedSteps[i+1])], state='disabled')
                else:
                    canvas.itemconfig(route.lines[cells[route.orderedSteps[i]].getNeighbor(route.orderedSteps[i+1])], state='hidden')
        
        coords = ()
        for point in route.endCoords:
            coords += point.flatten(camera, width, height)
        if hasattr(route, 'endPolygonId'):
            canvas.coords(route.endPolygonId, coords)
            canvas.tag_raise(route.endPolygonId)
            canvas.tag_raise(route.startPolygonId)
        else:
            route.endPolygonId = canvas.create_polygon(coords, fill=route.color, outline=route.color, state='disabled')
        if cells[route.endIndex].normal.dot(camera.view) < 0:
            canvas.itemconfig(route.endPolygonId, state='disabled')
        else:
            canvas.itemconfig(route.endPolygonId, state='hidden')
        


def showLevelSelection(container, initializeLevel, numLevels):
    canvas = container.canvas
    canvas.delete('all')
    canvas.config(bg='black')
    width = container.width
    height = container.height
      
    def menuCoord(num, type):
        w = width / 4
        h = height / numLevels
        if h > 50: h = 50
        up = 10
        left = 10
        if type == 'button':
            return (left, up + num * h, left + w, up + num * h, left + w, (num + 1) * h, left, (num + 1) * h)
        elif type == 'text':
            return (left + w / 2, up + num * h + (h / 2))
        elif type == 'check1':
            return (left + w * 1.3 - 7, up + h * num + (h/2) - 8, left + w * 1.3, up + h * num + (h/2))
        elif type == 'check2':
            return (left + w * 1.3 + 5, up + h * num + (h/2) - 16, left + w * 1.3, up + h * num + (h/2))
        elif type == 'percent':
            return (left + w * 1.3 + 25, up + h * num + (h / 2))        
            
    class Level(object):
        def __init__(self, num, complete, percent):
            self.num = num
            button = canvas.create_polygon(menuCoord(num-1, 'button'), fill='#337733', outline='white', activefill='#229922', activewidth=3)
            canvas.tag_bind(button, '<Button-1>', self.go)
            text = canvas.create_text(menuCoord(num-1, 'text'), state='disabled', text='Level '+str(num))
            if complete:
                canvas.create_line(menuCoord(num-1, 'check1'), fill='#229922', width=5, capstyle='round')
                canvas.create_line(menuCoord(num-1, 'check2'), fill='#229922', width=5, capstyle='round')
            text = canvas.create_text(menuCoord(num-1, 'percent'), text = str(percent) + '%', fill='#888888')
        def go(self, event):
            initializeLevel(self.num)
            
    file = open('levels.txt', 'r')
    file.seek(0)
    for i in range(2):
        file.readline()
    for i in range(numLevels):
        data = eval(file.readline())
        complete = data[1]
        percent = data[2]
        level = Level(i+1, complete, percent)
    file.close()                   
    
