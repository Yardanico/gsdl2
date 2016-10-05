#Author : Sean McKiernan (Mekire)
#Purpose: Maze creation using the 'Depth first search' with recursive backtracking.
#License: Free for everyone and anything (no warranty expressed or implied).

#Code taken from http://www.pygame.org/project-Lost+the+Plot-2097-.html
#Almost no modification - just changed pygame to gsdl2 (really)
import sys,os,random,math

import gsdl2
from gsdl2.locals import *

gsdl2.init()

MAZESIZE   = (800,600)
SCREENSIZE = (800,700)
SCREEN = gsdl2.display.set_mode(SCREENSIZE)

#graphics and fonts
mazebar    = gsdl2.image.load("mazebar.png").convert()
checkbox   = gsdl2.image.load("checkbox.png").convert()
pressed    = gsdl2.image.load("pressed.png").convert_alpha()
##arialsmall = pygame.font.SysFont("arial", 13, bold=True, italic=False)
arialsmall = gsdl2.font.Font("ArialNb.TTF", 13)
##arial      = pygame.font.SysFont("arial", 20, bold=True, italic=False)
arial      = gsdl2.font.Font("ArialNb.TTF", 20)

#constant globals
MYCOLORS  = {"start": (255,155,0),"goal":(0,100,255),"halls":(255,255,255),
             "search":(255,0,255),"sol": (70,183,0), "bord": (255,0,0)}
SIZELIST  = ((1,1),(2,2),(5,5),(10,10),(25,25),(50,50))
ADJACENTS = ((0,-1),(1,0),(0,1),(-1,0))
ADJWALLS  = (0b0010,0b0001,0b1000,0b0100) 
OPWALLS   = {0b1000:0b0010,0b0100:0b0001,0b0010:0b1000,0b0001:0b0100}
ADJCHECK  = {(0,-1):0b1000,(1, 0):0b0100,(0, 1):0b0010,(-1,0):0b0001}            

class GenPoint:
    #to allow for multiple generation points I pull this info into a seperate class
    def __init__(self,gencell,border):
        self.gencell     = gencell
        self.genID       = None
        self.genbound    = 0b0000
        self.currentcell = []
        self.visited   = {}
        self.border    = border
        self.stack = [[],[],[],[]]
        self.myneighbors = self.get_neighbors(self.gencell[0])
        self.get_gen_bounds()
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

    def get_neighbors(self,cell):
        #returns the neighbors as well as the direction that would take you there
        neighbors = []
        for i,adj in enumerate(ADJACENTS):
            check = (cell[0]+adj[0],cell[1]+adj[1])
            if check not in self.border:
                neighbors.append((check,ADJWALLS[i]))
        return neighbors

    def get_gen_bounds(self):
        self.genbound = 0b0000
        for neighb in self.myneighbors:
            self.genbound |= OPWALLS[neighb[1]]
        self.gencell = (self.gencell[0],self.genbound)

class _CellDraw:
    #both my generator and solver inherit from this to gain these draw functions
    def draw_cell(self,cell,color):
        loc = cell[0]
        self.draw_core(cell,color)
        self.draw_walls(cell,color)

    def draw_core(self,cell,color):
        loc = cell[0]
        self.screen.fill(color,((loc[0]*self.cell_size[0]+self.wall_size[0]+self.buffer[0],
                                 loc[1]*self.cell_size[1]+self.wall_size[1]+self.buffer[1]),self.core_size))
     
    def draw_walls(self,cell,color):
        #Note that cells only draw their top and right walls.
        #This prevents walls from being twice as thick as desired.
        loc = cell[0]
        wal = cell[1]
        if (wal & 0b1000):
            self.screen.fill(color,((loc[0]*self.cell_size[0]+self.wall_size[0]+self.buffer[0],
                                     loc[1]*self.cell_size[1]+self.buffer[1]),(self.core_size[0],
                                                                               self.wall_size[1])))
        if (wal & 0b0100):
            self.screen.fill(color,((loc[0]*self.cell_size[0]+self.cell_size[0]+self.buffer[0],
                                     loc[1]*self.cell_size[1]+self.wall_size[1]+self.buffer[1]),(self.wall_size[0],
                                                                                                 self.core_size[1])))
            
class AMazeing(_CellDraw):
    #Primary maze generator
    def __init__(self):
        self.screen      = SCREEN
        self.animate = True
        self.loops   = False
        self.reset   = False
        self.difcol  = False

        #This is the percent chance of revisiting a cell and creating a loop if 'loops' is on.
        #Putting this much above 1% gets silly really quickly. Possibly even lower would be better.
        self.loopchance = 1
        
        self.clock   = gsdl2.time.Clock()
        self.fps     = 65  #I don't think I currently use this anywhere.
        self.sizeind = 4
        self.wallind = 2
        self.init()
        
    def init(self):
        #used for resetting without altering user preferences
        self.state       = "START"
        self.calc_size()
        self.drawn       = False
        self.solvetime   = False
        
        self.genpoints = [] #a list of GenPoint classes
        self.genIDs    = None
        self.startcell = None
        self.goalcell  = None
        
        self.border    = set()
        self.visited   = set()
        self.neighbors = {}
        self.dirdict   = {}

        #generates the border with regards to the cell size
        #if generators are allowed in the border it must be two cells thick (at least)
        for i in range(self.screen.get_width()//self.cell_size[0]):
            self.border |= set(((i, 0),))
            self.border |= set(((i, -1),))##
            self.border |= set(((i,MAZESIZE[1]//self.cell_size[1]-1),))
            self.border |= set(((i,MAZESIZE[1]//self.cell_size[1]),))##
        for j in range(MAZESIZE[1]//self.cell_size[1]):
            self.border |= set((( 0,j),))
            self.border |= set((( -1,j),))##
            self.border |= set(((self.screen.get_width()//self.cell_size[0]-1,j),))
            self.border |= set(((self.screen.get_width()//self.cell_size[0],j),))##

        self.timestart = 0.0
        self.timeend   = 0.0

        #used for solving
        self.searching = None
        self.solution  = None
        self.MySolver  = None

        #button's pressed
        self.startpress = False
        self.resetpress = False

        self.gentime = ""
        self.slvtime = ""
        self.length  = ""   

    def calc_size(self):
        self.core_size   = SIZELIST[self.sizeind]
        self.wall_size   = SIZELIST[self.wallind]
        self.cell_size   = tuple(self.core_size[i]+self.wall_size[i] for i in range(2))
        self.buffer = ((MAZESIZE[0] % self.cell_size[0]-self.wall_size[0])//2,
                       (MAZESIZE[1] % self.cell_size[1]-self.wall_size[1])//2)
        
    def draw(self):
        if self.state != "GENERATE":
            self.screen.fill((0,0,0),((0,0),MAZESIZE))
        self.screen.fill(MYCOLORS["bord"],((0,0),(MAZESIZE[0],self.cell_size[1]+self.buffer[1])))
        self.screen.fill(MYCOLORS["bord"],((0,0),(self.cell_size[0]+self.buffer[0],MAZESIZE[1])))
        self.screen.fill(MYCOLORS["bord"],((0,(MAZESIZE[1]//self.cell_size[1]-1)*self.cell_size[1]+self.buffer[1]+self.wall_size[1]),
                                           (MAZESIZE[0],self.cell_size[1]+self.buffer[1]+10)))
        
        self.screen.fill(MYCOLORS["bord"],(((MAZESIZE[0]//self.cell_size[0]-1)*self.cell_size[0]+self.buffer[0]+self.wall_size[0],0),                                           
                                           (self.cell_size[0]+self.buffer[0]+10,MAZESIZE[1])))
        self.maze_bar()
        if not self.animate and self.state in ("SOLVED","DONE") or self.reset:
            if self.difcol:
                for Gen in self.genpoints:
                    for cell in Gen.visited:
                        self.draw_cell((cell,Gen.visited[cell]),Gen.color)
            else:
                for cell in self.dirdict:
                    self.draw_cell((cell,self.dirdict[cell]),MYCOLORS["halls"])
            self.reset = False
        if self.searching:
            for cell in self.searching:
                if cell not in [self.startcell,self.goalcell]:
                    self.draw_cell((cell,self.dirdict[cell]),MYCOLORS["search"])
            self.draw_core((self.startcell,self.dirdict[self.startcell]),MYCOLORS["start"])
            self.draw_walls((self.startcell,self.dirdict[self.startcell]),MYCOLORS["search"])
        if self.solution:
            for cell in self.solution:
                if cell != self.goalcell:
                    self.draw_core((cell,None),MYCOLORS["sol"])
            for cell in self.MySolver.solwalls:
                    self.draw_walls((cell,self.MySolver.solwalls[cell]),MYCOLORS["sol"])
            self.draw_core((self.goalcell,self.dirdict[self.goalcell]),MYCOLORS["goal"])
            self.draw_core((self.startcell,self.dirdict[self.startcell]),MYCOLORS["start"])
      
    def maze_bar(self):
        self.screen.blit(mazebar,(0,600))
        self.screen.blit(arialsmall.render(str(self.core_size[0]).zfill(2),1,MYCOLORS["halls"]),(763,MAZESIZE[1]+41))
        self.screen.blit(arialsmall.render(str(self.wall_size[0]).zfill(2),1,MYCOLORS["halls"]),(671,MAZESIZE[1]+41))
        if   self.state == "START":
            self.screen.blit(arial.render("Please place your generation points.",1,(0,0,0)),(270,MAZESIZE[1]+5))
        elif self.state == "READY":
            self.screen.blit(arial.render("Press 'space' or click start to begin generation",1,(0,0,0)),(225,MAZESIZE[1]+5))
        elif   self.state == "DONE":
            if not self.startcell:
                self.screen.blit(arial.render("Please place your start point.",1,(0,0,0)),(295,MAZESIZE[1]+5))
            else:
                self.screen.blit(arial.render("Please place your goal point.",1,(0,0,0)),(295,MAZESIZE[1]+5))
        elif   self.state == "SOLVE":
            self.screen.blit(arial.render("Press 'space' or click start to solve your maze.",1,(0,0,0)),(225,MAZESIZE[1]+5)) 
        if self.gentime:
            self.screen.blit(arialsmall.render("Generation time (ms)",1,(0,0,0)),(5,MAZESIZE[1]+5))
            self.screen.blit(arialsmall.render(": "+self.gentime,1,(0,0,0)),(130,MAZESIZE[1]+5))
        if self.slvtime:
            self.screen.blit(arialsmall.render("Solve time (ms)",1,(0,0,0)),(5,MAZESIZE[1]+17))
            self.screen.blit(arialsmall.render(": "+self.slvtime,1,(0,0,0)),(130,MAZESIZE[1]+17))
            self.screen.blit(arialsmall.render("Path length (cells)",1,(0,0,0)),(5,MAZESIZE[1]+29))
            self.screen.blit(arialsmall.render(": "+self.length,1,(0,0,0)),(130,MAZESIZE[1]+29))
        if not self.animate:
            self.screen.blit(checkbox,(114,MAZESIZE[1]+61))
        if not self.loops:
            self.screen.blit(checkbox,(212,MAZESIZE[1]+61))
                 
    def cell_targ(self):
        return ((self.target[0]-self.buffer[0])//self.cell_size[0],(self.target[1]-self.buffer[1])//self.cell_size[1])
    
    def event_loop(self):
        self.target = gsdl2.mouse.get_pos()
        for click in gsdl2.event.get():
            if click.type == MOUSEBUTTONDOWN:
                hit = gsdl2.mouse.get_pressed()
                print(hit)
                if hit[0]:
                    self.target = gsdl2.mouse.get_pos()
                    if (0 < self.target[0] < self.screen.get_width()) and (0 < self.target[1] < MAZESIZE[1]):
                        #place start/goal
                        if self.state == "START":
                            self.place_gen()
                        elif self.state == "DONE":
                            self.place_goal()
                    #reset button
                    elif 300 < self.target[0] < 400 and (MAZESIZE[1]+40 < self.target[1] < MAZESIZE[1]+90):
                        self.init()
                        self.resetpress = True
                    #start button
                    elif 425 < self.target[0] < 525 and (MAZESIZE[1]+40 < self.target[1] < MAZESIZE[1]+90):
                        self.start_it()
                    #toggle animation on/off
                    elif 31 < self.target[0] < 128 and (MAZESIZE[1]+59 < self.target[1] < MAZESIZE[1]+77):
                        self.tog_anim()
                    #toggle loops on/off
                    elif 146 < self.target[0] < 226 and (MAZESIZE[1]+59 < self.target[1] < MAZESIZE[1]+77):
                        self.tog_loop()

                    if self.state not in ["GENERATE","SOLVING"]:
                        #make cell size bigger/smaller
                        if   759 < self.target[0] < 779 and (MAZESIZE[1]+18 < self.target[1] < MAZESIZE[1]+38):
                            self.cell_up()
                        elif 759 < self.target[0] < 779 and (MAZESIZE[1]+61 < self.target[1] < MAZESIZE[1]+81):
                            self.cell_down()
                        #make walls thinner/thicker
                        elif 667 < self.target[0] < 687 and (MAZESIZE[1]+18 < self.target[1] < MAZESIZE[1]+38):
                            self.wall_up()
                        elif 667 < self.target[0] < 687 and (MAZESIZE[1]+61 < self.target[1] < MAZESIZE[1]+81):
                            self.wall_down()

            #hotkeys      
            if click.type == KEYDOWN:
                #start
                if click.key == K_SPACE:
                    self.start_it()
                #reset
                elif click.key == K_RETURN:
                    self.init()
                    self.resetpress = True
                #toggle animation
                elif click.key == K_d:
                    self.tog_anim()
                #toggle loops on/off
                elif click.key == K_l:
                    self.tog_loop()
                #resets maze to unsolved (essentially a refresh key)
                elif click.key == K_i:
                    if self.state != "GENERATE":
                        self.initial()
                #toggle generator specific colors on/off (refresh after pressing if not mid-generation)
                elif click.key == K_c:
                    self.difcol = (True if not self.difcol else False)
                    if self.state != "START":
                        self.reset = True
                        self.draw()
                        gsdl2.display.update()
                    
                #change cell size
                if self.state not in ["GENERATE","SOLVING"]:
                    if   click.key in [K_KP_PLUS,K_PLUS,K_EQUALS]:
                        self.cell_up()
                    elif click.key in [K_KP_MINUS,K_MINUS] :
                        self.cell_down()
                #quit
                if click.key == K_ESCAPE:
                    self.state = "QUIT"

            #reset start/reset buttons to unpushed
            if click.type in [MOUSEBUTTONUP,KEYUP]:
                if   self.startpress:
                    self.startpress = False
                    self.screen.blit(mazebar,(425,MAZESIZE[1]+40),(425,40,100,50))
                    gsdl2.display.update()
                elif self.resetpress:
                    self.resetpress = False
                    self.screen.blit(mazebar,(300,MAZESIZE[1]+40),(300,40,100,50))
                    gsdl2.display.update()
                    
            if click.type == gsdl2.QUIT: self.state = "QUIT"

        #make start/reset buttons pushed
        if self.startpress:
            self.screen.blit(pressed,(425,MAZESIZE[1]+40))
            gsdl2.display.update()
        elif self.resetpress:
            self.screen.blit(pressed,(300,MAZESIZE[1]+40))
            gsdl2.display.update()

    def initial(self):
        #resets maze to an unsolved state without deleting current maze
        history = self.dirdict
        gens    = self.genpoints
        self.init()
        self.dirdict   = history
        self.genpoints = gens
        self.state     = "DONE"
        self.solvetime = True
        self.drawn     = False
        self.reset     = True
        
    #raise and lower cell size
    def cell_up(self):
        if self.sizeind < len(SIZELIST)-1:
            self.sizeind += 1
            self.init()
    def cell_down(self):
        if self.sizeind > 0:
            self.sizeind -= 1
            self.init()
    def wall_up(self):
        if self.wallind < len(SIZELIST)-1:
            self.wallind += 1
            self.init()
    def wall_down(self):
        if self.wallind > 0:
            self.wallind -= 1
            self.init()
            
    #creates a solver class
    def create_solver(self):
        self.MySolver = Solver(self.startcell,self.goalcell,self.dirdict,self.animate,self.screen)
        self.MySolver.timestart = gsdl2.time.get_ticks()
        self.MySolver.get_openset()
        self.MySolver.cell_size = self.cell_size
        self.MySolver.wall_size = self.wall_size
        self.MySolver.core_size = self.core_size
        self.MySolver.buffer    = self.buffer
        self.state = "SOLVING"
    #toggle animation on/off
    def tog_anim(self):
        self.animate = (True if not self.animate else False)
        if self.MySolver:
            self.MySolver.animate = self.animate
        if self.animate:
            #regards toggling animation on/off during generation or solving
            if self.state == "GENERATE":
                for Gen in self.genpoints:
                    for cell in Gen.visited:
                        if not self.difcol:
                            self.draw_cell((cell,Gen.visited[cell]),MYCOLORS["halls"])
                        else:
                            self.draw_cell((cell,Gen.visited[cell]),Gen.color)
            elif self.state == "SOLVING":
                if self.searching:
                    for cell in self.searching:
                        if cell not in [self.startcell,self.goalcell]:
                            self.draw_cell((cell,self.dirdict[cell]),MYCOLORS["search"])
                    self.draw_cell((self.startcell,self.dirdict[self.startcell]),MYCOLORS["start"])
                if self.solution:
                    for cell in self.solution:
                        if cell != self.goalcell:
                            self.draw_core((cell,None),MYCOLORS["sol"])
                    for cell in self.MySolver.solwalls:
                            self.draw_walls((cell,self.MySolver.solwalls[cell]),MYCOLORS["sol"])
                    self.draw_core((self.goalcell,self.dirdict[self.goalcell]),MYCOLORS["goal"])
                    self.draw_core((self.startcell,self.dirdict[self.startcell]),MYCOLORS["start"])   
            self.screen.blit(mazebar,(114,MAZESIZE[1]+61),(114,61,13,13))
        else:
            self.screen.blit(checkbox,(114,MAZESIZE[1]+61))
        gsdl2.display.update()
    #toggle loops on/off
    def tog_loop(self):
        self.loops = (False if self.loops else True)
        if self.loops:
            self.screen.blit(mazebar,(212,MAZESIZE[1]+61),(212,61,13,13))
        else:
            self.screen.blit(checkbox,(212,MAZESIZE[1]+61))
        gsdl2.display.update()
        
    #start button functionality
    def start_it(self):
        if self.genpoints and not self.solvetime and self.state != "GENERATE":
            self.state = "GENERATE"
            self.timestart = gsdl2.time.get_ticks()
            if self.animate:
                for Gen in self.genpoints:
                    for check in self.neighbors[Gen.gencell[0]]:
                        if not self.difcol:
                            self.draw_cell(check,MYCOLORS["halls"])
                        else:
                            self.draw_cell(check,Gen.color)
                    self.screen.fill((0,0,0),((Gen.gencell[0][0]*self.cell_size[0]+self.buffer[0],
                                               Gen.gencell[0][1]*self.cell_size[1]+self.buffer[1]),self.cell_size))
                    if not self.difcol:
                        self.draw_cell(Gen.gencell,MYCOLORS["halls"])
                    else:
                        self.draw_cell(Gen.gencell,Gen.color)
        elif self.state == "SOLVE":
            self.create_solver()
        self.startpress = True
        self.maze_bar()
        gsdl2.display.update()
        
    #place generator points
    def place_gen(self):
        gencell = (self.cell_targ(),0b0000)
        NewGen = GenPoint(gencell,self.border)

        if self.check_overlap(NewGen):
            if not self.genIDs:
                NewGen.genID = 1
                self.genIDs  = 1
            else:
                self.genIDs  <<= 1
                NewGen.genID = (self.genIDs)
            self.genpoints.append(NewGen)
            self.neighbors[gencell[0]] = NewGen.myneighbors     
            for j,cell in enumerate(NewGen.myneighbors):
                NewGen.currentcell.append(cell)
                NewGen.stack[j].append(cell[0])
                self.dirdict[cell[0]]   = cell[1]
                NewGen.visited[cell[0]] = cell[1]
            while [] in NewGen.stack:
                NewGen.stack.remove([])
            NewGen.visited[NewGen.gencell[0]] = NewGen.gencell[1]
            self.dirdict[NewGen.gencell[0]] = NewGen.gencell[1]
            for vis in NewGen.visited:
                self.visited |= set((vis,))
            self.visited |= set((NewGen.gencell[0],))
            self.screen.fill(MYCOLORS["start"],((gencell[0][0]*self.cell_size[0]+self.buffer[0],
                                                 gencell[0][1]*self.cell_size[1]+self.buffer[1]),self.cell_size))
            self.maze_bar()
            gsdl2.display.update()

    def check_overlap(self,Gen):
        #This deals with generators being placed close together.
        for OtherGen in self.genpoints:
            if   Gen.gencell[0] == OtherGen.gencell[0]:
                return 0
            else:
                checklist = Gen.myneighbors[:]
                for vis,way in checklist:  
                    if vis in OtherGen.visited:
                        Gen.myneighbors.remove((vis,way))
                        Gen.get_gen_bounds()
                    if vis == OtherGen.gencell[0]:
                        if Gen.gencell[0] in OtherGen.visited:
                            OtherGen.visited.pop(Gen.gencell[0])
                        for cell in OtherGen.currentcell:
                            if cell[0] == Gen.gencell[0]:
                                OtherGen.currentcell.remove(cell)
                                OtherGen.myneighbors.remove(cell)
                                OtherGen.get_gen_bounds()
                                OtherGen.visited[OtherGen.gencell[0]] = OtherGen.gencell[1]
                                self.dirdict[OtherGen.gencell[0]] = OtherGen.gencell[1]
                        for stack in OtherGen.stack:
                            for cell in stack:
                                if cell == Gen.gencell[0]:
                                    OtherGen.stack.remove(stack)
                                    break
        return 1
                 
    #placing start/goal cells
    def place_goal(self):
        if not self.startcell:
            self.startcell = self.cell_targ()
            self.draw_core((self.startcell,None),MYCOLORS["start"])
        else:
            self.goalcell = self.cell_targ()
            self.border.discard(self.goalcell)
            self.visited |= set((self.goalcell,))
            self.state = "SOLVE"
            self.draw_core((self.goalcell,None),MYCOLORS["goal"])
        self.maze_bar()
        gsdl2.display.update()

    def generation(self):
        def gen_anim(Gen,check):
            if self.animate:
                if not self.difcol:
                    self.draw_cell(check,MYCOLORS["halls"])
                else:
                    self.draw_cell(check,Gen.color)

        def merge_gens(Gen,OtherGen,check):
            #Logic for allowing a cell to 'revisit' another cell 
            #thereby connecting generators or creating a loop.
            updatecell      = (Gen.currentcell[i][0],Gen.currentcell[i][1] | OPWALLS[check[1]])
            otherupdatecell = (check[0],OtherGen.visited[check[0]] | check[1]) 
            Gen.visited[updatecell[0]]  = updatecell[1]
            self.dirdict[updatecell[0]] = updatecell[1]                                           
            OtherGen.visited[otherupdatecell[0]] = otherupdatecell[1]
            self.dirdict[otherupdatecell[0]]     = otherupdatecell[1]
            for k,cell in enumerate(OtherGen.currentcell):
                if cell and cell[0] == check[0]:
                    OtherGen.currentcell[k] = otherupdatecell
            Gen.currentcell[i] = updatecell
            
            if self.animate:
                if not self.difcol:
                    self.draw_walls(updatecell,MYCOLORS["halls"])
                    self.draw_walls((check[0],OtherGen.visited[check[0]]),MYCOLORS["halls"])
                else:
                    self.draw_walls(updatecell,Gen.color)
                    self.draw_walls((check[0],OtherGen.visited[check[0]]),OtherGen.color)
                gsdl2.display.update()
        
        #Definately a little messy on determining when to stop but works. (I'm sure there is an easier, simpler way)
        go = False
        for Gen in self.genpoints:
            if go: break
            for stack in Gen.stack:
                go = (True if stack else False)
                if go: break
        for Gen in self.genpoints:
            if self.state == "DONE":
                break
            for stack in Gen.stack:
                if go:
                    for i in range(len(Gen.stack)):
                        if Gen.currentcell[i]:
                            if Gen.currentcell[i][0] not in self.neighbors:
                                self.neighbors[Gen.currentcell[i][0]] = Gen.get_neighbors(Gen.currentcell[i][0])                                
                            if self.neighbors[Gen.currentcell[i][0]]:
                                check = random.choice(self.neighbors[Gen.currentcell[i][0]])
                                self.neighbors[Gen.currentcell[i][0]].remove(check)
                                if check[0] not in self.border:
                                    for OtherGen in self.genpoints:
                                        if check[0] not in self.visited:
                                            updatecell = (Gen.currentcell[i][0],Gen.currentcell[i][1] | OPWALLS[check[1]])
                                            Gen.visited[updatecell[0]] = updatecell[1]
                                            self.dirdict[updatecell[0]] = updatecell[1]
                                            if self.animate:
                                                if not self.difcol:
                                                    self.draw_walls(updatecell,MYCOLORS["halls"])
                                                else:
                                                    self.draw_walls(updatecell,Gen.color)
                                                gsdl2.display.update()
                                            Gen.stack[i].append(check[0])
                                            self.dirdict[check[0]] = check[1]
                                            Gen.currentcell[i] = check
                                            Gen.visited[check[0]] = check[1]
                                            self.visited |= set ((check[0],))
                                            gen_anim(Gen,check)
                                            break
                                        elif not (Gen.genID & OtherGen.genID) and check[0] in OtherGen.visited:
                                            merge_gens(Gen,OtherGen,check)
                                            #The below logic assures that generators only connect once,
                                            #thereby retaining a perfect maze (unless of course 'loops' is on).
                                            newID = Gen.genID | OtherGen.genID
                                            thisold = Gen.genID ; otherold = OtherGen.genID
                                            for ID in self.genpoints:
                                                if ID.genID in [thisold,otherold]:
                                                    ID.genID = newID
                                            break
                                        elif self.loops:
                                            #Reconnect to a visited cell at the chance set in 'self.loopchance'.
                                            chance = random.randint(1,100)
                                            if chance <= self.loopchance and check[0] in OtherGen.visited:
                                                merge_gens(Gen,OtherGen,check)
                                                break
                                    else:
                                        self.dirdict[Gen.currentcell[i][0]] = Gen.currentcell[i][1]
                            else:
                                if Gen.stack[i]:
                                    popped = Gen.stack[i].pop()
                                    Gen.currentcell[i] = (popped,self.dirdict[popped])
                                else:
                                    Gen.currentcell[i] = None
                else:
                    self.timeend = gsdl2.time.get_ticks()
                    self.gentime = str(self.timeend-self.timestart)
                    self.solvetime = True
                    self.state = "DONE"
                    self.maze_bar()
                    gsdl2.display.update()
                    if not self.animate:
                        self.drawn = False
                    break
           
    def update(self):
        if self.state not in  ["GENERATE","SOLVING"]:
            if not self.drawn:
                self.screen.fill(MYCOLORS["halls"])
                self.draw()
                gsdl2.display.update()
                self.drawn = True
            self.event_loop()
        elif self.state == "GENERATE":
            if self.animate:
                gsdl2.display.update()
            self.generation()
            self.event_loop()
            gsdl2.event.pump()
        elif self.state == "SOLVING":
            if self.animate:
                gsdl2.display.update()
            if self.MySolver.solved:
                self.solution = self.MySolver.evaluate()
                self.slvtime = str(self.MySolver.timeend-self.MySolver.timestart)
                self.length = str(len(self.solution))
                self.state = "SOLVED"
                self.maze_bar()
                gsdl2.display.update()
                if not self.animate:
                    self.drawn = False
            else:
                result = self.MySolver.evaluate()
                if result:
                    self.searching = result
                else:
                    self.state = "SOLVED"
                    if not self.animate:
                        self.drawn = False
            self.event_loop()
            gsdl2.event.pump()
                    
        if self.state == "QUIT":
            gsdl2.quit();sys.exit()

class Solver(_CellDraw):
    def __init__(self,start,goal,visited,animate,screen):
        self.dirdict   = visited
        self.screen    = screen
        self.animate   = animate
        self.cell_size = (20,20)
        self.wall_size = (10,10)
        self.core_size = (10,10)
        self.solwalls  = {}
        self.buffer    = (0,0)
        
        self.startcell   = start
        self.goalcell    = goal
        self.currentcell = self.startcell
        self.nextcell    = None

        self.altmethod  = None
        self.solved     = False
        self.solution   = []

        self.timestart = 0.0
        self.timeend   = 0.0

        self.hx = {} #optimal estimate to goal
        self.gx = {} #cost from start to current position
        self.fx = {} #distance-plus-cost heuristic function

        self.closedset = set()
        self.openset   = set()
        self.gx[self.startcell] = 0
        self.hx[self.startcell] = self.get_dist(self.startcell,self.goalcell)

        self.closedset |= set((self.startcell,))
        self.came_from  = {}

        self.state    = None
        self.pathdone = False
        self.pathtime = False

    def get_dist(self,start,goal):
        #optimum path distance for orthoganal movement 'Rook'
        distance = abs(goal[0]-start[0])+abs(goal[1]-start[1])
        return distance

    def get_neighbors(self):
        openset = set()
        for (i,j) in ADJACENTS:
            check = (self.currentcell[0]+i,self.currentcell[1]+j)
            if (ADJCHECK[(i,j)] & self.dirdict[self.currentcell]) and check not in self.closedset:
                openset |= set((check,))
        return openset
                
    def get_openset(self):
        self.openset = self.get_neighbors()

    def get_path(self,cell):
        #Most of this is for aesthetic reasons.  I didn't like walls not directly on the path being filled.
        if cell in self.came_from:
            self.solution.append(cell)
            self.currentcell = self.came_from[cell]
            direction = (self.currentcell[0]-self.solution[-1][0],self.currentcell[1]-self.solution[-1][1])
            if self.animate:
                if self.currentcell not in (self.startcell,self.goalcell):
                    self.draw_core((self.currentcell,None),MYCOLORS["sol"])
                    if direction in [(0,1),(-1,0)]:
                        self.draw_walls((self.currentcell,OPWALLS[ADJCHECK[direction]]),MYCOLORS["sol"])
                    else:
                        self.draw_walls((cell,ADJCHECK[direction]),MYCOLORS["sol"])
            if direction in [(0,1),(-1,0)]:
                self.solwalls[self.currentcell] = self.solwalls.setdefault(self.currentcell,0) | OPWALLS[ADJCHECK[direction]]
            else:
                self.solwalls[cell] = self.solwalls.setdefault(cell,0) | ADJCHECK[direction]
        else:
            direction = (self.currentcell[0]-self.solution[-1][0],self.currentcell[1]-self.solution[-1][1])
            if self.animate:
                if direction in [(0,1),(-1,0)]:
                    self.draw_walls((cell,OPWALLS[ADJCHECK[direction]]),MYCOLORS["sol"])
                else:
                    self.draw_walls((self.solution[-1],ADJCHECK[direction]),MYCOLORS["sol"])
            if direction in [(0,1),(-1,0)]:
                self.solwalls[cell] = self.solwalls.setdefault(cell,0) | OPWALLS[ADJCHECK[direction]]
            else:
                self.solwalls[self.solution[-1]] = self.solwalls.setdefault(self.solution[-1],0) | ADJCHECK[direction]
            self.pathdone = True

    def evaluate(self):
        if self.openset and not self.pathtime:
            if self.nextcell:
                self.currentcell = self.nextcell
            if not self.altmethod or not self.nextcell:
                for cell in self.openset:
                    if cell not in self.came_from:
                        self.gx[cell] = 1
                        self.hx[cell] = self.get_dist(cell,self.goalcell)
                        self.fx[cell] = self.gx[cell]+self.hx[cell]
                        self.came_from[cell] = self.startcell
                    if self.currentcell not in self.openset:
                        self.currentcell = cell
                    elif self.fx[cell] < self.fx[self.currentcell]:
                        self.currentcell = cell
                    
            if self.currentcell == self.goalcell:
                self.pathtime = True
            
            self.openset.discard(self.currentcell)
            self.closedset |= set((self.currentcell,))
            if self.animate:
                if self.currentcell not in (self.startcell,self.goalcell):
                    self.draw_cell((self.currentcell,self.dirdict[self.currentcell]),MYCOLORS["search"])
                    self.draw_walls((self.startcell,self.dirdict[self.startcell]),MYCOLORS["search"])

            neighbors = self.get_neighbors()
            self.nextcell = None
            for cell in neighbors:
                tent_g = self.gx[self.currentcell]+1
                if cell not in self.openset:
                    self.openset |= set((cell,))
                    tent_better = True
                elif cell in self.gx and tent_g < self.gx[cell]:
                    tent_better = True
                else:
                    tent_better = False

                if tent_better:
                    self.came_from[cell] = self.currentcell
                    self.gx[cell] = tent_g
                    self.hx[cell] = self.get_dist(cell,self.goalcell)
                    self.fx[cell] = self.gx[cell]+self.hx[cell]
                    if not self.nextcell:
                        self.nextcell = cell
                    elif self.fx[cell]<self.fx[self.nextcell]:
                        self.nextcell = cell
            return self.closedset            
        elif self.pathtime and not self.pathdone:
            self.get_path(self.currentcell)
            return self.closedset 
        elif self.pathdone:
            self.timeend = gsdl2.time.get_ticks()
            if not self.solved:
                self.solved = True
                self.state = "DONE"
                return self.closedset
            else:
                return self.solution
        else:
            #reached if no solution is found or possible.
            #Beware that searching for a solution when no solution is possible is very time consuming.
            self.timeend = gsdl2.time.get_ticks()
            self.state = "DONE"
            return 0
    
#####           
def main():
    Maze.update()

#####
if __name__ == "__main__":
    Maze = AMazeing()
    while 1:
        main()
