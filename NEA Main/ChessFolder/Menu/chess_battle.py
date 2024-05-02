from move import Move
from pieces import King, Queen, Rook, Bishop, Knight, Pawn, Piece
import copy

'''
This file contains the object that is manipulated with by the user in the battle menu
It handles moves on the board, resets, finds valid moves etc
There is also a class which manages the castling rights for the game
'''

class StateOfGame:
    def __init__(self):
        # the chess board where "b" represents black and "w" represents white, "--" = blank space
        self.board: list[list[str]] = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ] 


        #setup the game
        self.whiteTurn: bool = True
        self.log: list[Move] = []
        self.turn_number: int = 0

        self.white_king_location: tuple = (7, 4)
        self.black_king_location: tuple = (0, 4)

        self.stalemate: bool = False
        self.checkmate: bool = False

        self.castling: CastlingRights = CastlingRights()

        self.en_passant_possible: tuple = ()
        self.en_passant_log: list = [()]

    #return the piece in a row and column
    def piece_in(self, row, col) -> str:
        return self.board[row][col]

    def update_castle_rights(self, move: Move, undo: bool):
        # Determine the color and type of the piece moved
        color, piece_type = move.the_piece_moved[0], move.the_piece_moved[-1]

        # Define a mapping for rook columns to castling sides
        rook_columns_to_sides = {0: "Q", 7: "K"}

        # Update castling rights if it's not an undo operation
        if not undo:
            # If the piece moved is the king, disable both castling rights
            if piece_type == "K":
                self.castling.update(color, "K", False)
                self.castling.update(color, "Q", False)
            # If the piece moved is a rook, disable the corresponding castling right
            elif piece_type == "R" and move.starting_column in rook_columns_to_sides:
                self.castling.update(color, rook_columns_to_sides[move.starting_column], False)

            self.castling.add_to_history()
        else:
            # For undo operations, revert to the previous castling rights
            self.castling.pop_history()  # remove the move being undone
            self.castling.rights = copy.deepcopy(self.castling.get_history()[-1])

    # if there are no pieces from the king to the rook (king side)
    def can_king_side_castle(self, row, column) -> bool:
        try:
            return self.piece_in(row, column + 1) == "--" and self.piece_in(row, column + 2) == "--"
        except:
            return False

    # if there are no pieces from king to the rook (queen side)
    def can_queen_side_castle(self, row, column) -> bool:
        try:
            return self.board[row][column - 1] == "--" and self.board[row][column - 2] == "--" and self.board[row][column - 3] == "--"
        except:
            return False

    def get_castle_moves(self, row, column, possible_move_log: list) -> None:
        # if the piece is attacked
        if self.is_square_attacked(row, column):
            # dont append any moves
            return

        # Determine the color of the king based on the current turn
        king_color = "w" if self.whiteTurn else "b"

        # Check for king-side castling
        if self.castling.rights[king_color]["K"] and self.can_king_side_castle(row, column):
            # if the squares are not attacked
            if not self.is_square_attacked(row, column + 1) and not self.is_square_attacked(row, column + 2):
                possible_move_log.append(
                    Move(
                        (row, column),
                        (row, column + 2),
                        self.board,
                        is_castling=True,
                    )
                )

        # Check for queen-side castling
        if self.castling.rights[king_color]["Q"] and self.can_queen_side_castle(row, column):
            # if the squares are not attacked
            if not self.is_square_attacked(row, column - 1) and not self.is_square_attacked(row, column - 2):
                possible_move_log.append(
                    Move(
                        (row, column),
                        (row, column - 2),
                        self.board,
                        is_castling=True,
                    )
                )

    # make a move on the board
    def make_move(self, move: Move, temporary=False):
        #alters the board to update it
        self.board[move.starting_row][move.starting_column] = "--"
        self.board[move.ending_row][move.ending_column] = move.the_piece_moved
        # logs the move for an undo button + history of game
        self.log.append(move)
        # changes the persons turn.  
        self.whiteTurn = not self.whiteTurn  

        #if a king or rook has been moved the castling rights must be updated as per the rules.
        if move.the_piece_moved == "wK":
            self.white_king_location = (move.ending_row, move.ending_column)
            if not temporary:
                self.castling.update("w", "K", False)
                self.castling.update("w", "Q", False)

        elif move.the_piece_moved == "bK":
            self.black_king_location = (move.ending_row, move.ending_column)
            if not temporary:
                self.castling.update("b", "K", False)
                self.castling.update("b", "Q", False)

        if move.the_piece_moved == "wR":
            if move.starting_row == 7:
                # left rook
                if move.starting_column == 0:  
                    if not temporary:
                        self.castling.update("w", "Q", False)

                # right rook
                elif move.starting_column == 7:  
                    if not temporary:
                        self.castling.update("w", "K", False)

        # if there has been a castle move
        if move.is_castle_move:
            # moved kingside since positive
            if move.ending_column - move.starting_column == 2:
                # moves rook  
                self.board[move.ending_row][move.ending_column - 1] = self.board[move.ending_row][move.ending_column + 1]  
                self.board[move.ending_row][move.ending_column + 1] = "--"
            # moved queenside
            else:
                # moves rook  
                self.board[move.ending_row][move.ending_column + 1] = self.board[move.ending_row][move.ending_column - 2]  
                self.board[move.ending_row][move.ending_column - 2] = "--"

        #if there has been a enpassant move
        if move.is_enpassant_move:
            # the pawn captured must be changed to blank
            self.board[move.starting_row][move.ending_column] = "--"

        if move.the_piece_moved[1] == "P" and abs(move.starting_row - move.ending_row) == 2:
            # en passant is possible
            self.en_passant_possible = ((move.starting_row + move.ending_row) // 2, move.starting_column)
        else:
            # reset en passant
            self.en_passant_possible = ()

        # if the move isnt tempoarary (not being used to generate valid moves)
        if not temporary:
            self.update_castle_rights(move, undo=False)
            self.en_passant_log.append(self.en_passant_possible)
            if not self.whiteTurn:
                self.turn_number += 1

    #undo a move on the board
    def undo_move(self, temporary: bool = False):
        # if any moves have been played
        if len(self.log) != 0:

            # the move is popped from the list so that it can be undone.
            move: Move = self.log.pop()  
            self.board[move.starting_row][move.starting_column] = move.the_piece_moved
            # reverses the move
            self.board[move.ending_row][move.ending_column] = move.the_piece_captured
            # reverses the turn  
            self.whiteTurn = not self.whiteTurn  

            # if a king move has been undone correct its location
            if move.the_piece_moved == "wK":
                self.white_king_location = (move.starting_row, move.starting_column)
            elif move.the_piece_moved == "bK":
                self.black_king_location = (move.starting_row, move.starting_column)

            if move.is_castle_move:
                # kingside
                if move.ending_column - move.starting_column == 2:  
                    self.board[move.ending_row][move.ending_column + 1] = self.board[move.ending_row][move.ending_column - 1]
                    self.board[move.ending_row][move.ending_column - 1] = "--"
                #queenside
                else:
                    self.board[move.ending_row][move.ending_column - 2] = self.board[move.ending_row][move.ending_column + 1]
                    self.board[move.ending_row][move.ending_column + 1] = "--"

            if move.is_enpassant_move:
                self.board[move.ending_row][move.ending_column] = "--"
                self.board[move.starting_row][move.ending_column] = move.the_piece_captured

            # if the undo isnt tempoarary (not being used to generate valid moves)
            if not temporary:
                if len(self.en_passant_log) > 1:
                    self.en_passant_log.pop()
                    self.en_passant_possible = self.en_passant_log[-1]
                if self.turn_number >= 1 and self.whiteTurn:
                    self.turn_number -= 1

                # Update castle rights after undoing move
                self.update_castle_rights(move, undo=True)

    # get all valid moves from a list of possible moves (moves that can be legally played as per the rules)
    def get_valid_moves(self) -> list:

        # get all the possible chess moves
        fully_valid_moves = self.get_possible_moves()

        # assigns temporary variables for the enpassant and castling co-ordinates
        temp_en_passant = self.en_passant_possible
        temp_castling = self.castling


        # get all castle moves
        if self.whiteTurn:
            self.get_castle_moves(
                self.white_king_location[0],
                self.white_king_location[1],
                fully_valid_moves,
            )
        else:
            self.get_castle_moves(
                self.black_king_location[0],
                self.black_king_location[1],
                fully_valid_moves,
            )


        # go down the list of possible moves, in increments of -1
        for i in range(len(fully_valid_moves) - 1, -1, -1):
            # make a temporary move
            self.make_move(fully_valid_moves[i], temporary= True)
            # reverse the turns
            self.whiteTurn = not self.whiteTurn
            # if the move leads to the player's own king being captured:
            if self.in_check():
                # remove that move from the fully valid moves list
                fully_valid_moves.remove(fully_valid_moves[i])
            # reverse the turn back to the original
            self.whiteTurn = not self.whiteTurn
            # undo the temporary move done
            self.undo_move(temporary=True)
        # checkmate or stalesmate since no valid moves
        if len(fully_valid_moves) == 0:  
            if self.in_check():
                self.checkmate = True
            else:
                self.stalemate = True
        # en passant
        self.en_passant_possible = temp_en_passant



        self.castling = temp_castling
        return fully_valid_moves

    #check if a king is in check by checking if the square the king is on is attacked
    def in_check(self) -> bool:
        if self.whiteTurn:
            return self.is_square_attacked(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.is_square_attacked(self.black_king_location[0], self.black_king_location[1])

    #check if a square is attacked by a piece
    def is_square_attacked(self, row, column) -> bool:
        # reverses the turn
        self.whiteTurn = not self.whiteTurn
        # gets the opponents possible moves
        opponent_moves = self.get_possible_moves()
        # reverses the turn
        self.whiteTurn = not self.whiteTurn
        # loop through all the opponents moves
        for move in opponent_moves:
            # if there is a move with that ending row and column
            if move.ending_row == row and move.ending_column == column:
                # the square is attacked
                return True
        return False

    # get all possible moves on the board by looping through the board and using the piece classes methods for the respective piece
    def get_possible_moves(self) -> list:

        # Initialize an empty list to store all possible moves.
        moves = []
        # Iterate through each row on the board.
        for row in range(8):
            # Iterate through each column in the current row.
            for column in range(8):
                # Get the piece at the current position.
                piece = self.board[row][column]
                # If the square is empty, skip to the next iteration.
                if piece == "--":
                    continue

                # Determine if it's white or black's turn based on the piece's color.
                player_turn = piece[0]
                # If the piece's color does not match the current player's turn, skip to the next iteration.
                if (player_turn == "w" and not self.whiteTurn) or (player_turn == "b" and self.whiteTurn):
                    continue

                # Extract the type of the piece (e.g., "P" for Pawn).
                piece_type = piece[1]
                # Map the piece type to its corresponding class.
                piece_class = {
                    "P": Pawn,
                    "B": Bishop,
                    "N": Knight,
                    "R": Rook,
                    "Q": Queen,
                    "K": King,
                }[piece_type]

                # Create an instance of the piece class, passing the player's turn and the current player's color.
                piece_instance = piece_class(player_turn, self.whiteTurn)

                # if the piece_class is a Pawn set en_passant_possible
                if isinstance(piece_instance, Pawn):
                    piece_instance.en_passant_possible = self.en_passant_possible

                # Get all valid moves for the current piece.
                valid_moves = piece_instance.all_possible_moves(player_turn, row, column, self.board, self.whiteTurn)

                # Add the valid moves for the current piece to the list of all possible moves.
                moves.extend(valid_moves)
        return moves

    # promote any pawn that has reached the back rank to a queen
    def pawn_promotion(self):
        for column in range(8):
            if self.board[0][column] == "wP":
                self.board[0][column] = "wQ"
            elif self.board[7][column] == "bP":
                self.board[7][column] = "bQ"

    # find the players turn by checking if the objects self.whiteTurn is true or not
    def player_turn(self) -> str:
        if self.whiteTurn:
            turn = "White's Turn"
        else:
            turn = "Black's Turn"

        return turn

    # get the points of each user by looping through the board and if a piece is present it will get its value and add it to its previous value until
    # all pieces have been looped through for each colour
    def get_points(self) -> int:
        def get_piece_points(piece_type):
            # Define the points for each piece type
            points = {"P": 1, "B": 3, "N": 3, "R": 5, "Q": 9, "K": 0}
            return points.get(piece_type, 0)

        self.white_points = sum(get_piece_points(piece[1]) for row in self.board for piece in row if piece[0] == "w")
        self.black_points = sum(get_piece_points(piece[1]) for row in self.board for piece in row if piece[0] == "b")
        # if positive white has more points and vice versa
        self.total_points = self.white_points - self.black_points
        return self.total_points

    # check if the king is in checkmate, by checking if it is in check and if there are any valid moves the king can play
    def in_checkmate(self) -> bool:
        if len(self.get_valid_moves()) == 0 and self.in_check():
            return True
        return False
    
    # checks if there is a draw by insufficient material in the game
    def is_draw(self) -> bool:
        # a draw occurs if there are: 1 knight or bishop.
        white_pieces = {"B": 0, "N": 0}
        black_pieces = {"B": 0, "N": 0}
        #loops through an 8x8 board  
        for row in range(8):
            for col in range(8):
                # if there is any of these pieces a checkmate can still occur
                if self.board[row][col][1] in ["Q","R","P"]:
                    return False
                
                # checks for the count of bishops or knights in the program
                if self.board[row][col][0] == "w":
                    if self.board[row][col][1] == "B":
                        white_pieces["B"] += 1
                    elif self.board[row][col][1] == "N":
                        white_pieces["N"] += 1
                elif self.board[row][col][0] == "b":
                    if self.board[row][col][1] == "B":
                        black_pieces["B"] += 1
                    elif self.board[row][col][1] == "N":
                        black_pieces["N"] += 1
        #if there is either 1 of each, bishop and knight or 2 of a bishop or knight there is no draw
        if (white_pieces["B"] == 1 and white_pieces["N"] == 1) or (black_pieces["B"] == 1 and black_pieces["N"] == 1):
            return False
        elif (white_pieces["B"] == 2 or white_pieces["N"] == 2) or (black_pieces["B"] == 2 or black_pieces["N"] == 2):
            return False
        #otherwise it is a draw
        return True

    #resets the chess board and all other important variables
    def reset_game(self):
        # reset the board back to its original state
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        # Clear the move log
        self.log = []
        # Reset the turn number to 1  
        self.turn_number = 0  

        # reset the game fully
        self.whiteTurn = True
        self.checkmate = False
        self.stalemate = False

        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)

        self.castling = CastlingRights()
        
        self.en_passant_possible: tuple = ()
        self.en_passant_log: list = [()]

# this class manages the game's castling rights
class CastlingRights:
    def __init__(self):
        self.rights = {"w": {"K": True, "Q": True}, "b": {"K": True, "Q": True}}
        self.history: list = []
        self.history.append({"w": {"K": True, "Q": True}, "b": {"K": True, "Q": True}})

    # updates a castling right for a specific, player and side
    def update(self, player, side, value):
        self.rights[player][side] = value


    def add_to_history(self):
        self.history.append(copy.deepcopy(self.rights))

    # gets the castling rights history
    def get_history(self) -> list:
        return self.history

    # pops the history of the castling rights so that when a move is undone it uses the previous turns castle rights
    def pop_history(self) -> dict:
        return self.history.pop()
