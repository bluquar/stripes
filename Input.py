from GamePieces import Route

def determineActiveCell(container, event):
    width = container.width
    height = container.height
    for cell in [container.cells.cells[i] for i in container.cells.cells]:
        if cell.normal.dot(container.camera.view) < 0:
            if cell.containsPoint(event.x, event.y, container.camera, width, height):
                return cell.index
                break
    else:
        return 0

def motion(event, container, drawFn):
    if container.inMenu:
        pass
    else:
        grab = True
        rotate = True
        if hasattr(container, 'rotating'):
            if container.rotating and not hasattr(container, 'activeRoute'):
                grab = False
        if grab:
            draw = False
            container.activeIndex = determineActiveCell(container, event)
            if hasattr(container, 'activeRoute'):
                draw = container.routes.add(container.cells, container.activeIndex, container.activeRoute)
                rotate = False
            else:
                if container.activeIndex:
                    activeRoute = container.cells.cells[container.activeIndex].containsEndPoint(container.routes.routes)
                    if activeRoute:
                        container.activeRoute = activeRoute
                        rotate = False
                        draw = container.routes.add(container.cells, container.activeIndex, container.activeRoute, 'reset')
                    else:
                        activeRoute = container.cells.cells[container.activeIndex].containsRoutePoint(container.routes.routes, 0)
                        if activeRoute:
                            print 'grabbing route %d' % (activeRoute)
                            container.activeRoute = activeRoute
                            rotate = False
                            draw = container.routes.add(container.cells, container.activeIndex, container.activeRoute)
            if isinstance(draw, Route):
                if hasattr(draw, 'lines'):
                    for i in range(len(draw.orderedSteps)-1):
                        container.canvas.itemconfig(draw.lines[container.cells.cells[draw.orderedSteps[i]]], state='hidden')
                        container.canvas.itemconfig(draw.lines[container.cells.cells[draw.orderedSteps[i]].getNeighbor(draw.orderedSteps[i+1])], state='hidden')
                draw.hidden = True
            elif isinstance(draw, list):
                for route in container.routes.routes:
                    if hasattr(route, 'hidden'):
                        if not route.overlappedBy(container.routes.getRoute(abs(draw[0]))):
                            del route.hidden
            if draw:
                drawFn()
#        if rotate:
        if hasattr(container, 'rotating') and hasattr(container, 'xLast') and hasattr(container, 'yLast'):
            if container.rotating:
                if rotate:
                    x = event.x - container.xLast
                    y = container.yLast - event.y
                    container.camera.rotate(x, y)
                    drawFn()
                else:
                    x = container.xLast - event.x
                    y = event.y - container.yLast
                    factor = 1
                    if hasattr(container, 'activeIndex') and container.activeIndex != 0:
                        factor = abs(container.camera.view.unit().dot(container.cells.cells[container.activeIndex].normal.unit()))
                    container.camera.rotate(x * (1.5 - factor), y * (1.5 - factor))
                    drawFn()
        container.rotating = True
        container.xLast = event.x
        container.yLast = event.y
    
def release(event, container, drawFn):
    if not container.inMenu:
        for route in container.routes.routes:
            if hasattr(route, 'hidden'):
                del route.hidden
        container.rotating = False
        if hasattr(container, 'activeRoute'):
            container.routes.clip(container.activeRoute, container.cells)
            del container.activeRoute
        for cell in container.cells.cells:
            container.canvas.itemconfig(container.cells.cells[cell].polygonId, fill='#000000', activefill='#333333')
        for route in container.routes.routes:
            for step in route.orderedSteps:
                container.canvas.itemconfig(container.cells.cells[step].polygonId, fill=route.dullColor, activefill=route.lightColor)
        drawFn()
   
def zoom(event, container, drawFn):
    if container.inMenu:
        pass
    else:
        container.camera.resize(event.delta)
        drawFn()
        
def showIdcs(container, drawFn):
    if container.inMenu:
        pass
    else:
        cells = container.cells.cells
        for i in container.cells.cells:
            cells[i].texts = True
        drawFn()
def hideIdcs(container, drawFn):
    if container.inMenu:
        pass
    else:
        cells = container.cells.cells
        for i in container.cells.cells:
            cells[i].texts = False
        drawFn()