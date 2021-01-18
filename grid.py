import numpy as np
from typing import Callable, Dict


class Grid:
    def __init__(self, *, grid_size: int = 4, max_tile: int = 2048) -> None:
        self.grid_size: int = grid_size
        self.max_tile: int = max_tile
        self.score: int = 0

        self.grid: np.ndarray = np.zeros((grid_size, grid_size), dtype=np.int16)

        self.move_map: Dict[str, Callable[[Grid], None]] = {
            'w': self.moveUp,
            's': self.moveDown,
            'a': self.moveLeft,
            'd': self.moveRight
        }

    def move(self, direction: str) -> None:
        return self.move_map.get(direction, lambda *args: None)()

    def is_win(self) -> bool:
        return self.max_tile in self.grid

    def is_lose(self) -> bool:
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                # is marge possible
                if j != self.grid_size - 1 and self.grid[i, j] == self.grid[i, j + 1] or \
                   i != self.grid_size - 1 and self.grid[i, j] == self.grid[i + 1, j]:
                    return False

        return 0 not in self.grid

    def generate_twos(self, number_of_twos: int = 1) -> None:
        non_zero_indices: np.ndarray = np.column_stack(np.where(self.grid == 0))

        for ind in np.random.randint(0, non_zero_indices.shape[0], size=number_of_twos):
            x, y = non_zero_indices[ind]

            if self.grid.sum() in (0, 2):
                self.grid[x, y] = 2
            else:
                self.grid[x, y] = np.random.choice((2, 4))

    def moveLeft(self) -> None:
        self.shift_left()

        for i in range(self.grid_size):
            for j in range(self.grid_size - 1):
                if self.grid[i, j] == self.grid[i, j + 1] and self.grid[i, j] != 0:
                    self.grid[i, j] *= 2
                    self.grid[i, j + 1] = 0

                    self.score += self.grid[i, j]
                    # j = 0

        self.shift_left()

    def moveUp(self) -> None:
        self.rotateLeft()
        self.moveLeft()
        self.rotateRight()

    def moveRight(self) -> None:
        self.shift_right()

        for i in range(self.grid_size):
            for j in range(self.grid_size - 1, 0, -1):
                if self.grid[i, j] == self.grid[i, j - 1] and self.grid[i, j] != 0:
                    self.grid[i, j] *= 2
                    self.grid[i, j - 1] = 0

                    self.score += self.grid[i, j]
                    # j = 0

    def moveDown(self) -> None:
        self.rotateLeft()
        self.moveLeft()
        self.shift_right()
        self.rotateRight()

    def shift_grid(self, direction: int) -> None:
        mask = self.grid != 0
        flipped_mask = mask.sum(1, keepdims=True) > np.arange(self.grid_size - 1, -1, -1)
        flipped_mask = flipped_mask[:, ::direction]
        self.grid[flipped_mask] = self.grid[mask]
        self.grid[~flipped_mask] = 0

    def shift_left(self) -> None:
        self.shift_grid(-1)

    def shift_right(self) -> None:
        self.shift_grid(1)

    def rotateLeft(self) -> None:
        self.grid = np.rot90(self.grid)

    def rotateRight(self) -> None:
        self.grid = np.rot90(self.grid, k=3)

    def __str__(self) -> str:
        return str(self.grid)

    def __repr__(self) -> str:
        return str(self)

    def __getitem__(self, item) -> np.int16:
        return self.grid[item[0], item[1]]
