"""Uses functions from wordlock_functions.py to play the wordlock game"""

import random
import wordlock_functions as wf

TEST = 'T'
EASY = 'E'
HARD = 'H'
SECTION_HINT = 1
MOVE_HINT = 2

def generate_starting_point() -> str:
    """Return a scrambled version of wf.ANSWER
    
    >>> random.seed(42)
    >>> generate_starting_point()
    'ACTGODOXFMUE'
    """
    starter = ''
    for i in range(len(wf.ANSWER) // wf.SECTION_LENGTH):
        section = list(wf.ANSWER[wf.SECTION_LENGTH * i:wf.SECTION_LENGTH * (i + 1)])
        random.shuffle(section)
        starter = starter + ''.join(section)
    return starter

def get_section_hint(state: str) -> int:
    """Return a random section_num corresponding to a section of state that is 
    not correctly arranged.
    
    >>> random.seed(42)
    >>> get_section_hint('CATDGOXOFMUE')
    3
    >>> get_section_hint('CTADGOXOFMUE')
    4
    """
    section_nums = [i + 1 for i in range(len(state) // wf.SECTION_LENGTH)]
    random.shuffle(section_nums)
    for section_num in section_nums:
        if not wf.check_section(state, section_num):
            return section_num
    return 0 # should never get here

def is_valid_mode(mode: str) -> bool:
    """Return True if and only if mode is a valid mode, and False otherwise.
    
    >>> is_valid_mode('T')
    True
    >>> is_valid_mode('S')
    False
    """
    return mode in (TEST, EASY, HARD)

def in_test_mode(mode: str) -> bool:
    """Return True if and only if mode indicates the game is in test mode, and 
    False otherwise.
    
    >>> in_test_mode('T')
    True
    >>> in_test_mode('E')
    False
    """
    return mode == TEST

def in_easy_mode(mode: str) -> bool:
    """Return True if and only if mode indicates the game is in easy mode, and 
    False otherwise.
    
    >>> in_easy_mode('E')
    True
    >>> in_easy_mode('H')
    False
    """
    return mode == EASY

def make_move(state: str, section_num: int, move: str) -> str:
    """Return the new game state after performing the game move specified by 
    move on the section of state correspoding to section_num.
    
    >>> make_move('ATCDOGFOXEMU', 1, 'R')
    'CATDOGFOXEMU'
    >>> make_move('CATDOGFOXUME', 4, 'C')
    The section is incorrect
    'CATDOGFOXUME'
    """
    if move == wf.CHECK:
        check_result = wf.check_section(state, section_num)
        if check_result:
            print('The section is correct')
        else:
            print('The section is incorrect')
    else:
        state = wf.change_state(state, section_num, move) 
    return state

def get_mode() -> str:
    """Return a valid game mode entered by the user. 
    """
    mode = input('Enter the mode to play [(T)est, (E)asy, or (H)ard]: ')
    while not is_valid_mode(mode):
        print('Invalid mode!')
        mode = input('Enter the mode to play [(T)est, (E)asy, or (H)ard]: ') 
    return mode

def get_section_number() -> int:
    """Return a valid section number entered by the user.
    """
    section_num = input('Enter a section number (1 - 4): ')
    while not (section_num.isdigit() and wf.is_valid_section(int(section_num))):
        print('Invalid section number!')
        section_num = input('Enter a section number (1 - 4): ')
    return int(section_num)    

def get_move() -> str:
    """Return a valid move entered by the user.
    """
    msg = 'Enter a move for that section (C to check, S to swap, R to rotate): '
    move = input(msg)
    while not wf.is_valid_move(move):
        print('Invalid move!')
        move = input(msg)    
    return move

def get_hints(state: str, mode: str, hint_type: str, section_num: int = 0) -> int:
    """Return 1 if a hint was given, and 0 if not. Prompt the user to answer 
    whether they would like a hint of type hint_type if and only if mode 
    indicates the game is in easy mode. 
    If yes, generate the hint on how to rearrange state (only using section_num 
    if hint_type corresponds to a move hint) and print the hint. 
    """
    if in_easy_mode(mode):
        if hint_type == SECTION_HINT:
            hint = input('Enter Y if you want a section hint: ')
            if hint == 'Y':
                print('Your section hint is: ' + str(get_section_hint(state)))
                return 1
        elif hint_type == MOVE_HINT:
            hint = input('Enter Y if you want a move hint: ')
            if hint == 'Y': 
                print('Your move hint is: ' + wf.get_move_hint(state, section_num))      
                return 1
    return 0

def play_game(state: str, mode: str) -> int:
    """Return the number of moves taken to arrive at the correct answer. 
    Run the main loop in game-mode mode, prompting the user for input and
    consequently updating state. 
    """
    moves = 0
    if in_test_mode(mode):
        print('Answer: ' + wf.ANSWER)
            
    while state != wf.ANSWER:
        print('Current state: ' + state)
        moves += get_hints(state, mode, SECTION_HINT)     
        section_num = get_section_number() 
        moves += get_hints(state, mode, MOVE_HINT, section_num)
        move = get_move()
        state = make_move(state, section_num, move)
        moves += 1  
    return moves

if __name__ == '__main__':
    
    import doctest
    #doctest.testmod()
    
    start_state = generate_starting_point()
    game_mode = get_mode()
    num_moves = play_game(start_state, game_mode)
    print('You won the game in ' + str(num_moves) + ' moves!')
