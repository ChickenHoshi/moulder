import pygame, sys, math, random, time
from pygame.locals import*

pygame.init()
FPS = 60
fpsClock = pygame.time.Clock()
#set up window
scale = .5
windowX, windowY = int(1280*scale),int(800*scale)
WXh,WYh = windowX//2, windowY//2
DISPLAYSURF = pygame.display.set_mode((windowX,windowY),DOUBLEBUF)
flags=DISPLAYSURF.get_flags()
pygame.display.set_caption('Game')

#set up colors

BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0,200,0)
BROWN = (100,100,0)
RED = (200,0,0)
BLUE = (0,0,200)

'''
 _______ _       _______ _______ _______ _______ _______ 
(  ____ ( \     (  ___  (  ____ (  ____ (  ____ (  ____ \
| (    \| (     | (   ) | (    \| (    \| (    \| (    \/
| |     | |     | (___) | (_____| (_____| (__   | (_____ 
| |     | |     |  ___  (_____  (_____  |  __)  (_____  )
| |     | |     | (   ) |     ) |     ) | (           ) |
| (____/| (____/| )   ( /\____) /\____) | (____//\____) |
(_______(_______|/     \\_______\_______(_______\_______)
                                                         
'''

class Game():
     def __init__(self,name):
          self.name = name
          self.mpos = (0,0)
          self.lmb = False
          self.keys = False
          self.time = 0
     def update(self, fpsClock):
          if self.time < 1200: self.time += 1
          else: self.time  =0
          if self.time%60==0: pygame.display.set_caption(self.name+' | '+str(int(fpsClock.get_fps()))+' FPS')
          self.mpos = pygame.mouse.get_pos()
          self.lmb = pygame.mouse.get_pressed()[0]
          self.keys = pygame.key.get_pressed()
          
class Vector2(object):
     def __init__(self, x=0.0, y=0.0):
          self.x = x
          self.y = y
     def __str__(self):
          return "(%s, %s)"%(self.x, self.y)
     @classmethod
     def from_points(cls, P1, P2):
          return cls( P2[0] - P1[0], P2[1] - P1[1] )
     def get_magnitude(self):
          return math.sqrt( self.x**2 + self.y**2 )
     def normalize(self):
          magnitude = self.get_magnitude()
          self.x /= magnitude
          self.y /= magnitude
     def __add__(self, rhs):
          if isinstance(rhs, Vector2):
               return Vector2(self.x + rhs.x, self.y + rhs.y)
          else:
               return Vector2(self.x + rhs[0], self.y + rhs[1])
     def __sub__(self, rhs):
          if isinstance(rhs, Vector2):
               return Vector2(self.x - rhs.x, self.y - rhs.y)
          else:
               return Vector2(self.x - rhs[0], self.y - rhs[1])
     def __neg__(self, rhs):
          return Vector2(-self.x, -self.y)
     def __mul__(self, scalar):
          return Vector2(self.x * scalar, self.y * scalar)
     def __truediv__(self, scalar):
          return Vector2(self.x / scalar, self.y / scalar)
     def get_tuple(self):
          return (self.x, self.y)



class MouldSquare():
     def __init__(self, pos = Vector2(100,100), resolution = Vector2(36,24), size = Vector2(300,200)):
          self.pos = pos
          self.res = resolution
          self.size = size
          self.points = []
          self.makePoints()
     def makePoints(self):
          w = self.size.x / self.res.x
          h = self.size.y / self.res.y
          for i in range(self.res.y + 1):
               self.points.append([])
               for j in range(self.res.x + 1):
                    x = self.pos.x + j * w
                    y = self.pos.y + i * h
                    self.points[-1].append(ProtoMaterial(Vector2(x,y)))
     def draw(self, mode = 1):
          if mode == 1:
               for row in range(len(self.points)-1):
                    for col in range(len(self.points[row])-1):
                         pygame.draw.polygon(DISPLAYSURF, self.get_color(row,col), (
                                   self.points[row][col].pos.get_tuple(),
                                   self.points[row + 1][col].pos.get_tuple(),
                                   self.points[row + 1][col + 1].pos.get_tuple(),
                                   self.points[row][col + 1].pos.get_tuple(),
                              ))
##          elif mode == 2:
##               for col in range(len(self.points[0])-1):
##                    pygame.draw.line(DISPLAYSURF,BLACK,self.points[0][col].get_tuple()
##                                     ,self.points[0][col + 1].get_tuple())
##                    pygame.draw.line(DISPLAYSURF,BLACK,self.points[self.res.y][col].get_tuple()
##                                     ,self.points[self.res.y][col + 1].get_tuple())
##               for row in range(len(self.points)-1):
##                    pygame.draw.line(DISPLAYSURF,BLACK,self.points[row][0].get_tuple()
##                                     ,self.points[row+1][0].get_tuple())
##                    pygame.draw.line(DISPLAYSURF,BLACK,self.points[row][self.res.x].get_tuple()
##                                     ,self.points[row+1][self.res.x].get_tuple())
     def update(self):
          for row in range(len(self.points)):
               for col in range(len(self.points[row])):
                    if self.points[row][col].temp > 273: self.points[row][col].temp -= (self.points[row][col].temp-273)*.001
                    elif self.points[row][col].temp < 273: self.points[row][col].temp -= (self.points[row][col].temp-273)*.001
                    if self.points[row][col].temp < 273 < 1: self.points[row][col].temp  = 1
                    if self.points[row][col].pos.y < 20: self.points[row][col].pos.y = 20
                    if self.points[row][col].pos.y > windowY - 20: self.points[row][col].pos.y = windowY - 20
                    if self.points[row][col].pos.x < 20: self.points[row][col].pos.x = 20
                    if self.points[row][col].pos.x > windowX - 20: self.points[row][col].pos.x = windowX - 20
     def get_color(self,row, col):
          n = (self.points[row][col].temp + self.points[row+1][col].temp +\
              self.points[row+1][col+1].temp + self.points[row][col+1].temp)/4
          if n > 500: n = 500
          elif n < 0: n = 0
          c = n/500*255
          return (c,c,c)
               
          
                    
                    
class ProtoMaterial():
     def __init__(self, pos = Vector2(), temp = 273):
          self.pos = pos
          self.temp = temp
     
               
                  


'''        
 _______         _       _______________________________ _       _______ 
(  ____ |\     /( (    /(  ____ \__   __\__   __(  ___  ( (    /(  ____ \
| (    \| )   ( |  \  ( | (    \/  ) (     ) (  | (   ) |  \  ( | (    \/
| (__   | |   | |   \ | | |        | |     | |  | |   | |   \ | | (_____ 
|  __)  | |   | | (\ \) | |        | |     | |  | |   | | (\ \) (_____  )
| (     | |   | | | \   | |        | |     | |  | |   | | | \   |     ) |
| )     | (___) | )  \  | (____/\  | |  ___) (__| (___) | )  \  /\____) |
|/      (_______|/    )_(_______/  )_(  \_______(_______|/    )_\_______)
                                                                         
'''

def hammer(size, pointList, heat = False, cool = False):
     m = Vector2(G.mpos[0],G.mpos[1])
     for row in range(len(pointList)):
          for col in range(len(pointList[row])):
               dp = pointList[row][col].pos-m
               dmag = dp.get_magnitude()
               if dmag == 0: dmag = 0.001
               if heat:
                    pointList[row][col].temp += 100/(dmag)
               elif cool:
                    pointList[row][col].temp -= 100/(dmag)
               else:
                    pointList[row][col].pos += dp*(900/(dmag*900000000/(pointList[row][col].temp*100)))

G = Game('Moulder')
def main():
     global flags
     m = MouldSquare()



     
     
     while True: ##main game loop
          G.update(fpsClock)
          if G.lmb:
               hammer(50, m.points)

          elif G.keys[K_SPACE]:
               hammer(50, m.points, True)
          elif G.keys[K_c]:
               hammer(50, m.points, cool = True)
          m.update()
          DISPLAYSURF.fill(WHITE)
          m.draw()
          for event in pygame.event.get():
               if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                         pass
                    if event.key == K_ESCAPE:
                         pygame.quit()
                         sys.exit()
                    if event.key == K_f:
                         if flags&FULLSCREEN == False:
                              flags |= FULLSCREEN
                              pygame.display.set_mode((windowX,windowY), flags)
                         else:
                              flags ^= FULLSCREEN
                              pygame.display.set_mode((windowX,windowY), flags)
               if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1: #LMB
                         pass
               if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
          pygame.display.update()
          fpsClock.tick(FPS)


if __name__ == '__main__':
     main()
