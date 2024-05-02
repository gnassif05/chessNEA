import pygame as pg

'''
This file handles the text that is shown on the display.
It is solely used in the chess_main.py file.
An example of its use would be with the display of the points system.
'''

# Defining a class for handling text in the chess program
class Text():
    def __init__(self, font, scale, text, colour):
        # Setting the font and size for the text
        self.font_size = pg.font.SysFont(font, scale)
        # Storing the desired text string
        self.text = text
        # Storing the colour of the text
        self.colour = colour

    # Method to draw the text on the screen at a specified position (x,y)
    def draw_text_on_screen(self, x, y, screen):
        # Rendering the text with the specified font, size, and colour
        text = self.font_size.render(self.text, True, self.colour)
        # Drawing the text on the screen at the specified position
        screen.blit(text,(x,y))
    
    # Method to remove the text from the screen by drawing a rectangle of the background colour over it
    def remove_text_on_screen(self, x, y, screen):
        # Drawing a rectangle of the background colour over the text to essentially remove the text
        pg.draw.rect(screen,(41,43,47), (x,y, 40,100))