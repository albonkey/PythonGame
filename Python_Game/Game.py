from tkinter import *
from random import *
from time import sleep
#Class for creating the player. Parameters: name, x, y, facing, inventory, monsters, money
class PlayerMaker:
    def __init__(self,name,x,y,facing,inventory,monsters,money,img):
        self.name = name
        self.x = x
        self.y = y
        self.facing = facing
        self.inventory = inventory
        self.monsters = monsters
        self.money = money
        self.img = img
#Class for specifying how much the stats lvl up. Parameters: lvl, hp, attack, defence, spAtt, spDef, speed
class LvlUpStats:
    def __init__(self,max_hp,attack,defence,spAtt,spDef,speed):
        self.max_hp = max_hp
        self.attack = attack
        self.defence = defence
        self.spAtt = spAtt
        self.spDef = spDef
        self.speed = speed
#Class for creating abilities. Parameters: name, type, baseDmg, accuracy
class AbilityMaker:
    def __init__(self,name,type,dmg,accuracy):
        self.name = name
        self.type = type
        self.dmg = dmg
        self.accuracy = accuracy
#Class for creating Monsters. Parameters: art, type, secondaryType, lvl, exp, maxhp, attack, defence, spAtt, spDef, speed, abilities, lvlUp(Use the class LvlUpStats for this)
class MonsterMaker:
    def __init__(monster,id, art,type,secondaryType,lvl,exp,max_hp,attack,defence,spAtt,spDef,speed,abilities,lvlUp):
        monster.id = id
        monster.art = art
        monster.type = type
        monster.secondaryType = secondaryType
        monster.lvl = lvl
        monster.exp = exp
        monster.max_hp = max_hp
        monster.hp = max_hp
        monster.attack = attack
        monster.defence = defence
        monster.spAtt = spAtt
        monster.spDef = spDef
        monster.speed = speed
        monster.abilities = abilities
        monster.lvlUp = lvlUp
        monster.img = PhotoImage(file="./Monsters/"+monster.art+"/picture1.png")

    def lvlUpFunction(lvlUp):
        monster.max_hp += monster.lvlUp.max_hp
        monster.attack += monster.lvlUp.attack
        monster.defence += monster.lvlUp.defence
        monster.spAtt += monster.lvlUp.spAtt
        monster.spDef += monster.lvlUp.spDef
        monster.speed += monster.lvlUp.speed
#Class for making trainers. Parameters: x, y, facing, monsters, reward, img
class TrainerMaker:
    def __init__(self,x,y,facing,monsters,reward,img):
        self.x = x
        self.y = y
        self.facing = facing
        self.monsters = monsters
        self.reward = reward
        self.img = img
#Class for making different type of terrain. Parameters: x, y, type, lvl, region
class TerrainMaker:
    def __init__(self,x,y,type,lvl,region):
        self.x = x
        self.y = y
        self.type = type
        self.lvl = lvl
        self.region = region
#Class for setting size of a canvas. Parameters: width, height
class CanvasMaker:
    def __init__(self,width,height):
        self.width = width
        self.height = height

def leftKey(event):
    map.move(playerXY,-30,0)
    player.x -= 30
    if blockChecker() == False:
        map.move(playerXY,30,0)
        player.x += 30
def rightKey(event):
    map.move(playerXY,30,0)
    player.x += 30
    if blockChecker() == False:
        map.move(playerXY,-30,0)
        player.x -= 30
def upKey(event):
    map.move(playerXY,0,-30)
    player.y -= 30
    if blockChecker() == False:
        map.move(playerXY,0,30)
        player.y += 30
def downKey(event):
    map.move(playerXY,0,30)
    player.y += 30
    if blockChecker() == False:
        map.move(playerXY,0,-30)
        player.y -= 30
def mapMaker():
    global map
    global playerXY
    root.bind("<Left>", leftKey)
    root.bind("<Right>", rightKey)
    root.bind("<Up>", upKey)
    root.bind("<Down>", downKey)
    map = Canvas(root,width = startingPlace.width,height = startingPlace.height)
    battleScreen.pack_forget()
    map.pack()
    for i in range(0,len(mapArray)):
        dy = (30*i)+15
        dx = 15
        for s in mapArray[i]:

            map.create_image(dx,dy,image=terrain[s])
            dx += 30
    for obj in range(1):
        map.create_image(13*30+15,2*30+15,image=terrain[7])
    playerXY = map.create_image(player.x+15,player.y+5,image=player.img)
def blockChecker():
    for i in range(len(mapArray)):
        dy = 30*i
        dx = 0
        for s in mapArray[i]:
            if s == 2 or s == 3 or s == 4 or s == 5:
                if dy == player.y and dx == player.x or player.x < 0 or player.x > 600-30 or player.y < 0 or player.y > 600-30:
                        print ("Block")
                        return False
            if s == 1:
                if dy == player.y and dx == player.x :
                    rnd = random()
                    if rnd < 0.04:
                        print ("Monster")
                        createBattleScreen(fireman,createRandomMonster())
            dx += 30
def createRandomMonster():
    global id
    if region == "Home":
        monsterTypes = ["Grassman","Fireman","Waterman"]
        rnd = randint(0,len(monsterTypes)-1)
        m_lvl = randint(1,3)
        monster = MonsterMaker(id,monsters[rnd].art,monsters[rnd].type,monsters[rnd].secondaryType,monsters[rnd].lvl*m_lvl,monsters[rnd].exp,monsters[rnd].max_hp,monsters[rnd].attack,monsters[rnd].defence,monsters[rnd].spAtt,monsters[rnd].spDef,monsters[rnd].speed,monsters[rnd].abilities,monsters[rnd].lvlUp)
        id += 1
        return monster

def createBattleScreen(self,target):
    map.pack_forget()
    root.geometry("600x600")
    root.bind("<Left>", "")
    root.bind("<Right>", "")
    root.bind("<Up>", "")
    root.bind("<Down>", "")
    font=dict(family='Courier New, monospace', size=18, color='#7f7f7f')
    myMonsterStats = Label(battleScreen, text=self.art+" "+str(self.lvl)+"  hp:"+str(self.hp)+"/"+str(self.max_hp), anchor=W, padx=20, height=5).grid(column=0,row=0,columnspan=5,sticky=N+S+E+W)
    enemyMonsterStats = Label(battleScreen, text=target.art+" "+str(target.lvl)+"  hp:"+str(target.hp)+"/"+str(target.max_hp), anchor=W, padx=20, height=5).grid(column=4,row=0,columnspan=5,sticky=N+S+E+W)
    myMonster = Label(battleScreen, image=self.img).grid(column = 0, row=1, columnspan = 4,rowspan=4)
    enemyMonster = Label(battleScreen, image=target.img).grid(column = 5, row = 1, columnspan = 4,rowspan=4)
    att_1 = Button(battleScreen, text=self.abilities[0].name, command= lambda: attack(self,self.abilities[0],target)).grid(row=5,column=0, columnspan=3,rowspan=2, sticky=N+S+E+W)
    att_2 = Button(battleScreen, text=self.abilities[1].name).grid(row=5,column=3,columnspan=4,rowspan=2, sticky=N+S+E+W)
    att_3 = Button(battleScreen, text=self.abilities[2].name).grid(row=7,column=0,columnspan=3,rowspan=2, sticky=N+S+E+W)
    att_4 = Button(battleScreen, text=self.abilities[3].name).grid(row=7,column=3,columnspan=4,rowspan=2, sticky=N+S+E+W)
    opt_1 = Button(battleScreen, text="Fight").grid(row=5,column=7,columnspan=1,rowspan=2, sticky=N+S+E+W)
    opt_2 = Button(battleScreen, text="Bag").grid(row=5,column=8,columnspan=1,rowspan=2, sticky=N+S+E+W)
    opt_3 = Button(battleScreen, text="Monsters").grid(row=7,column=7,columnspan=1,rowspan=2, sticky=N+S+E+W)
    opt_4 = Button(battleScreen, text="Run", command=mapMaker).grid(row=7,column=8,columnspan=1,rowspan=2, sticky=N+S+E+W)

    battleScreen.pack(side=LEFT,fill="both")

def attack(self,ability,target):
    if self.speed > target.speed:
        target.hp -= ability.dmg-(int(target.defence/2))
        if target.hp > 0:
            enemyAttack(target,self)
    else:
        enemyAttack(target,self)
        if self.hp > 0:
            target.hp -= ability.dmg -(int(target.defence/2))

    if self.hp <= 0 or target.hp <= 0:
        if self.hp <= 0:
            print ("Your monster died..")
        else:
            print ("You killed",target.art)
        mapMaker()
    #Updating stats

    myMonsterStats = Label(battleScreen, text=self.art+" "+str(self.lvl)+"  hp:"+str(self.hp)+"/"+str(self.max_hp), anchor=W,padx=20).grid(column=0,row=0,columnspan=5,sticky=N+S+E+W)
    enemyMonsterStats = Label(battleScreen, text=target.art+" "+str(target.lvl)+"  hp:"+str(target.hp)+"/"+str(target.max_hp),anchor=W,padx=20).grid(column=4,row=0,columnspan=5,sticky=N+S+E+W)

def enemyAttack(self,target):
    rnd = randint(0,3)
    if self.abilities[rnd].dmg > 0:
        target.hp -= self.abilities[rnd].dmg-(int(target.defence/2))
root = Tk()


#Keybindings

#Variables
battleScreen = Frame(width=600, height=600, bg="green", colormap="new")
terrain = [PhotoImage(file="./Terrain/grass.png"),
            PhotoImage(file="./Terrain/bush.png"),
            PhotoImage(file="./Terrain/water.png"),
            PhotoImage(file="./Terrain/fence.png"),
            PhotoImage(file="./Terrain/fence_v.png"),
            PhotoImage(file="./Terrain/fence_c.png"),
            PhotoImage(file="./Terrain/fence_t.png"),
            PhotoImage(file="./Terrain/hp_house.png")
            ]

monsters = []
phA =AbilityMaker("","normal",0,0)
scratch = AbilityMaker("Scratch","normal",3,0.8)
leafcut = AbilityMaker("Leafcut","Grass",4,0.7)
fireman = MonsterMaker(1,"Fireman","fire","fighter",1,0,10,3,3,1,1,0.5,[scratch,phA,phA,phA],LvlUpStats(.2,.3,.2,.2,.2,.1))
grassman = MonsterMaker(2,"Grassman","grass","none",1,0,8,4,2,2,1,0.6,[leafcut,leafcut,leafcut,phA],LvlUpStats(.2,.3,.2,.2,.2,.1))
waterman = MonsterMaker(3,"Waterman","water","ice",1,0,9,3,2,1,1,0.4,[scratch,phA,phA,phA],LvlUpStats(.2,.3,.2,.2,.2,.1))
monsters.append(fireman)
monsters.append(grassman)
monsters.append(waterman)
player = PlayerMaker("Carl",30,30,"E",{"pokeballs":5,"potion":2},[fireman],500,PhotoImage(file="./Character/front.png"))

map = None
playerXY = None
region = "Home"
id= 4
#Terrain
grass = 0
bush = 1
water = 2
fence = 3
fence_v = 4
fence_c = 5
fence_t = 6
hp_house = 7

#Regions
startingPlace = CanvasMaker(600,600)

#Map Layout
mapArray = [[fence,fence,fence,fence,fence,fence,fence,fence,fence,fence,fence,fence_t,fence,fence,fence,fence,fence,fence,fence,fence,fence],
            [grass,grass,grass,grass,grass,bush,bush,bush,bush,bush,bush,fence_v,grass,grass,grass,grass,grass,grass,grass,grass,grass],
            [grass,grass,grass,grass,grass,bush,bush,bush,bush,bush,bush,fence_v,grass,grass,grass,grass,grass,grass,grass,grass,grass],
            [grass,grass,water,water,water,water,water,water,bush,bush,bush,fence_v,grass,grass,grass,grass,grass,grass,grass,grass,grass],
            [grass,grass,water,water,water,water,water,water,bush,bush,bush,fence_v,grass,grass,grass,grass,grass,grass,grass,grass,grass],
            [grass,grass,water,water,water,water,water,water,bush,bush,bush,fence_v,grass,grass,grass,grass,grass,grass,grass,grass,grass],
            [grass,grass,water,water,water,water,water,water,water,water,water,water,grass,grass,grass,grass,grass,grass,grass,grass,grass],
            [grass,grass,water,water,water,water,water,water,water,water,water,water,grass,grass,grass,grass,grass,grass,grass,grass,grass],
            [grass,grass,water,water,water,water,water,water,water,water,water,water,grass,grass,grass,grass,grass,grass,grass,grass,grass],
            [grass,grass,water,water,water,water,water,water,water,water,water,water,grass,grass,grass,grass,grass,grass,grass,grass,grass],
            [grass,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass],
            [grass,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass,fence,fence,fence,fence,fence_c,grass,grass,grass,grass],
            [grass,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass,bush,bush,bush,bush,fence_v,grass,grass,grass,grass],
            [grass,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass,bush,bush,bush,bush,fence_v,grass,grass,grass,grass],
            [fence,fence,fence,fence,fence,fence,fence,fence,fence_c,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass],
            [bush,bush,bush,bush,bush,bush,bush,bush,fence_v,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass],
            [bush,bush,bush,bush,bush,bush,bush,bush,fence_v,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass],
            [bush,bush,bush,bush,bush,bush,bush,bush,fence_v,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass],
            [bush,bush,bush,bush,bush,bush,bush,bush,fence_v,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass],
            [bush,bush,bush,bush,bush,bush,bush,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass,grass]
]


mapMaker()
mainloop()
