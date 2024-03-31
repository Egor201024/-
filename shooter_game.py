#Создай собственный Шутер!
from pygame import *
from random import randint


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

    def collidepoint(self,x,y):
        return self.rect.collidepoint(x,y)

class Player(GameSprite):
    def update(self): 
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 700-5-self.rect.width:
            self.rect.x += self.speed

    def fire(self):
        y = self.rect.y
        x = self.rect.centerx
        bullet = Bullet('bullet.png',x,y,15,30,5)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500-self.rect.height:
            self.rect.x = randint(5,700-5-self.rect.width)
            self.rect.y = -self.rect.height
            self.speed = randint(1,3)
            lost +=1

class Storit(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500-self.rect.height:
            self.rect.x = randint(5,700-5-self.rect.width)
            self.rect.y = -self.rect.height
            self.speed = randint(1,3)



class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


window = display.set_mode((700,500))
display.set_caption('шутер')

background = transform.scale(image.load('galaxy.jpg'), (700,500))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play(-1)

font.init()
font1 = font.Font(None,36)
start = GameSprite('Start.png',300,225,100,50,0)
player = Player('rocket.png',316,400,68,100,7)
enemy_count = 5
enemyes = sprite.Group()
for i in range(enemy_count):
    enemy = Enemy('ufo.png', randint(5,700-5-90),-50,90,50, randint(1,3))
    enemyes.add(enemy)

storit_count = 3
storites = sprite.Group()
for i in range(enemy_count):
    storit = Storit('asteroid.png', randint(5,700-5-90),-50,90,50, randint(1,2))
    storites.add(storit)

bullets = sprite.Group()


game = True
finish = True
menu = True
lost = 0
score = 0
text=0
fond_lose = font1.render('Тебя скушали! :))',1, (250,0,0))
fond_lose2 = font1.render("В тебя врезался остероид",1, (250,0,0))
fond_win = font1.render('ТЫ всех уничтожел :) хаха',1, (0,250,0))

clock = time.Clock()
FPS = 60

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
    
    if menu == True:
        window.blit(background,(0,0))    
        start.reset()
        pressed = mouse.get_pressed()
        pos = mouse.get_pos()
        if pressed[0]:
            if start.collidepoint(pos[0],pos[1]):
                menu = False
                finish = False
        if text == 1:
            window.blit(fond_win,(250,175))
        elif text == 2:
            window.blit(fond_lose,(250,175))
        elif text == 3:
            window.blit(fond_lose2,(250,175))
        lost = 0 
        score=0
        enemyes.empty()
        for i in range(enemy_count):
            enemy = Enemy('ufo.png', randint(5,700-5-90),-50,90,50, randint(1,3))
            enemyes.add(enemy)
        storites.empty()
        for i in range(enemy_count):
            storit = Storit('asteroid.png', randint(5,700-5-90),-50,90,50, randint(1,2))
            storites.add(storit)
        bullets.empty()
        
    
    if finish != True:


        window.blit(background,(0,0))
        player.update()
        enemyes.update()
        bullets.update()
        storites.update()
        player.reset()
        enemyes.draw(window)
        bullets.draw(window)
        storites.draw(window)

        sprite_list1 = sprite.spritecollide(player,enemyes,False)
        if len(sprite_list1)> 0 or lost>10:
            text = 2
            finish=True
            menu = True

        
        sprite_list2 = sprite.spritecollide(player,storites,False)
        if len(sprite_list2):
            text = 3
            finish=True
            menu = True

        sprite_list = sprite.groupcollide(enemyes, bullets, True,True)
        for m in sprite_list:
            score+=1
            enemy = Enemy('ufo.png',randint(5, 700-5-70),-50,90,50, randint(1,3))
            enemyes.add(enemy)
        if score>999 :
            text = 1
            finish = True
            menu = True







        fond_lost = font1.render('Пропущено'+str (lost),1, (0,140,0))
        window.blit ( fond_lost , ( 10 , 50))
        fond_score = font1.render('Счет'+str (score),1, (0,140,0))
        window.blit ( fond_score , ( 10 , 5))



    display.update()
    clock.tick(FPS)
