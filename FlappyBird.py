import pygame
from pygame.locals import *
import random
import time

pygame.init()

clock = pygame.time.Clock()
fps = 60
screen_width = 1280
screen_height = 1024

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

#define font
font = pygame.font.SysFont('Open Sans', 90)

#define colors
bird_color = (250, 58, 26)

#define game variables
ground_scroll = 0
scroll_speed = 5
flying = False
game_over = False
pipe_gap = 300
pipe_frequency = 1500 #milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False
play_once = 0
click_twice = 0
daily_high_score = 0

with open("high_score.txt", "r") as file:
    high_score = int(file.read())

with open("games_played.txt", "r") as file:
    games_played = int(file.read())

with open("time_achieved.txt", "r") as file:
    time_achieved = file.read()
    print(time_achieved)

#load images
bg = pygame.image.load('img/bg.png').convert_alpha()
ground_img = pygame.image.load('img/ground.png').convert_alpha()
button_img = pygame.image.load('img/restart.png').convert_alpha()

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2) - 184
    score = 0

    return score

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = self.image = pygame.image.load(f'img/bird{num}.png').convert_alpha()
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):

        if flying == True:
            #gravity
            self.vel += 0.75
            if self.vel > 12:
                self.vel = 12
            if self.rect.bottom < 840:
                self.rect.y += int(self.vel)

        if game_over == False:
            #jump
            if pygame.key.get_pressed()[K_SPACE] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -12.5
                jump = pygame.mixer.music.load('img/jump.wav')
                pygame.mixer.music.play()
            if pygame.key.get_pressed()[K_SPACE] == 0:
                self.clicked = False

            #handle the animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            #rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png').convert_alpha()
        self.rect = self.image.get_rect()
        #position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2) + score * 2 / 3]

        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2) - score * 2 / 3]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):

        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()
        
        #check if mouse is over the button
        if pygame.key.get_pressed()[K_SPACE] == 1:
            action = True

        #draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2) - 184)

bird_group.add(flappy)

#create restart button instance
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)

run = True
while run:
    clock.tick(fps)

    #draw background
    screen.blit(bg, (0,0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    #draw the ground
    screen.blit(ground_img, (ground_scroll, 840))

    #check for score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
                progress = pygame.mixer.music.load('img/progress.wav')
                pygame.mixer.music.play()
                

    draw_text("Score: " + str(score), font, bird_color, int(screen_width / 2) - 500, 30)

    draw_text("Daily High Score: " + str(daily_high_score), font, bird_color, int(screen_width / 2) - 50, 30)

    draw_text("High Score: " + str(high_score), font, bird_color, int(screen_width / 2) - 600, screen_height - 105)

    draw_text("Games Played: " + str(games_played), font, bird_color, int(screen_width / 2), screen_height - 90)

    draw_text("Time Achieved: " + time.ctime(int(time_achieved)), pygame.font.SysFont('Open Sans', 33), bird_color, int(screen_width / 2) - 600, screen_height - 35)

    #look for collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    #check if bird has hit the ground
    if flappy.rect.bottom >= 840:
        game_over = True
        flying = False
   
    if game_over == False and flying == True:

        #generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-score - 50, score + 50)
            btm_pipe = Pipe(screen_width, int(screen_height / 2 - 82) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2 - 82) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        #draw and scroll the ground
        ground_scroll -= scroll_speed
        if (scroll_speed < 20):
            scroll_speed += 0.00005 * score 

        if (pipe_frequency > 300):
            pipe_frequency -= 0.005 * score
           
        if abs(ground_scroll) > 53:
            ground_scroll = 0

        pipe_group.update()
   
    #check for game over and reset
    if game_over == True:
        if (score > high_score):
            time_achieved = time.time()
            with open("time_achieved.txt", "w") as file:
                file.write(str(int(time.time())))
            high_score = score
            with open("high_score.txt", "w") as file:
                file.write(str(high_score))
        if (score > daily_high_score):
            daily_high_score = score

        if play_once < 2:
            play_once += 1
        if play_once == 1:
            death = pygame.mixer.music.load('img/death.wav')
            pygame.mixer.music.play()
            games_played += 1
            with open("games_played.txt", "w") as file:
                file.write(str(games_played))

        if button.draw() == True and pygame.key.get_pressed()[K_SPACE] == 1:
            click_twice += 1
            if click_twice >= 10:
                game_over = False
                score = reset_game()
                play_once = 0
                scroll_speed = 5
                pipe_frequency = 1500
                click_twice = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if pygame.K_SPACE and flying == False and game_over == False:
            flying = True

    pygame.display.update()

pygame.quit()