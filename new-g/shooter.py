import pygame
import os

pygame.init()

screen_width = 800
screen_height = int(screen_width * 0.8)


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('shooter')

#set framerate
clock = pygame.time.Clock()
FPS = 60

#define gravity variable
GRAVITY = 0.75
#define player action variable
moving_left = False
moving_right = False

#define bg color
BG = (144, 201, 120)
RED = (255, 0, 0)

def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (screen_width, 300))

class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air =  True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0 
        self.update_time = pygame.time.get_ticks()
        #load all images for the players 
        animation_types = ['Idle', 'Run','Jump']
        for animation in animation_types:
            #reset temporaryt list of images
            temp_list = []
            #count number of files in the folder
            num_of_frames = len(os.listdir(f'new-g/img/{self.char_type}/{animation}'))

            for i in range(num_of_frames):
                img = pygame.image.load(f'new-g/img/{self.char_type}/{animation}/{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), (int(img.get_height()) * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        #jump n   
        if self.jump == True and self.in_air == False:
            self.vel_y  = -11
            self.jump = False
            self.in_air = True
        #apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y
        #check collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        #update the rect position
        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        #update anmation 
        ANIMATION_COOLDOWN = 100
        #update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enought time has passed since the lst updte
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
        
    def update_action(self, new_action):
        #check of ythe new action is different to the prevo=ious one
        if new_action != self.action:
            self.action = new_action
            #update the animation setting 
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False),self.rect)

player = Soldier('player',200, 200, 3, 5)
enemy = Soldier('enemy', 400, 200, 3, 6)


running = True

while running:

    clock.tick(FPS)
    
    draw_bg()

    player.update_animation()
    player.draw()
    enemy.draw()

    #update player actions
    if player.alive:
        if player.in_air:
            player.update_action(2)
        if moving_left or moving_right:
            player.update_action(1)# 1 means running
        else:
            player.update_action(0)#0 means idle

        player.move(moving_left, moving_right)
            
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            running = False
        #key pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                running = False
        #key released
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False

    pygame.display.update()
pygame.quit()