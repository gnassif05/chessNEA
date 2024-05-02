
import pygame as pg

'''
This file creates Buttons and Images for the program. 
The buttons when clicked return True and the Images return nothing when clicked
An example where this is used is in the menu system; when a button is clicked a loop runs that changes the mode
'''

# Defining a class for displaying images on the screen
class Main_UI():
    def __init__(self, x, y, scale, image):
        # Getting the height and width of the image
        image_height = image.get_height()
        image_width = image.get_width()
        
        # Scaling the image based on the provided scale factor
        self.image = pg.transform.scale(image, (int(image_width*scale), int(image_height*scale)))
        # Getting the rectangle of the scaled image
        self.rect = self.image.get_rect()
        # Setting the top left position of the rectangle
        self.rect.topleft = (x, y)

# Defining a class for buttons, which inherits from Main_UI
class Button(Main_UI):
    def __init__(self, x, y, scale, image):
        super().__init__(x, y, scale, image)
        # Initializing a flag to track if the button has been clicked
        self.clicked = False
        
    # Method to draw the button on the screen and handle click events
    def draw_button(self, display):
        action = False
        # Getting the current mouse position
        mouse_pos = pg.mouse.get_pos()
        # Checking if the mouse is over the button
        if self.rect.collidepoint(mouse_pos):
            # Checking if the left mouse button is pressed and the button has not been clicked yet
            if pg.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
            # Resetting the clicked flag if the left mouse button is released
            if pg.mouse.get_pressed()[0] == 0:
                self.clicked = False

        # Drawing the button image on the display
        display.blit(self.image, (self.rect.x, self.rect.y))
        # Returning the action flag
        return action

# Defining a class for displaying images, which inherits from Main_UI
class Image(Main_UI):
    def __init__(self, x, y, scale, image):
        super().__init__(x, y, scale, image)
    
    # Method to draw the image on the screen
    def draw_image(self, display):
        # Drawing the image on the display
        display.blit(self.image, (self.rect.x, self.rect.y))