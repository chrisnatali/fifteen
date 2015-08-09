"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

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

    ##################################################################
    # Phase one methods
    def nrow_by_mcol_check(self, nrows, mcols):
        """
        check if upper left nxm is solved

        to check if puzzle is solved use:

        puzzle.n_by_m_check(puzzle.get_height() - 1, 
                            puzzle.get_width() - 1)
        
        """
        positions = [(row, col) for row in range(nrows) for col in range(mcols)]
        for pos in positions:
            if not self._correct_position(*pos):
                return False
    
        return True


    def valid_moves(self):
        """
        Return a string with the valid single moves for the zero tile
        based on it's position
        """
        moves = ""
        czt = self.current_position(0, 0)

        if czt[0] > 0: 
            moves += "u"
        if czt[0] < self.get_height() - 1:
            moves += "d"
        if czt[1] > 0:
            moves += "l"
        if czt[1] < self.get_width() - 1:
            moves += "r"

        return moves

    def _correct_position(self, row, col):
        """
        Check whether the number in the position is correct
        """
        return self.get_number(row, col) == row*self.get_width() + col

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        if self.get_number(target_row, target_col) != 0:
            return False

        # check rows below
        for row in range(target_row + 1, self.get_height()):
            for col in range(self.get_width()):
                if not self._correct_position(row, col):
                    return False

        # now check cols to the right 
        for col in range(target_col + 1, self.get_width()):
            if not self._correct_position(target_row, col):
                return False

        return True 

    def _move(self, move_string, target_position):
        """
        move zero tile via update_puzzle and update
        the tile positions and all_moves string locals
        to the outer function
        """
        self.update_puzzle(move_string)
        # finding the new zero and target tile positions 
        # could be sped up, but keep it simple for now
        czt = self.current_position(0, 0)
        ctt = self.current_position(*target_position)
        return czt, ctt

    def _move_zero_to_target(self, target_row, target_col):
        """
        move the zero tile to the target position
        """
        # czt:  current zero tile position 
        czt = self.current_position(0, 0)
        # tt: target tile id's by target_row, target_col
        target_tile = (target_row, target_col)
      
        all_moves = ""

        # move up to target
        while czt[0] > target_tile[0]:
            czt, dummy_ctt = self._move("u", target_tile)
            all_moves += "u"
        
        # move down to target
        while czt[0] < target_tile[0]:
            czt, dummy_ctt = self._move("d", target_tile)
            all_moves += "d"

        # move left to target
        while czt[1] > target_tile[1]:
            czt, dummy_ctt = self._move("l", target_tile)
            all_moves += "l"

        # move right to target
        while czt[1] < target_tile[1]:
            czt, dummy_ctt = self._move("r", target_tile)
            all_moves += "r"

        return all_moves

    def _position_tile(self, target_row, target_col, dest_row, dest_col):
        """
        Position the target tile (id'd by target_row, target_col) in 
        the destination position (id'd by dest_row, dest_col) leaving
        the zero tile in position (dest_row, dest_col - 1)
        """

        # czt:  current zero tile position 
        czt = self.current_position(0, 0)
        # target_tile: target tile id's by target_row, target_col
        target_tile = (target_row, target_col)
        # dtt:  destination target tile position
        dtt = (dest_row, dest_col)
        # ctt:  current target tile position 
        ctt = self.current_position(target_row, target_col)
       
        all_moves = ""

        # move up to target
        while czt[0] > ctt[0]:
            czt, ctt = self._move("u", target_tile)
            all_moves += "u"

        # move left to target
        while czt[1] > ctt[1]:
            czt, ctt = self._move("l", target_tile)
            all_moves += "l"

        # move right to the 1 position left of target if needed
        while czt[1] + 1 < ctt[1]:
            czt, ctt = self._move("r", target_tile)
            all_moves += "r"


        # if target were directly above, we need to 
        # reposition zero to the left
        if czt[0] < ctt[0]:
            czt, ctt = self._move("ld", target_tile)
            all_moves += "ld"

        assert (ctt[1] - czt[1]) == 1, "zero tile should be 1 left of target"

        # move target left to dest col
        while ctt[1] > dtt[1]:
            # case 1:  we're in top row
            if ctt[0] == 0:
                czt, ctt = self._move("rdllu", target_tile)
                all_moves += "rdllu"
            else:
                czt, ctt = self._move("rulld", target_tile)
                all_moves += "rulld"

        # move target right to dest col
        while ctt[1] < dtt[1]:
            # case 1:  we're in top row
            if ctt[0] == 0:
                czt, ctt = self._move("drrul", target_tile)
                all_moves += "drrul"
            else:
                czt, ctt = self._move("urrdl", target_tile)
                all_moves += "urrdl"

        # move target down to dest row 
        while ctt[0] < dtt[0]:
            czt, ctt = self._move("druld", target_tile)
            all_moves += "druld"

        return all_moves

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """

        assert target_row > 1 and target_col > 0
        return self._position_tile(target_row, target_col, 
                                   target_row, target_col)

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """

        assert target_row > 1
        # czt:  current zero tile position 
        czt = self.current_position(0, 0)
        assert czt == (target_row, 0)

        # target_tile: target tile id'd by target_row, target_col
        target_tile = (target_row, 0)
      
        all_moves = ""

        # first move 
        czt, ctt = self._move("ur", target_tile)
        all_moves += "ur"

        assert czt == (target_row - 1, 1)
        # if target is not in expected position, we need to do more
        if ctt != target_tile:
            all_moves += self._position_tile(target_tile[0], target_tile[1], 
                                             czt[0], czt[1])
            czt = self.current_position(0, 0)
            assert czt == (target_row - 1, 0)
            czt, ctt = self._move("ruldrdlurdluurddlur", target_tile)
            all_moves += "ruldrdlurdluurddlur"

        last_move = "r" * ((self.get_width() - 1) - czt[1])
        czt, ctt = self._move(last_move, target_tile)
        all_moves += last_move

        return all_moves 

    #############################################################
    # Phase two methods

    def _check_below_or_right(self, target_row, target_col):
        """
        check whether tiles either below or to the right of 
        the target are in their correct positions
        """
        for row in range(self.get_height()):
            for col in range(self.get_width()):
                if row > target_row or col > target_col:
                    if not self._correct_position(row, col):
                        return False

        return True
 
    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        czt = self.current_position(0, 0)
        if czt != (0, target_col):
            return False
        
        # check if row1, target_col has correct tile
        if not self._correct_position(1, target_col):
            return False
        
        return self._check_below_or_right(1, target_col)

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        czt = self.current_position(0, 0)
        if czt != (1, target_col):
            return False

        # now check all positions below *or* to the right
        return self._check_below_or_right(1, target_col)

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert target_col > 1
        # czt:  current zero tile position 
        czt = self.current_position(0, 0)
        assert czt == (0, target_col), "zero tile ({}, {})".format(*czt)

        # target_tile: target tile id'd by target_row, target_col
        target_tile = (0, target_col)
      
        all_moves = ""

        # first move 
        czt, ctt = self._move("ld", target_tile)
        all_moves += "ld"

        assert czt == (1, target_col - 1)
        # if target is not in expected position, we need to do more
        if ctt != target_tile:
            all_moves += self._position_tile(target_tile[0], target_tile[1], czt[0], czt[1])
            czt = self.current_position(0, 0)
            ctt = self.current_position(*target_tile)
            assert ctt[0] == 1 and czt == (ctt[0], ctt[1] - 1)
            czt, ctt = self._move("urdlurrdluldrruld", target_tile)
            all_moves += "urdlurrdluldrruld"

        assert czt == (1, target_col - 1)
        return all_moves 

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        moves = self._position_tile(1, target_col, 
                                    1, target_col)

        # move zero tile to position 0, target_col
        dummy_czt, dummy_ctt = self._move("ur", (0, 0))
        moves += "ur"
        return moves
        
    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        czt = self.current_position(0, 0)
        assert czt[0] < 2 and czt[1] < 2
        # move the zero tile to its proper position
        moves = self._move_zero_to_target(0, 0)

        if not self.nrow_by_mcol_check(2, 2):
            one_pos = self.current_position(0, 1)
            if one_pos == (1, 0):
                czt, dummy_ctt = self._move("drul", (0, 1))
                moves += "drul"
            else:
                assert one_pos == (1, 1)
                czt, dummy_ctt = self._move("rdlu", (0, 1))
                moves += "rdlu"

        # assert self.two_by_two_check(), "unsolvable 2x2"
        return moves

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # start by moving zero down to lower right
        moves = self._move_zero_to_target(self.get_height() - 1, 
                                          self.get_width() - 1)

        # now solve each row below 1 from bottom up
        for row in range(self.get_height() - 1, 1, -1):
            for col in range(self.get_width() - 1, 0, -1):
                moves += self.solve_interior_tile(row, col)
                assert self.lower_row_invariant(row, col - 1),\
                   "row: {}\npuzzle:\n{}".format(row, self)

            moves += self.solve_col0_tile(row)
            # ensure the current row has been solved
            assert self.lower_row_invariant(row - 1, self.get_width() - 1),\
                   "row: {}\npuzzle:\n{}".format(row, self)

        # ensure that all rows below 1 are solved
        assert self.row1_invariant(self.get_width() - 1)
        # solve row 1 from right to left stopping at col 1
        for col in range(self.get_width() - 1, 1, -1):
            moves += self.solve_row1_tile(col)
            assert self.row0_invariant(col)
            moves += self.solve_row0_tile(col)
            assert self.row1_invariant(col - 1)

        # finally solve the 2x2
        moves += self.solve_2x2()

        return moves


# Start interactive simulation
# poc_fifteen_gui.FifteenGUI(Puzzle(2, 3))


