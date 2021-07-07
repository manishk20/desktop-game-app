import pygame
pygame.init()
win=pygame.display.set_mode((500,480))
pygame.display.set_caption("myfirstapp")
clock=pygame.time.Clock()

music=pygame.mixer.music.load("./music.mp3")
pygame.mixer.music.play(-1)
walkRight = [pygame.image.load("./assets/R1.png"), pygame.image.load("./assets/R2.png"), pygame.image.load("./assets/R3.png"), pygame.image.load("./assets/R4.png"), pygame.image.load("./assets/R5.png"), pygame.image.load("./assets/R6.png"), pygame.image.load("./assets/R7.png"), pygame.image.load("./assets/R8.png"), pygame.image.load("./assets/R9.png")]
walkLeft = [pygame.image.load("./assets/L1.png"), pygame.image.load("./assets/L2.png"), pygame.image.load("./assets/L3.png"), pygame.image.load("./assets/L4.png"), pygame.image.load("./assets/L5.png"), pygame.image.load("./assets/L6.png"), pygame.image.load("./assets/L7.png"), pygame.image.load("./assets/L8.png"), pygame.image.load("./assets/L9.png")]
bg = pygame.image.load("./assets/bg.jpg")
char = pygame.image.load("./assets/standing.png")
score = 0
class player(object):
    def __init__(self,x,y,width,height):
        self.x=x#self means the variable of its own class
        self.y=y
        self.width=width
        self.height=height
        self.vel=4
        self.jumpCount=10
        self.left=False
        self.right=False
        self.walkcount=0
        self.isjump=False
        self.standing=True
        self.hitbox=(self.x+20,self.y,28,60)
        
    def draw(self,win):#it only draws character
        if self.walkcount+1>=27:#till 26 as we have only 0 to 8 images of each walk
            self.walkcount=0
        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkcount//3],(self.x,self.y))
                self.walkcount+=1#each image from 9 will be used 3 times countinuously at each frame(iteration of main loop)
                # as walkcount//3 
            #pygame.draw.rect(win,(134,0,5),(x,y,width,height))
            elif self.right:#here we choose n=3 means 3 same images of each frames
                win.blit(walkRight[self.walkcount//3],(self.x,self.y))
                self.walkcount+=1
        else:#when standing
            if self.right:#last movenment right or left
                win.blit(walkRight[0],(self.x,self.y))
            else:
                win.blit(walkLeft[0],(self.x,self.y))
        self.hitbox=(self.x+18,self.y+4,28,58)# +20 of x due to sprite default position defect
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)#at each frame position changes so in draw method
    def hit(self):
        self.x=60
        self.y=410
        self.walkcount=0
        self.isjump=False
        self.jumpCount=10
        font1=pygame.font.SysFont("comicsans",80)#it defines the font for text in pygame: (type of font and , size)
        text=font1.render('-5',1,(255,0,0))#it renders or defines the text " " the font1 on screen on position
        win.blit(text,(250-(text.get_width()/2),200))#text.get_width()=>returns the above text width
        pygame.display.update()
        i=0
        while i<300:
            pygame.time.delay(10)
            i+=1
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    i=301
                    pygame.quit()
        
class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x=x
        self.y=y
        self.radius=radius
        self.color=color
        self.facing=facing
        self.vel=8*facing
    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)

class enemy(object):
    walkRight = [pygame.image.load('./assets/R1E.png'), pygame.image.load('./assets/R2E.png'), pygame.image.load('./assets/R3E.png'), pygame.image.load('./assets/R4E.png'), pygame.image.load('./assets/R5E.png'), pygame.image.load('./assets/R6E.png'), pygame.image.load('./assets/R7E.png'), pygame.image.load('./assets/R8E.png'), pygame.image.load('./assets/R9E.png'), pygame.image.load('./assets/R10E.png'), pygame.image.load('./assets/R11E.png')]
    walkLeft = [pygame.image.load('./assets/L1E.png'), pygame.image.load('./assets/L2E.png'), pygame.image.load('./assets/L3E.png'), pygame.image.load('./assets/L4E.png'), pygame.image.load('./assets/L5E.png'), pygame.image.load('./assets/L6E.png'), pygame.image.load('./assets/L7E.png'), pygame.image.load('./assets/L8E.png'), pygame.image.load('./assets/L9E.png'), pygame.image.load('./assets/L10E.png'), pygame.image.load('./assets/L11E.png')]
    def __init__(self,x,y,width,height,end):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.end=end
        self.path=[self.x,self.end]
        self.vel=3
        self.walkCount = 0
        self.health=10
        self.visible=True
        self.hitbox=(self.x+20,self.y,28,60)#it initializes hitbox att in enemy with some initial values
    def hit(self):
        #print("hit......everytime enemy got hit it will be executed")
        if self.health>0:
            self.health-=1
        else:
            self.visible=False

    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkCount+1>=33:
                self.walkCount=0
            if self.vel>0:
                win.blit(self.walkRight[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1
            else:
                win.blit(self.walkLeft[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1
            self.hitbox=(self.x+20,self.y,28,60)
            pygame.draw.rect(win,(255,0,0),(self.hitbox[0],self.hitbox[1]-20,50,10))
            pygame.draw.rect(win,(0,120,0),(self.hitbox[0],self.hitbox[1]-20,50-(5*(10-self.health)),10))
            #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    def move(self):
        if self.vel>0:#moving right
            if self.x+self.vel<=self.path[1]:
                self.x+=self.vel
            else:
                self.vel*=-1
        else:#moving left (vel is negative)
            if self.x-self.vel>=self.path[0]:
                self.x+=self.vel
            else:
                self.vel*=-1#making of positive

def redrawGameWindow():

    win.blit(bg,(0,0))
    man.draw(win)
    text=font.render('Score : '+ str(score),1,(0,0,0))
    win.blit(text,(350,10))
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()
#main loop
shootLoop=0
font = pygame.font.SysFont('comicsans',30,True)
bullets=[]#list of objects of bullets projectile
man=player(10,410,50,50)
run=True
goblin=enemy(100,410,64,64,380)
while run:
    clock.tick(27)#even we are still the frames will iterate...decides the time of each iteration of while on each frames
    if shootLoop>0:
        shootLoop+=1
    if shootLoop  > 5:
        shootLoop=0
    if goblin.visible==True:
        if man.hitbox[1]<goblin.hitbox[1]+goblin.hitbox[3] and man.hitbox[1]+man.hitbox[3]>goblin.hitbox[1]:
                if man.hitbox[0]+man.hitbox[2]>goblin.hitbox[0] and man.hitbox[0]<goblin.hitbox[0]+goblin.hitbox[2]:#goblin.hitbox[0]+width
                    man.hit()
                    score -= 5
                
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    for bullet in bullets:
        if bullet.y-bullet.radius<goblin.hitbox[1]+goblin.hitbox[3] and bullet.y+bullet.radius>goblin.hitbox[1]:
            if bullet.x+bullet.radius>goblin.hitbox[0] and bullet.x-bullet.radius<goblin.hitbox[0]+goblin.hitbox[2]:#goblin.hitbox[0]+width
                goblin.hit()
                if goblin.visible:
                    score += 1
                bullets.pop(bullets.index(bullet))
        if bullet.x<500 and bullet.x>0:
            bullet.x+=bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
    keys=pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and shootLoop==0:
        if man.left:
            facing = -1
        else:
            facing=1
        if len(bullets)<10:
            bullets.append(projectile(round(man.x+man.width//2),round(man.y+man.height//2),7,(255,255,0),facing))
        shootLoop=1
    elif keys[pygame.K_LEFT] and man.x>=man.vel:
        man.x-=man.vel
        man.left=True
        man.right=False
        man.standing=False
    elif keys[pygame.K_RIGHT] and man.x<=(500-man.width)-man.vel:
        man.x+=man.vel
        man.right=True
        man.left=False
        man.standing=False
    else:
        man.standing=True
        man.walkcount=0
    if not (man.isjump):# during at ground
        """if keys[pygame.K_UP] and y>=vel:
            y-=vel
        if keys[pygame.K_DOWN] and y<=(500-height)-vel:
            y+=vel"""
        if keys[pygame.K_UP] :
            man.isjump=True
            man.left=False
            man.right=False
            man.walkcount=0
            
    else:#during jump
        if man.jumpCount>=-10: 
            neg=1#10 to -10 oscillation
            if man.jumpCount<0:#for second half
                neg=-1
            man.y-=(man.jumpCount ** 2)*0.5*neg#y=y-{(jumpCount**2)*0.5*neg}
            man.jumpCount-=1
        else:#jump is over
            man.isjump=False
            man.jumpCount=10
    """if x<=-(width):
        x=500-width
    if y>=(500):
        y=0
    if x>=500:
        x=0
    if y<=-(height):
        y=500-height"""
    redrawGameWindow()
pygame.quit()

"""
always in game bullets are on to launch but list of bullet is empty
it only fills when SPACE is tapped but fills not more than 5
so only maximum 10 bullets can be seen on screen
"""
