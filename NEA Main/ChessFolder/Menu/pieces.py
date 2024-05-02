from move import Move

'''
This file contains the classes for every piece
It has one parent class: Piece, and 6 child classes.
Each child class inherits the turn and color of the piece being accessed from the Piece class 

The child classes contain the algorithms that find all possible moves that the respective piece can play
It then returns these moves to a possible moves list
'''


# Piece class represents a generic chess piece. It contains common attributes for all pieces.
class Piece:
    def __init__(self, color, white_turn):
        # The color of the piece (either 'w' for white or 'b' for black)
        self.color = color
        # The turn of the piece (True for white's turn, False for black's turn)
        self.turn = white_turn

# Pawn class represents a pawn piece. It inherits from the Piece class.
class Pawn(Piece):
    def __init__(self, color, white_turn):
        super().__init__(color, white_turn)
        # A tuple to store the position of the pawn that can be captured by en passant
        self.en_passant_possible = ()

    # this method finds all possible moves the pawn can play and appends these moves the valid_pawn_moves list, which is then returned upon completion
    def all_possible_moves(self, color, row, column, board, white_turn):
        # Calculate all valid moves for a pawn, including moving forward, capturing diagonally,
        # and moving two squares forward on the first move
        valid_pawn_moves = []
        if white_turn:
            if self.color == "w":
                # Check if the square in front of the pawn is empty
                if row - 1 >= 0 and board[row - 1][column] == "--":
                    valid_pawn_moves.append(Move((row, column), (row - 1, column), board))
                    # Check if it's the pawn's first move and the two squares in front are empty
                    if row == 6 and board[row - 2][column] == "--":
                        # if so the pawn can move two squares forward
                        valid_pawn_moves.append(Move((row, column), (row - 2, column), board))
                # Check if there's an enemy piece diagonally to the left
                if column - 1 >= 0 and board[row - 1][column - 1][0] == "b":
                    valid_pawn_moves.append(Move((row, column), (row - 1, column - 1), board))
                # Check if there's an enemy piece diagonally to the right
                if column + 1 <= 7 and board[row - 1][column + 1][0] == "b":
                    valid_pawn_moves.append(Move((row, column), (row - 1, column + 1), board))

                #if the co-ordinate to the diagonal right and left of the pawn is en passant possible
                if column + 1 <= 7 and (row - 1, column + 1) == self.en_passant_possible:
                    valid_pawn_moves.append(Move((row, column), (row - 1, column + 1), board, is_enpassant=True))
                if column - 1 >= 0 and (row - 1, column - 1) == self.en_passant_possible:
                    valid_pawn_moves.append(Move((row, column), (row - 1, column - 1), board, is_enpassant=True))
                    
            return valid_pawn_moves
        else:
            if self.color == "b":
                #if the co-ordinate to the diagonal right and left of the pawn is en passant possible 
                if column + 1 < 8 and (row + 1, column + 1) == self.en_passant_possible:
                    valid_pawn_moves.append(Move((row, column), (row + 1, column + 1), board, is_enpassant=True))
                if column - 1 >= 0 and (row + 1, column - 1) == self.en_passant_possible:
                    valid_pawn_moves.append(Move((row, column), (row + 1, column - 1), board, is_enpassant=True))

                # Check if the square in front of the pawn is empty
                if row + 1 < 8 and board[row + 1][column] == "--":
                    valid_pawn_moves.append(Move((row, column), (row + 1, column), board))
                    # Check if it's the pawn's first move and the two squares in front are empty
                    if row == 1 and board[row + 2][column] == "--":
                        # if so the pawn can move two squares forward
                        valid_pawn_moves.append(Move((row, column), (row + 2, column), board))
                # Check if there's an enemy piece diagonally to the left
                if column + 1 < 8 and board[row + 1][column + 1][0] == "w":
                    valid_pawn_moves.append(Move((row, column), (row + 1, column + 1), board))
                # Check if there's an enemy piece diagonally to the right
                if column - 1 >= 0 and board[row + 1][column - 1][0] == "w":
                    valid_pawn_moves.append(Move((row, column), (row + 1, column - 1), board))

            return valid_pawn_moves

# Bishop class represents a bishop piece. It inherits from the Piece class.
class Bishop(Piece):
    def __init__(self, color, white_turn):
        super().__init__(color, white_turn)

    # this method finds all possible moves the bishop can play and appends these moves the valid_bishop_moves list, which is then returned upon completion
    def all_possible_moves(self, color, row, column, board, white_turn):
        # list for all valid_bishop_moves
        valid_bishop_moves = []
        if white_turn:
            if self.color == "w":
                # Check diagonally up-left
                i, j = row - 1, column - 1
                while i >= 0 and j >= 0 and (board[i][j] == "--" or board[i][j][0] == "b"):
                    valid_bishop_moves.append(Move((row, column), (i, j), board))
                    if board[i][j] != "--":
                        break
                    i -= 1
                    j -= 1

                # Check diagonally up-right
                i, j = row - 1, column + 1
                while i >= 0 and j < 8 and (board[i][j] == "--" or board[i][j][0] == "b"):
                    valid_bishop_moves.append(Move((row, column), (i, j), board))
                    if board[i][j] != "--":
                        break
                    i -= 1
                    j += 1

                # Check diagonally down-left
                i, j = row + 1, column - 1
                while i < 8 and j >= 0 and (board[i][j] == "--" or board[i][j][0] == "b"):
                    valid_bishop_moves.append(Move((row, column), (i, j), board))
                    if board[i][j] != "--":
                        break
                    i += 1
                    j -= 1

                # Check diagonally down-right
                i, j = row + 1, column + 1
                while i < 8 and j < 8 and (board[i][j] == "--" or board[i][j][0] == "b"):
                    valid_bishop_moves.append(Move((row, column), (i, j), board))
                    if board[i][j] != "--":
                        break
                    i += 1
                    j += 1
            return valid_bishop_moves

        else:
            if self.color == "b":
                # Check diagonally up-left
                i, j = row - 1, column - 1
                while i >= 0 and j >= 0 and (board[i][j] == "--" or board[i][j][0] == "w"):
                    valid_bishop_moves.append(Move((row, column), (i, j), board))
                    if board[i][j] != "--":
                        break
                    i -= 1
                    j -= 1

                # Check diagonally up-right
                i, j = row - 1, column + 1
                while i >= 0 and j < 8 and (board[i][j] == "--" or board[i][j][0] == "w"):
                    valid_bishop_moves.append(Move((row, column), (i, j), board))
                    if board[i][j] != "--":
                        break
                    i -= 1
                    j += 1

                # Check diagonally down-left
                i, j = row + 1, column - 1
                while i < 8 and j >= 0 and (board[i][j] == "--" or board[i][j][0] == "w"):
                    valid_bishop_moves.append(Move((row, column), (i, j), board))
                    if board[i][j] != "--":
                        break
                    i += 1
                    j -= 1

                # Check diagonally down-right
                i, j = row + 1, column + 1
                while i < 8 and j < 8 and (board[i][j] == "--" or board[i][j][0] == "w"):
                    valid_bishop_moves.append(Move((row, column), (i, j), board))
                    if board[i][j] != "--":
                        break
                    i += 1
                    j += 1

            return valid_bishop_moves

# Rook class represents a rook piece. It inherits from the Piece class.
class Rook(Piece):
    def __init__(self, color, white_turn):
        super().__init__(color, white_turn)

    # this method finds all possible moves the rook can play and appends these moves the valid_rook_moves list, which is then returned upon completion
    def all_possible_moves(self, color, row, column, board, white_turn):
        # list for all valid_rook_moves
        valid_rook_moves = []
        if white_turn:
            if self.color == "w":
                # Check horizontally to the left
                j = column - 1
                while j >= 0 and (board[row][j] == "--" or board[row][j][0] == "b"):
                    valid_rook_moves.append(Move((row, column), (row, j), board))
                    if board[row][j] != "--":
                        break
                    j -= 1

                # Check horizontally to the right
                j = column + 1
                while j < 8 and (board[row][j] == "--" or board[row][j][0] == "b"):
                    valid_rook_moves.append(Move((row, column), (row, j), board))
                    if board[row][j] != "--":
                        break
                    j += 1

                # Check vertically upwards
                i = row - 1
                while i >= 0 and (board[i][column] == "--" or board[i][column][0] == "b"):
                    valid_rook_moves.append(Move((row, column), (i, column), board))
                    if board[i][column] != "--":
                        break
                    i -= 1

                # Check vertically downwards
                i = row + 1
                while i < 8 and (board[i][column] == "--" or board[i][column][0] == "b"):
                    valid_rook_moves.append(Move((row, column), (i, column), board))
                    if board[i][column] != "--":
                        break
                    i += 1
            return valid_rook_moves
        else:
            if self.color == "b":
                # Check horizontally to the left
                j = column - 1
                while j >= 0 and (board[row][j] == "--" or board[row][j][0] == "w"):
                    valid_rook_moves.append(Move((row, column), (row, j), board))
                    if board[row][j] != "--":
                        break
                    j -= 1

                # Check horizontally to the right
                j = column + 1
                while j < 8 and (board[row][j] == "--" or board[row][j][0] == "w"):
                    valid_rook_moves.append(Move((row, column), (row, j), board))
                    if board[row][j] != "--":
                        break
                    j += 1

                # Check vertically upwards
                i = row - 1
                while i >= 0 and (board[i][column] == "--" or board[i][column][0] == "w"):
                    valid_rook_moves.append(Move((row, column), (i, column), board))
                    if board[i][column] != "--":
                        break
                    i -= 1

                # Check vertically downwards
                i = row + 1
                while i < 8 and (board[i][column] == "--" or board[i][column][0] == "w"):
                    valid_rook_moves.append(Move((row, column), (i, column), board))
                    if board[i][column] != "--":
                        break
                    i += 1

            return valid_rook_moves

# King class represents a king piece. It inherits from the Piece class.
class King(Piece):
    def __init__(self, color, white_turn):
        super().__init__(color, white_turn)

    # this method finds all possible moves the king can play and appends these moves the valid_king_moves list, which is then returned upon completion
    def all_possible_moves(self, color, row, column, board, white_turn):
        # list for all valid_king_moves
        valid_king_moves = []
        if white_turn:
            if self.color == "w":
                #Move down
                if row + 1 < 8 and (board[row + 1][column] == "--" or board[row + 1][column][0] == "b"):
                    valid_king_moves.append(Move((row, column), (row + 1, column), board))
                #Move up
                if row - 1 >= 0 and (board[row - 1][column] == "--" or board[row - 1][column][0] == "b"):
                    valid_king_moves.append(Move((row, column), (row - 1, column), board))
                #Move right
                if column + 1 < 8 and (board[row][column + 1] == "--" or board[row][column + 1][0] == "b"):
                    valid_king_moves.append(Move((row, column), (row, column + 1), board))
                # Move Left
                if column - 1 >= 0 and (board[row][column - 1] == "--" or board[row][column - 1][0] == "b"):
                    valid_king_moves.append(Move((row, column), (row, column - 1), board))
                # Move Up-Right
                if row + 1 < 8 and column + 1 < 8 and (board[row + 1][column + 1] == "--" or board[row + 1][column + 1][0] == "b"):
                    valid_king_moves.append(Move((row, column), (row + 1, column + 1), board))
                # Move Up-Left
                if row + 1 < 8 and column - 1 >= 0 and (board[row + 1][column - 1] == "--" or board[row + 1][column - 1][0] == "b"):
                    valid_king_moves.append(Move((row, column), (row + 1, column - 1), board))
                # Move Down-Right
                if row - 1 >= 0 and column + 1 < 8 and (board[row - 1][column + 1] == "--" or board[row - 1][column + 1][0] == "b"):
                    valid_king_moves.append(Move((row, column), (row - 1, column + 1), board))
                # Move Down-Left
                if row - 1 >= 0 and column - 1 >= 0 and (board[row - 1][column - 1] == "--" or board[row - 1][column - 1][0] == "b"):
                    valid_king_moves.append(Move((row, column), (row - 1, column - 1), board))
            return valid_king_moves

        else:
            if self.color == "b":
                # Move down
                if row + 1 < 8 and (board[row + 1][column] == "--" or board[row + 1][column][0] == "w"):
                    valid_king_moves.append(Move((row, column), (row + 1, column), board))
                # Move up
                if row - 1 >= 0 and (board[row - 1][column] == "--" or board[row - 1][column][0] == "w"):
                    valid_king_moves.append(Move((row, column), (row - 1, column), board))
                # Move right
                if column + 1 < 8 and (board[row][column + 1] == "--" or board[row][column + 1][0] == "w"):
                    valid_king_moves.append(Move((row, column), (row, column + 1), board))
                # Move Left
                if column - 1 >= 0 and (board[row][column - 1] == "--" or board[row][column - 1][0] == "w"):
                    valid_king_moves.append(Move((row, column), (row, column - 1), board))
                # Move Up-Right
                if row + 1 < 8 and column + 1 < 8 and (board[row + 1][column + 1] == "--" or board[row + 1][column + 1][0] == "w"):
                    valid_king_moves.append(Move((row, column), (row + 1, column + 1), board))
                # Move Up-Left
                if row + 1 < 8 and column - 1 >= 0 and (board[row + 1][column - 1] == "--" or board[row + 1][column - 1][0] == "w"):
                    valid_king_moves.append(Move((row, column), (row + 1, column - 1), board))
                # Move Down-Right
                if row - 1 >= 0 and column + 1 < 8 and (board[row - 1][column + 1] == "--" or board[row - 1][column + 1][0] == "w"):
                    valid_king_moves.append(Move((row, column), (row - 1, column + 1), board))
                # Move Down-Left
                if row - 1 >= 0 and column - 1 >= 0 and (board[row - 1][column - 1] == "--" or board[row - 1][column - 1][0] == "w"):
                    valid_king_moves.append(Move((row, column), (row - 1, column - 1), board))
            return valid_king_moves

# Queen class represents a queen piece. It inherits from the Piece class.
class Queen(Piece):
    def __init__(self, color, white_turn):
        super().__init__(color, white_turn)

    # this method finds all possible moves the queen can play and appends these moves the valid_queen_moves list, which is then returned upon completion
    def all_possible_moves(self, color, row, column, board, white_turn):
        # list for all valid_queen_moves
        valid_queen_moves = []
        if white_turn:
            if self.color == "w":
                # Check horizontally to the left
                j = column - 1
                while j >= 0 and (board[row][j] == "--" or board[row][j][0] == "b"):
                    valid_queen_moves.append(Move((row, column), (row, j), board))
                    if board[row][j] != "--":
                        break
                    j -= 1

                # Check horizontally to the right
                j = column + 1
                while j < 8 and (board[row][j] == "--" or board[row][j][0] == "b"):
                    valid_queen_moves.append(Move((row, column), (row, j), board))
                    if board[row][j] != "--":
                        break
                    j += 1

                # Check vertically upwards
                i = row - 1
                while i >= 0 and (board[i][column] == "--" or board[i][column][0] == "b"):
                    valid_queen_moves.append(Move((row, column), (i, column), board))
                    if board[i][column] != "--":
                        break
                    i -= 1

                # Check vertically downwards
                i = row + 1
                while i < 8 and (board[i][column] == "--" or board[i][column][0] == "b"):
                    valid_queen_moves.append(Move((row, column), (i, column), board))
                    if board[i][column] != "--":
                        break
                    i += 1

                # check diagonally up-left
                i, j = row - 1, column - 1
                while i >= 0 and j >= 0 and (board[i][j] == "--" or board[i][j][0] == "b"):
                    valid_queen_moves.append(Move((row, column), (i, j), board))
                    if board[i][j] != "--":
                        break
                    i -= 1
                    j -= 1

                # Check diagonally up-right
                i, j = row - 1, column + 1
                while i >= 0 and j < 8 and (board[i][j] == "--" or board[i][j][0] == "b"):
                    valid_queen_moves.append(Move((row, column), (i, j), board))
                    if board[i][j] != "--":
                        break
                    i -= 1
                    j += 1

                # Check diagonally down-left
                i, j = row + 1, column - 1
                while i < 8 and j >= 0 and (board[i][j] == "--" or board[i][j][0] == "b"):
                    valid_queen_moves.append(Move((row, column), (i, j), board))
                    if board[i][j] != "--":
                        break
                    i += 1
                    j -= 1

                # Check diagonally down-right
                i, j = row + 1, column + 1
                while i < 8 and j < 8 and (board[i][j] == "--" or board[i][j][0] == "b"):
                    valid_queen_moves.append(Move((row, column), (i, j), board))
                    if board[i][j] != "--":
                        break
                    i += 1
                    j += 1
            return valid_queen_moves
        else:
            if self.color == "b":
                # Check horizontally to the left
                j = column - 1
                while j >= 0 and (board[row][j] == "--" or board[row][j][0] == "w"):
                    valid_queen_moves.append(Move((row, column), (row, j), board))
                    if board[row][j] != "--":
                        break
                    j -= 1

                # Check horizontally to the right
                j = column + 1
                while j < 8 and (board[row][j] == "--" or board[row][j][0] == "w"):
                    valid_queen_moves.append(Move((row, column), (row, j), board))
                    if board[row][j] != "--":
                        break
                    j += 1

                # Check vertically upwards
                i = row - 1
                while i >= 0 and (board[i][column] == "--" or board[i][column][0] == "w"):
                    valid_queen_moves.append(Move((row, column), (i, column), board))
                    if board[i][column] != "--":
                        break
                    i -= 1

                # Check vertically downwards
                i = row + 1
                while i < 8 and (board[i][column] == "--" or board[i][column][0] == "w"):
                    valid_queen_moves.append(Move((row, column), (i, column), board))
                    if board[i][column] != "--":
                        break
                    i += 1

                # check diagonally up-left
                i, j = row - 1, column - 1
                while i >= 0 and j >= 0 and (board[i][j] == "--" or board[i][j][0] == "w"):
                    valid_queen_moves.append(Move((row, column), (i, j), board))
                    if board[i][j] != "--":
                        break
                    i -= 1
                    j -= 1

                # Check diagonally up-right
                i, j = row - 1, column + 1
                while i >= 0 and j < 8 and (board[i][j] == "--" or board[i][j][0] == "w"):
                    valid_queen_moves.append(Move((row, column), (i, j), board))
                    if board[i][j] != "--":
                        break
                    i -= 1
                    j += 1

                # Check diagonally down-left
                i, j = row + 1, column - 1
                while i < 8 and j >= 0 and (board[i][j] == "--" or board[i][j][0] == "w"):
                    valid_queen_moves.append(Move((row, column), (i, j), board))
                    if board[i][j] != "--":
                        break
                    i += 1
                    j -= 1

                # Check diagonally down-right
                i, j = row + 1, column + 1
                while i < 8 and j < 8 and (board[i][j] == "--" or board[i][j][0] == "w"):
                    valid_queen_moves.append(Move((row, column), (i, j), board))
                    if board[i][j] != "--":
                        break
                    i += 1
                    j += 1
            return valid_queen_moves

# Knight class represents a knight piece. It inherits from the Piece class.
class Knight(Piece):
    def __init__(self, color, white_turn):
        super().__init__(color, white_turn)

    # this method finds all possible moves the knight can play and appends these moves the valid_knight_moves list, which is then returned upon completion
    def all_possible_moves(self, color, row, column, board, white_turn):
        valid_knight_moves = []
        if white_turn:
            if self.color == "w":
                # Possible knight moves relative to its position
                # all possible moves by the knight are in an "L" position
                knight_moves = [
                    (row + 2, column + 1),
                    (row + 2, column - 1),
                    (row - 2, column + 1),
                    (row - 2, column - 1),
                    (row + 1, column + 2),
                    (row + 1, column - 2),
                    (row - 1, column + 2),
                    (row - 1, column - 2),
                ]

                # Filter possible moves
                for move in knight_moves:
                    r, c = move
                    if 0 <= r < 8 and 0 <= c < 8 and (board[r][c] == "--" or board[r][c][0] == "b"):
                        valid_knight_moves.append(Move((row, column), (r, c), board))

            return valid_knight_moves
        else:
            if self.color == "b":
                # Possible knight moves relative to its position
                # all possible moves by the knight are in an "L" position
                knight_moves = [
                    (row + 2, column + 1),
                    (row + 2, column - 1),
                    (row - 2, column + 1),
                    (row - 2, column - 1),
                    (row + 1, column + 2),
                    (row + 1, column - 2),
                    (row - 1, column + 2),
                    (row - 1, column - 2),
                ]

                # Filter possible moves
                for move in knight_moves:
                    r, c = move
                    if 0 <= r < 8 and 0 <= c < 8 and (board[r][c] == "--" or board[r][c][0] == "w"):
                        valid_knight_moves.append(Move((row, column), (r, c), board))
            return valid_knight_moves
