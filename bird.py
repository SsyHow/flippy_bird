import pygame 
from pygame.locals import * 
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, game_state):
        pygame.sprite.Sprite.__init__(self)
        self.game_state = game_state
        self.images = []
        self.index = 0 
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'img/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y] 
        self.vel = 0 
        self.clicked = False
    
    def update(self):
        if self.game_state.flying:
            self.vel += 0.5 
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel) 
        
        if not self.game_state.game_over:
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False 

            # Animation
            self.counter += 1
            flap_cooldown = 5 
            if self.counter > flap_cooldown:
                self.counter = 0 
                self.index = (self.index + 1) % len(self.images)
            
            # Rotate
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)