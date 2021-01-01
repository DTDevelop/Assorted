# classes / gameplay loop / some functions redacted

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction
    def move_to_target(self, target_row, target_col, move_string,check = True):
        """
        helper function
        moves 0 tile to end tile
        """
        zero_tile = self.current_position(0,0)
        if zero_tile != (target_row, target_col):
            #prioritize left & up movements, then down / right movements to ensure invariant stands
            while self.current_position(0,0)[1] > target_col: #left
                self.update_puzzle('l')
                move_string += 'l'
            while self.current_position(0,0)[0] > target_row: #up
                self.update_puzzle('u')
                move_string += 'u'
            while self.current_position(0,0)[1] < target_col: #right
                self.update_puzzle('r')
                move_string += 'r'
            while self.current_position(0,0)[0] < target_row: #down
                self.update_puzzle('d')
                move_string += 'd'
        #assert should stand true and zero tile should be at target location

        #if check:
        #    assert self.lower_row_invariant(target_row, target_col)
        return move_string
    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        col_check = target_col
        initial = target_col
#        if self.current_position(0,0) == (0, target_col):
#            return True
#        if self.current_position(0,0) != (0, target_col):
#            return False

        while col_check < self.get_width():
            if col_check == initial:
                if self.current_position(0,0) == (0, target_col):
                    col_check += 1
                    continue
                else:
                    return False
            if self.current_position(0, col_check) != (0, col_check):
                return False
            col_check += 1

        #checking row_1
        col_check = target_col
        while col_check < self.get_width():
            if self.current_position(1, col_check) != (1, col_check):
                return False
            col_check += 1

        return self.lower_row_invariant(2,0,True,True)

        def solve_2x2(self):
            """
            Solve the upper left 2x2 part of the puzzle
            Updates the puzzle and returns a move string
            """
            #place 0, tile to prepare to algorithm
            move_set = ''
            self.update_puzzle('lu')
            move_set += 'lu'

            while self.current_position(0,1) != (0,1) or self.current_position(1,1) != (1,1) or self.current_position(1,0) != (1,0):

                self.update_puzzle('rdlu')
                move_set += 'rdlu'

            return move_set
