import pygame
from sys import exit
import random

pygame.init()

clock = pygame.time.Clock()

# Window
win_height = 720
win_width = 551
window = pygame.display.set_mode((win_width, win_height))

# Images
rocket_images = [pygame.image.load("assets/rocketship.png"),
               pygame.image.load("assets/flame.png"),
               pygame.image.load("assets/rocketship.png")]

background_image = pygame.image.load("assets/background.png")
game_over_image = pygame.image.load("assets/game_over.png")
start_image = pygame.image.load("assets/start_menu.png")
meteor_image = pygame.image.load("assets/meteor.png")

# Game
scroll_speed = 2
rocket_start_position = (100, 250)
font = pygame.font.SysFont('Segoe', 26)
x_meteor = win_width + random.randint(100, 300)
# Timer variables
start_time = pygame.time.get_ticks()
score = 0
paused = False
game_stopped = True


class Rocket(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = rocket_images
        self.image = self.images[1]
        self.rect = self.image.get_rect()
        self.rect.center = rocket_start_position
        self.image_index = 0
        self.vel = 0
        self.flap = False
        self.alive = True

    # Animate rocket
    def update(self, user_input):
        # Check if the rocket is flapping
        if self.flap:
            # Use the flame image when flapping
            self.image = self.images[1]
        else:
            # Use the regular rocket image when not flapping
            self.image = self.images[self.image_index // 10]

        # Gravity and Flip
        self.vel += 0.5
        if self.vel > 7:
            self.vel = 7
        if 0 < self.rect.y < win_height:
            self.rect.y += int(self.vel)
        if self.vel == 0:
            self.flap = False

        # Check if the rocket is flapping
        if self.flap:
            # Use the flame image when flapping
            self.image = self.images[1]
        else:
            # Use the regular rocket image when not flapping
            self.image = self.images[self.image_index // 10]

        # User Input
        if user_input[pygame.K_SPACE] and not self.flap and self.rect.y > 0 and self.alive:
            self.flap = True
            self.vel = -7


class Meteor(pygame.sprite.Sprite):
    def __init__(self, y, image, scale_factor):
        pygame.sprite.Sprite.__init__(self)
        original_image = image
        self.original_image = pygame.transform.scale(original_image, (int(original_image.get_width() * scale_factor),
                                                                     int(original_image.get_height() * scale_factor)))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = win_width + random.randint(100, 300)  # Start from the right side of the window
        self.rect.y = y
        self.rotation_angle = 0  # Initial rotation angle
        self.rotation_speed = 3  # Adjust the rotation speed as needed

    def update(self):
        # Move meteor towards the left
        self.rect.x -= scroll_speed
        if self.rect.x <= -self.rect.width:
            self.kill()

        # Rotate meteor
        self.rotation_angle += self.rotation_speed
        if self.rotation_angle >= 360:
            self.rotation_angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.rotation_angle)


def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


def main():
    # Instantiate rocket
    rocket = pygame.sprite.GroupSingle()
    rocket.add(Rocket())

    # Setup meteors
    meteors = pygame.sprite.Group()
    meteor_timer = 0
    
    global score
    global start_time
    

    run = True
    while run:
        quit_game()
        window.fill((0, 0, 0))

        # User Input
        user_input = pygame.key.get_pressed()

        # Background
        window.blit(background_image, (0, 0))

        # Draw - meteor, rocket
        meteors.draw(window)
        rocket.draw(window)

        # Updates - meteor, rocket
        if rocket.sprite.alive:
            meteors.update()
        rocket.update(user_input)

        # Spawn meteors
        if meteor_timer <= 0 and rocket.sprite.alive:
            y_meteor = random.randint(0, win_height)
            meteors.add(Meteor(y_meteor, meteor_image, random.uniform(0.3, 0.9)))
            meteor_timer = random.randint(50, 100)
        meteor_timer -= 1
        
        # Update timer (score)
        if rocket.sprite.alive:
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
            score = round(elapsed_time,2)

        # Render and display the score
        score_text = font.render('Score: ' + str(score), True, pygame.Color(255, 255, 255))
        window.blit(score_text, (20, 20))

        # Collision Detection
        collision_meteors = pygame.sprite.spritecollide(rocket.sprites()[0], meteors, False)
        if collision_meteors or not (0 < rocket.sprite.rect.y < win_height):
            rocket.sprite.alive = False
            window.blit(game_over_image, (win_width // 2 - game_over_image.get_width() // 2,
                                          win_height // 2 - game_over_image.get_height() // 2))
            if user_input[pygame.K_r]:
                start_time = pygame.time.get_ticks()
                break

        clock.tick(60)
        pygame.display.update()

def menu():
    global game_stopped
    
    while game_stopped:
        quit_game()
        
        # Draw menu
        window.fill((0, 0, 0))
        window.blit(background_image, (0, 0))
        window.blit(start_image, (win_width // 2 - game_over_image.get_width() // 2,
                                          win_height // 2 - game_over_image.get_height() // 2))
        
        # User input
        user_input = pygame.key.get_pressed()
        if user_input[pygame.K_SPACE]:
            main()
            
        pygame.display.update()

if __name__ == "__main__":
    menu()
