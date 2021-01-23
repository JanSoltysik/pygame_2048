"""
A file contains a 2048 openai environment
implementation.
"""
from typing import Union, Tuple, Dict

import gym  # type: ignore
import numpy as np  # type: ignore

from utils.grid import Grid


class Env2048(gym.Env):
    """
    Class wrapping game's logic in order to create
    environment compatible with OpenAI Gym standard.

    Attributes
    ----------
    grid: Grid
        A class containing game's logic.
    action_space: gym.space.Discrete
        Discrete space of actions in available in game,
        only four moves are valid in 2048.
    observation_space: gym.spaces.Box
        A space containing available observations.
    steps: int
        Current number of performed moves.
    max_illegal_moves: int
        Allowed number of illegal moves.
    num_illegal_moves: int
        Current number of illegal moves.
    illegal_move_reward: float
        Reward acquired for making an illegal move.
    reward_range: Tuple[float, float]
        A tuple of floats representing all the possible rewards.
    max_steps: int
        Maximal number of steps.
    """
    metadata = {'render.modes': ['ascii']}

    def __init__(self) -> None:
        self.grid: Grid = Grid()

        self.action_space: gym.spaces.Discrete = \
            gym.spaces.Discrete(4)
        self.observation_space: gym.spaces.Box = \
            gym.spaces.Box(0, 1,
                           (self.grid.grid_size, self.grid.grid_size,
                            self.grid.grid_size * self.grid.grid_size),
                            dtype=np.int16)

        self.steps: int = 0
        self.max_steps: int = 10000
        self.max_illegal_moves: int = 10
        self.num_illegal_moves: int = 0
        self.illegal_move_reward: float = 0.0
        self.reward_range: Tuple[float, float] =\
            (0.0, self.grid.grid_size * self.grid.grid_size)

    def get_info(self, info: Union[None, Dict[str, Union[int, bool, float]]] = None
                 ) -> Dict[str, Union[int, bool, float]]:
        """
        Returns current state of a environment in
        a dictionary format.

        Parameters
        ----------
        info: Union[None, Dict[str, Union[int, bool, float]]
            Current state of an environment which will
            be updated.
        Returns
        -------
        Dict[str, Union[int, bool, float]
            Updated state of an environment.
        """
        if not info:
            info = {}
        info['highest'] = np.max(self.grid.grid)
        info['score'] = self.grid.score
        info['steps'] = self.steps
        return info

    def step(self, action: str
             ) -> Tuple[Grid, float, bool,
                        Dict[str, Union[int, bool, float]]]:
        """
        Performs a move given by an action.

        Parameters
        ----------
        action: str
            One of four available moves.
        Returns
        -------
        Tuple[Grid, float, bool, dict]
            Tuple containing current state of game's grid,
            reward for a performed move, boolean which
            tells if game is over and dict containing
            updated information about game's state.
        """
        self.steps += 1
        reward: float = 0.0
        done: bool = False

        info: Dict[str, Union[bool, int, float]] = {
            'is_valid': True
        }
        is_valid: bool = self.grid.move(action)
        if is_valid:
            reward = float(self.grid.score)
            done = self.grid.is_win() or self.grid.is_lose()
        else:
            info['is_valid'] = False
            reward = self.illegal_move_reward
            self.num_illegal_moves += 1
            done = self.steps > self.max_steps or\
                self.num_illegal_moves > self.max_illegal_moves or\
                self.grid.is_win() or self.grid.is_lose()

        return self.grid, reward, done, info

    def reset(self) -> Tuple[Grid, float, bool,
                             Dict[str, Union[int, bool, float]]]:
        """
        Resets an environment to the begin state.

        Returns
        -------
        Tuple[Grid, float, bool, dict]
            Tuple containing initial state of game's grid,
            reward reward at the beginning of the game,
            boolean which tells if game is over
            and dict containing
            updated information about game's state.
        """
        self.grid.reset()
        self.grid.generate_twos(number_of_twos=2)
        self.steps = 0
        self.num_illegal_moves = 0

        return self.grid, 0.0, False, self.get_info()

    def render(self, mode: str = 'ascii') -> str:
        """
        Converts current state of environment to string.

        Parameters
        ----------
        mode: str, optional
            Current implementation only supports
            ascii format.
        Returns
        -------
        str
            Current grid, score and highest value in the grid
            converted to a string.
        """
        rendered_env: str = f"Score: {self.grid.score}\n"
        rendered_env += f"Highest: {np.max(self.grid.grid)}\n"
        rendered_env += f"{self.grid!s}\n\n"
        return rendered_env
