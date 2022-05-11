from pygame import *
from random import randint

lost = 0

font.init()
font = font.SysFont('Arial', 40)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_widht, player_height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_widht, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y        
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):        
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, 45)
        bullets.add(bullet)
        
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

score = 0            

player = Player("rocket.png", 300, 375, 5, 80, 100)
win_width = 700
win_height = 500

window = display.set_mode((700, 500))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))

clock = time.Clock()
FPS = 60

bullets = sprite.Group()

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy("ufo.png", randint(80, win_width - 80), 0, randint(1, 6), 80, 50)
    monsters.add(monster)

game = True
finish = False

#font1 = font.SysFont('Arial', 40)
win = font.render('YOU WIN', True, (255, 215, 0))
lose = font.render('YOU LOSE', True, (255, 0, 0))
text_lose = font.render("Пропущено: " + str(lost), 1, (255, 255, 255))
text_score = font.render("Убито: " + str(score), 1, (255, 255, 255))


mixer.init()
mixer.music.load('space.ogg')
#mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

while game:

    for e in event.get():
        if e.type == QUIT:
            game = False 
        
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()

    if finish != True:
        window.blit(background,(0, 0))
        text_lose = font.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        text_score = font.render("Убито: " + str(score), 1, (255, 255, 255))
        window.blit(text_score, (10, 20))
        player.reset()
        player.update() 
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)

        colliders = sprite.groupcollide(monsters, bullets, True, True)
        for c in colliders:
            score = score + 1
            monster = Enemy("ufo.png", randint(80, win_width - 80), -40, randint(1,5), 80, 50)
            monsters.add(monster)

        if lost > 5:
            window.blit(lose, (200, 200))
            finish = True
        if score > 20:
            window.blit(win, (200, 200))
            finish = True

    clock.tick(FPS)

    display.update()