import random, os
import pygame
from pygame.locals import *
import math
import random

screenWidth, screenHeight = 640, 480
 
def load_image(file_name, colorkey=None):
  full_name = os.path.join('data', file_name)

  try:
    image = pygame.image.load(full_name)
  except pygame.error as message:
    print('Cannot load image:', full_name)
    raise SystemExit(message)

  image = image.convert()

  if colorkey is not None:
    if colorkey is -1:
      colorkey = image.get_at((0,0))
    image.set_colorkey(colorkey, RLEACCEL)

  return image, image.get_rect()


def load_sound(name):
  class No_Sound:
    def play(self): pass

  if not pygame.mixer or not pygame.mixer.get_init():
    return No_Sound()

  #fullname = os.path.join('data', name)
  fullname = os.path.join('data', name)
  if os.path.exists(fullname):
    sound = pygame.mixer.Sound(fullname)
  else:
    print('File does not exist:', fullname)
    return No_Sound

  return sound

class Params(object):

  def __init__(self, params=dict(), **args):
    self.m_params=params
    self.m_params.update(args)

  def initParam(self, name, default=None):
    self.m_params.setdefault(name,default)
    return self.m_params[name]

  def getParam(self, name, default=None):
    self.m_params.get(name,default)
    return self.m_params[name]

  def setParam(self, name, value):
    self.m_params[name] = value
    return self.m_params[name]
   
class Object2D(pygame.sprite.Sprite, Params):

  def __init__(self, params=dict(), **args):
    params.update(args)
    Params.__init__(self, params)
    pygame.sprite.Sprite.__init__(self) #call Sprite initalizer

  def moveAbs(self,x,y):
    pass

  def moveRel(self,x,y):
    self.rect.move_ip((x,y))

  def initImages(self, name, frames = 4, speed = 5):
    self.imageFrameCount = self.initParam('imageFrameCount', frames)
    self.imageList = []

    for x in range(self.imageFrameCount):
      im, r = load_image('%s%d.bmp' % (name, x+1), -1)
      if x == 0: rect = r
      self.imageList.append(im)
      
    self.imageSpeed = self.initParam('imageSpeed', speed)
    self.imageIncr = 0
    self.imageFrame = 0
    image = self.imageList[self.imageFrame]
    return image, rect 

  def updateImage(self):
      self.imageIncr += 1
      if  self.imageIncr >= self.imageSpeed:
        self.imageFrame += 1
        if self.imageFrame >= self.imageFrameCount:
          self.imageFrame = 0
        self.image = self.imageList[self.imageFrame]
        self.imageIncr = 0
        return self.image

class Ship(Object2D):
  """This class is for the players ship"""
  
  def __init__(self, params=dict(), **args):
    params.update(args)
    super(Ship, self).__init__(params) #call Sprite initalizer
    self.image, self.rect = self.initImages('char/good')
    self.rect.center = (320,450)
    self.x_velocity = 0
    self.y_velocity = 0
    self.speed = 8

  def moveUp(self):
    self.y_velocity = self.speed * -1

  def moveDown(self):
    self.y_velocity = self.speed

  def moveLeft(self):
    self.x_velocity = self.speed * -1

  def moveRight(self):
    self.x_velocity = self.speed

  def update(self):
    self.updateImage()
    self.moveRel(self.x_velocity, self.y_velocity)

    if self.rect.left < 0:
      self.rect.left = 0
    elif self.rect.right > screenWidth:
      self.rect.right = screenWidth

    if self.rect.top <= 260:
      self.rect.top = 260
    elif self.rect.bottom >= screenHeight:
      self.rect.bottom = screenHeight


class Enemy(Object2D):
  """This class is for the enemy ships"""

  Xcenter = int(screenWidth/2)
  MAX_ANGLE = 25

  def __init__(self, params=dict(), **args):
    params.update(args)
    super(Enemy, self).__init__(params)
    self.image, self.rect = self.initImages('enemy/bad')
    self.maxDev = .1
    self.startX = self.initParam('startX', int(screenWidth/2) )
    self.prev = self.startX
    self.direction = 1
    self.speed = .5
    self.angle = random.randint(1, Enemy.MAX_ANGLE)
    self.rect.centerx = self.startX
    self.rect.centery = 50
    self.x_velocity = 0
    self.y_velocity = 0

  def update(self):
    #movement
   
    #choose graphic
    self.updateImage()
     
    # y coord
    self.y_velocity = self.speed + math.sin(self.angle) * 3
    
    # x coord
    moveX = Enemy.Xcenter * math.sin(self.angle) * math.exp(-.1 * self.angle)
    temp = self.startX + self.direction * moveX
    self.x_velocity = temp - self.prev
    self.prev = temp
    self.angle = self.angle + (self.maxDev * self.direction); # change horizontal pos

    if (self.angle > self.MAX_ANGLE) or (self.angle < 1):
      self.direction = -self.direction

    self.moveRel(self.x_velocity, self.y_velocity)

    if self.rect.left < 0:
      self.rect.left = 0
    elif self.rect.right > screenWidth:
      self.rect.right = screenWidth

    if self.rect.top <= 0:
      self.rect.top = 0
    elif self.rect.bottom >= screenHeight:
      self.rect.bottom = screenHeight

    #random 1 - 60 determines if firing
    fire=random.randint(1,300)
    if fire == 1:
      ebomb_sprites.add(Bomb(self.rect.midbottom))
      pygame.mixer.Channel(1).play(EnemyFire)

class Fire(Object2D):
  """This class is for the players weapons"""

  def __init__(self, startpos, params=dict(), **args):
    params.update(args)
    super(Fire, self).__init__(params)
    self.image, self.rect = load_image('char/bullet1.bmp', -1)
    self.rect.center = startpos
    self.speed = -8
    #self.CharFire = load_sound(os.path.join("char", "CharFire1.wav"))
    #self.CharFire.play()
 
  def update(self):
    if self.rect.bottom <= 0:
      self.kill()
    else:
      self.rect.move_ip((0, self.speed))

class Rocket(Object2D):
  """This class is for the players weapons"""

  def __init__(self, startpos, params=dict(), **args):
    params.update(args)
    super(Rocket, self).__init__(params)
    self.image, self.rect = self.initImages('char/rocket')
    self.rect.center = startpos
    self.speed = -4
    self.speedIncr = -1
    self.maxCounter = 5
    self.count = 0

  def update(self):
    self.updateImage()
    if self.rect.bottom <= 0:
      self.kill()
    else:
      self.count += 1
      if self.count <= self.maxCounter:
        self.count=0
        self.speed += self.speedIncr
      self.rect.move_ip((0, self.speed))

class Bomb(Object2D):
  """This class is for the enemies weapons"""

  def __init__(self, startpos, params=dict(), **args):
    params.update(args)
    super(Bomb, self).__init__(params)
    self.image, self.rect = self.initImages('enemy/bomb')
    self.rect.midtop = startpos
    #self.EnemyFire =load_sound(os.path.join("enemy", "enemyFire1.wav"))
    #self.EnemyFire.play()

  def update(self):
    self.updateImage()
    if self.rect.bottom >= screenHeight:
      self.kill()
    else:
      self.rect.move_ip((0, 4))

def main():
  random.seed()
  pygame.init()
  pygame.mixer.init(channels=5)

  pygame.display.set_caption('Space Game')
  pygame.mouse.set_visible(False)

  screen = pygame.display.set_mode((screenWidth, screenHeight),  pygame.RESIZABLE)
  background_image, background_rect = load_image('stars.bmp')
  screen.blit(background_image, (0,0))

  explode1 =load_sound(os.path.join("char", "explode1.wav"))
  explode2 =load_sound(os.path.join("enemy", "explode1.wav"))
  global CharFire, EnemyFire
  CharFire = load_sound(os.path.join("char", "CharFire1.wav"))
  #shot1 =load_sound(os.path.join("enemy", "enemyFire1.wav"))
  EnemyFire =load_sound(os.path.join("enemy", "enemyFire1.wav"))

  ship = Ship()
  playership_sprite = pygame.sprite.RenderClear()
  bomb_sprites = pygame.sprite.RenderClear()
  rocket_sprites = pygame.sprite.RenderClear()
  enemyship_sprites = pygame.sprite.RenderClear()
  
  global ebomb_sprites
  ebomb_sprites = pygame.sprite.RenderClear()

  font = pygame.font.Font(None, 36)
  running = 1
  counter = 0
  wave = 1
  score, prevScore = 0, 0
  waveFinished = False
  numberof_hits = 0
 
  while running:
    numberof_shots = 0
    enemy_killed = 0
    deathCount = 0

    for bad in range(wave*3):
      enemyship_sprites.add(Enemy(startX = random.randint(10, screenWidth), angle = random.randint(1, Enemy.MAX_ANGLE)))

    playership_sprite.add(ship)
    playerHit = False
    #explode2.play()

    while not waveFinished:
      text = font.render("score %d" % (prevScore), 1, (255, 10, 10))
      textpos = text.get_rect()
      textpos.centerx = background_image.get_rect().centerx
      background_image.blit(text, textpos)
      pygame.time.delay(30)
  
      if not playerHit:
        for event in pygame.event.get():
              if event.type == QUIT:
                running = 0
              elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                  running = 0
                elif event.key == K_LEFT:
                  ship.moveLeft()
                elif event.key == K_RIGHT:
                  ship.moveRight()
                elif event.key == K_UP:
                  ship.moveUp()
                elif event.key == K_DOWN:
                  ship.moveDown()
                elif event.key == K_f:
                  if len(bomb_sprites) < 4:
                    bomb_sprites.add(Fire(ship.rect.midtop))
                    numberof_shots += 1
                    pygame.mixer.Channel(0).play(CharFire)
                elif event.key == K_g:
                  if len(rocket_sprites) < 3:
                    rocket_sprites.add(Rocket(ship.rect.midtop))
                    numberof_shots += 1
                    pygame.mixer.Channel(1).play(CharFire)
              elif event.type == KEYUP:
                if event.key == K_LEFT:
                  ship.x_velocity = 0
                elif event.key == K_RIGHT:
                  ship.x_velocity = 0
                elif event.key == K_UP:
                  ship.y_velocity = 0
                elif event.key == K_DOWN:
                  ship.y_velocity = 0
  
      counter += 1
      if counter >= 200:
        enemyship_sprites.add(Enemy(startX = random.randint(10, screenWidth), angle = random.randint(1, Enemy.MAX_ANGLE)))
        counter = 0
  
      ebomb_sprites.clear(screen, background_image)
      enemyship_sprites.clear(screen, background_image)
      bomb_sprites.clear(screen, background_image)
      playership_sprite.clear(screen, background_image)
      rocket_sprites.clear(screen, background_image)
  
      bomb_sprites.update()
      playership_sprite.update()
      ebomb_sprites.update()
      enemyship_sprites.update()
      rocket_sprites.update()
  
      #See if players fire hit any enemy ships
      for hit in pygame.sprite.groupcollide(enemyship_sprites, bomb_sprites, 1, 1):
        pygame.mixer.Channel(2).play(explode1)
        enemy_killed += 1
        score += 100
  
      #See if players rocket hit any enemy ships
      for hit in pygame.sprite.groupcollide(enemyship_sprites, rocket_sprites, 1, 1):
        pygame.mixer.Channel(3).play(explode1)
        enemy_killed += 1
        score += 500
  
      if not playerHit:
        for hit in list(pygame.sprite.groupcollide(ebomb_sprites, playership_sprite, 1, 0).keys()):
          numberof_hits += 1
          playerHit = True
          pygame.mixer.Channel(4).play(explode2)

        for hit in list(pygame.sprite.groupcollide(enemyship_sprites, playership_sprite, 1, 0).keys()):
          numberof_hits += 1
          playerHit = True
          pygame.mixer.Channel(4).play(explode2)
        
      if enemyship_sprites.sprites() == []:
        waveFinished = True;
        
      if playerHit:
        ship.x_velocity = 0
        ship.y_velocity = 0
        deathCount += 1
        if deathCount > 100:
          waveFinished = True

      screen.blit(background_image, (0,0))
      text = font.render("score %d" % (prevScore), 1, (0,0,0))
      textpos = text.get_rect()
      textpos.centerx = background_image.get_rect().centerx
      background_image.blit(text, textpos)
      text = font.render("score %d" % (score), 1, (255, 10, 10))
      prevScore = score
      textpos = text.get_rect()
      textpos.centerx = background_image.get_rect().centerx
      background_image.blit(text, textpos)

      ebomb_sprites.draw(screen)
      bomb_sprites.draw(screen)
      enemyship_sprites.draw(screen)
      playership_sprite.draw(screen)
      rocket_sprites.draw(screen)
    
      pygame.display.flip()
  
    pygame.time.delay(5000)

    if not playerHit:
      wave +=1

    screen.blit(background_image, (0,0))
    pygame.display.flip()
    
    ebomb_sprites.empty()
    bomb_sprites.empty()
    enemyship_sprites.empty()
    playership_sprite.empty()
    rocket_sprites.empty()
    
    waveFinished = False

    if numberof_hits >= 3:
      running = False

  pygame.time.delay(3000)
  screen = pygame.display.set_mode((screenWidth, screenHeight))

  

if __name__ == '__main__':
  main()
