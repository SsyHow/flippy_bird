
import pygame 
from pygame.locals import * 

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position, game_state):
        pygame.sprite.Sprite.__init__(self)
        self.game_state = game_state
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(self.game_state.pipe_gap/2)]
        else:
            self.rect.topleft = [x, y + int(self.game_state.pipe_gap/2)]
    
    def update(self):
        self.rect.x -= self.game_state.scroll_speed
        if self.rect.right < 0:
            self.kill()