import pygame
import sys

WIDTH, HEIGHT = 800, 600
GRAVITY = pygame.Vector2(0, 0.5)
FRICTION = 0.99

class Particle:
    def __init__(self, x, y, pinned=False):
        self.pos = pygame.Vector2(x, y)
        self.old_pos = pygame.Vector2(x, y)
        self.acceleration = pygame.Vector2(0, 0)
        self.pinned = pinned

    def update(self):
        if self.pinned:
            return
        velocity = (self.pos - self.old_pos) * FRICTION
        self.old_pos = self.pos.copy()
        self.pos += velocity + self.acceleration
        self.acceleration = pygame.Vector2(0, 0)

    def apply_force(self, force):
        if not self.pinned:
            self.acceleration += force

    def constrain(self):
        if self.pos.x < 0:
            self.pos.x = 0
        elif self.pos.x > WIDTH:
            self.pos.x = WIDTH
        if self.pos.y < 0:
            self.pos.y = 0
        elif self.pos.y > HEIGHT:
            self.pos.y = HEIGHT

class Spring:
    def __init__(self, p1, p2, rest_length):
        self.p1 = p1
        self.p2 = p2
        self.rest_length = rest_length

    def update(self):
        delta = self.p2.pos - self.p1.pos
        dist = delta.length()
        diff = (dist - self.rest_length) / dist
        if not self.p1.pinned:
            self.p1.pos += delta * 0.5 * diff
        if not self.p2.pinned:
            self.p2.pos -= delta * 0.5 * diff

class Cloth:
    def __init__(self, width, height, spacing):
        self.particles = []
        self.springs = []
        for y in range(height):
            row = []
            for x in range(width):
                pinned = y == 0 and x % 5 == 0
                p = Particle(x * spacing + 100, y * spacing + 100, pinned)
                row.append(p)
                self.particles.append(p)
                if x > 0:
                    self.springs.append(Spring(row[x - 1], p, spacing))
                if y > 0:
                    self.springs.append(Spring(self.particles[-width], p, spacing))
        
    def update(self):
        for p in self.particles:
            p.apply_force(GRAVITY)
            p.update()
        for s in self.springs:
            s.update()
        for p in self.particles:
            p.constrain()
    
    def draw(self, screen):
        for s in self.springs:
            pygame.draw.line(screen, (255, 255, 255), s.p1.pos, s.p2.pos, 1)
        for p in self.particles:
            pygame.draw.circle(screen, (255, 0, 0), p.pos, 3)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
cloth = Cloth(30, 20, 20)

last_mouse_pos = pygame.mouse.get_pos()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))
    
    current_mouse_pos = pygame.mouse.get_pos()
    mouse_movement = pygame.Vector2(current_mouse_pos) - pygame.Vector2(last_mouse_pos)
    last_mouse_pos = current_mouse_pos


    for p in cloth.particles:
        p.apply_force(mouse_movement * 0.1)

    cloth.update()
    cloth.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)
