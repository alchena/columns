#Alan Chen 16976197

#fallers states
FALLING = ']'
LANDED = '|'
FROZEN = '.'

#faller size can be changed 
FALLER_SIZE = 3

class Faller():
    def __init__(self, column: int, jewels: [str]):
        '''
        Each faller has a state, jewels, column, and an extra
        list that keeps track of each jewels position
        by tracking their row index in a column.
        Each jewel is initally marked with a
        falling state. 
        '''
        self._jewels_with_state = self._create_initial_falling_jewels(jewels)
        self._jewels_rows = self._create_initial_jewel_rows_list()
        self._faller_column = column
        self._faller_state = FALLING

    def _create_initial_falling_jewels(self, jewels):
        '''
        Marks jewels with falling state
        '''
        jewels_with_state = []
        for jewel in jewels:
            jewels_with_state.append(jewel+FALLING)
        return jewels_with_state
    
    def _create_initial_jewel_rows_list(self) -> [int]:
        '''
        creates a list that contains indexes row positions
        whose, indexes correspond with the jewels
        in the list jewels_with_state.
        '''
        jewel_positions = []
        for index in range(FALLER_SIZE):
            jewel_positions.append(index)
        return jewel_positions
        
    def state(self) -> str:
        return self._faller_state
    
    def column(self) -> int:
        return self._faller_column

    def jewels(self) -> [str]:
        '''
        returns the list of jewels
        in the faller
        '''
        return self._jewels_with_state
    
    def jewel_row_indexes(self) -> [int]:
        return self._jewels_rows

    def change_state(self, state) -> None:
        '''
        Changes the state of the faller given what
        it was previously.
        - these if assumptions are made since they
        follow the core mechanics of the game
        '''
        if self._faller_state == FALLING and state == LANDED:
            for index in range(len(self._jewels_with_state)):
                self._jewels_with_state[index] = self._jewels_with_state[index].replace(FALLING,LANDED)
            self._faller_state = LANDED
        if self._faller_state == LANDED and state == FALLING:
            for index in range(len(self._jewels_with_state)):
                self._jewels_with_state[index] = self._jewels_with_state[index].replace(LANDED, FALLING)
            self._faller_state = FALLING
        if self._faller_state == LANDED and state == FROZEN:
            for index in range(len(self._jewels_with_state)):
                self._jewels_with_state[index] = self._jewels_with_state[index].replace(LANDED, FROZEN)
            self._faller_state = FROZEN


    def move(self, column) -> None:
        '''
        moving the faller consists of replacing the column
        '''
        self._faller_column = column
        
    def update_jewel_indexes(self) -> None:
        '''
        If called will effectively move
        every jewel down a row.
        '''
        for index in range(len(self._jewels_rows)):
            self._jewels_rows[index] = self._jewels_rows[index] + 1

    def rotate(self) -> None:
        '''
        Rotates the faller by popping the last
        jewel and inserting it to the front
        '''
        self._jewels_with_state.insert(0, self._jewels_with_state.pop())
    
    

        
