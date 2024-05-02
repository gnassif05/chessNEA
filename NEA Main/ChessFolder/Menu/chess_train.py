from pieces import King, Queen, Rook, Bishop, Knight, Pawn

'''
This file contains the object that is manipulated with by the user in the train menu
It handles moves on the board, resets, finds valid moves etc
'''


class CreateState:
    def __init__(self):
        # starting empty board
        self.board = [
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
        ]

        # setup the game
        self.whiteTurn = True
        self.log = []
        self.stalemate = False
        self.checkmate = False
        self.adding_pieces = True
        self.turn_number = 0

    def reset_board(self):
        # resets the board to the starting empty board
        self.board = [
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
        ]

        # resets the game to setup
        self.whiteTurn = True
        self.log = []
        self.stalemate = False
        self.checkmate = False
        self.adding_pieces = True
        self.turn_number = 0

    # adds the piece by changing the boards' value at the position clicked to the piece variable
    def add_piece(self, row, column, piece):
        self.board[row][column] = piece

    # removes the piece by changing the boards' value at the position clicked to "--"
    def remove_piece(self, row, column):
        self.board[row][column] = "--"

    def make_move(self, move, temporary : bool = False):
        # makes the move by altering the board with the move class
        self.board[move.starting_row][move.starting_column] = "--"
        self.board[move.ending_row][move.ending_column] = move.the_piece_moved

        # logs the move for an undo button + history of game
        self.log.append(move)

        # changes the turn.  
        self.whiteTurn = not self.whiteTurn  

        # update king's position if the king moved
        if move.the_piece_moved == "wK":
            self.white_king_location = (move.ending_row, move.ending_column)
        elif move.the_piece_moved == "bK":
            self.black_king_location = (move.ending_row, move.ending_column)

        # if the move is not temporary to ensure the move validation doesnt alter turn numbers
        if not temporary:
            # if white has moved increased the turn number since a chess turn is both blacks and whites move
            if self.whiteTurn is False:
                self.turn_number += 1

    def undo_move(self, temporary = False):
        if len(self.log) != 0:
            # the move is popped from the list so that it can be undone.
            move = self.log.pop()

            # reverses the move  
            self.board[move.starting_row][move.starting_column] = move.the_piece_moved
            self.board[move.ending_row][move.ending_column] = move.the_piece_captured  

            # reverses the turn
            self.whiteTurn = not self.whiteTurn

            # update king's position if the king was the piece moved
            if move.the_piece_moved == "wK":
                self.white_king_location = (move.starting_row, move.starting_column)
            elif move.the_piece_moved == "bK":
                self.black_king_location = (move.starting_row, move.starting_column)


            # if the move is not temporary to ensure the move validation doesnt alter turn numbers
            if not temporary:
                # if it was white's turn, the turn number should fall since a chess turn is both blacks and whites move
                if self.turn_number >= 1 and self.whiteTurn is False:
                    self.turn_number -= 1

    def get_valid_moves(self) -> list:
        # get all the possible chess moves
        fully_valid_moves = self.get_possible_moves()
        
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

        return fully_valid_moves

    def in_check(self) -> bool:

        #get the positions of each king
        white_king_location = self.find_white_king()
        black_king_location = self.find_black_king()

        # return if the kings co-ordinate position is attacked
        if self.whiteTurn:
            return self.is_square_attacked(white_king_location[0], white_king_location[1])
        else:
            return self.is_square_attacked(black_king_location[0], black_king_location[1])

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

    def is_black_king_attacked(self, row, column) -> bool:
        # get the oppponents moves for black king exclusively
        opponent_moves = self.get_possible_moves()
        # loop through all opponent moves
        for move in opponent_moves:
            # if there is a move with that ending row and column
            if move.ending_row == row and move.ending_column == column:
                # the king is attacked
                return True
        return False

    def get_possible_moves(self) -> list:
        moves = []
        # rows in board
        for row in range(8):
            # columns in given row  
            for column in range(8):
                # gets the first value in each square of the board to indicate player turn, so w = white, b = black
                player_turn = self.board[row][column][0]  
                if (player_turn == "w" and self.whiteTurn) or (player_turn == "b" and not self.whiteTurn):
                    # gets the second value in each square of the board to indicate the piece.
                    piece = self.board[row][column][1]

                    # If piece is a pawn
                    if piece == "P":
                        # Promote the pawn if it's in the back rank  
                        self.pawn_promotion()
                        pawn = Pawn(player_turn, self.whiteTurn)  
                        # Get pawn moves for the pawn at this row and column
                        pawn_valid_moves = pawn.all_possible_moves(player_turn, row, column, self.board, self.whiteTurn)
                        # Add the valid pawn moves to the moves list
                        moves.extend(pawn_valid_moves)

                    # If piece is a bishop
                    if piece == "B":
                        bishop = Bishop(player_turn, self.whiteTurn)
                        bishop_valid_moves = bishop.all_possible_moves(player_turn, row, column, self.board, self.whiteTurn)
                        # Add the valid bishop moves to the moves list
                        moves.extend(bishop_valid_moves)
                        
                    # If piece is a rook
                    if piece == "R":
                        rook = Rook(player_turn, self.whiteTurn)
                        rook_valid_moves = rook.all_possible_moves(player_turn, row, column, self.board, self.whiteTurn)
                        # Add the valid rook moves to the moves list
                        moves.extend(rook_valid_moves)
                        
                    # If piece is a king
                    if piece == "K":
                        king = King(player_turn, self.whiteTurn)
                        king_valid_moves = king.all_possible_moves(player_turn, row, column, self.board, self.whiteTurn)
                        # Add the valid king moves to the moves list
                        moves.extend(king_valid_moves)
                        
                    # If piece is a knight
                    if piece == "N":
                        knight = Knight(player_turn, self.whiteTurn)
                        knight_valid_moves = knight.all_possible_moves(player_turn, row, column, self.board, self.whiteTurn)
                        # Add the valid knight moves to the moves list
                        moves.extend(knight_valid_moves)
                        
                    # If piece is a queen
                    if piece == "Q":
                        queen = Queen(player_turn, self.whiteTurn)
                        queen_valid_moves = queen.all_possible_moves(player_turn, row, column, self.board, self.whiteTurn)
                        # Add the valid queen moves to the moves list
                        moves.extend(queen_valid_moves)
        return moves

    # calculate the points by looping through the board and adding each pieces value to self.white_points and self.black_points
    def get_points(self) -> int:
        self.white_points = 0
        self.black_points = 0
        chess_points = {"P": 1, "B": 3, "N": 3, "R": 5, "Q": 9, "K": 0}

        for row in range(8):
            for column in range(8):
                if self.board[row][column] != "--":
                    if self.board[row][column][0] == "w":
                        self.white_points += chess_points[self.board[row][column][1]]
                    else:
                        self.black_points += chess_points[self.board[row][column][1]]
        self.total_points = int(self.white_points) - int(self.black_points)
        return self.total_points

    def pawn_promotion(self):
        # if the pawn are in the back ranks promote them to a queen
        for column in range(8):
            if self.board[0][column] == "wP":
                self.board[0][column] = "wQ"
            elif self.board[7][column] == "bP":
                self.board[7][column] = "bQ"

    # return the player turn
    def player_turn(self) -> str:
        if self.whiteTurn:
            turn = "White's Turn"
        else:
            turn = "Black's Turn"

        return turn

    def is_their_white_king(self):
        # check if white king is there by looping through the board and returning True if "wK" is found
        for row in range(8):
            for column in range(8):
                if self.board[row][column] == "wK":
                    return True
        return False

    def is_their_black_king(self):
        # check if black king is there by looping through the board and returning True if "bK" is found
        for row in range(8):
            for column in range(8):
                if self.board[row][column] == "bK":
                    return True
        return False

    def find_white_king(self):
        # find white king by looping through the board and returning the co-ordinates of the white king
        for row in range(8):
            for column in range(8):
                if self.board[row][column] == "wK":
                    return (row, column)
        return ()

    def find_black_king(self):
        # find black king by looping through the board and returning the co-ordinates of the black king
        for row in range(8):
            for column in range(8):
                if self.board[row][column] == "bK":
                    return (row, column)
        return ()

    def in_checkmate(self):
        # if there are no valid moves and there is a check, there is a checkmate
        if len(self.get_valid_moves()) == 0 and self.in_check():
            return True
        return False
