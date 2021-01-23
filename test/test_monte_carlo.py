"""
File contains unit tests for bot class.
"""
import unittest
from typing import List, Callable

import numpy as np  # type: ignore

from utils.grid import Grid
from mcts_bot.monte_carlo import MonteCarloTreeSearch,\
    make_random_move,\
    get_moves_list


class MCTSTestCase(unittest.TestCase):
    """
    Case which tests if Monte Carlo Tree Search
    bot is working correctly.
    """
    def setUp(self) -> None:
        """
        Initialize required objects for all the tests.
        """
        self.grid: Grid = Grid()
        self.bot: MonteCarloTreeSearch = MonteCarloTreeSearch(self.grid)

    def test_move_list(self) -> None:
        """
        Tests if list of all the moves is created properly.
        """
        list_of_moves: List[Callable[[], bool]] = get_moves_list(self.grid)
        self.assertEqual(len(list_of_moves), self.grid.grid_size)

        self.grid.grid = np.array(
            [[0, 2, 0, 0],
             [0, 0, 0, 0],
             [0, 0, 4, 2],
             [2, 0, 0, 4]]
        )
        list_of_moves[0]()
        self.assertTrue((self.grid.grid == [
            [2, 2, 4, 2],
            [0, 0, 0, 4],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]).all()
        )
        list_of_moves[1]()
        self.assertTrue((self.grid.grid == [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 2],
            [2, 2, 4, 4]]).all()
        )
        list_of_moves[2]()
        self.assertTrue((self.grid.grid == [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [2, 0, 0, 0],
            [4, 8, 0, 0]]).all()
        )
        list_of_moves[3]()
        self.assertTrue((self.grid.grid == [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 2],
            [0, 0, 4, 8]]).all()
        )

    def test_random_move(self) -> None:
        """
        Tests if move was performed after call
        of random_move function.
        """
        test_grid: np.ndarray = np.array(
            [[0, 0, 0, 0],
             [0, 2, 2, 0],
             [0, 2, 2, 0],
             [0, 0, 0, 0]]
        )
        self.grid.grid = np.copy(test_grid)
        make_random_move(get_moves_list(self.grid))

        self.assertFalse(
            (test_grid == self.grid.grid).all())

    @unittest.skipIf(False, "Set to False if bot verification not needed.")
    def test_bot(self) -> None:
        """
        Tests if bot works as designed.
        """
        self.grid = Grid()
        self.bot.grid = self.grid
        search_move_list: List[Callable[[], bool]] = get_moves_list(self.grid)

        self.grid.generate_twos(number_of_twos=2)
        while not (self.grid.is_win() or self.grid.is_lose()):
            ind = self.bot()
            search_move_list[ind]()
            self.grid.generate_twos(number_of_twos=1)
            # print(self.grid)

        self.assertTrue(self.grid.is_win())
        self.assertFalse(self.grid.is_lose())


if __name__ == "__main__":
    unittest.main()
