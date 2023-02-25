#Alan Chen 16976197
#spotsgame_model
from faller import Faller
from gamestate import GameState,EMPTY,FALLING,LANDED,FROZEN,MATCH_MARK,DISPLAY_BOARD_ROW_INDEX, GameOver

import random

RED_JEWEL = 'S'
BLUE_JEWEL = 'T'
PURPLE_JEWEL = 'V'
GREEN_JEWEL = 'W'
CYAN_JEWEL = 'X'
YELLOW_JEWEL = 'Y'
PINK_JEWEL = 'Z'

JEWELS_AVAILABLE = 'STVWXYZ'

class Jewel:
    '''
    'Jewel'class is really a class created
    to hold the information about rectangles
    and these rectangles represent each jewel
    '''
    def __init__(self, frac_x: float, frac_y: float, width: float, height:float, jewel:str):
        '''
        Each rectangle has a fractional x and
        y location coordinate, fractional_width,
        fractional_height, and also a color
        that represents the jewel.
        '''
        self._top_left_x = frac_x
        self._top_left_y = frac_y
        self._width = width
        self._height = height
        self._color = self._determine_color(jewel)
        

    def top_left_coord(self) -> (float, float):
        '''
        returns the top left fractional_coordinates
        '''
        return self._top_left_x, self._top_left_y
    
    def width(self) -> float:
        '''
        returns the fractional width
        '''
        return self._width
    
    def height(self) -> float:
        '''
        returns the fractional height
        '''
        return self._height

    def color(self) -> (int, int, int):
        '''
        returns the color in a tuple (r,g,b)
        '''
        return self._color
    

    def _determine_color(self, jewel: str):
        '''
        Determines which color to
        to put in to the color attribute for
        Jewel depending on what letter 'jewel'
        was given. Also alters the color if the
        state of the jewel is a matched or landed.
        '''
        landed_saturation = 1
        if jewel == EMPTY:
            return (0,0,0)
        if MATCH_MARK in jewel:
            return (255,255,255)
        if LANDED in jewel:
            landed_saturation = 3/4
        if RED_JEWEL in jewel:
            return (int(255 * landed_saturation), 0, 0)
        if BLUE_JEWEL in jewel:
            return (0, 0, int(255 * landed_saturation))
        if PURPLE_JEWEL in jewel:
            return (int(128*landed_saturation), 0, int(128*landed_saturation))
        if GREEN_JEWEL in jewel:
            return (0,int(128*landed_saturation), 0)
        if CYAN_JEWEL in jewel:
            return (0,int(255*landed_saturation),int(255*landed_saturation))
        if YELLOW_JEWEL in jewel:
            return (int(255 * landed_saturation), int(255 * landed_saturation), 0)
        if PINK_JEWEL in jewel:
            return (int(255 * landed_saturation), int(192 * landed_saturation), int(203 * landed_saturation))

class ColumnsState: 
    def __init__(self) -> None:
        '''
        ColumnsState contains a gamestate attribute
        that has multiple functions used in columns game.
        It also contains a faller attribute that contains
        a Faller object. And an attribute to
        keep track of the boards current visuals.
        '''
        self._gamestate = GameState(6,13)
        self._faller = self._create_random_faller()
        self._board = self._update_board(self._gamestate)
        
    def all_jewels(self) -> [Jewel]:
        return self._board
    

    def tick(self) -> None:
        '''
        This function basically runs the core
        loop of the columns game, depending on
        what state the faller is in, the gamestate
        and board will be updated accordingly
        '''
        if self._faller.state() != FROZEN:
            #this moves the faller down as time passes
            self._gamestate.tick(self._faller)
            self._board = self._update_board(self._gamestate)
            return
        if self._faller.state() == FROZEN:
            if self._gamestate.match_found() == True:
                #this removes any possible matches and marks
                #any possible ones found after collapsing
                self._gamestate.remove_matches()
                self._gamestate.mark_matches()
                self._board = self._update_board(self._gamestate)
                return
            
            if self._gamestate.match_found() == False:
                #if no matches are found, we want to check
                #if any jewels are out of the display board
                #check_game_over checks for this
                self._gamestate.check_game_over()
                #if that check is passed, a new faller is created
                self._faller = self._create_random_faller()
                self._board = self._update_board(self._gamestate)
                return

    def rotate(self) -> None:
        '''
        rotates the faller and the board gets updated
        to reflect this change
        '''
        if self._faller.state() != FROZEN:
            #only works if current faller is not frozen
            self._gamestate.rotate_faller(self._faller)
            self._board = self._update_board(self._gamestate)
            
    def move_right(self) -> None:
        '''
        Moves the faller to the next right column
        and board gets updated to reflect this change
        '''
        if self._faller.state() != FROZEN:
            #only works if current faller is not frozen
            self._gamestate.move_faller_right(self._faller)
            self._board = self._update_board(self._gamestate)
            
    def move_left(self) -> None:
        '''
        Moves the faller to the next left column
        and board gets updated to reflect this change
        '''
        if self._faller.state() != FROZEN:
            self._gamestate.move_faller_left(self._faller)
            self._board = self._update_board(self._gamestate)
    
    def _create_random_faller(self) -> None:
        '''
        Creates a faller with a random
        list of jewels with a column that
        is not full.
        '''
        random_column = self._get_faller_spawn_column()
        faller_jewels = self._create_faller_jewels_list()
        return Faller(random_column, faller_jewels)
    
    def _get_faller_spawn_column(self) -> int:
        '''
        Returns a column number that is not full
        if all columns are full, column 0 is chosen
        '''
        available_columns = self._gamestate.get_available_columns()
        if len(available_columns) > 0:
            random_index = random.randint(0,len(available_columns)-1)
            random_column = available_columns[random_index]
            return random_column
        else:
            return 0
        
    def _create_faller_jewels_list(self) -> [str]:
        '''
        Returns a random list of 'jewels' of size 3
        '''
        random_jewel1 = random.randint(0,6)
        random_jewel2 = random.randint(0,6)
        random_jewel3 = random.randint(0,6)
        faller_jewels = list(JEWELS_AVAILABLE[random_jewel1]
                             + JEWELS_AVAILABLE[random_jewel2]
                             + JEWELS_AVAILABLE[random_jewel3])
        return faller_jewels
        
    def _update_board(self, gamestate) -> [Jewel]:
        '''
        Converts the gamestate board to a list
        of cells that contain information of how
        pygame should draw the board
        '''
        jewels_list = []
        
        board = gamestate.board()
        
        #needed to track how far we are away from the origin
        counter_y = 0
        
        for row_index in range(DISPLAY_BOARD_ROW_INDEX, gamestate.rows()):
            #each new cell will have an incremented x and y top left coord.
            frac_y = 0.08 + 0.06 * counter_y
            counter_x = 0
            for column_index in range(gamestate.columns()):
                frac_x = 0.33 + 0.06 * counter_x
                jewel = board[column_index][row_index]
                jewels_list.append(Jewel(frac_x, frac_y, 0.05, 0.05, jewel))
                #next x-coord increment
                counter_x += 1
            #next y-coord increment
            counter_y += 1
            
        return jewels_list
    
