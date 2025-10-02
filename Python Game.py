import csv
from copy import deepcopy

groupNumber = 17
groupName = {'Victoria Li' : 'u5568587',\
             'Callum Green' : 'u5546208',\
             'Phurich Rachawat' : 'u5548642',\
             'Aamna Zulfiqar' : 'u5512747',\
             'Zhe Kai Ng' : 'u5565323'}


###############################################################################
# Task 1

def newGame(p1, p2):
    """
    Initialises a new game with two players.

    Args:
        p1 (str): Name of Player 1.
        p2 (str): Name of Player 2.

    Returns:
        dict: A dictionary containing the game state, including player names,
              the current player, and the game board.

    Raises:
        TypeError: If p1 or p2 is not a string.
    """
    
    #Both players must be valid strings
    if not isinstance(p1, str) or not isinstance(p2, str):
        raise TypeError("Player names must be strings.")

    return { #dictionary
        #player names
        'Player 1': p1,
        'Player 2': p2,
        
        #First turn is player 1
        'Who': 1,
        
        #3D Board game initialized to 0's
        'Board': [[[0 for _ in range(6)] for _ in range(6)] for _ in range(4)]
    }

###############################################################################

###############################################################################
# Task 2

def printBoard(board):
    """
    Returns a formatted string representation of the game board.

    Args:
        board (list): A 3D list representing the board state.

    Returns:
        str: A string representation of the board with proper alignment and spacing.

    Raises:
        TypeError: If board is not a 3D list.
    """

    #Check if input is a valid board(4x6x6)
    if not (isinstance(board, list) and len(board) == 4 and
            all(isinstance(layer, list) and len(layer) == 6 for layer in board) and
            all(isinstance(row, list) and len(row) == 6 for layer in board for row in layer)):
        raise TypeError("Invalid board structure.")
        
        
    #Row and collumn labels
    row_labels = ['a', 'b', 'c', 'd', 'e', 'f']
    col_labels = ['A', 'B', 'C', 'D', 'E', 'F']
    
    #Headers and collumn labels
    board_str = "   Layer 1    |   Layer 2    |   Layer 3    |   Layer 4\n"
    
    #Add collumn labels for each layer, seperated by |
    board_str += "  " + " |  ".join(["|".join(col_labels)] * 4) + "\n"
    
    #Seperators between labels and grid
    board_str += " " + "| ".join(["-+-+-+-+-+-+-"] * 4) + "\n"
    
    
    #Loop through each row
    for row in range(6):
        #Add label
        row_str = [row_labels[row]] 
        #Loop through each level
        for level in range(4):
            #Add row values. 0's replaced with spaces
            row_str.append("|" + "|".join(
                str(board[level][row][col]) if board[level][row][col] != 0 else " " for col in range(6))) 
            #row seperators
            if level < 3: row_str.append(" |" + row_labels[row])
        board_str += "".join(row_str) + "\n"
        

    return board_str

###############################################################################

###############################################################################
# Task 3


class ColumnFullError(Exception):
    '''
    
    Error raised when there is an insertion attempt into a full collumn
    
    '''
    
    pass

class InvalidColumnFormat(Exception):
    
    '''
    
    Error raised when inserted collumn format is incorrect
    
    '''
    
    
def posToIndex(col,board):
    
    '''
    
    Converts collumn identifier in letter form (Eg. Aa) into board indices
    
    Input:
        col(str): Collumn identifier of length 2. Contains 1 uppercase letter A-F (collumn)
                  and 1 lower case letter a-f (row)
        board (list): A 3D array representning the game board (4 x 6 x 6 board)
        
    Returns:
        list: The indices of the first empty slot in the collumn col in form
              [k, j, i] where k is the level, j is the row index, and i is the collumn index
    
    Raises:
        ColumnFullError: If the column is full.
        InvalidColumnFormatError: If col is wrongly formatted
    
    '''

    #Create dictionaries (row_letters, col_letters) to map row and collumn
    #letters to corresponding indices in the 3D board array
    
    row_letters = {'a': 0, 'b': 1, 'c': 2, 'd' : 3, 'e' : 4, 'f' : 5}
    
    col_letters = {'A': 0, 'B': 1, 'C': 2, 'D' : 3, 'E' : 4, 'F' : 5}
    
    
    #Checks if col input is exactly 2 characters, one lower case and one upper
    #case to define rows and collumns. If not, raise exception.
    
    if len(col) != 2 or not ((col[0] in row_letters and col[1] in col_letters) or 
                             (col[1] in row_letters and col[0] in col_letters)):
        
        raise InvalidColumnFormat(f"Invalid column format: {col}")
        

    # Extracting indices from the letters

    
    #row index is the lowercase letter. For characters in col, find the lowercase letter
    row_index = row_letters[col[0]] if col[0] in row_letters else row_letters[col[1]]
    
    #collumn index is the uppercase letter. For characters in col, find the uppercase letter
    col_index = col_letters[col[0]] if col[0] in col_letters else col_letters[col[1]]
    

    # Iterate through all floor_lvls. 
    #Find the first available slot in the column
    
    for floor_lvl in range(4):
        if board[floor_lvl][row_index][col_index] == 0:
            return [floor_lvl, row_index, col_index]


    # No empty space found. Raise collumn full error
    raise ColumnFullError(f"Column {col} is full")



###############################################################################

###############################################################################
# Task 4

class IndexOutOfRange(Exception):
    
    '''
    Error raised when inserted index is invalid
    
    '''
    
    pass


def indexToPos(ind):
    
    '''
    Converts a list of board indices to corresponding letter collumn indentifiers
    
    Input:
        ind(list): List of integers representing the board indices in 2D or 3D cases.
    
    Return:
        str: Letter collumn identifier in form 'Xx'
        
    Raises:
        IndexOutOfRange: If i or j are not between 0 and 5.
    
    '''
    
    
    #Map row and collumn indices to letter collumn identifiers
    row_indices = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f'}
    
    col_indices = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F'}
    
    
    #Splitting 2D,3D, and invalid cases
    if len(ind) == 2:
        j = ind[0] #j = row index
        i = ind[1] #i = collumn index
    elif len(ind) == 3:
        j = ind[1] #j = row index
        i = ind[2] #i = collumn index
    else:
        raise IndexOutOfRange(f" Index must be of length 2 or 3: {ind}")
        
    #Invalid index error checks
    if j not in row_indices or i not in col_indices:
        raise IndexOutOfRange(f"Invalid index: {ind}")
        
        
    #Display collumn index first then row index to be in form 'Xx'
    return col_indices[i] + row_indices[j] 
        
    


###############################################################################

###############################################################################
# Task 5

def saveGame(game, fname):
    """
    Saves the game state to a CSV file.

    Args:
        game (dict): The current game state.
        fname (str): The filename to save the game to.
    """
    with open(fname, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write player information
        writer.writerow(["Player 1", game['Player 1']])
        writer.writerow(["Player 2", game['Player 2']])
        writer.writerow(["Who", game['Who']])
        writer.writerow(["Board"])  
        
        # Flatten the 3D board into 2D format 
        for layer in game['Board']:
            for row in layer:
                writer.writerow(row)
                


###############################################################################

###############################################################################
# Task 6

def loadGame(fname):
    """
    Loads the game state from a CSV file.

    Args:
        fname (str): The filename to load the game from.

    Returns:
        dict: The restored game state dictionary.
    """
    with open(fname, mode='r', newline='') as file:
        reader = csv.reader(file)
        
        # Read player names
        player1 = next(reader)[1]
        player2 = next(reader)[1]
        
        # Read current turn
        who = next(reader)[1]
        
        # Skip 'Board' line
        next(reader)
        
        # Read board values
        board = []
        for _ in range(4):  # Read 4 layers
            layer = [list(map(int, next(reader))) for _ in range(6)]
            board.append(layer)
        
        return {
            'Player 1': player1,
            'Player 2': player2,
            'Who': who,
            'Board': board
        }
    


###############################################################################

###############################################################################
# Task 7

def findValidMoves(board):
    """
    Finds all non-full columns in the board and returns them as valid moves.

    Args:
        board (list): The 3D board representation.

    Returns:
        list: A list of valid moves in the form of 'xX' or 'Xx'.
    """
    row_labels = ['a', 'b', 'c', 'd', 'e', 'f']
    col_labels = ['A', 'B', 'C', 'D', 'E', 'F']
    valid_moves = []
    
    for row in range(6):
        for col in range(6):
            # If the top layer (highest) at (row, col) is empty (0), it's a valid move
            if board[3][row][col] == 0:
                #valid_moves.append(f"{row_labels[row]}{col_labels[col]}")
                valid_moves.append(f"{col_labels[col]}{row_labels[row]}")
    
    return valid_moves
    

###############################################################################

###############################################################################
# Task 8

class MoveNotMade(Exception):
    """
    Exception raised when a move cannot be made due to an invalid column reference,
    incorrect format, or if the column is full.
    """
    pass

def makeMove(game, move):
    """
    Attempts to place a piece in the specified column.
    
    Args:
        game (dict): The current game state.
        move (str): A string representing the column in the form 'xX' or 'Xx'.
    
    Returns:
        dict: A new game state dictionary after the move is made.
    
    Raises:
        MoveNotMade: If the move is invalid or the column is full.
    """

    # Validate move format
    if len(move) != 2 or not (move[0].isalpha() and move[1].isalpha()):
        raise MoveNotMade("Invalid move format. Must be 'xX' or 'Xx'.")
        
    try:
        # Get the indices for the move
        k, j, i = posToIndex(move, game['Board'])
    except (InvalidColumnFormat, ColumnFullError) as e:
        raise MoveNotMade(str(e))
    
    # Create a deep copy of the game
    new_game = deepcopy(game)
    
    # Place the current player's piece in the determined location
    new_game['Board'][k][j][i] = new_game['Who']
    
    # Switch to the next player
    new_game['Who'] = 1 if new_game['Who'] == 2 else 2
    
    return new_game



###############################################################################

###############################################################################
# Task 9

def isWinner(game):
    """
    Checks whether there is a winner in the current board of the given game.
    
    Args:
        game (dict): The current game state.
        
    Returns:
       1 if Player 1 has won,
       2 if Player 2 has won,
       0 if there is no winner and the board is not full,
      -1 if there is no winner and the board is full.
    """
    board = game['Board']  # layer 4 x row 6 x col 6
    
    # A quick helper to check if the board is completely filled (no 0s).
    def board_is_full(bd):
        for k in range(4):
            for j in range(6):
                for i in range(6):
                    if bd[k][j][i] == 0:
                        return False
        return True

    # Directions in 3D to check for 4 in a row:
    # (dk, dj, di) indicates how we move in layer (k), row (j), and col (i)
    directions = [
        (1, 0, 0),  # through layers
        (0, 1, 0),  # along rows
        (0, 0, 1),  # along columns
        (1, 1, 0),
        (1, 0, 1),
        (0, 1, 1),
        (1, -1, 0),
        (1, 0, -1),
        (0, 1, -1),
        (1, 1, 1),
        (1, 1, -1),
        (1, -1, 1),
        (1, -1, -1)
    ]
    
    # Check all positions as potential "starting" points
    for k in range(4):       # layer index
        for j in range(6):   # row index
            for i in range(6):  # column index
                player = board[k][j][i]
                # Only check if this cell is occupied (1 or 2)
                if player != 0:
                    # Explore each direction
                    for dk, dj, di in directions:
                        ''' 
                        We want to see if we can get 3 more cells (total of 4)
                        in that direction without going out of bounds,
                        and if they match player.
                        '''
                        valid_line = True
                        for step in range(1, 4):  # steps of 1,2,3
                            nk = k + dk * step
                            nj = j + dj * step
                            ni = i + di * step
                            # Check boundaries
                            if not (0 <= nk < 4 and 0 <= nj < 6 and 0 <= ni < 6):
                                valid_line = False
                                break
                            # Check if same player
                            if board[nk][nj][ni] != player:
                                valid_line = False
                                break
                        # If all 4 in a row matched, we have a winner
                        if valid_line:
                            return player  # either 1 or 2

    # If no winner, check if board is full
    if board_is_full(board):
        return -1
    else:
        return 0
    
    
    

###############################################################################

###############################################################################
# Task 10

class GameOverError(Exception):
    """
    Error raised when no valid moves remain (i.e. the game is over).
    """
    pass

def suggestMove(game):
    """
    Suggests a valid move for the next player in the form 'xX' or 'Xx'.
    If there are no valid moves, raises GameOverError.

    Args:
        game (dict): The current game state.

    Returns:
        str: A valid move, e.g., 'aA' or 'Aa'.

    Raises:
        GameOverError: If no valid moves remain (the board is full).
    """
    # Get all valid moves from Task 7
    valid_moves = findValidMoves(game['Board'])

    # If no valid moves, game is over
    if not valid_moves:
        raise GameOverError("No valid moves left. The board is full.")

    # Otherwise, return any valid move (e.g. the first one)
    return valid_moves[0]
    


###############################################################################

###############################################################################
# Task 11

def playGame():
    """
    
    Function that plays the game with 2 players (human or AI). The game
    continues until there is a winner or the board is full. Supports saving, 
    loading, and move validation
    
    """
    
    # Ask for Player 1’s name (or load an existing game)
    p1 = input("Input Player 1's name (or type 'load' to resume playing): ").strip()
    
    if p1.lower() == 'load': #meaning we want to load an existing game
        filename = input("Enter the filename of your game: ").strip()
        game = loadGame(filename)  # Using Task 6 to load the game
        
        if not game: #Any other input will create a new game 
            print("Starting a new game")
            return
        print("Game loaded")
    else:
        # Start a new game
        p2 = input("Enter Player 2's name: ").strip() 
        game = newGame(p1, p2)  # Using task 1 to create a new game
        
        
    while True:
        # Print the board using Task 2
        print(printBoard(game['Board']))

        # Find who's turn it is
        current_player = game['Who']
        player_name = game[f'Player {current_player}']
        
        print(f"\n{player_name} (Player {current_player})'s turn:")
        
        
        if player_name == 'C': #Playing against AI
            try:
                move = suggestMove(game)  # Using task 10
                print(f"Computer plays: {move}")
                game = makeMove(game, move)  # Using task 8
            except GameOverError: #Board full. Error handling
                print("Games over! It's a draw.")
                break
        else:
            while True:
                move = input("Enter your move ('xX'), or type 'save' to save the game: ").strip()

                # Save the game
                if move.lower() == 'save':
                    filename = input("Enter filename to save the game: ").strip()
                    saveGame(game, filename)  # Uses Task 5 function
                    print("Game saved")
                    continue  # Ask for a move again

                # Otherwise make the move
                try:
                    game = makeMove(game, move)  # Uses Task 8 function
                    break  # Move successful, exit loop
                except MoveNotMade as e:
                    print(f"Invalid move: {e}. Input again")  # Handles invalid moves
                    
                    
                    
        # After every move, check for a winner
        result = isWinner(game)

        if result == 1:
            print(printBoard(game['Board']))
            print(f"\n{game['Player 1']} (Player 1) wins")
            break
        elif result == 2:
            print(printBoard(game['Board']))
            print(f"\n{game['Player 2']} (Player 2) wins")
            break
        elif result == -1:
            print(printBoard(game['Board']))
            print("\nIt's a draw. Game over")
            break


###############################################################################


###############################################################################
# Testing Function
def testFunctionCalls():
    '''
    Input:  [none]
    
    Output: [none]
    
    You can use this function to test if your function names are correct.
    To call the function: "testFunctionCalls()"
    '''
    c = input('The following function will test whether your code can be \
successfully called, i.e. you have used the correct name. \
This function does not test whether the outputs of the functions \
are of the correct type, so passing this function does not \
guarentee that your code will successfully run and you should \
still perform your own checks. \n\nIf you accept these limitations \
type "y" to proceed: ')
    if c == 'y':
        print('You have chosen to proceed.\n\n')
        try:
            newGame.__doc__
            print('Task 1: Call to "newGame" successful.\n')
        except:
            print('Task 1: Call to "newGame" UNSUCCESSFUL.\n')
        
        try:
            printBoard.__doc__
            print('Task 2: Call to "printBoard" successful.\n')
        except:
            print('Task 2: Call to "printBoard" UNSUCCESSFUL.\n')
            
        try:
            posToIndex.__doc__
            print('Task 3: Call to "posToIndex" successful.')
        except:
            print('Task 3: Call to "posToIndex" UNSUCCESSFUL.')
         
        try:
            InvalidColumnFormat()
            print('Task 3: "InvalidColumnFormat" found.')
        except:
            print('Task 3: "InvalidColumnFormat" NOT FOUND.')
        
        try:
            ColumnFullError()
            print('Task 3: "ColumnFullError" found.\n')
        except:
            print('Task 3: "ColumnFullError" NOT FOUND.\n')
         
        try:
            indexToPos.__doc__
            print('Task 4: Call to "indexToPos" successful.')
        except:
            print('Task 4: Call to "indexToPos" UNSUCCESSFUL.')
        
        try:
            IndexOutOfRange()
            print('Task 4: "IndexOutOfRange" found.\n')
        except:
            print('Task 4: "IndexOutOfRange" NOT FOUND.\n')
        
        try:
            saveGame.__doc__
            print('Task 5: Call to "saveGame" successful.\n')
        except:
            print('Task 5: Call to "saveGame" UNSUCCESSFUL.\n')
            
        try:
            loadGame.__doc__
            print('Task 6: Call to "loadGame" successful.\n')
        except:
            print('Task 6: Call to "loadGame" UNSUCCESSFUL.\n')
            
        try:
            findValidMoves.__doc__
            print('Task 7: Call to "finValidMoves" successful.\n')
        except:
            print('Task 7: Call to "findValidMoves" UNSUCCESSFUL.\n')
            
        try:
            makeMove.__doc__
            print('Task 8: Call to "makeMove" successful.')
        except:
            print('Task 8: Call to "makeMove" UNSUCCESSFUL.')
        
        try:
            MoveNotMade()
            print('Task 8: "MoveNotMade" found.\n')
        except:
            print('Task 8: "MoveNotMade" NOT FOUND.\n')
        
        try:
            isWinner.__doc__
            print('Task 9: Call to "isWinner" successful.\n')
        except:
            print('Task 9: Call to "isWinner" UNSUCCESSFUL.\n')
            
        try:
            suggestMove.__doc__
            print('Task 10: Call to "suggestMove" successful.')
        except:
            print('Task 10: Call to "suggestMove" UNSUCCESSFUL.')
            
        try:
            GameOverError()
            print('Task 10: "GameOverError" found.\n')
        except:
            print('Task 10: "GameOverError" NOT FOUND.\n')
            
        try:
            playGame.__doc__
            print('Task 11: Call to "playGame" successful.\n')
        except:
            print('Task 11: Call to "playGame" UNSUCCESSFUL.\n')
    else:
         print('You have chosen not to proceed.')   
###############################################################################
