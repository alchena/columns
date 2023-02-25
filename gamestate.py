#Alan Chen 16976197

from faller import Faller, FALLING, LANDED, FROZEN, FALLER_SIZE
_ROWS_FOR_FALLER_SPAWN = FALLER_SIZE
_FALLER_SPAWN_LOCATION_INDEX = _ROWS_FOR_FALLER_SPAWN - 1
EMPTY = ''
MATCH_MARK = '*'
DISPLAY_BOARD_ROW_INDEX= FALLER_SIZE

class GameOver(Exception):
    pass

class GameState():
    def __init__(self, columns: int, rows: int, contents=[]):
        self._columns = columns
        #Add 3 extra rows for ease of access to "queued" faller jewels
        #Ui would have to account for this by adding _ROWS_FALLER_SPAWN to the start row
        self._rows = rows + _ROWS_FOR_FALLER_SPAWN
        if contents == []:
            self._board = self._create_empty_board()
        else:
            self._board = self._create_board_with_contents(contents)
        
    def _create_empty_board(self) -> [str]:
        '''
        creates a gameboard in column row format
        '''
        board = []
        for num_cols in range(self._columns):
            column = []
            for num_rows in range(self._rows):
                column.append(EMPTY)
            board.append(column)
        return board


    def _create_board_with_contents(self, contents: [[str]]) -> [str]:
        '''
        Creates a board with specified contents in the format of
        rows and columns. This function translates that to form
        a gameboard 2d list in the format of columns and rows.
        '''
        board = []
        #since contents are in [row][col] we convert to [col][row]
        for column_index in range(self._columns):
            column = []
            for row_index in range(self._rows):
                #since we created extra rows for out fallers we must account for that
                if row_index >= _ROWS_FOR_FALLER_SPAWN:
                    #we do not want to append any empty jewels
                    if contents[row_index-_ROWS_FOR_FALLER_SPAWN][column_index] != EMPTY:
                        #all jewels that are not a faller should be marked with a frozen state
                        # - we subtract from the row_index because the
                        # - contents does not have the extra rows for fallers
                        # - like the row attribute does
                        column.append(contents[row_index-_ROWS_FOR_FALLER_SPAWN][column_index] + FROZEN)
                else:
                    column.append(EMPTY)
                    
            #Because we do not include empty jewels initially,
            #the lengths of each column is not correct, we
            #address it here by inserting empty spots
            #to the beginning of each column
            while len(column) != self._rows:
                column.insert(0, EMPTY)
                
            board.append(column)
        
        return board


        
    def columns(self) -> int:
        return self._columns
    
    def rows(self) -> int:
        return self._rows
    
    def board(self) -> [str]:
        return self._board



    def tick(self, Faller) -> None:
        '''
        This function is used to simulate the crude gravity
        and handles the state of the faller after every call
        to it. 
        '''
        faller_state = Faller.state()
        faller_jewels = Faller.jewels()
        faller_column = Faller.column()
        faller_gem_indexes = Faller.jewel_row_indexes()
        
        #returns the index of where an empty spot is found on that fallers particular column
        empty_row_index_in_column = self._get_bottom_most_empty_row_index(faller_column)
        
        if faller_state == FALLING:
            #If the only empty spot is in the faller spawn rows then its gameover
            if empty_row_index_in_column <= _FALLER_SPAWN_LOCATION_INDEX:
                raise GameOver
            
            #checks the next row to see if it's empty or if its the bottom-most row
            if faller_gem_indexes[FALLER_SIZE-1] + 1 == empty_row_index_in_column:
                #if that that pass, the state of the faller is changed to landed
                Faller.change_state(LANDED)
                #jewels will move up one row index - crude gravity
                Faller.update_jewel_indexes()
                #updating the gameboard
                self._clear_previous_faller(faller_column, FALLING)
                self._add_faller_to_board(Faller)
                
            else:
                #Regular moving down one row by updating the indexes  - crude gravity
                Faller.update_jewel_indexes()
                #updating the gameboard
                self._clear_previous_faller(faller_column, FALLING)
                self._add_faller_to_board(Faller)

        if faller_state == LANDED:
            #assuming that if you call tick again after a landed faller
            #you'll want to freeze it
            Faller.change_state(FROZEN)
            #update gameboard to change the landed faller to show as frozen
            self._add_faller_to_board(Faller)
            #also marks any matches found.
            self.mark_matches()
            

    def move_faller_left(self, Faller) -> None:
        '''
        Moves the faller to the left and updates the
        board to reflect this change. If the shift to
        the right is can't be done, as in the next column is
        not possible or the next_column is blocked,
        no change is done to the board.
        - these 2 move functions are very much the same but
        - decided to make them into seperate for better
        - readability
        '''
        initial_column = Faller.column()
        left_column = initial_column - 1
        faller_state = Faller.state()
        bottom_jewel_row_index = Faller.jewel_row_indexes()[2]
        #checks to see if the next column is possible
        if left_column != -1:
             #checks to see if next_column is not blocked
            if self._board[left_column][bottom_jewel_row_index] == EMPTY:
                Faller.move(left_column)
                self._clear_previous_faller(initial_column, faller_state)
                self._change_state_due_to_moving_left_right(Faller)
                self._add_faller_to_board(Faller)

                    
    def move_faller_right(self, Faller) -> None:
        '''
        Moves the faller to the right and updates the
        board to reflect this change. If the shift to
        the right is can't be done, as in the next column is
        not possible or the next_column is blocked,
        no change is done to the board.
        '''
        initial_column = Faller.column()
        right_column = initial_column + 1
        faller_state = Faller.state()
        bottom_jewel_row_index = Faller.jewel_row_indexes()[2]
        #checks to see if the next column is possible
        if right_column != self._columns:
            #checks to see if next_column is not blocked
            if self._board[right_column][bottom_jewel_row_index] == EMPTY:
                Faller.move(right_column)
                #updating board to reflect this change
                self._clear_previous_faller(initial_column, faller_state)
                self._change_state_due_to_moving_left_right(Faller)
                self._add_faller_to_board(Faller)


    def rotate_faller(self, Faller) -> None:
        '''
        Rotates the faller by calling the the
        fallers method for doing so, then
        updates the board
        '''
        #rotates the faller
        Faller.rotate()
        
        #updating board 
        faller_column = Faller.column()
        faller_state = Faller.state()
        self._clear_previous_faller(faller_column, faller_state)
        self._add_faller_to_board(Faller)
        


    def remove_matches(self) -> None:
        '''
        Updates the gameboard by removing all
        jewels marked with MATCH_MARK. Collapses
        the gameboard after the removal as
        well.
        '''
        for column_index in range(self._columns):
            for row_index in range(self._rows):
                if MATCH_MARK in self._board[column_index][row_index]:
                    #pop will remove the matched jewel from the board
                    self._board[column_index].pop(row_index)
                    #insert will 'push' all the elements down the column, 'collapsing'
                    self._board[column_index].insert(0, EMPTY)

                    

    def mark_matches(self) -> None:
        '''
        Goes through the set of matched jewels and
        marks them for match deletion for used for
        remove_matchs()
        '''
        matches_found = self._match_set()
        for element in matches_found:
            #each element in matches_found is a tuple of size 2
            jewel_column = element[0]
            jewel_row = element[1]
            jewel_marked_match = self._board[jewel_column][jewel_row][0] + MATCH_MARK
            self._board[jewel_column][jewel_row] = jewel_marked_match

    def match_found(self) -> bool:
        '''
        Returns True if a possible match of 3
        or more is found by checking the length
        of the set found in _match_set()
        '''
        matches_found = self._match_set()
        if len(matches_found) != 0:
            return True
        else:
            return False

    def check_game_over(self) -> None:
        '''
        This function checks to see if any jewels
        are in the faller spawn rows, if there are but
        no matches are found(no possible collapsing), then
        a gameover error is raised. Does nothing otherwise.
        '''
        if self._check_if_jewel_in_faller_spawn() and not self.match_found():
            raise GameOver

    def get_available_columns(self) -> [int]:
        '''
        This function returns a list of available columns that
        a faller can spawn in, full columns are considered
        unavavilable and are not appended to the list.
        '''
        available_columns = []
        for column in range(self._columns):
            row_index = self._get_bottom_most_empty_row_index(column)
            if row_index > _FALLER_SPAWN_LOCATION_INDEX:
                available_columns.append(column)
        return available_columns
                
            

    #private functions
    #tick helper function
    def _check_if_jewel_in_faller_spawn(self) -> bool:
        '''
        Goes through every column in the board and checks to
        see if a jewel is found in any of the faller spawn
        rows, intended to be used only with check_game_over.
        If just one is found the loop breaks early and returns True.
        Otheriwise it returns False.
        '''
        for column in range(self._columns):
            for row in range(_ROWS_FOR_FALLER_SPAWN):
                if self._board[column][row] != EMPTY:
                    return True
        return False

    #matching functions
    def _match_set(self) -> {(int,int)}:
        '''
        Returns a set that contains the 'coordinates'
        of where each element is contained in a
        match of 3 or greater
        '''
        jewel_index_set = set()
        
        for col in range(self._columns):
            #we dont look look at matches for the spawn rows for fallers
            for row in range(self._rows):
                for jewel_index in self._get_matches(col,row):
                    jewel_index_set.add(jewel_index)
                    
        return jewel_index_set


    def _check_matching(self, col: int, row: int, coldelta: int, rowdelta: int) -> [(int,int)]:
        '''
        Checks in a certain direction of a given cell in the gameboard
        depending on what values codelta and rowdelta are. If any matches are
        found, Returns a list containing tuples of a size two,
        with the first element being the column index and the second
        index containg the row index
        '''
        match_list = []
        
        start_cell = self._board[col][row]

        if start_cell == EMPTY:
            return match_list
        
        else:
            incr = 0
            #while loop to get all matches 
            while True:
                if not self._is_valid_column_number(col + coldelta * incr):
                    break
                if not self._is_valid_row_number(row + rowdelta * incr):
                    break
                if self._board[col + coldelta *incr][row + rowdelta * incr] != start_cell:
                    break
                else:
                    match_list.append((col + coldelta * incr, row + rowdelta * incr))
                    incr += 1
                    
            return match_list

    def _get_matches(self, col: int, row: int) -> [(int,int)]:
        '''
        Calls the _check_matching in various directions, each
        call to _check_matching is then checked to see if
        it has a length of greater than 3. If the length is greater
        than or equal to three the list contents is then added to
        an encompassing list that will be returned
        '''
        all_matches_found_for_cell = []
        match1 = self._check_matching(col, row, 0, 1)
        match2 = self._check_matching(col, row, 1, 1) 
        match3 = self._check_matching(col, row, 1, 0) 
        match4 = self._check_matching(col, row, 1, -1) 
        match5 = self._check_matching(col, row, 0, -1) 
        match6 = self._check_matching(col, row, -1, -1) 
        match7 = self._check_matching(col, row, -1, 0) 
        match8 = self._check_matching(col, row, -1, 1)
        if len(match1) >= 3:
            all_matches_found_for_cell.extend(match1)
        if len(match2) >= 3:
            all_matches_found_for_cell.extend(match2)
        if len(match3) >= 3:
            all_matches_found_for_cell.extend(match3)
        if len(match4) >= 3:
            all_matches_found_for_cell.extend(match4)
        if len(match5) >= 3:
            all_matches_found_for_cell.extend(match5)
        if len(match6) >= 3:
            all_matches_found_for_cell.extend(match6)
        if len(match7) >= 3:
            all_matches_found_for_cell.extend(match7)
        if len(match8) >= 3:
            all_matches_found_for_cell.extend(match8)
            
        return all_matches_found_for_cell

            
    def _is_valid_column_number(self, column_number:int) -> bool:
        '''Returns True if the given column number is valid; returns False otherwise'''
        return 0 <= column_number < self._columns

    def _is_valid_row_number(self, row_number: int) -> bool:
        '''Returns True if the given row number is valid,
           spawn rows for fallers do not count'''
        return 0 <= row_number < self._rows
        

    #moving the faller functions
    def _change_state_due_to_moving_left_right(self, Faller) -> None:
        '''
        Handles changing of state when faller is moved left or right.
        '''
        bottom_jewel_row_index = Faller.jewel_row_indexes()[2]
        faller_column = Faller.column()
        #if there is no jewel at the bottom of the faller
        #after moving to the next column its still falling
        if bottom_jewel_row_index != self._rows - 1 and self._board[faller_column][bottom_jewel_row_index+1] == EMPTY:
            Faller.change_state(FALLING)
        else:
            #otherwise its landed
            Faller.change_state(LANDED)

    def _add_faller_to_board(self, Faller) -> None:
        '''
        Adds the faller to the board at the indexes located.
        '''
        faller_jewels = Faller.jewels()
        jewel_indexes = Faller.jewel_row_indexes()
        faller_column = Faller.column()
        for jewel_index in range(FALLER_SIZE):
            jewel_row = jewel_indexes[jewel_index]
            self._board[faller_column][jewel_row] = faller_jewels[jewel_index]
                 


    def _clear_previous_faller(self, faller_column: int, faller_state: str) -> None:
        '''
        Used during gravity, otherwise doubles will be shown
        '''
        for row in range(self._rows):
            #can be EMPTY but for readability sake naming it jewel_with_state
            jewel_with_state = self._board[faller_column][row]
            if faller_state in jewel_with_state:
                self._board[faller_column][row] = EMPTY
                
                
    def _get_bottom_most_empty_row_index(self, column:int) -> int:
        '''
        used to check to see if faller is spwning on a full row
        '''
        for row_index in range(self._rows-1, -1, -1):
            if self._board[column][row_index] == EMPTY:
                return row_index

