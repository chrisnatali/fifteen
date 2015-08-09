import poc_fifteen as fif
import random

def test_lower_row_invariant():
    """
    Check true/false case
    """

    grid = [[1,2,3],
            [4,5,0],
            [6,7,8]]

    puz = fif.Puzzle(3, 3, grid)

    assert puz.lower_row_invariant(1, 2), "lr invariant should hold"
    puz.update_puzzle("ldru")
    assert not puz.lower_row_invariant(1, 2), "lr invariant should hold"

def test_solve_interior_tile():
    """
    Ensure all handled cases are solved correctly
    """

    # case 1:  directly above
    grid = [[1,2,8],
            [4,5,3],
            [6,7,0]]

    puz = fif.Puzzle(3, 3, grid)
    puz.solve_interior_tile(2, 2)
    assert puz.lower_row_invariant(2, 1), "lr invariant should hold"

    # case 2:  directly left
    grid = [[1,2,6],
            [4,5,3],
            [8,7,0]]

    puz = fif.Puzzle(3, 3, grid)
    puz.solve_interior_tile(2, 2)
    assert puz.lower_row_invariant(2, 1), "lr invariant should hold"

    # case 3:  above and left
    grid = [[8,2,6],
            [4,5,3],
            [1,7,0]]

    puz = fif.Puzzle(3, 3, grid)
    puz.solve_interior_tile(2, 2)
    assert puz.lower_row_invariant(2, 1), "lr invariant should hold"

def test_solve_col0_tile():

    # solve for row 2, col 0
    grid = [[1,2,6],
            [4,5,3],
            [0,7,8]]

    puz = fif.Puzzle(3, 3, grid)
    puz.solve_col0_tile(2)
    assert puz.lower_row_invariant(1, 2), "lr invariant should hold"

def test_row1_invariant():

    grid = [[1,3,2],
            [4,0,5],
            [6,7,8]]

    puz = fif.Puzzle(3, 3, grid)
    assert puz.row1_invariant(1), "row1 invariant should hold"

def test_row0_invariant():

    grid = [[3,0,2],
            [1,4,5],
            [6,7,8]]

    puz = fif.Puzzle(3, 3, grid)
    assert puz.row0_invariant(1), "row0 invariant should hold"

def test_solve_row1_tile():

    def solve_row1_grid(grid, col):
        puz = fif.Puzzle(4, 4, grid)
        assert puz.row1_invariant(col), "row1 invariant should hold"
        puz.solve_row1_tile(col)
        assert puz.row0_invariant(col), "row0 invariant should hold"


    grid1 = [[6,1,2,3],
             [4,5,0,7],
             [8,9,10,11],
             [12,13,14,15]]

    grid2 = [[4,1,2,3],
             [6,5,0,7],
             [8,9,10,11],
             [12,13,14,15]]

    solve_row1_grid(grid1, 2)
    solve_row1_grid(grid2, 2)

def test_solve_row0_tile():

    def solve_row0_grid(grid, col):
        puz = fif.Puzzle(4, 4, grid)
        assert puz.row0_invariant(col), "row0 invariant should hold"
        puz.solve_row0_tile(col)
        assert puz.row1_invariant(col - 1), "row1 invariant should hold"


    grid1 = [[5,6,2,0],
             [4,3,1,7],
             [8,9,10,11],
             [12,13,14,15]]

    grid2 = [[3,1,2,0],
             [6,5,4,7],
             [8,9,10,11],
             [12,13,14,15]]

    solve_row0_grid(grid1, 3)
    solve_row0_grid(grid2, 3)


def shuffle_puzzle(puzzle, num_moves):
    """
    Shuffle the puzzle with num_moves
    """
    moves = ""
    puz = puzzle.clone()
    for dummy in range(num_moves):
        valid_moves = puz.valid_moves()
        move = valid_moves[random.randrange(len(valid_moves))]
        puz.update_puzzle(move)
        moves += move

    return puz, moves


def test_solve_2x2():

    grid = [[0, 1],
            [2, 3]]

    puz = fif.Puzzle(2, 2, grid)
    # sort it via 10 random moves
    shuffled, moves = shuffle_puzzle(puz, 10)
    print("moves: {}".format(moves))
    puz.solve_2x2()
    assert puz.nrow_by_mcol_check(2, 2)

def test_solve_4x4():

    grid = [[0,1,2,3],
            [4,5,6,7],
            [8,9,10,11],
            [12,13,14,15]]

    puz = fif.Puzzle(4, 4, grid)
    # sort it via 30 random moves
    shuffled, moves = shuffle_puzzle(puz, 1000)
    print("shuffled board:\n {}".format(shuffled))
    shuffled.solve_puzzle()
    assert shuffled.nrow_by_mcol_check(shuffled.get_height() - 1, 
                                 shuffled.get_width() - 1)

def test_solve_5x5():

    num_rows = num_cols = 5
    grid = [[col + (num_cols * row) 
             for col in range(num_cols)] 
            for row in range(num_rows)]
    
    puz = fif.Puzzle(num_rows, num_cols, grid)
    # sort it via 30 random moves
    shuffled, moves = shuffle_puzzle(puz, 1000)
    print("shuffled board:\n {}".format(shuffled))
    shuffled.solve_puzzle()
    assert shuffled.nrow_by_mcol_check(shuffled.get_height() - 1, 
                                 shuffled.get_width() - 1)


def test_solve_problem():

    grid = [[1,3,7,6],
            [4,9,2,10],
            [8,13,14,5],
            [12,0,15,11]]

    puz = fif.Puzzle(4, 4, grid)
    puz.solve_puzzle()
    assert puz.nrow_by_mcol_check(3,3) 
