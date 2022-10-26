import pygame, math, random
pygame.init()

WHITE = (255,255,255)
width = 1280
height = 800
nRays = 1
nWalls = 3

class Wall():
    def __init__(self,a,b
                #a = (random.randint(0, width), random.randint(0, height)),
                #b = (random.randint(0, width), random.randint(0, height))
                ):
        self.a = tuple(a)
        self.b = tuple(b)

    def show(self,screen):
        pygame.draw.line(screen, WHITE, self.a, self.b)

class Ray():
    def __init__(self, pos1, pos2, angle):
        self.x1 = pos1[0]
        self.y1 = pos1[1]
        self.pos1 = pos1
        self.x2 = pos2[0]
        self.y2 = pos2[1]
        self.pos2 = pos2
        self.angle = angle

    def show(self, screen):
        pygame.draw.line(screen, WHITE, self.pos1, self.pos2)



class Particle():
    def __init__(self):
        self.x = width/2
        self.y = height/2
        self.pos = (self.x, self.y)
        self.rays = [(self.x + math.cos(math.radians(angle)),
                    self.y + math.sin(math.radians(angle))) for angle in range(0, 360, nRays)]

    def update(self):
        self.x = pygame.mouse.get_pos()[0]
        self.y = pygame.mouse.get_pos()[1]
        self.pos = (self.x, self.y)
        self.rays = [(self.x + math.cos(math.radians(angle)),
                      self.y + math.sin(math.radians(angle))) for angle in range(0, 360, nRays)]

    def show(self,screen, walls):
        pygame.draw.circle(screen, WHITE, pygame.mouse.get_pos(), 10)

        for ray in self.rays:
            closest = None
            record = math.inf
            for wall in walls:
                pt = self.cast(wall, ray)
                if pt:
                    d = math.hypot(self.x - pt[0], self.y - pt[1])
                    if d < record:
                        record = d
                        closest = pt

            if closest:    
                pygame.draw.line(screen, WHITE, self.pos, closest)

    def cast(self, wall, ray):
        x1 = wall.a[0]
        y1 = wall.a[1]
        x2 = wall.b[0]
        y2 = wall.b[1]

        x3 = self.x
        y3 = self.y
        x4 = ray[0]
        y4 = ray[1]

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if den == 0:
            return None
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
        if (t > 0 and t < 1 and u > 0):
            pt = (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
            return pt
        else:
            return None
        


class Game():
    def __init__(self):                
        self.walls = [
            Wall((random.randint(0, width), random.randint(0, height)), (random.randint(0, width), random.randint(0, height))) 
            for _ in range(nWalls)]
        #"""
        self.walls.append(Wall((-2,-1),(width,0)))
        self.walls.append(Wall((width, 0), (width, height)))
        self.walls.append(Wall((0, height), (width, height)))
        self.walls.append(Wall((-1, 0), (0, height)))
        #"""
        self.particle = Particle()
        self.screen = pygame.display.set_mode([width, height])

        self.running = True

    def run(self):
        pygame.mouse.set_visible(False)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.update()
            self.show(self.screen)

        pygame.quit()

    def update(self):
        self.particle.update()
    
    def show(self,screen):
        self.screen.fill((0, 0, 0))

        self.particle.show(screen, self.walls)
        for wall in self.walls:
            wall.show(screen)

        pygame.display.flip()

game = Game()
game.run()
