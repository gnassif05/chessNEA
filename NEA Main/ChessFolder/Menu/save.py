import pickle
from chess_battle import StateOfGame

'''
This file handles the save/load system
It is solely used in the chess_main.py file
This contains the functions and class used to operate the save/load system in the battle mode.
Pickle is used to serialise the StateOfGame object to a byte stream so that it can be stored in a file.
'''

# Function to save the current state of the game to a file.
def save_save_states(save_states, filename):
    # open file as write in byte
    with open(filename, 'wb') as file:
        # loop through the save states and serialise it and save it
        for save_state in save_states:
            # serializing the save state object and writing it to the file.
            pickle.dump(save_state, file)


# Function to load previously saved game states from a file.
def load_save_states(filename):
    # open file as read in byte
    with open(filename, 'rb') as file:
        save_states = []
        # Continuously attempting to load save states until the end of the file is reached
        while True:
            # loop until the end of the file and avoid end of file error
            try: 
                save_state = pickle.load(file)
                #Appending the loaded save state to the list of save states
                save_states.append(save_state)
            except EOFError:
                break
        # Returning the list of loaded save states.
        return save_states

# Defining a class to represent a saved game state.
class SaveState:
    def __init__(self, name, game_state, move_notations):
        # the name the user wishes to save the file under
        self.name:str = name
        # the StateOfGame object being saved
        # this is done to ensure no data is lost upon loading the save file
        self.game_state:StateOfGame = game_state
        # the notations being saved
        self.move_notations = move_notations