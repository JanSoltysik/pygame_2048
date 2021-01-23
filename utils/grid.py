"""
A file with implementation of 2048 logic.
"""
from enum import Enum
from typing import Callable, Dict, Tuple

import numpy as np  # type: ignore


class Direction(Enum):
    """
    Enum used to describe direction of shifting the grid.
    ---
    LEFT: direction used to shift elements to the left side.
    RIGHT: direction used to shift elements to the right side.
    """
    LEFT = 1
    RIGHT = -1


class MoveDirection(Enum):
    """
    Enum used to determine move direction.
    """
    UP = "w"
    DOWN = "s"
    LEFT = "a"
    RIGHT = "d"


class Grid:
    """
    A class representing a grid used in 2048 game, it contains all the required
    logic used for the whole game.

    Attributes
    ----------
    gird_size: int
        A size of created gird, in original game this value is set to 4.
    max_tile: int
        A value required to successfully finish the game.
    score: int
        Current score of the grid, which is calculated from values of merged cells in the grid.
    grid: np.ndarray
        A numpy array which represents grid_size x grid_size board on which game is taking place.
    move_map: Dict[str, Callable[[], bool]]
        A dictionary which translates keys to methods which move cells in our grid.
    """
    def __init__(self, *, grid_size: int = 4, max_tile: int = 2048) -> None:
        """
        Parameters
        ----------
        :grid_size: int, optional
            Size of the grid is set to grid_size x grid_size (default is 4).
        :max_tile: int, optional
            Number required to win a game (default is 2048).
        """
        self.grid_size: int = grid_size
        self.max_tile: int = max_tile
        self.score: int = 0

        self.grid: np.ndarray = np.zeros((grid_size, grid_size), dtype=np.int16)

        self.move_map: Dict[str, Callable[[], bool]] = {
            MoveDirection.UP.value: self.move_up,
            MoveDirection.DOWN.value: self.move_down,
            MoveDirection.LEFT.value: self.move_left,
            MoveDirection.RIGHT.value: self.move_right
        }

    def move(self, direction: str) -> bool:
        """
        Moves grid in the given direction.

        Parameters
        ----------
        direction: str
            Direction in which grid is going to be moved.

        Returns
        -------
        bool
            True if move in a given direction is valid, False otherwise.
        """
        return self.move_map.get(direction, lambda *args: False)()

    def is_win(self) -> bool:
        """
        Checks if grid is in a winning state.

        Returns
        -------
        bool
            True if won (max_title is present in a grid).
        """
        return self.max_tile in self.grid

    def is_lose(self) -> bool:
        """
        Checks if grid is in a loosing state.

        Returns
        -------
        bool
            True if lost (no more cells merges possible and all the cells aren't equal to 0).
        """
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if j != self.grid_size - 1 and self.grid[i, j] == self.grid[i, j + 1] or \
                   i != self.grid_size - 1 and self.grid[i, j] == self.grid[i + 1, j]:
                    return False

        return 0 not in self.grid

    def generate_twos(self, number_of_twos: int) -> None:
        """
        Generate given number of 2/4 in grid on non-zero positions.

        Parameters
        ----------
        number_of_twos: int
            Number of elements we want to generate.
        """
        non_zero_indices: np.ndarray = np.column_stack(np.where(self.grid == 0))
        try:
            for ind in np.random.choice(
                    range(non_zero_indices.shape[0]), number_of_twos, replace=False):
                x_cord, y_cord = non_zero_indices[ind]

                if self.grid.sum() in (0, 2):
                    self.grid[x_cord, y_cord] = 2
                else:
                    self.grid[x_cord, y_cord] = np.random.choice((2, 4))
        except ValueError:
            # there isn't any zero elements in the grid
            pass

    def merge_same_neighbours(self, direction: Direction) -> None:
        """
        Merge neighbours in the grid with the same value
        if the made move is pushing them towards each other.

        Parameters
        ----------
        direction: Direction
            Direction in with we are moving our grid.
        """
        y_range = range(self.grid_size - 1) if direction == Direction.LEFT else \
            range(self.grid_size - 1, 0, direction.value)
        for i in range(self.grid_size):
            for j in y_range:
                if self.grid[i, j] == self.grid[i, j + direction.value] and self.grid[i, j] != 0:
                    self.grid[i, j] *= 2
                    self.grid[i, j + direction.value] = 0
                    self.score += self.grid[i, j]

    def move_left(self) -> bool:
        """
        Moves and merge all the elements in the grid to the left side.

        Returns
        -------
        bool
            True if move valid, False otherwise.
        """
        current_grid: np.ndarray = np.copy(self.grid)

        self.shift_left()
        self.merge_same_neighbours(Direction.LEFT)
        self.shift_left()

        return not np.array_equal(current_grid, self.grid)

    def move_right(self) -> bool:
        """
        Moves and merge all the elements in the grid to the right side.

        Returns
        -------
        bool
            True if move valid, False otherwise.
        """
        current_grid: np.ndarray = np.copy(self.grid)
        self.shift_right()
        self.merge_same_neighbours(Direction.RIGHT)

        return not np.array_equal(current_grid, self.grid)

    def move_up(self) -> bool:
        """
        Moves and merge all the elements in the grid towards the up.

        Returns
        -------
        bool
            True if move valid, False otherwise.
        """
        current_grid: np.ndarray = np.copy(self.grid)
        self.rotate_left()
        self.move_left()
        self.rotate_right()

        return not np.array_equal(current_grid, self.grid)

    def move_down(self) -> bool:
        """
        Moves and merge all the elements in the grid towards the down.

        Returns
        -------
        bool
            True if move valid, False otherwise.
        """
        current_grid: np.ndarray = np.copy(self.grid)
        self.rotate_left()
        self.move_left()
        self.shift_right()
        self.rotate_right()

        return not np.array_equal(current_grid, self.grid)

    def shift_grid(self, direction: Direction) -> None:
        """
        Shift all non-zero elements to the given direction (without merging same value elements).

        Parameters
        ----------
        direction: Direction
            A direction in which elements will be shifted.
        """
        mask: np.ndarray = self.grid != 0
        flipped_mask: np.ndarray =\
            mask.sum(1, keepdims=True) > np.arange(self.grid_size - 1, -1, -1)
        flipped_mask = flipped_mask[:, ::-direction.value]
        self.grid[flipped_mask] = self.grid[mask]
        self.grid[~flipped_mask] = 0

    def shift_left(self) -> None:
        """
        Shift all non-zero elements to the left side.
        """
        self.shift_grid(Direction.LEFT)

    def shift_right(self) -> None:
        """
        Shift all non-zero elements to the right side.
        """
        self.shift_grid(Direction.RIGHT)

    def rotate_left(self) -> None:
        """
        Rotate gird by 90 degrees counter-clockwise.
        """
        self.grid = np.rot90(self.grid)

    def rotate_right(self) -> None:
        """
        Rotate gird by 90 degrees clockwise.
        """
        self.grid = np.rot90(self.grid, k=3)

    def reset(self) -> None:
        """
        Reset the game state to a starting state.
        """
        self.grid = np.zeros((self.grid_size, self.grid_size),
                             dtype=np.int16)
        self.score = 0

    def __str__(self) -> str:
        """
        Converts grid to a string format.

        Returns
        -------
        str
            grid_size x grid_size board in a string format.
        """
        return str(self.grid)

    def __repr__(self) -> str:
        """
        Prints the class name with a attributes values.

        Returns
        -------
        str
            Short representation of created object.
        """
        return f"Grid(size={self.grid_size}, score={self.score})"

    def __getitem__(self, item: Tuple[int, int]) -> np.int16:
        """
        Get access to given cell in a grid.

        Parameters
        ----------
        item: Tuple[int, int]
            Position of a given cell in a grid.

        Returns
        -------
        int
            Value of a cell ath a given position.
        """
        return self.grid[item[0], item[1]]

    def __setitem__(self, item: Tuple[int, int], value: int) -> None:
        """
        Set grid element on a given position to a acquired value.

        Parameters
        ----------
        item: Tuple[int, int]
            Position of a given cell in a grid.
        value: int
            New value for a grid element.
        """
        self.grid[item[0], item[1]] = value
