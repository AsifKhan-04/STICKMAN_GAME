import pygame

pygame.init() #initialising the pygame

win = pygame.display.set_mode((500, 480)) #dimensions of the window


pygame.display.set_caption("First Game") #caption of the game

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
             pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
             pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'),
            pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),
            pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg1.jpg') #background of the game
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()
bulletSound=pygame.mixer.Sound('bullet.wav') #inserting sound for gun fire

music = pygame.mixer.music.load('music.mp3') #inserting the background music
pygame.mixer.music.play(-1) #-1  for continuingly playing the sound


score = 0 #for score 1


class player(object):
    def __init__(self, x, y, width, height): #initialisation
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0  #counting the sprites
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52) #(x,y,width,height) #rectangle is being built as a hit box

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not (self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52) #the hit box is once again written here because it should move with our image
        # pygame.draw.rect(win, (255,0,0), self.hitbox,2)  #here self.hitbox draws a rectangle
    def hit(self): #this is the method when the goblin hits the player
        self.x = 60 #changing the ch. dimensions
        self.y = 410
        self.walkCount=0
        font1=pygame.font.SysFont('comicsans',100)
        text=font1.render('-5',1,(255,0,0))
        win.blit(text, (250 - (text.get_width()/2),200))
        pygame.display.update()
        i=0
        while i<300:
            pygame.time.delay(10)   #the delay when goblin hits us 
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()



class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'),
                 pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
                 pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'),
                 pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'),
                pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
                pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'),
                pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10 #max of health if it is crossed enemy will become invisible
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33: #we have 11 images and 3 frames for each
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10)) #health box
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            # pygame.draw.rect(win, (255,0,0), self.hitbox,2)

    def move(self): #as the enemy should change his direction time to time this method is used
        if self.vel > 0: #right movement
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else: #left movement
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1 #if player hits
        else:
            self.visible = False
        print('hit')


def redrawGameWindow():
    win.blit(bg, (0, 0))  #we r going to fill this window with background so blit function is used
    text = font.render('Score: ' + str(score), 1, (0, 255, 0)) #renders thw new twxt (0,0,0)--->black
    win.blit(text, (390, 10)) #text,position
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()


# mainloop
font = pygame.font.SysFont('comicsans', 30, True) #for drawing some text in pygame ("font name",size,bold,italic)
man = player(200, 410, 64, 64)    #instance of the player
goblin = enemy(100, 410, 64, 64, 450)
shootLoop = 0
bullets = []
run = True
while run:
    clock.tick(27)
    if man.hitbox[1]  < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:  # here we are checking the same but for the x coordinate
            man.hit()  # if conditions are satisfied we call this method
            score -= 5  # score dec when we hit the gblin


    if shootLoop > 0: #this is done to have a break between the bullts i.e.., one by one
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get(): #event is something done by the user like movement of the mouse
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + \
                    goblin.hitbox[2]:  #here we are checking the same but for the x coordinate
                goblin.hit() #if conditions are satisfied we call this method
                score += 1 #score inc when we hit the gblin
                bullets.pop(bullets.index(bullet))  #when bullets got hit to the goblun they disappear

        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed() #instructions from the user

    if keys[pygame.K_SPACE] and shootLoop == 0:
        bulletSound.play() #plays the sound when we release a bullet
        if man.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 5:
            bullets.append(
                projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (0, 0, 0), facing))

        shootLoop = 1

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel: #here we are constraining the area of the window
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0

    if not (man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    redrawGameWindow()

pygame.quit()
