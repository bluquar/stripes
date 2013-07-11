
from math import pi

from Tkinter import Tk, Frame, Canvas, Label, BOTH, LEFT, N, E, S, W, X, Y
import Tkinter
from ttk import Button, Style

from Geometry import Locus, Vector
from GamePieces import Neighbor, Route, Cell, Camera
from GameSets import CellGroup, RouteGroup
from Render import drawCells, drawRoutes, showLevelSelection
from Input import motion, release, zoom, showIdcs, hideIdcs

class Container(Frame):
    def __init__(self, parent, width, height):
        
        Frame.__init__(self, parent, background="#22aaff")
        self.parent = parent
        self.initUI(width, height)
        
    def initUI(self, width, height):
        self.inMenu = True
        
        self.width = width 
        self.height = height
        
        self.parent.title("Stripes")
        self.style = Style()
        self.style.theme_use('default') #clam, default, alt, classic
        
        self.pack(fill=BOTH, expand=1)
               
        self.canvas = Canvas(self, width=width, height=height-30, background='#335533')
  
        def resize(event):
            self.width = event.width
            self.height = event.height
            if self.inMenu:
                pass
            else:
                self.draw()

        self.bind('<Configure>', resize)
        self.canvas.bind('<B1-Motion>', lambda(e): motion(e, self, self.draw))
        self.canvas.bind('<ButtonRelease-1>', lambda(e): release(e, self, self.draw))
        self.canvas.bind('<MouseWheel>', lambda(e): zoom(e, self, self.draw))

        def initializeLevel(levelNum):
            
            self.currentLevel = levelNum
            
            self.inMenu = False
            self.canvas.delete('all')
            self.camera = Camera(200, pi / 40)
            self.cells = CellGroup('cube', '3', 4, self)
            
            file = open('levels.txt', 'r')
            colors = eval(file.readline())
            file.close()
            
            self.routes = RouteGroup('cube', '3', 4, levelNum, self.cells, self, colors)
            self.activeIndex = 0
            self.draw()
            
            hideIdcs(self, self.draw)

        numLevels = 10
        
        def save(toMenu):
            lines = []
            file = open('levels.txt', 'r+')
            for i in range(numLevels+2):
                lines.append(file.readline())
            levelInfo = eval(lines[self.currentLevel+1])
            percent = self.cells.percent(self.routes.routes)
            complete = self.routes.complete()
            if percent < levelInfo[2]:
                percent = levelInfo[2]
            if levelInfo[1] == True:
                complete = True
            nodes = levelInfo[0]
            lines[self.currentLevel+1] = '(' + str(nodes) + ',' + str(complete) + ',' + str(percent) + ')\n'
            file.seek(0)
            for line in lines:
                file.write(line)
            file.write('\n' + lines[len(lines)-1])
            file.close()
            if toMenu:
                showLevelSelection(self, initializeLevel, numLevels)

        frame = Frame(self, width=width, height=30,background='#999999')

        menuButton = Button(self, text="Level Select", command=lambda: save(True))
        menuButton.pack(in_=frame, side=LEFT, anchor=W, ipadx=6, padx=6)
        
        closeButton = Button(self, text="Close", command=self.quit)
        closeButton.pack(in_=frame, side=LEFT, anchor=E, padx=6)
        
        showButton = Button(self, text='Show #s', command=lambda: showIdcs(self, self.draw))
        showButton.pack(in_=frame, side=LEFT, anchor=E, padx=6)
        
        hideButton = Button(self, text='Hide #s', command=lambda: hideIdcs(self, self.draw))
        hideButton.pack(in_=frame, side=LEFT, anchor=E, padx=6)
        
        frame.pack(anchor=W, fill=BOTH, expand=1)

        self.canvas.pack(fill=BOTH, expand=1)
        showLevelSelection(self, initializeLevel, numLevels)
        
    def draw(self):
        drawCells(self)
        drawRoutes(self)
    
def main():
  
    root = Tk()
    
    width = 800
    height = 700
    
    root.geometry(str(width) + 'x' + str(height) + '+1000+300')
    
    app = Container(root, width, height)
    
    root.mainloop() 

if __name__ == '__main__':
    main()
