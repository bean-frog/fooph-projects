import pygame
import math
import random

class Ball(pygame.sprite.Sprite):
    VELOCITY = 5 

    def __init__(self, x, y, radius=10, color=(255, 255, 255)):
        super().__init__()
        self.radius = radius

        # transparent surface
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(x, y))

        self.vx = Ball.VELOCITY
        self.vy = -Ball.VELOCITY

    def update(self, screen_rect):
        self.rect.x += self.vx
        self.rect.y += self.vy

        # bounce off side walls with very slight angle randomness
        if self.rect.left <= screen_rect.left or self.rect.right >= screen_rect.right:
            # keep ball within screen bounds
            if self.rect.left <= screen_rect.left:
                self.rect.left = screen_rect.left
            if self.rect.right >= screen_rect.right:
                self.rect.right = screen_rect.right
            
            self.vx = -self.vx

            # small angle randomness
            angle = math.atan2(self.vy, self.vx)
            delta = random.uniform(-0.05, 0.05) 
            angle += delta
            self.vx = Ball.VELOCITY * math.cos(angle)
            self.vy = Ball.VELOCITY * math.sin(angle)

        # bounce off top wall with slight angle randomness
        if self.rect.top <= screen_rect.top:
            self.rect.top = screen_rect.top
            self.vy = -self.vy
            # small angle randomness
            angle = math.atan2(self.vy, self.vx)
            delta = random.uniform(-0.05, 0.05)
            angle += delta
            self.vx = Ball.VELOCITY * math.cos(angle)
            self.vy = Ball.VELOCITY * math.sin(angle)
