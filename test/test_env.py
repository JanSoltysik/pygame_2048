"""
Contains tests for created OpenAI Gym Env.
"""
import unittest
from typing import Dict, Union, Tuple

import numpy as np  # type: ignore

from utils.grid import MoveDirection, Grid
from rl_bot.envs.env_2048 import Env2048


class EnvTestCase(unittest.TestCase):
    """
    Tests if implemented environment is working
    as designed.
    """

    def setUp(self) -> None:
        """
        Initialize all required variables.
        """
        self.env: Env2048 = Env2048()

    def test_reset(self) -> None:
        """
        Tests if environment is resetting properly.
        """
        rested_env: Tuple[Grid, float, bool,
                          Dict[str, Union[int, bool, float]]] = self.env.reset()
        self.assertEqual((rested_env[0].grid != 0).sum(), 2)
        self.assertEqual(rested_env[1], 0.0)
        self.assertFalse(rested_env[2])

    def test_render(self) -> None:
        """
        Tests if env render is created properly.
        """
        size: int = self.env.grid.grid_size
        self.env.grid.grid = np.zeros((size, size))

        proper_render: str = "Score: 0\n"
        proper_render += "Highest: 0.0\n"
        proper_render += f"{np.zeros((size, size))!s}\n\n"

        self.assertEqual(self.env.render(), proper_render)

    def test_valid_step(self) -> None:
        """
        Tests environment with valid step execution.
        """
        self.env.reset()
        state: Tuple[Grid, float, bool,
                          Dict[str, Union[int, bool, float]]] =\
            self.env.step(MoveDirection.RIGHT.value)

        self.assertTrue(not state[0].is_win() and not state[0].is_lose())
        self.assertLessEqual(state[1], 4)
        self.assertFalse(state[2])

    def test_invalid_step(self) -> None:
        """
        Tests environment with invalid step execution.
        """
        size: int = self.env.grid.grid_size
        self.env.grid.grid =\
            np.arange(1, size * size + 1).reshape((size, size))
        state: Tuple[Grid, float, bool,
                     Dict[str, Union[int, bool, float]]] = \
            self.env.step(MoveDirection.RIGHT.value)

        self.assertTrue(state[0].is_lose())
        self.assertEqual(state[1], 0.)
        self.assertTrue(state[2])


if __name__ == "__main__":
    unittest.main()
