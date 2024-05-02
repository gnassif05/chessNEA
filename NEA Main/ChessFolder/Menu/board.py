import pygame as pg

'''
This file holds the Board class which manages highlighting pieces valid moves, drawing the pieces onto the board and drawing the actual board
It is solely used in chess_main.py
'''


class Board:
    def __init__(self, screen):
        self.screen = screen
        self.square_size = 80
        self.red_squares = {}

    #loads the chess piece images into a dictionary and returns this dictionary
    def load_chess_piece_images(self, scale) -> dict:
        images = {}
        pieces = ["bP", "bK", "bQ", "bN", "bR", "bB", "wP", "wR", "wN", "wB", "wK", "wQ"]
        # loops through the pieces list
        for n in pieces:
            images[n] = pg.transform.scale(pg.image.load("ChessFolder/Themes/Classic/" + n + ".png"), scale)
            # appends to the dictionary the image n with the pygame image load
        return images

    #draws the squares for the board
    def draw_squares(self):
        colors = [pg.Color(str("white")), pg.Color(str("gray"))]
        #loops through 8x8 which is the dimensions of the board
        for row in range(8):
            for column in range(8):
                # calculates what colour the square must be by modding the sum of (row and column) by 2 and if it is 0 the colour is white, and if it is 1 its black
                square_colour = colors[(row + column) % 2]
                # creates a rect on the screen 
                # the x axis is added by 500 and y axis is added by 100 to calibrate it for the menu system.
                pg.draw.rect(
                    self.screen,
                    square_colour,
                    (500 + (column * self.square_size), 100 + (row * self.square_size), self.square_size, self.square_size),
                )

    #draws the pieces onto the board
    #the parameter object takes in either gs or cs value depending on whether the board is for the train or battle mode
    def draw_pieces(self, object):
        #assigns the the returned dictionary to chess_battle_images variable
        chess_battle_images = self.load_chess_piece_images((80, 80))
        #loops through 8x8 board
        for row in range(8):
            for column in range(8):
                #the piece at the location (row,column) in the chess board
                chess_piece = object.board[row][column]
                if chess_piece != "--":
                    #blit the chess piece image on to the screen
                    self.screen.blit(
                        chess_battle_images[chess_piece],
                        (500 + (column * self.square_size), 100 + (row * self.square_size)),
                    )

    #this highlights all valid moves the player can play when a user clicks on a piece. It also creates a border of the square of the piece that was last moved and the piece selected
    def highlight_squares(self, object, valid_moves, square_selected):
        #highlights the border of the square of the piece that was last moved
        if len(object.log) > 0:
            last_move = object.log[-1]
            # Create a surface for highlighting
            surface = pg.Surface((80, 80), pg.SRCALPHA)
            # Red border
            pg.draw.rect(surface, (0, 215, 0), surface.get_rect(), width=3)  
            self.screen.blit(surface, (500 + last_move.ending_column * 80, 100 + last_move.ending_row * 80))

        #if the user has selected a square, it highlights the square the user is clicking on
        if square_selected != ():
            row, col = square_selected
            if object.board[row][col][0] == ("w" if object.whiteTurn else "b"):
                # Create a surface for highlighting
                surface = pg.Surface((80, 80), pg.SRCALPHA)
                # Blue border 
                pg.draw.rect(surface, (0, 0, 255), surface.get_rect(), width=3) 
                self.screen.blit(surface, (500 + col * 80, 100 + row * 80))
                # Highlight moves from that square
                surface = pg.Surface((80, 80), pg.SRCALPHA)  
                # Grey circle representing valid moves
                pg.draw.circle(surface, (100, 100, 100, 100), (40, 40), 20)
                for move in valid_moves:
                    #if the piece selected has valid moves blit the grey circles onto the board where the valid moves are
                    if move.starting_row == row and move.starting_column == col:
                        self.screen.blit(surface, (500 + move.ending_column * 80, 100 + move.ending_row * 80))

    # Handles right-click events on the board. If a square is not already marked as red, it marks it as red. If it is already red, it removes the mark.
    def right_click(self, row, column):
        if (row, column) not in self.red_squares:
            self.red_squares[(row, column)] = True
        else:
            del self.red_squares[(row, column)]

    # Draws red squares on the board. It iterates through all squares marked as red and draws them on the screen.
    def draw_red_squares(self):
        red = pg.Color("red")
        red.a = 50
        gray = pg.Color("gray")
        white = pg.Color("white")

        for square in self.red_squares.items():
            row = square[0][0]
            column = square[0][1]
            is_red = square[1]

            if self.screen.get_at((row, column)) != "red" and is_red:
                # Create a surface for the rectangle
                rect_surface = pg.Surface((self.square_size, self.square_size), pg.SRCALPHA)
                rect_surface.set_alpha(255)
                # Fill the surface with the red color
                rect_surface.fill(red)
                # Draw the surface onto the screen
                self.screen.blit(rect_surface, (500 + (column * self.square_size), 100 + (row * self.square_size)))

            else:
                # Create a surface for the rectangle
                rect_surface = pg.Surface((self.square_size, self.square_size), pg.SRCALPHA)
                # Fill the surface with the white or gray color based on the square's position
                rect_surface.fill(white if [(row + column) % 2] == 0 else gray)
                # Draw the surface onto the screen
                self.screen.blit(rect_surface, (500 + (column * self.square_size), 100 + (row * self.square_size)))

    # Draws the entire board, including squares, pieces, highlights for valid moves, and red squares.
    def draw_board(self, object, valid_moves, square_selected):
        self.draw_squares()
        self.draw_pieces(object)
        self.highlight_squares(object, valid_moves, square_selected)
        self.draw_red_squares()

    # Draws the board without highlighting valid moves or red squares. Useful for displaying an empty board.
    def draw_empty_board(self, object):
        self.draw_squares()
        self.draw_pieces(object)