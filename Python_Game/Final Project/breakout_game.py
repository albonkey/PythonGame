from tkinter import *
import time

#Class which helps to make the block objects. Parameters(x,y,width,height,life)
class Block:
    def __init__(self,x,y,w,h,life):
        self.id = id
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.life = life

#Class to set up the blocks.
class BlockHandler:
    def __init__(self):
        self.draw = None
        self.blocks = []
        self.nrCols = 5
        self.nrRows = 5
        self.colors = ["","green","blue","yellow","orange","pink"] #Colors of the blocks depending on their life


    #Function to make the blocks. Takes the parameter lvl, which decides the life of the blocks.
    def blockMaker(self,lvl):
        self.blocks = []
        for i in range(1,game.width,int(game.width/self.nrCols)):
            for j in range(0,self.nrRows):
                s = Block(i,35*j,(game.width/self.nrCols)-5,30,game.lvl)
                self.blocks.append(s)

    def newLvl(self):
        pos = game.canvas.coords(ball.shape)
        if game.score == self.nrCols* self.nrRows*game.lvl:
            if pos[1] == 30*(self.nrRows+1):
                game.lvl += 1
                self.blockMaker(game.lvl)
                game.levelDisplay.configure(text="Lvl:"+ str(game.lvl))
    #Function to check if the ball is colliding with the blocks.
    def checkCollision(self,_ball,_block):
        pos = game.canvas.coords(_ball.shape)
        distX = abs(pos[0]+_ball.r-_block.x-(_block.w/2))
        distY = abs(pos[1]+_ball.r-_block.y-(_block.h/2))
        if distX > (_block.w/2 + _ball.r):
            return False
        if distY > _block.h/2 + _ball.r:
            return False
        if distX <= _block.w/2: #Checks if the ball is colliding from the side
            return 2
        if distY <= _block.h/2: #Checks if the ball is colliding from top/bottom.
            return 3
        dx = distX - _block.w/2
        dy = distY - _block.h/2
        return dx*dx+dy*dy <= _ball.r*_ball.r #Checks if it colliding at the corner

    #Checks the status of checkCollision. If the ball is chrasing with a block it pops the block, and changes direction of the ball.
    def blockCollision(self):
        blockIndex = 0
        for block in self.blocks:
            pop = False
            if self.checkCollision(ball,block): #checking if the ball collided at the corner, and changes x and y if so.
                pop = True
                ball.speedy *= -1
                ball.speedx *= -1
            if self.checkCollision(ball,block) == 2: #Checking if the ball collided at the side, and will change x if so.
                pop = True
                ball.speedx *= -1
            if self.checkCollision(ball,block) == 3: #Checking if it collided from the top or the bottom and changes y if so.
                pop = True
                ball.speedy *= -1
            if pop:
                block.life -= 1
                if block.life == 0:
                    self.blocks.pop(blockIndex)
                    game.score += 1
                    game.scoreDisplay.configure(text="Score:"+ str(game.score))
            blockIndex += 1
        self.newLvl()

    def blockUpdate(self):
        self.blockCollision()
        game.canvas.delete("BLOCK")
        for block in self.blocks:
            game.canvas.create_rectangle(block.x,block.y,block.x+block.w,block.y+block.h,fill=self.colors[block.life], tag="BLOCK")

#Class which handles the ball
class Ball:
    def __init__(self):
        self.r = 15 # Radius of the ball
        self.shape = game.canvas.create_oval(game.width/2, game.height-50, (game.width/2)+self.r*2,game.height-50+self.r*2, fill="red") #Creating the ball
        self.speedx = 0 #Speed of the x values of the ball
        self.speedy = 0 #Speed of the y values of the ball
        self.active = True #The ball is updated when this is true
        self.move_active()

    #Function to update where the ball is. Checks for walls and where the pad is.
    def ball_update(self):
        game.canvas.move(self.shape, self.speedx, self.speedy)
        pos = game.canvas.coords(self.shape)
        posPad = game.canvas.coords(pad.shape)
        blockIndex = 0;
        if pos[2] >= game.width or pos[0] <= 0: #Checking if the ball hits the walls
            self.speedx *= -1
        if pos[1] <= 0: # Checking if the ball hits the roof.
            self.speedy *= -1
        if pos[3] >= game.height: # If the ball goes all the way to the bottom, then its Game Over
            game.gameOver()
        if pos[3] > posPad[1] and pos[0]+self.r > posPad[0] and pos[0]+self.r < posPad[2] and pos[3]-self.r < posPad[3]: #If the ball hits the pad change its y- direction
                game.canvas.move(self.shape,0,-10) #To not make it stuck in the pad
                self.speedy *= -1

    #Moves the ball
    def move_active(self):
        if self.active:
            self.ball_update()
#Class for the pad.
class Pad:
    def __init__(self):
        self.x = game.width/2
        self.y = game.height-60
        self.w = 100
        self.s = 10
        self.r = False
        self.l = False
        self.shape = game.canvas.create_rectangle(self.x,self.y,self.x+self.w,self.y+10, fill="red")
        self.move_active()

    #Updates the were the pad is going. Left or Right Getting parameter from self.move_active()
    def updatePad(self,dir):
        pos = game.canvas.coords(self.shape)
        if dir == 0:
            if pos[2] >= game.width:
                self.x = game.width-self.s
            else:
                self.x += self.s
                game.canvas.move(self.shape,self.s,0)
        if dir == 1:
            if pos[0]<= 0:
                self.x = 0
            else:
                self.x += self.s
                game.canvas.move(self.shape,-self.s,0)
    #Runs the updatePad function.
    def move_active(self):
        if game.r:
            self.updatePad(0)
        if game.l:
            self.updatePad(1)

#class for setting up the game,canvas and score/lvl displays. Also handling key events
class Game:
    def __init__(self):
        #Variables for different things in the game.
        self.gameStartUp = True
        self.width = 500
        self.height = 700
        self.score = 0
        self.lvl = 1
        self.blocks = []
        self.l = False
        self.r = False

        #Setting up the window
        self.root = Tk()
        self.root.configure(bg="#3aaa35")
        self.bg_pic = PhotoImage(file = "./bg.png")
        #Binding the keys, to the window
        self.root.bind("<KeyPress>",self.keyPress)
        self.root.bind("<KeyRelease>",self.keyRelease)
        #Setting up the canvas
        self.canvas = Canvas(self.root, width=self.width, height=self.height,highlightthickness=0)
        self.canvas.grid(row=0,columnspan=2)
        self.canvas.create_image(0,0,image=self.bg_pic, anchor=NW)
        #Making a frame to contain the menu
        self.menu = Frame(self.root)
        self.menu.grid(row=0, columnspan=2, rowspan=2,sticky=N+S+E+W)

        #Making a frame to contain the buttons and text
        self.buttonFrame = Frame(self.menu,height=100,width=self.width)
        self.buttonFrame.grid(sticky=E+W)
        #Title of the game
        self.title = Label(self.buttonFrame,text="Breakout Game",width= 18,height=3,font=("Courier", 44))
        self.title.grid(sticky=E+W,row=0)
        #Button to start the game
        self.startBtn = Button(self.buttonFrame,text="Start",command=self.start,width= 20,height=3)
        self.startBtn.grid(row=1,pady=20)
        #Button to exit the game.
        self.exitBtn = Button(self.buttonFrame,text="Exit",command=lambda:sys.exit(),width= 20,height=3 )
        self.exitBtn.grid(row=2)
        #Text to show your score
        self.menuScore = Label(self.buttonFrame,text="",width=20,height=3)
        self.menuScore.grid(row=3)

        self.scoreDisplay = Label(self.root,text="Score:"+str(self.score),bg="#3aaa35")
        self.levelDisplay = Label(self.root,text="Lvl "+str(self.lvl),bg="#3aaa35",anchor=E)


    #This is run when the start button is pressed. It gives speed to the ball and hides the menu Frame.
    def start(self):
        if self.gameStartUp:
            self.gameEngine()
            self.gameStartUp = False
        self.canvas.move(ball.shape,0,-100)
        self.lvl = 1
        self.score = 0
        ball.speedy = -5
        ball.speedx = -5

        print (ball.speedy)

        self.menu.grid_forget()
        pad.updatePad(1)
        blockHandler.blockMaker(self.lvl)
        self.scoreDisplay.configure(text="Score:"+str(self.score))
        self.levelDisplay.configure(text="Lvl"+str(self.lvl))
        self.levelDisplay.grid(row=1)
        self.scoreDisplay.grid(row=1,column=1)

    #This runs when the game is over. It stops the ball and opens up the menu Frame again.
    def gameOver(self):
        self.scoreDisplay.grid_forget()
        self.levelDisplay.grid_forget()

        self.menuScore.configure(text="Your score: "+str(self.score))

        ball.speedy = 0
        ball.speedx = 0
        self.menu.grid(row=0, columnspan=2, rowspan=2,sticky=N+S+E+W)

    #Checking if the left key or the right key is pressed. Returns true if it is. Is used to steer the pad.
    def keyPress(self,event):
        if event.keysym == "Left":
            self.l = True
        if event.keysym == "Right":
            self.r = True
    def keyRelease(self,event):
        if event.keysym == "Left":
            self.l = False
        if event.keysym == "Right":
            self.r = False

    def gameEngine(self):
        blockHandler.blockUpdate()
        pad.move_active()
        ball.move_active()
        self.root.after(12, self.gameEngine)
#Initialzing everything
game = Game()
pad = Pad()
ball = Ball()
blockHandler = BlockHandler()
game.root.mainloop()
