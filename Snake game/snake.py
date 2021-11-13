import pygame
from pygame.locals import *
import time
import random

size = 40
background_color = (28,58,128)
death_color = (255,0,0)

class Apple:
    def __init__(self, parent_screen):

        self.image = pygame.image.load("resources/Images/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = size*3
        self.y = size*3

    def draw(self):

        self.parent_screen.blit(self.image,(self.x,self.y))

        pygame.display.update()

    def move(self):

        self.x = random.randint(0, 12)*size
        self.y = random.randint(0, 12)*size

class Snake:
    def __init__(self, parent_screen, length):

        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/Images/block.jpg").convert()
        self.x = [size]*length
        self.y = [size]*length
        self.direction = 'right'

    def increase_length(self):

        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):


        for i in range(self.length):

            self.parent_screen.blit(self.block,(self.x[i],self.y[i]))
        
        pygame.display.update()

    def walk(self):

        for i in range(self.length-1,0,-1):

            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]
            
        if self.direction == 'up':

            self.y[0] -= size
            self.draw()

        if self.direction == 'down':
            
            self.y[0] += size
            self.draw()

        if self.direction == 'left':

            self.x[0] -= size
            self.draw()

        if self.direction == 'right':

            self.x[0] += size
            self.draw()
      
    def move_left(self):

        self.direction = 'left'
  
    def move_right(self):

        self.direction = 'right'
    
    def move_down(self):

        self.direction = 'down'

    def move_up(self):

        self.direction = 'up'
    

class game:
    def __init__(self):

        pygame.init()
        pygame.mixer.init()
        self.background_music()
        self.blocknum = 2
        self.surface = pygame.display.set_mode((850, 800))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):

        if x1 >= x2 and x1 < x2 + size:
            if y1 >= y2 and y1 < y2 + size:
                return True
        return False

    def background_music(self):

        music = pygame.mixer.music.load("resources/music/bg_music_1.mp3")
        pygame.mixer.music.play(-1)

    def audio(self, sound):

        sound = pygame.mixer.Sound(f"resources/music/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def render_background(self):

        bg = pygame.image.load("resources/Images/background.jpg")
        self.surface.blit(bg, (0,0))

    def play(self):

        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.update()

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            
            self.audio("ding")
            self.snake.increase_length()
            self.apple.move()
        
        for i in range(1, self.snake.length):

            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.audio("crash")
                raise "Game over"
    
    def pause_message(self):

        font_1 = pygame.font.SysFont('arial', 80)
        font_2 = pygame.font.SysFont('arial', 40)
        msg_1 = font_1.render("Paused!", True, (255, 255, 255))
        self.surface.blit(msg_1, (280, 300))
        msg_2 = font_2.render("To resume press Home key", True, (255, 255, 255))
        self.surface.blit(msg_2, (200, 400))
        
        pygame.display.update()

    def show_game_over(self):

        self.surface.fill((death_color))
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game score: {self.snake.length - 1}", True, (255, 255, 255))
        self.surface.blit(line1, (320, 450))
        line2 = font.render("Game Over! To play again press enter, to exit press escape", True, (255, 255, 255))
        self.surface.blit(line2, (50, 400))

        pygame.display.update()
        pygame.mixer.music.pause()

    def reset(self):

        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def display_score(self):

        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length - 1}", True, (255, 255, 255))
        self.surface.blit(score, (350, 10))
  
    def run(self):
    
        running = True
        pause = False

        while running:

            for event in pygame.event.get():

                if event.type == KEYDOWN:

                    if event.key == K_ESCAPE:
                        running = False
                        
                    if event.key == K_RETURN:

                        pygame.mixer.music.play(-1)
                        pause = False
                        self.reset()

                    if event.key == K_PAUSE:

                        self.pause_message()
                        pygame.mixer.music.pause()
                        pause = True

                    if event.key == K_HOME:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:

                        if event.key == K_UP:

                            self.snake.move_up()

                        if event.key == K_DOWN:

                            self.snake.move_down()

                        if event.key == K_LEFT:

                            self.snake.move_left()

                        if event.key == K_RIGHT:

                            self.snake.move_right()

                elif event.type == QUIT:

                    running = False

            try:

                if not pause:

                    self.play()

            except Exception as e:

                self.show_game_over()

                pause = True
        
            time.sleep(0.15)

if __name__ == '__main__':

    game = game()
    
    game.run()