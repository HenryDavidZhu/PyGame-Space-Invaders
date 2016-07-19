'''
    PyGame remake of Space Invaders
    Author: Henry Zhu
    Date: 07/18/16
'''

from pygame import *
import random
import sys

class Sprite:
    '''
        A Sprite class that can initialize a sprite based on an image, and display it.

        Parameters:
            filename -> the path of the image to be used
            xpos -> the x position of the sprite
            ypos -> the y position of the sprite
    '''
    def __init__(self, filename, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.sprite_image, self.rect = load_image(filename, (0, 0, 0))
        self.sprite_image.set_colorkey((0, 0, 0)) 

    def display(self, screen):
        '''
            Displays the sprite onto the screen.

            Parameters:
                screen -> the PyGame display to draw onto.
        '''
        screen.blit(self.sprite_image, (self.xpos, self.ypos))

    def set_rect_attributes(self, x, y):
        self.rect.left = x
        self.rect.top = y
        self.rect.right = x + self.rect.width
        self.rect.bottom = y + self.rect.height

    def intersect(self, sprite_2):
        '''
            Returns whether a sprite intersects with another sprite.

            Parameters:
                sprite_2 -> the sprite to compare intersection with

            Returns:
                Whether the sprite intersects with sprite_2
        '''
        return self.rect.colliderect(sprite_2.rect)

def load_image(path, colorkey):
    '''
        Returns an image and its bounding rectangle based on a filename.

        Parameters:
            path -> the path of the picture
            colorkey -> the color defined to be transparent

        Returns:
            the loaded image
            the bounding rectangle of the image
    '''
    try:
        sprite_image = image.load(path)
    except error, message:
        print("Cannot load image: {0}".format(path))

    sprite_image = sprite_image.convert()

    if colorkey is not None:
        if colorkey is -1:
            colorkey = sprite_image.get_at((0, 0))
        sprite_image.set_colorkey(colorkey, RLEACCEL)

    return sprite_image, sprite_image.get_rect()

def main():
    '''
        The main function runs the Space Invader game, implementing all the logic, calculation,
        and user interaction.
    '''
    init()
    screen = display.set_mode((800, 600))
    display.set_caption("Space Invaders")

    fighter = Sprite("spaceship.png", 357, 520)

    enemies = []
    bullets_good = [] # List of all of the bullets fired by the hero / fighter
    bullets_bad = []

    for i in range(14): # Add the enemies into the enemies list
        new_enemy = Sprite("enemy.png", 55 * i + 7, 30)
        enemies.append(new_enemy)

    while True:
        screen.fill((0, 0, 0)) # Continiously refresh the background of the screen

        if len(enemies) == 0: # The player wins the game
            print("You win!")
            quit()
            sys.exit()

        for enemy in enemies: # Draw the enemies onto the screen
            enemy.set_rect_attributes(enemy.xpos, enemy.ypos)
            enemy.display(screen)

        selected_enemy = random.randint(0, len(enemies) - 1)
        shoot_probability = random.randint(0, 18)

        if shoot_probability == 5:
            bullet_x = enemies[selected_enemy].xpos
            bullet_y = enemies[selected_enemy].ypos

            bad_bullet = Sprite("enemy_bullet.png", bullet_x, bullet_y + 50)
            bullets_bad.append(bad_bullet)

        for bullet in bullets_good: # Draw the bullets onto the screen
            bullet.ypos -= 10
            bullet.set_rect_attributes(bullet.xpos, bullet.ypos)

            for enemy in enemies:
                if bullet.intersect(enemy) == 1:
                    enemies.remove(enemy)

            bullet.display(screen)

        for bad_bullet in bullets_bad:
            bad_bullet.ypos += 10
            bad_bullet.set_rect_attributes(bad_bullet.xpos, bad_bullet.ypos)

            if bad_bullet.intersect(fighter) == 1:
                print("You lose!")
                quit()
                sys.exit()

            bad_bullet.display(screen)

        for keyevent in event.get(): # Go through key press events
            if keyevent.type == QUIT:
                quit()
                sys.exit()
            if keyevent.type == KEYDOWN:
                if keyevent.key == K_UP:
                    # Create a new bullet and add it to the list of bullets fired by the hero
                    bullet = Sprite("bullet.png", fighter.xpos + 34, fighter.ypos - 20)
                    bullets_good.append(bullet)

        keys = key.get_pressed()

        if keys[K_LEFT] and fighter.xpos >= 0:
            fighter.xpos -= 5
        if keys[K_RIGHT] and fighter.xpos <= 800 - 85:
            fighter.xpos += 5

        fighter.set_rect_attributes(fighter.xpos, fighter.ypos)

        fighter.display(screen)
        display.update()
        pass

main() # Run the game!