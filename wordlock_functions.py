"""Starter code for CSC108 Assignment 1 Winter 2018"""

# Game setting constants
SECTION_LENGTH = 3
ANSWER = 'CATDOGFOXEMU'

# Move constants
SWAP = 'S'
ROTATE = 'R'
CHECK = 'C'

def get_section_start(section_number: int) -> int:
    """ Return the starting index of the section corresponding to section_num.
    
    >>> get_section_start(1)
    0
    >>> get_section_start(3)
    6
    """
    return (section_number - 1) * SECTION_LENGTH

def is_valid_move(move_const: str) -> bool:
    """Returns True if and only if the parameter represents a valid move,
    i.e. it matches one of the three move constants.
    
    >>> is_valid_move('S')
    True
    >>> is_valid_move('SU')
    False
    """
    
    return move_const in 'SRC' and len(move_const) == 1

def is_valid_section(section_number: int) -> bool:
    """Returns True if and only if the parameter represents a section number 
    that is valid for the current answer string and section length.
    
    >>>is_valid_section(1)
    True
    >>>is_valid_section('B')
    False
    """
    
    return 0 < section_number <= len(ANSWER)/SECTION_LENGTH 

def check_section(game_state: str, section_number: int) -> bool:
    """Return True if and only if the specified section in the game state
    matches the same section in the answer string. 
    
    >>>check_section('CATDOGFOXEMU', 2)
    True     
    >>>check_section('CATODGFOXEMU', 2)
    False
    """
    
    num = get_section_start(section_number)
    return ANSWER[num:num+SECTION_LENGTH] == game_state[num:num+SECTION_LENGTH]

def change_state(game_state: str, section_number: int, move: str) -> str:
    """Returns a new string that reflects the updated game state after applying
    the given move to the specified section
    
    >>>change_state('TCAGODOFXUME', 2, 'S')
    'TCADOGOFXUME'
    >>>change_state('ATCGODOFXUME', 1, 'R')
    CATGODOFXUME
    """
    
    num = get_section_start(section_number)
    c1 = game_state[num]
    c2 = game_state[num+(SECTION_LENGTH-1)]
    i = 0
    update = ''
    if move == 'S':
        while i < len(game_state):
            if i == num:
                update = update + c2
            elif i == num+SECTION_LENGTH-1:
                update = update + c1
            else:
                update = update + game_state[i]
            i = i + 1
    elif move == 'R':
        while i < len(game_state):
            if (num+1) <= i <= (num+SECTION_LENGTH-1):
                update = update + game_state[i-1]
            elif i == num:
                update = update + c2
            else:
                update = update + game_state[i]
            i = i +1
    return update

def get_move_hint(game_state: str, section_number: int) -> str:
    """ return a move that will help the player rearrange the specified section 
    correctly. 
    
    >>>get_move_hint('CATGODFOXEMU', 2)
    'SWAP'
    >>>get_move_hint('CATDOGFOXMUE', 4)
    'ROTATE'
    """
    
    num = get_section_start(section_number)    
    if game_state[num+1] != ANSWER[num+1]:
        return 'ROTATE'
    else:
        return 'SWAP'