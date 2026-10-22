import random
from aibooks.sudoku import complete_grid, is_valid_solution, solve, make_puzzle, make_book


def test_permuted_solution_valid():
    for seed in range(5):
        assert is_valid_solution(complete_grid(random.Random(seed)))


def test_generated_puzzles_uniquely_solvable():
    for seed in (4, 19):
        p, expected = make_puzzle(random.Random(seed), clues=40)
        n, solved = solve(p)
        assert n == 1
        assert solved == expected
        assert sum(x != 0 for row in p for x in row) == 40


def test_invalid_puzzle_rejected():
    invalid = tuple(tuple(1 if c in (0, 1) and r == 0 else 0
                          for c in range(9)) for r in range(9))
    assert solve(invalid) == (0, None)


def test_book_seed_reproducible_and_distinct():
    a = make_book(20, 42, clues=40)
    b = make_book(20, 42, clues=40)
    assert [x["hash"] for x in a] == [x["hash"] for x in b]
    assert len({x["hash"] for x in a}) == 20
