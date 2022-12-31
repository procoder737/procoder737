import pygame as p
from pygame.locals import *
import sys as s
import random as r
import time as t
 
p.init()
vec = p.math.Vector2 #2 for two dimensional

HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60
 
FramePerSec = p.time.Clock()
 
displaysurface = p.display.set_mode((WIDTH, HEIGHT))

p.display.set_caption("Game")
 
class Player(p.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.surf = p.Surface((30, 30))
        self.surf.fill((255,255,0))
        self.rect = self.surf.get_rect()
   
        self.pos = vec((10, 360))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.jumping = False
        self.score = 0 
 
    def move(self):
        self.acc = vec(0,0.5)
    
        pressed_keys = p.key.get_pressed()
                
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
                 
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
         
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
             
        self.rect.midbottom = self.pos
 
    def jump(self): 
        hits = p.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
           self.jumping = True
           self.vel.y = -15
 
    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3
 
    def update(self):
        hits = p.sprite.spritecollide(self ,platforms, False)
        if self.vel.y > 0:        
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    if hits[0].point == True:   
                        hits[0].point = False   
                        self.score += 1          
                    self.pos.y = hits[0].rect.top +1
                    self.vel.y = 0
                    self.jumping = False
 
 
class platform(p.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = p.Surface((r.randint(50,100), 12))
        self.surf.fill((0,255,0))
        self.rect = self.surf.get_rect(center = (r.randint(0,WIDTH-10),
                                                 r.randint(0, HEIGHT-30)))
        self.speed = r.randint(-1, 1)
        
        self.point = True   
        self.moving = True
        
    
    def move(self):
        hits = self.rect.colliderect(P1.rect)
        if self.moving == True:  
            self.rect.move_ip(self.speed,0)
            if hits:
                P1.pos += (self.speed, 0)
            if self.speed > 0 and self.rect.left > WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH
 
 
def check(platform, groupies):
    if p.sprite.spritecollideany(platform,groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 40) and (abs(platform.rect.bottom - entity.rect.top) < 40):
                return True
        C = False
 
def plat_gen():
    while len(platforms) < 6:
        width = r.randrange(50,100)
        p  = platform()      
        C = True
         
        while C:
             p = platform()
             p.rect.center = (r.randrange(0, WIDTH - width),
                              r.randrange(-50, 0))
             C = check(p, platforms)
        platforms.add(p)
        all_sprites.add(p)
 
 
        
PT1 = platform()
P1 = Player()
 
PT1.surf = p.Surface((WIDTH, 20))
PT1.surf.fill((255,0,0))
PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))
 
all_sprites = p.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)
 
platforms = p.sprite.Group()
platforms.add(PT1)

PT1.moving = False
PT1.point = False   ##
 
for x in range(r.randint(4,5)):
    C = True
    pl = platform()
    while C:
        pl = platform()
        C = check(pl, platforms)
    platforms.add(pl)
    all_sprites.add(pl)
 
 
while True:
    P1.update()
    for event in p.event.get():
        if event.type == QUIT:
            p.quit()
            s.exit()
        if event.type == p.KEYDOWN:    
            if event.key == p.K_SPACE:
                P1.jump()
        if event.type == p.KEYUP:    
            if event.key == p.K_SPACE:
                P1.cancel_jump()

    if P1.rect.top > HEIGHT:
        for entity in all_sprites:
            entity.kill()
            t.sleep(1)
            displaysurface.fill((255,0,0))
            p.display.update()
            t.sleep(1)
            p.quit()
            s.exit()
 
    if P1.rect.top <= HEIGHT / 3:
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()
 
    plat_gen()
    displaysurface.fill((0,0,0))
    f = p.font.SysFont("Verdana", 20)     
    g  = f.render(str(P1.score), True, (123,255,0))   
    displaysurface.blit(g, (WIDTH/2, 10))   
     
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        entity.move()
 
    p.display.update()
    FramePerSec.tick(FPS)