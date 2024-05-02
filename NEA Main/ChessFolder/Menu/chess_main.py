'''
This file is the file that is run.
It imports all necessary objects in all the other files and it holds the algorithms for the menu system and others.
It deals with what the user is trying to input into the program and calls the proper methods/functions needed to respond accordingly to the user
'''

# importing all the libraries needed.
import pygame as pg
from tkinter import messagebox, simpledialog

# importing all the different classes and functions.
from display_images import Button, Image
from chess_battle import StateOfGame
from text import Text
from board import Board
from move import Move, MoveLog
from chess_train import CreateState
from save import save_save_states, load_save_states, SaveState

# initialising pygame
pg.init()

# The constants used throughout the code:
MENU_WIDTH = 1300
MENU_HEIGHT = 900
SQUARE_SIZE = 80
FPS = 30

# the SCREEN initialised by pygame with the dimensions set by the constants above, it is also a constant:
SCREEN = pg.display.set_mode((MENU_WIDTH, MENU_HEIGHT))

# board dimensions and width useful info to remember
"""
board_width = 640
board_height = 640
dimension = 8
Loads images for the pieces. 
"""

# the buttons and images being initialised that are found in both battle and train menu:
back_button = Button(20, 700, 1, pg.image.load("ChessFolder/ButtonImages/back-button.png").convert_alpha())
chess_white_checkmate_image = Image(675, 193.5, 1, pg.image.load("ChessFolder/ButtonImages/white-checkmate.png").convert_alpha())
chess_black_checkmate_image = Image(675, 193.5, 1, pg.image.load("ChessFolder/ButtonImages/black-checkmate.png").convert_alpha())
stalesmate_image = Image(675, 193.5, 1, pg.image.load("ChessFolder/ButtonImages/stalesmate.png").convert_alpha())
draw_image = Image(675, 193.5, 1, pg.image.load("ChessFolder/ButtonImages/draw.png").convert_alpha())
move_log_image = Image(20, 50, 1, pg.image.load("ChessFolder/ButtonImages/move-log.png").convert_alpha())

# the sounds used during the game:
capture_sound = pg.mixer.Sound("ChessFolder/Sounds/capture.mp3")
castle_sound = pg.mixer.Sound("ChessFolder/Sounds/castle.mp3")
move_sound = pg.mixer.Sound("ChessFolder/Sounds/move-self.mp3")
check_sound = pg.mixer.Sound("ChessFolder/Sounds/move-check.mp3")
checkmate_sound = pg.mixer.Sound("ChessFolder/Sounds/checkmate.mp3")

# the class used for setting up the board on both menus:
board_setup = Board(SCREEN)

# the class used for playing the chess game, gs is used in battle, cs is used in train:
gs = StateOfGame()
cs = CreateState()

# the move log classes used in the battle menu, and the train menu:
move_log_battle = MoveLog("Arial", 15, 30, 150, SCREEN)
move_log_train = MoveLog("Arial", 15, 30, 150, SCREEN)

# the dynamic menu system:
def battle_menu():
    clock = pg.time.Clock()
    run = True

    # keeps track of the last click of the user
    square_selected = ()
    # keeps track of the players clicks  
    player_clicks = []  

    #creates global variables for gs and move_log_battle so that they can be used everywhere.
    global gs
    global move_log_battle

    # generates all valid moves for the first turn of the game
    valid_moves = gs.get_valid_moves()
    # a valid move hasnt been made; this is done to ensure the program isnt constantly calling get_valid_moves()
    valid_move_made = False  

    # this creates the player_turn variable which keeps track if its white's or black's turn and a Text object to display said turn.
    player_turn = gs.player_turn()
    whos_turn_is_it = Text("Arial", 40, f"{player_turn}", (255, 255, 255))

    # the reset_button that when clicked resets the board and the tips text which just notifies the user how to undo a move.
    reset_button = Button(1150, 365, 0.5, pg.image.load("ChessFolder/ButtonImages/reset-button-1.png").convert_alpha())
    tips = Text("Arial", 40, "Press back arrow ← to undo a move!", (255, 255, 255))


    # the buttons used to save, load and delete chess games:
    save_load_button = Button(20, 800, 1, pg.image.load("ChessFolder/ButtonImages/save-load.png"))
    bin_button = Button(320,780,1,pg.transform.scale(pg.image.load("ChessFolder/ButtonImages/bin.png"),(100,100)))

    while run:
        # sets up the new menu
        SCREEN.fill((41, 43, 47))
        pg.display.set_caption("Battle Menu")

        # this draws the board throughout the game, from start to finish.
        board_setup.draw_board(gs, valid_moves, square_selected)

        # draws the images for the move_log, and tips.  
        move_log_image.draw_image(SCREEN)
        tips.draw_text_on_screen(500, 800, SCREEN)

        #creates a new object for whos_turn_is_it and draws is it on the screen, since the text changes from "White's Turn to Black's Turn"
        whos_turn_is_it = Text("Arial", 40, f"{player_turn}", (255, 255, 255))
        whos_turn_is_it.draw_text_on_screen(500, 30, SCREEN)

        # if the save/load button is clicked on the screen (this also draws the save/load button on screen).
        if save_load_button.draw_button(SCREEN):
            save_load_input = simpledialog.askstring("Save or Load", "Input 'save' to save the game or 'load' to load a previous save file.")
            # try and except to ensure that an expected attributeError(None is inputted) does not cause the program to crash
            try:
                if save_load_input.lower() == "save":                
                    # load the array of saves
                    loaded_save_states:list[SaveState] = load_save_states( 'saved_games.txt' )                
                    save_state: SaveState

                    # this while loop ensures that the name for the save is unique by repeatedly prompting the user to enter a unique name.        
                    while True:     
                        # user is prompted to enter a unique name:
                        name_save = simpledialog.askstring("Enter a unique name for the save name for the game", "The name must be unique!")
                        if name_save == None:
                            break
                        
                        #name_found is initially setup as False, it will change if a duplicate chess game has been saved with the same name.
                        name_found = False                    
                        for save_state in loaded_save_states:
                            # check if save name exists in the array of saves
                            if save_state.name == name_save:
                                #if save name exists name_found is set to True 
                                name_found = True
                                # break for loop
                                break
                        
                        #if the name has not been found keep name_found = False
                        if not name_found: 
                            # break while loop
                            break
                    
                    # if name_save had an input and it was unique:
                    if name_save != None:
                        # create a saveState object to save the current game's info
                        new_save_state = SaveState( name_save, gs, move_log_battle.move_notations )

                        # add the save state to the array of saves
                        loaded_save_states.append( new_save_state )
                        
                        # save the file
                        save_save_states( loaded_save_states, 'saved_games.txt' )

                        # prompt to let user know game has saved
                        messagebox.showinfo("Game saved", f"The game has been saved under the name {name_save}")
                
                # if load is inputted:
                elif save_load_input.lower() == "load":
                    
                    # load the array of saves
                    loaded_save_states:list[SaveState] = load_save_states( 'saved_games.txt' )
                    
                    # get list of game names
                    save_names = [save_state.name for save_state in loaded_save_states]

                    #makes sure none doesnt get passed through
                    save_names = [name for name in save_names if name is not None]

                    while True:    
                        # ask user to type in the name of the game they want to load
                        name_save = simpledialog.askstring("Enter a name from the following list", ", ".join( save_names ))
                        # if the user closes the dialog or enters nothing:
                        if name_save is None:
                            break

                        # name_found is set to false unless the save is in the list of save_names                        
                        name_found = False                        
                        if name_save in save_names:
                            name_found = True                        
                        if name_found:
                            break
                    
                    #if a save with the name inputted is found and that name inputted is not nothing:
                    if name_save is not None and name_found is True:

                        new_state: SaveState
                        
                        # creates a new_state for the loaded game
                        for save_state in loaded_save_states:
                            if save_state.name == name_save:
                                new_state = save_state
                                
                        # load the game state from save
                        gs = new_state.game_state
                        move_log_battle.move_notations = new_state.move_notations

                        #restart the square_selected and player_clicks so previous clicks from saves dont carry over.
                        square_selected = ()
                        player_clicks = []

                        #recheck player turn and generate new valid_moves 
                        player_turn = gs.player_turn()
                        valid_moves = gs.get_valid_moves()

            except AttributeError:
                pass        
        
        #if the bin_button is clicked (this also draws the bin button on screen).
        if bin_button.draw_button(SCREEN):
            delete_all_or_one = simpledialog.askstring("Delete save","Would you like to delete one save file or all?\n Input 'one' or 'all'.")
            # try and except to ensure that an expected attributeError(None is inputted) does not cause the program to crash
            try: 
                if delete_all_or_one.lower() == "all":
                    delete_input = messagebox.askyesno("About to delete all save files!", "Are you sure you would like to delete all your save files?")
                    # if the user's response clicked is yes:
                    if delete_input:
                        messagebox.showinfo("Deleted","Save files deleted.")
                        # reset the loaded save states list
                        loaded_save_states = []
                        with open("saved_games.txt", "w") as file:
                            #remove all contents in the file
                            file.truncate(0)

                elif delete_all_or_one.lower() == "one":
                    loaded_save_states: list[SaveState] = load_save_states('saved_games.txt')            
                    # get list of game names
                    save_names = [save_state.name for save_state in loaded_save_states]
                    # remove all save names where name is None
                    save_names = [name for name in save_names if name is not None]

                    # Ask user to type in the name of game they want to delete
                    name_save = simpledialog.askstring("Enter a name from the following list", ", ".join(save_names))
                    if name_save is not None:
                        # Find and remove the save state with the given name
                        loaded_save_states = [save_state for save_state in loaded_save_states if save_state.name != name_save]
                        
                        # Save the updated list of save states
                        save_save_states(loaded_save_states, 'saved_games.txt')
            except AttributeError:
                pass
        # if the back button is pressed ( this also draws the back button):
        if back_button.draw_button(SCREEN):
            #remove the red highlighting  
            board_setup.red_squares = {}
            # exit the while loop which causes the program to go back to main menu
            run = False

        # if reset button is pressed ( this also draws the reset button ):
        if reset_button.draw_button(SCREEN):
            # reset everything:
            move_log_battle.reset_move_log()
            board_setup.red_squares = {}
            gs.reset_game()
            player_turn = "White's Turn"
            # re generate valid moves from the starting position
            valid_moves = gs.get_valid_moves()


        for event in pg.event.get():
            # if the user quits the program:
            if event.type == pg.QUIT:
                run = False
                # close pygame
                pg.quit()

            # if the user presses a button on their mouse:
            elif event.type == pg.MOUSEBUTTONDOWN:
                # if the button is left click:
                if event.button == 1:
                    # gets position of the mouse click
                    mouse_location = pg.mouse.get_pos()
                    # makes sure mouse position looking at the board.  
                    if (500 <= mouse_location[0] <= 1140) and (100 <= mouse_location[1] <= 740):

                        # gets the column the mouse is in, in relation to the chess board. The "- 500" is so that it calibrates for the whole background (move log etc, the board isnt the only thing in the background) 
                        mouse_column = (mouse_location[0] - 500) // SQUARE_SIZE
                        # gets the row the mouse is in, in relation to the chess board. The "- 100" is so that it calibrates for the whole background (move log etc, the board isnt the only thing in the background) 
                        mouse_row = (mouse_location[1] - 100) // SQUARE_SIZE

                        # if the user clicked same square twice:
                        if square_selected == (mouse_row,mouse_column):
                            # reset the list and tuple:  
                            square_selected = ()  
                            player_clicks = []
                        else:

                            # creates a (column,row) co-ordinate.
                            square_selected = (mouse_row,mouse_column)
                            # append the clicks into the player clicks array.  
                            player_clicks.append(square_selected)  
                        
                        # after 2nd click in two different squares:
                        if len(player_clicks) == 2:

                            # uses the Move object to create a chess move with the players recorded moves. 
                            chess_move = Move(player_clicks[0], player_clicks[1], gs.board)

                            # loops through all the valid_moves on the board  
                            for i in range(len(valid_moves)):
                                # if the users move is in the valid_moves list:
                                if chess_move == valid_moves[i]:
                                    # make the move
                                    gs.make_move(valid_moves[i])

                                    #reset the highlight
                                    board_setup.red_squares = {}

                                    # promote any pawn that has made to its back rank
                                    gs.pawn_promotion()

                                    # play appropriate sounds
                                    if valid_moves[i].is_castle_move:
                                        castle_sound.play()
                                    elif chess_move.the_piece_captured != "--" or valid_moves[i].is_enpassant_move:
                                        if gs.in_check() and not (gs.in_checkmate()):
                                            check_sound.play()
                                        else:
                                            capture_sound.play()
                                    elif gs.in_check():
                                        check_sound.play()
                                    else:
                                        move_sound.play()
                                    if gs.in_checkmate():
                                        checkmate_sound.play()
                                    
                                    # set valid_move_made = True
                                    valid_move_made = True

                                    # draw the board.
                                    board_setup.draw_board(gs, valid_moves, square_selected)

                                    # reset so player can make another move  
                                    square_selected = ()  
                                    player_clicks = []
                                    
                                    # switch player_turn text
                                    player_turn = gs.player_turn()

                                    # add appropriate notation to the move log
                                    move_notation = chess_move.get_chess_notation(gs.turn_number, gs)
                                    move_log_battle.add_move(move_notation)

                            # if the move was not valid, reset the players clicks so another move can be made
                            if not valid_move_made:
                                player_clicks = [square_selected]
                            
                            # update the screen
                            pg.display.flip()

                # if right click is pressed:            
                elif event.button == 3:
                    # gets position of the mouse click
                    mouse_location = pg.mouse.get_pos()

                    # makes sure mouse position looking at the board.
                    if (500 <= mouse_location[0] <= 1140) and (100 <= mouse_location[1] <= 740):

                        # gets the column the mouse is in, in relation to the chess board. The "- 500" is so that it calibrates for the size of the background  
                        mouse_column = (mouse_location[0] - 500) // SQUARE_SIZE
                        # gets the row the mouse is in, in relation to the chess board. The "- 100" is so that it calibrates for the size of the background  
                        mouse_row = (mouse_location[1] - 100) // SQUARE_SIZE

                        # make the square clicked highlighted  
                        board_setup.right_click(mouse_row, mouse_column)

                        # update the screen
                        pg.display.flip()

            
            elif event.type == pg.KEYDOWN:

                #if back key is pressed undo move   
                if event.key == pg.K_LEFT:
                    # if there have been previous moves:  
                    if len(gs.log) > 0:
                        # undo the move
                        gs.undo_move()
                        board_setup.red_squares = {}

                        # regenerate valid moves since we just undid the move.
                        valid_move_made = True  
                        move_sound.play()

                        # reset checkmate or stalemate:
                        gs.checkmate = False
                        gs.stalemate = False
                        
                        # remove last move log
                        move_log_battle.remove_last_move()

                        # switch the player turn text
                        if player_turn == "White's Turn":
                            player_turn = "Black's Turn"
                        else:
                            player_turn = "White's Turn"

        # points system for the pieces
        if gs.get_points() > 0 or gs.get_points() < 0:  
            absolute_value_points = abs(gs.get_points())
            white_points = Text("Arial", 20, f"+{absolute_value_points}", (255, 255, 255))
            black_points = Text("Arial", 20, f"+{absolute_value_points}", (255, 255, 255))
            if gs.get_points() > 0:
                black_points.remove_text_on_screen(1150, 100, SCREEN)
                white_points.draw_text_on_screen(1150, 720, SCREEN)
            if gs.get_points() < 0:
                white_points.remove_text_on_screen(1150, 720, SCREEN)
                black_points.draw_text_on_screen(1150, 100, SCREEN)

        # if a valid move has been made:
        if valid_move_made:
            # generate all valid mvoes again from current position.
            valid_moves = gs.get_valid_moves()
            # dont generate valid moves constantly  
            valid_move_made = False  

        # if there has been a checkmate:
        if gs.checkmate is True:

            # if its white's turn they have been checkmate so draw black victory:
            if gs.player_turn() == "White's Turn":
                chess_black_checkmate_image.draw_image(SCREEN)
            # vice versa
            else:
                chess_white_checkmate_image.draw_image(SCREEN)

        # if there has been a stalemate:        
        elif gs.stalemate is True:
            stalesmate_image.draw_image(SCREEN)

        elif gs.is_draw():
            draw_image.draw_image(SCREEN)
            valid_moves = []


        # draw the move notation
        move_log_battle.draw_move_log()

        # the frames per second of the program:
        clock.tick(FPS)

        # update the screen:
        pg.display.flip()

def train_menu():
    clock = pg.time.Clock()
    run = True

    # loads the images for the pieces clicked to add pieces to the board
    chess_create_images = board_setup.load_chess_piece_images((100, 100))

    # assigns the player's turn to the variable player turn
    player_turn = cs.player_turn()


    # creates the buttons for black and white used to allow the user to manually setup their board:
    white_king = Button(1150, 100, 1, chess_create_images["wK"])
    white_queen = Button(1150, 200, 1, chess_create_images["wQ"])
    white_rook = Button(1150, 300, 1, chess_create_images["wR"])
    white_bishop = Button(1150, 400, 1, chess_create_images["wB"])
    white_knight = Button(1150, 500, 1, chess_create_images["wN"])
    white_pawn = Button(1150, 600, 1, chess_create_images["wP"])

    black_king = Button(400, 100, 1, chess_create_images["bK"])
    black_queen = Button(400, 200, 1, chess_create_images["bQ"])
    black_rook = Button(400, 300, 1, chess_create_images["bR"])
    black_bishop = Button(400, 400, 1, chess_create_images["bB"])
    black_knight = Button(400, 500, 1, chess_create_images["bN"])
    black_pawn = Button(400, 600, 1, chess_create_images["bP"])


    # the buttons used throughout the train menu program, that when clicked perform a certain operation.
    x_button = Button(1150, 700, 1, pg.transform.scale(pg.image.load("ChessFolder/ButtonImages/x-button.png"), (100, 100)))
    reset_button = Button(400, 700, 1, pg.transform.scale(pg.image.load("ChessFolder/ButtonImages/reset-button-1.png"), (100, 100)))
    play_button = Button(662, 750, 1, pg.image.load("ChessFolder/ButtonImages/play-button.png"))

    # the piece selected for the user is by default set to --
    piece_selected = "--"

    # piece addition pngs
    pieces = {
        "wK": white_king,
        "wB": white_bishop,
        "wQ": white_queen,
        "wR": white_rook,
        "wN": white_knight,
        "wP": white_pawn,
        "bK": black_king,
        "bQ": black_queen,
        "bR": black_rook,
        "bB": black_bishop,
        "bN": black_knight,
        "bP": black_pawn,
    }
    
    # keeps track of the last click of the user
    square_selected = ()

    # keeps track of the players clicks  
    player_clicks = []  

    while run:
        # sets up the new menu
        SCREEN.fill((41, 43, 47))
        pg.display.set_caption("Train Menu")

        # draws the empty board
        board_setup.draw_empty_board(cs)

        # draws the move log image and creates the object to display whos turn it is
        move_log_image.draw_image(SCREEN)
        whos_turn_is_it = Text("Arial", 40, f"{player_turn}", (255, 255, 255))

        # if the user is still adding pieces and not playing the game
        if cs.adding_pieces:

            for piece_type, piece in pieces.items():
                # if a piece is clicked on the screen (this also draws the image):
                if piece.draw_button(SCREEN):
                    # if there is already a white or black king on the board, set piece selected back to -- to ensure multiple kings cant be placed
                    if (cs.is_their_white_king() and piece_type == "wK") or (cs.is_their_black_king() and piece_type == "bK"):
                        piece_selected = "--"
                    else:
                        # if not assign piece selected to the button drawn
                        piece_selected = piece_type

                # if the x button is clicked on the screen (this also draws the image)        
                if x_button.draw_button(SCREEN):
                    # set piece_selected to -- so they can remove pieces
                    piece_selected = "--"

                # if the play button is clicked on the screen (this also draws the image)
                if play_button.draw_button(SCREEN):
                    # if their is a black or white king:
                    if cs.is_their_black_king() and cs.is_their_white_king():
                        # create co_ordinates for both
                        white_row,white_column = cs.find_white_king()  
                        black_row, black_column = cs.find_black_king()
                        # if either king is attacked upon setup, the setup is invalid, and force the user to change this setup
                        if cs.is_square_attacked(white_row, white_column) or cs.is_black_king_attacked(black_row, black_column):
                            messagebox.showwarning(
                                "Invalid Setup",
                                "A king should not be able to be captured upon setup",
                            )
                        # otherwise adding pieces is set to False, since the game has begun
                        else:
                            cs.white_turn = True
                            cs.adding_pieces = False
                    #if there isnt both kings, force the user to have both
                    else: 
                        messagebox.showwarning(
                            "Invalid Setup",
                            "There must be a White King and a Black King on the board.",
                        )
        # if the game is going on and the user isnt adding pieces
        else:

            # draw whos turn it is
            whos_turn_is_it.draw_text_on_screen(500, 30, SCREEN)

            # calculate the points of each person and display it
            if cs.get_points() > 0 or cs.get_points() < 0:  
                absolute_value_points = abs(cs.get_points())
                white_points = Text("Arial", 20, f"+{absolute_value_points}", (255, 255, 255))
                black_points = Text("Arial", 20, f"+{absolute_value_points}", (255, 255, 255))
                if cs.get_points() > 0:
                    black_points.remove_text_on_screen(1150, 100, SCREEN)
                    white_points.draw_text_on_screen(1150, 720, SCREEN)
                if cs.get_points() < 0:
                    white_points.remove_text_on_screen(1150, 720, SCREEN)
                    black_points.draw_text_on_screen(1150, 100, SCREEN)

        # if the reset_button is clicked ( this also draws it on the screen )
        if reset_button.draw_button(SCREEN):
            # resets everything
            move_log_train.reset_move_log()
            player_turn = "White's Turn"
            board_setup.red_squares = {}
            cs.reset_board()

        # if the back button is clicked ( this also draws it on the screen )
        if back_button.draw_button(SCREEN):
            # erase all highlited squares
            board_setup.red_squares = {}
            # end the while loop and go back to main menu
            run = False

        for event in pg.event.get():

            # if the user quits the program:
            if event.type == pg.QUIT:
                run = False
                # end pygame
                pg.quit()

            # if the user presses anything on their mouse
            elif event.type == pg.MOUSEBUTTONDOWN:
                # gets position of the mouse click.  
                mouse_location = pg.mouse.get_pos()
                # left click is pressed:  
                if event.button == 1:
                    # makes sure mouse position looking at the board.
                    if (500 <= mouse_location[0] <= 1140) and (100 <= mouse_location[1] <= 740):
                        # gets the column the mouse is in, in relation to the chess board. The "- 500" is so that it targets the boards starting location on the menu.  
                        mouse_column = (mouse_location[0] - 500) // SQUARE_SIZE
                        # gets the row the mouse is in, in relation to the chess board. The "- 100" is so that it it targets the boards starting location on the menu.
                        mouse_row = (mouse_location[1] - 100) // SQUARE_SIZE

                        # if the user is adding pieces:  
                        if cs.adding_pieces:
                            # if kings are selected and in board, dont go into the if statement
                            if not ((cs.is_their_black_king() and piece_selected == "bK") or (cs.is_their_white_king() and piece_selected == "wK")):
                                #place the piece on the board  
                                cs.board[mouse_row][mouse_column] = piece_selected

                                if piece_selected != "--":
                                    # play piece placing sound if the piece played is a piece
                                    move_sound.play()
                        # if the user is not adding pieces:
                        else:
                            # if there arent any kings, force user to add more pieces
                            if not (cs.is_their_black_king() and cs.is_their_white_king()):
                                player_turn = "White's Turn"
                                cs.turn_number = 0
                                cs.whiteTurn = True
                                cs.adding_pieces = True
                                move_log_train.reset_move_log()
                            # otherwise:
                            else:

                                # promote pawns so that if a pawn is placed on the back rank, it auto promotes
                                cs.pawn_promotion()
                                # ensures both colors pawns promote  
                                cs.pawn_promotion()

                                # generate valid moves
                                valid_moves = cs.get_valid_moves()

                                # gets the column the mouse is in, in relation to the chess board. The "- 500" is so that it targets the boards starting location on the menu.
                                mouse_column = (mouse_location[0] - 500) // SQUARE_SIZE
                                # gets the row the mouse is in, in relation to the chess board. The "- 100" is so that it targets the boards starting location on the menu.
                                mouse_row = (mouse_location[1] - 100) // SQUARE_SIZE

                                # if the user clicked same square twice:  
                                if square_selected == (mouse_row,mouse_column):
                                    # reset the players clicks  
                                    square_selected = ()
                                    player_clicks = []  

                                # otherwise
                                else:
                                    # creates a (column,row) co-ordinate.
                                    square_selected = (mouse_row,mouse_column)
                                    # append the clicks into the player clicks array. 
                                    player_clicks.append(square_selected)

                                # after 2nd click  
                                if len(player_clicks) == 2:
                                    # uses the Move object to create a chess move with the players recorded moves.  
                                    chess_move = Move(player_clicks[0], player_clicks[1], cs.board)
                                    # if the chess move is in the boards list of valid moves: 
                                    if chess_move in valid_moves:
                                        # create the move if move is valid
                                        cs.make_move(chess_move)
                                        # calls pawn promotion to promote piece to queen if possible  
                                        cs.pawn_promotion()

                                        # plays appropriate sounds  
                                        if chess_move.is_castle_move:
                                            castle_sound.play()
                                        elif chess_move.the_piece_captured != "--":
                                            if cs.in_check() and not (cs.in_checkmate()):
                                                check_sound.play()
                                            else:
                                                capture_sound.play()
                                        elif cs.in_check():
                                            check_sound.play()
                                        else:
                                            move_sound.play()
                                        if cs.in_checkmate():
                                            checkmate_sound.play()

                                        # resets highlighted squares
                                        board_setup.red_squares = {}

                                        # draw the board.
                                        board_setup.draw_board(cs, valid_moves, square_selected)

                                        # reset so player can make another move  
                                        square_selected = ()  
                                        player_clicks = []

                                        # changes the player_turn 
                                        player_turn = cs.player_turn()

                                        # update the move notation with the new move
                                        move_notation = chess_move.get_chess_notation(cs.turn_number, cs) 
                                        move_log_train.add_move(move_notation)
                                    
                                    # otherwise
                                    else:
                                        player_clicks = [square_selected]

                                    # update screen
                                    pg.display.flip()

                # if right click is pressed and the user isnt adding pieces:
                elif event.button == 3 and not (cs.adding_pieces):
                    # makes sure mouse position looking at the board.
                    if (500 <= mouse_location[0] <= 1140) and (100 <= mouse_location[1] <= 740): 

                        # gets the column the mouse is in, in relation to the chess board. The "- 500" is so that it targets the boards starting location on the menu.
                        mouse_column = (mouse_location[0] - 500) // SQUARE_SIZE
                        # gets the row the mouse is in, in relation to the chess board. The "- 500" is so that it targets the boards starting location on the menu.  
                        mouse_row = (mouse_location[1] - 100) // SQUARE_SIZE 

                        #  highlight the  square
                        board_setup.right_click(mouse_row, mouse_column)

                        # update the screen
                        pg.display.flip()

            # if a key is pressed and pieces are not being added
            elif event.type == pg.KEYDOWN and not (cs.adding_pieces):
                # when back arrow is pressed:  
                if event.key == pg.K_LEFT:
                    # if there has been any moves  
                    if len(cs.log) > 0:
                        # undo the move and reset appropriate variables
                        cs.undo_move()
                        board_setup.red_squares = {}
                        move_sound.play()
                        cs.checkmate = False
                        cs.stalemate = False
                        move_log_train.remove_last_move()
                        if player_turn == "White's Turn":
                            player_turn = "Black's Turn"
                        else:
                            player_turn = "White's Turn"

        # if pieces are not being added
        if not (cs.adding_pieces):
            # if there is a checkmate draw correct image on screen
            if cs.checkmate:
                if cs.player_turn() == "Black's Turn":
                    chess_white_checkmate_image.draw_image(SCREEN)
                else:
                    chess_black_checkmate_image.draw_image(SCREEN)
            # if there is a stalemate draw correct image on screen
            elif cs.stalemate:
                stalesmate_image.draw_image(SCREEN)
            # otherwise regerenerate valid moves
            else:
                valid_moves = cs.get_valid_moves()
                board_setup.draw_board(cs, valid_moves, square_selected)  # draw the board.

        # draw the move log
        move_log_train.draw_move_log()

        # the fps
        clock.tick(FPS)

        # update the system
        pg.display.flip()

def chess_main_menu():

    clock = pg.time.Clock()

    run = True

    shorten = "ChessFolder/ButtonImages/"
    # loads the buttons that are used throughout the menu. load buttons only once so that it is less memory intensive
    battle_button = Button(457.225, 275, 0.55, pg.image.load(shorten + "battle-button.png").convert_alpha())
    train_button = Button(457.225, 425, 0.55, pg.image.load(shorten + "train-button.png").convert_alpha())
    quit_button = Button(457.225, 575, 0.55, pg.image.load(shorten + "quit-button.png").convert_alpha())

    # the chess menu text
    chess_menu_image_on_SCREEN = Image(397, 100, 1, pg.image.load(shorten + "chess-menu.png").convert_alpha())

    # the background image
    menu_background = pg.image.load("ChessFolder/BackgroundImages/menu_background.jpg")

    while run:
        # sets up the main menu
        pg.display.set_caption("Chess Menu")
        SCREEN.blit(menu_background, (0, 0))

        # draws the buttons and returns a value if clicked
        if battle_button.draw_button(SCREEN):
            # if clicked load this function
            battle_menu()  
        if train_button.draw_button(SCREEN):
            # if clicked load this function
            train_menu()
        if quit_button.draw_button(SCREEN):
            # if clicked end loop
            run = False

        # draw the chess menu text on the screen
        chess_menu_image_on_SCREEN.draw_image(SCREEN)

        for i in pg.event.get():
            # if the user quits the program
            if i.type == pg.QUIT:
                # exit the loop
                run = False
        
        # the fps
        clock.tick(FPS)

        # update the screen
        pg.display.flip()

    # quit the program
    pg.quit()

if __name__ == "__main__":
    # this runs the main menu:
    chess_main_menu()