"""Deterministic, algorithmically checked Sudoku puzzles.

No language model can declare a Sudoku 'solved' without this solver.
"""
from __future__ import annotations

from hashlib import sha256
import random

Grid = tuple[tuple[int, ...], ...]


def complete_grid(rng: random.Random) -> Grid:
    """Randomly permute a valid base grid, preserving its Sudoku properties."""
    def order() -> list[int]:
        return [3 * b + r for b in rng.sample(range(3), 3)
                for r in rng.sample(range(3), 3)]
    rows, cols = order(), order()
    digits = rng.sample(range(1, 10), 9)
    return tuple(tuple(digits[(r * 3 + r // 3 + c) % 9]
                       for c in cols) for r in rows)


def is_valid_solution(grid: Grid) -> bool:
    if len(grid) != 9 or any(len(row) != 9 for row in grid):
        return False
    expected = set(range(1, 10))
    if any(set(row) != expected for row in grid):
        return False
    if any({grid[r][c] for r in range(9)} != expected for c in range(9)):
        return False
    return all({grid[r][c] for r in range(br, br + 3)
                for c in range(bc, bc + 3)} == expected
               for br in (0, 3, 6) for bc in (0, 3, 6))


def solve(grid: Grid, limit: int = 2) -> tuple[int, Grid | None]:
    """Count up to `limit` solutions; use MRV backtracking for efficiency."""
    if limit < 1 or len(grid) != 9 or any(len(row) != 9 for row in grid):
        return 0, None
    if any(not isinstance(value, int) or isinstance(value, bool)
           or value < 0 or value > 9 for row in grid for value in row):
        return 0, None
    board = [list(row) for row in grid]
    for r in range(9):
        for c in range(9):
            value = board[r][c]
            if not value:
                continue
            board[r][c] = 0
            if value in candidates_excluded(board, r, c):
                return 0, None
            board[r][c] = value
    found = 0
    first: Grid | None = None

    def backtrack() -> None:
        nonlocal found, first
        if found >= limit:
            return
        best: tuple[int, int, list[int]] | None = None
        for r in range(9):
            for c in range(9):
                if board[r][c]:
                    continue
                options = [n for n in range(1, 10)
                           if n not in candidates_excluded(board, r, c)]
                if not options:
                    return
                if best is None or len(options) < len(best[2]):
                    best = (r, c, options)
                    if len(options) == 1:
                        break
            if best is not None and len(best[2]) == 1:
                break
        if best is None:
            found += 1
            if first is None:
                first = tuple(tuple(row) for row in board)
            return
        r, c, options = best
        for n in options:
            board[r][c] = n
            backtrack()
            board[r][c] = 0
            if found >= limit:
                return

    backtrack()
    return found, first


def candidates_excluded(board: list[list[int]], r: int, c: int) -> set[int]:
    return (set(board[r])
            | {board[i][c] for i in range(9)}
            | {board[i][j] for i in range(r // 3 * 3, r // 3 * 3 + 3)
               for j in range(c // 3 * 3, c // 3 * 3 + 3)})


def grid_hash(grid: Grid) -> str:
    return sha256("".join(str(v) for row in grid for v in row).encode()).hexdigest()


def make_puzzle(rng: random.Random, clues: int = 38) -> tuple[Grid, Grid]:
    if not 28 <= clues <= 70:
        raise ValueError("clues must be between 28 and 70")
    for _ in range(12):
        solution = complete_grid(rng)
        board = [list(row) for row in solution]
        positions = list(range(81))
        rng.shuffle(positions)
        remaining = 81
        for p in positions:
            if remaining <= clues:
                break
            r, c = divmod(p, 9)
            old = board[r][c]
            board[r][c] = 0
            candidate = tuple(tuple(row) for row in board)
            count, _ = solve(candidate)
            if count == 1:
                remaining -= 1
            else:
                board[r][c] = old
        if remaining == clues:
            puzzle = tuple(tuple(row) for row in board)
            assert solve(puzzle) == (1, solution), "Generator invariant violated"
            return puzzle, solution
    raise RuntimeError("Could not construct a unique Sudoku; try another seed")


def make_book(count: int, seed: int, clues: int = 38) -> list[dict]:
    if count < 20 or count > 150:
        raise ValueError("The pilot supports 20 to 150 puzzles")
    rng = random.Random(seed)
    result: list[dict] = []
    hashes: set[str] = set()
    for number in range(1, count + 1):
        for _ in range(30):
            puzzle, solution = make_puzzle(rng, clues)
            digest = grid_hash(puzzle)
            if digest not in hashes:
                hashes.add(digest)
                result.append({"number": number, "puzzle": puzzle,
                               "solution": solution, "hash": digest,
                               "clues": clues})
                break
        else:
            raise RuntimeError("Cannot avoid duplicate puzzles")
    return result
