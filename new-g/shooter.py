import pygame

pygame.init()

screen_width = 800
screen_height = int(screen_width * 0.8)


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('shooter')

#set framerate
clock = pygame.time.Clock()
FPS = 60
#define player action variable
moving_left = False
moving_right = False

#define bg color
BG = (144, 201, 120)

def draw_bg():
    screen.fill(BG)

class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        for i in range(5):
            img = pygame.image.load(f'Shooter-main/new-g/img/{self.char_type}/Idle/{i}.png')
            img =  pygame.transform.scale(img, (int(img.get_width() * scale), (int(img.get_height()) * scale)))
            self.animation_list.append(img)
        self.image = self.animation_list[self.frame_index]
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
        #update the rect position
        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        #update anmation 
        ANIMATION_COOLDOWN = 100
        #update image depending on current frame
        self.image = self.animation_list[self.frame_index]
        #check if enought time has passed since the lst updte
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0
        

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
            if event.key == pygame.K_ESCAPE:
                running = False
        #key released
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    pygame.display.update()
pygame.quit()