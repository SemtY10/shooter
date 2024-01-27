#Створи власний Шутер!

from pygame import *
from random import randint
from time import time as timer

W, H = 700, 500
win = display.set_mode((W, H))
display.set_caption("Maze")

bg = transform.scale (image.load("galaxy.jpg"), (W, H))
#FPS = 15
clock = time.Clock()
 
#TODO CLASSES
class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h, speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(img),(w,h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
 
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player (GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys [K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys [K_RIGHT] and self.rect.y < H - 70:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(bullet_img, self.rect.centerx, self.rect.top, 15, 20,15)
        bullets.add(bullet)             
    

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > H:
            self.rect.x = randint(80, W-160)
            self.rect.y = -60
            lost = lost +1
            
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


clock = time.Clock()
FPS = 60
game = True
finish = False

#TODO Images
player_img="rocket.png"
ufo_img= "ufo.png"
bullet_img= "bullet.png"
asteroid_img= "asteroid.png"
# TODO MUSIC
mixer.init()
volume_value = 0.5
mixer.music.set_volume(volume_value)
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")
#TODO FONTS
font.init()
text_1 = font.SysFont('Arial', 30)
text_2 = font.SysFont('Arial', 72)
text_win = text_2.render("YOU WIN", 1,(0,255,0))
text_lose = text_2.render("ALIENS WIN", 1,(150,0,0))

#TODO SPRITES
player = Player(player_img, 300, H-100, 80, 100, 10)

#TODO GROUPS
max_enemy = 6
aliens = sprite.Group()
for i in range(1, max_enemy):
    alien = Enemy(ufo_img, randint(80,W-160), -60, 80,50,randint(1,5))
    aliens.add(alien)
    
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy(asteroid_img, randint(80, W-160), -60, 80, 50, randint(1,7))
    asteroids.add(asteroid)

#TODO GAME
lost = 0
score = 0
game = True
finish = False
goal = 10
max_lost = 3
num_fire = 0
rel_time = False
life = 3
while game:
    win.blit (bg, (0, 0))
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    player.fire()
                    
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
                    
            if e.key == K_KP_MINUS and volume_value>0.1:
                volume_value -=0.1
                mixer.music.set_volume(volume_value)
                mixer.Sound.set_volume(fire_sound, volume_value)
            if e.key == K_KP_PLUS and volume_value<1:
                volume_value +=0.1
                mixer.music.set_volume(volume_value)
                mixer.Sound.set_volume(fire_sound, volume_value)
    
    if not finish:
        bullets.draw(win)
        bullets.update()
        player.update()
        player.reset()
        aliens.update()
        aliens.draw(win)
        asteroids.update()
        asteroids.draw(win) 
        
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = text_1.render("Reloading...", 1, (0, 0, 150))
                win.blit(reload,(250, H-100))
            else:
                num_fire = 0
                rel_time = False
        
        text_score = text_1.render(f"Score: {score}", 1,(255,255,255), (150,150,150))
        text_lost = text_1.render(f"Lost: {lost}", 1,(255,255,255), (150,150,150))
        win.blit(text_score, (10,20))
        win.blit(text_lost, (10,50))
    
        collides = sprite.groupcollide(aliens, bullets, True, True)
        for colide in collides:
            score += 1
            alien = Enemy(ufo_img, randint(80, W-160), -60, 80, 50, randint(1, 5))
            aliens.add(alien)
            
        if sprite.spritecollide(player, aliens, True) or sprite.spritecollide(player,asteroids,True):
            life -= 1
            
        if life == 0 or lost>= max_lost:
            finish = True
            win.blit(text_lose, (200, 200))
        
        if life == 3:
            life_color = (0,150,0)
        if life == 2:
            life_color = (150,150,0)
        if life == 1:
            life_color = (150,0,0)
            
        text_life = text_2.render(str(life), 1, life_color)
        win.blit(text_life, (W-50, 10))
            
        if score >= goal:
            finish = True
            win.blit(text_win, (200,200))
        
        
    else:
        finish = False
        score = 0
        lost = 0
        rel_time = False
        num_fire = 0
        life = 3
        for bullet in bullets:
            bullet.kill()
        for alien in aliens:
            alien.kill()
        for asteroid in asteroids:
            asteroid.kill()    
        time.delay(3000)
        for i in range(1, max_enemy):
            alien = Enemy(ufo_img, randint(80,W-160), -60, 80,50,randint(1,5))
            aliens.add(alien)
        for i in range(1,3):
            asteroid = Enemy(asteroid_img, randint(80, W-160), -60, 80, 50, randint(1,7))
            asteroids.add(asteroid)
        
        
    display.update()
    time.delay(50)
    #clock.tick(FPS)