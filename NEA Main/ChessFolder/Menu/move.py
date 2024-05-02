import pygame as pg

'''
This file contains the Move and Movelog class
The Move class manages the actual moves of the player by using the user's starting and ending square clicked to discover which piece is moved and captured.
The Movelog class gets the notation from the Move class to present these notations to the player through a table on the screen.
'''

#class which handles the move of a player
class Move:
    # converts the ranks in chess to rows that the computer can read
    ranks_to_rows: dict = {
        "1": 7,
        "2": 6,
        "3": 5,
        "4": 4,
        "5": 3,
        "6": 2,
        "7": 1,
        "8": 0,  
    }

    # reverses above dictionary for correct chess syntax.
    rows_to_ranks: dict = {val: key for key, val in ranks_to_rows.items()}  

    # converts the columns to the correct files syntax for correct chess syntax.
    columns_to_files: dict = {
        0: "a",
        1: "b",
        2: "c",
        3: "d",
        4: "e",
        5: "f",
        6: "g",
        7: "h",  
    }
    
    # reverses above dictionary for correct chess syntax.
    files_to_columns: dict = {val: key for key, val in columns_to_files.items()}

    def __init__(self, starting_square, ending_square, board, is_castling=False, is_enpassant=False):

        # gets the starting row and column of the move based on the starting square co-ordinates
        self.starting_row = starting_square[0]
        self.starting_column = starting_square[1]
        
        # gets the ending row and column of the move based on the starting square co-ordinates
        self.ending_row = ending_square[0]
        self.ending_column = ending_square[1]

        # finds the piece that is moved and captured by comparing the starting and ending rows and columns with the board
        self.the_piece_moved: str = board[self.starting_row][self.starting_column]
        self.the_piece_captured: str = board[self.ending_row][self.ending_column]

        # creates an id for the move so each move has a unique id
        self.move_id = self.starting_row * 1000 + self.starting_column * 100 + self.ending_row * 10 + self.ending_column

        # assigns a boolean to see if the move is special - enpassant or castling
        self.is_castle_move: bool = is_castling
        self.is_enpassant_move: bool = is_enpassant

        # if the move is an enpassant the piece captured is changed from -- to the appropriate pawn to prevent errors
        if self.is_enpassant_move:
            self.the_piece_captured = "wP" if self.the_piece_moved == "bP" else "bP"

        # does the move break castling:
        self.breaks_castling: bool = False
    
    # compare classes
    def __eq__(self, other) -> bool:
        if isinstance(other, Move):
            # if the moves have the same ids
            return self.move_id == other.move_id
        return False

    # get the proper chess notation of a move
    def get_chess_notation(self, turn_number, object) -> str:
        # if the move is a castle move:
        if self.the_piece_moved[1] == "K" and self.ending_column - self.starting_column !=1:
            if self.starting_column - self.ending_column == 2:
                notation = "O-O-O"
                return str(turn_number) + "." + notation
            else:
                notation = "O-O"
                return str(turn_number) + "." + notation
        
        # if the piece that moved was a pawn:
        elif self.the_piece_moved[1] == "P":
            location_of_the_first_piece_moved = self.get_file(self.starting_column)
            # en passant move:
            if self.starting_column != self.ending_column and self.the_piece_captured == "--":
                notation = (
                    str(turn_number)
                    + "."
                    + location_of_the_first_piece_moved
                    + "x"
                    + self.get_file(self.ending_column)
                    + self.get_rank(self.ending_row)
                    + ("#" if object.in_checkmate() else "+" if object.in_check() else "")
                )
                return notation
            # pawn captures a piece
            elif self.the_piece_captured != "--":
                notation = (
                    str(turn_number)
                    + "."
                    + location_of_the_first_piece_moved
                    + "x"
                    + self.get_file(self.ending_column)
                    + self.get_rank(self.ending_row)
                    + ("#" if object.in_checkmate() else "+" if object.in_check() else "")
                )
                return notation
            # pawn just moves
            else:
                notation = str(turn_number) + "." + self.get_file(self.ending_column) + self.get_rank(self.ending_row) + ("#" if object.in_checkmate() else "+" if object.in_check() else "")
                return notation
        # not a pawn move
        else:
            # piece just moves
            if self.the_piece_captured != "--":
                notation = (
                    str(turn_number)
                    + "."
                    + self.the_piece_moved[1]
                    + "x"
                    + self.get_file(self.ending_column)
                    + self.get_rank(self.ending_row)
                    + ("#" if object.in_checkmate() else "+" if object.in_check() else "")
                )
                return notation
            # piece captures something
            else:
                notation = (
                    str(turn_number)
                    + "."
                    + self.the_piece_moved[1]
                    + self.get_file(self.ending_column)
                    + self.get_rank(self.ending_row)
                    + ("#" if object.in_checkmate() else "+" if object.in_check() else "")
                )
                return notation

    # gets the rank of the row
    def get_rank(self, row):
        return self.rows_to_ranks[row]  

    # gets the file of the column
    def get_file(self, column):
        return self.columns_to_files[column]

# class which handles the movelog for the chess game
class MoveLog:
    def __init__(self, font, scale, x, y, screen):
        self.font_size = pg.font.SysFont(font, scale)
        self.move_notations = []
        # the (x,y) position where the move log image is needed
        self.x = x
        self.y = y
        self.screen = screen

    # adds a move to the move log by appending it to the list
    def add_move(self, move):
        self.move_notations.append(move)

    # remove the last move from the movelog by popping it from the list
    def remove_last_move(self):
        if self.move_notations:
            self.move_notations.pop()

    def draw_move_log(self):
        # difference in y co-ordinate for each move log
        y_offset = 0
        # Number of moves to display per row
        moves_per_row = 4
        # Loop through the move notations, in increments of 4, since we want 4 moves per row on the move log  
        for i in range(0, len(self.move_notations), moves_per_row):
            # creates a list slice which gets a subset of the move_notations list
            row_moves = self.move_notations[i : i + moves_per_row]
            # j marks the position from 0-3 to calculate the position on the move-log, move is the move notation itself. 
            for j, move in enumerate(row_moves):
                # the text surface for each move is created
                text_surface = self.font_size.render(move, True, (255, 255, 255))
                # the position is calculated based on the row and column of the move in the move log.
                self.screen.blit(text_surface, (self.x + (j * 75), self.y + y_offset))
            # Increase the y-coordinate for the next row
            y_offset += 15  

    def reset_move_log(self):
        # reset the notations list
        self.move_notations = []