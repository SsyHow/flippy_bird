import pygame 
from pygame.locals import * 
import random 
import gameState
import bird
import button
import pipe

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 936 

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

# Load images
bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png')
button_img = pygame.image.load('img/restart.png')

font = pygame.font.SysFont('Bauhaus 93', 60)

white = (255, 255, 255)
dark_blue = (0, 0, 102)

game_state = gameState.GameState()

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))



bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = bird.Bird(100, int(screen_height/2), game_state)
bird_group.add(flappy)
button = button.Button(screen_width//2 - 50, screen_height//2 - 100, button_img)

run = True 
while run:
    clock.tick(fps)
    screen.blit(bg, (0, 0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
 
    screen.blit(ground_img, (game_state.ground_scroll, 768))

    # Check the score
    if len(pipe_group) > 0:
        bird = bird_group.sprites()[0]
        first_pipe = pipe_group.sprites()[0]
        if bird.rect.left > first_pipe.rect.left and bird.rect.right < first_pipe.rect.right and not game_state.pass_pipe:
            game_state.pass_pipe = True 
        if game_state.pass_pipe and bird.rect.left > first_pipe.rect.right:
            game_state.score += 1
            game_state.pass_pipe = False

    draw_text(str(game_state.score), font, white, int(screen_width/2), 20)

    # Check for collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_state.game_over = True

    # Check if bird hit the ground
    if flappy.rect.bottom >= 768:
        game_state.game_over = True
        game_state.flying = False 

    if not game_state.game_over and game_state.flying:
        time_now = pygame.time.get_ticks()
        if time_now - game_state.last_pipe > game_state.pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = pipe.Pipe(screen_width, int(screen_height/2) + pipe_height, -1, game_state)
            top_pipe = pipe.Pipe(screen_width, int(screen_height/2) + pipe_height, 1, game_state)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            game_state.last_pipe = time_now

        # Scroll ground
        game_state.ground_scroll -= game_state.scroll_speed        
        if abs(game_state.ground_scroll) > 35:
            game_state.ground_scroll = 0

        pipe_group.update()

    # Check game over and reset
    if game_state.game_over:
        if button.draw():
            game_state.reset()
            pipe_group.empty()
            flappy.rect.x = 100
            flappy.rect.y = int(screen_height/2)
    if game_state.show_start_message:
        draw_text("Click to Start", font, dark_blue, screen_width//2 - 120, screen_height // 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
        if event.type == pygame.MOUSEBUTTONDOWN and not game_state.flying and not game_state.game_over:
            game_state.flying = True
            game_state.show_start_message = False

    pygame.display.update()

pygame.quit()
