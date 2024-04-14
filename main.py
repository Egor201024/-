from pygame import *
from random import choice

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h, speed):
        super().__init__()
        self.image = transform.scale(image.load(img),(w,h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.h = h
        self.rect.w = w
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class roket1(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < 500-5-self.rect.height:
            self.rect.y += self.speed

class roket2(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 500-5-self.rect.height:
            self.rect.y += self.speed  

class Snow(GameSprite):
    def __init__(self, img,x,y,w,h,speed):
        super().__init__(img,x,y,w,h,speed)
        self.speed_x=0
        self.speed_y=0
    def set_direction(self,speed_x,speed_y):
        self.speed_x = speed_x
        self.speed_y = speed_y
    def update(self):
        self.rect.x +=self.speed_x*self.speed
        self.rect.y +=self.speed_y*self.speed

    def check_direction(self,pl1,pl2):
        global point_l, point_r
        if self.rect.y<=0:
            self.speed_y*=-1
        elif self.rect.y >=500-self.rect.height:
            self.speed_y*=-1
            print(self.speed_y)
        elif self.rect.colliderect(pl1.rect):
            self.speed_x*=-1
        elif self.rect.colliderect(pl2.rect):
            self.speed_x*=-1

        elif self.rect.x <=0:
            point_r += 1
            self.rect.x = 800/2-self.rect.width/2
            self.rect.y = 500/2-self.rect.height/2
            self.set_direction(choice([-1,1]), choice([-1,1]))

        elif self.rect.x >=800-self.rect.width:
            point_l += 1
            self.rect.x = 800/2-self.rect.width/2
            self.rect.y = 500/2-self.rect.height/2
            self.set_direction(choice([-1,1]), choice([-1,1]))

window = display.set_mode((800,500))
display.set_caption('шутер')

background = transform.scale(image.load('forst.jpg'), (800,500))

player1 = roket1('var.png',50,250,55,100,7)
player2 = roket2('var2.png',700,250,55,100,7)
point_l = 0
point_r = 0
direction = [-1,1]
snow = Snow('snow.png',800/2-25,500/2-25,75,40,2)
snow.set_direction(choice(direction),choice(direction))


clock = time.Clock()
FPS = 60


game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    

    window.blit(background,(0,0))    
    player1.update()
    player2.update()
    snow.update()
    player1.reset()
    player2.reset()  
    snow.check_direction(player1,player2)
    snow.reset()  
            
            
            
    display.update()
    clock.tick(FPS)