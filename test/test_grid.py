"""
File contains unit tests for game logic.
"""
import unittest

import numpy as np  # type: ignore

from utils.grid import Grid


class GridTestCase(unittest.TestCase):
    """
    Tests which checks if grid class have implemented 2048 logic correctly.
    """

    def setUp(self) -> None:
        """
        Set up required attributes for tests
        """
        self.grid_size: int = 4
        self.grid: Grid = Grid(grid_size=4)
        self.test_grid: 'np.ndarray' = np.array(
            [[2, 0, 0, 4],
             [0, 2, 0, 0],
             [0, 2, 2, 0],
             [0, 0, 0, 2]]
        )

    def reset_grid(self) -> None:
        """
        Reset grid to have initial state
        """
        self.grid.grid = np.copy(self.test_grid)

    def test_grid_shape(self) -> None:
        """
        Tests if grid was correctly initialized.
        """
        self.assertEqual(self.grid.grid.shape, (self.grid_size, self.grid_size))

    def test_generation_of_elements(self) -> None:
        """
        Tests if 2/4 are correctly generated into a grid
        """
        self.assertEqual((self.grid.grid != 0).sum(), 0)

        self.grid.generate_twos(number_of_twos=1)
        self.assertEqual((self.grid.grid != 0).sum(), 1)

        self.grid.generate_twos(number_of_twos=2)
        self.assertEqual((self.grid.grid != 0).sum(), 3)

        self.grid.generate_twos(number_of_twos=13)
        self.assertEqual((self.grid.grid != 0).sum(), 16)

        self.grid.generate_twos(number_of_twos=1)
        self.assertEqual((self.grid.grid != 0).sum(), 16)

    def test_grid_shifting(self) -> None:
        """
        Test if grid elements are properly shifted.
        """
        self.reset_grid()

        self.grid.shift_left()
        self.assertTrue((self.grid.grid == np.array(
            [[2, 4, 0, 0],
             [2, 0, 0, 0],
             [2, 2, 0, 0],
             [2, 0, 0, 0]])).all()
        )
        self.grid.shift_right()
        self.assertTrue((self.grid.grid == np.array(
            [[0, 0, 2, 4],
             [0, 0, 0, 2],
             [0, 0, 2, 2],
             [0, 0, 0, 2]])).all()
        )

    def test_grid_rotation(self) -> None:
        """
        Tests if grid rotation over 90 degrees works as designed.
        """
        self.reset_grid()

        self.grid.rotate_left()
        self.assertTrue((self.grid.grid == np.array(
            [[4, 0, 0, 2],
             [0, 0, 2, 0],
             [0, 2, 2, 0],
             [2, 0, 0, 0]])).all()
        )
        self.grid.rotate_right()
        self.assertTrue((self.grid.grid == np.array(
            [[2, 0, 0, 4],
             [0, 2, 0, 0],
             [0, 2, 2, 0],
             [0, 0, 0, 2]])).all()
        )

    def test_grid_move_left(self) -> None:
        """
        Tests if grid's elements are properly shifted and merged while moved left.
        """
        self.reset_grid()
        self.grid.move_left()
        self.assertTrue((self.grid.grid == np.array(
            [[2, 4, 0, 0],
             [2, 0, 0, 0],
             [4, 0, 0, 0],
             [2, 0, 0, 0]])).all()
        )

    def test_grid_move_right(self) -> None:
        """
        Tests if grid's elements are properly shifted and merged while moved right.
        """
        self.reset_grid()
        self.grid.move_right()
        self.assertTrue((self.grid.grid == np.array(
            [[0, 0, 2, 4],
             [0, 0, 0, 2],
             [0, 0, 0, 4],
             [0, 0, 0, 2]])).all()
        )

    def test_grid_move_up(self) -> None:
        """
        Tests if grid's elements are properly shifted and merged while moved up.
        """
        self.reset_grid()
        self.grid.move_up()
        self.assertTrue((self.grid.grid == np.array(
            [[2, 4, 2, 4],
             [0, 0, 0, 2],
             [0, 0, 0, 0],
             [0, 0, 0, 0]])).all()
        )

    def test_grid_move_down(self) -> None:
        """
        Tests if grid's elements are properly shifted and merged while moved down.
        """
        self.reset_grid()
        self.grid.move_down()
        self.assertTrue((self.grid.grid == np.array(
            [[0, 0, 0, 0],
             [0, 0, 0, 0],
             [0, 0, 0, 4],
             [2, 4, 2, 2]])).all()
        )

    def test_getitem(self) -> None:
        """
        Tests if we can access grid elements using __getitem__ method.
        """
        self.reset_grid()
        self.assertTrue(self.grid[0, 0] == 2)

        self.grid[1, 1] = 10
        self.assertTrue(self.grid[1, 1] == 10)

    def test_is_win(self) -> None:
        """
        Tests if win is detected correctly.
        """
        self.grid[3, 3] = 2048
        self.assertTrue(self.grid.is_win())

    def test_is_lose(self) -> None:
        """
        Tests if lose is detected
        """
        self.assertFalse(self.grid.is_lose())

        self.grid.grid = np.arange(1, self.grid_size * self.grid_size + 1).\
            reshape((self.grid_size, self.grid_size))

        self.assertTrue(self.grid.is_lose())


if __name__ == "__main__":
    unittest.main()
