import copy
import numpy as np  # type: ignore
from multiprocessing import Pool
from typing import List, Callable

from utils.grid import Grid


def make_random_move(available_moves: List[Callable[[], bool]]) -> bool:
    """
    Given a list of possible grid moves randomly pick one and perform it.

    Parameters
    ----------
    available_moves: List[Callable[[], bool]]
        List of all the possible grid's moves.

    Returns
    -------
    bool
        True if performed move was valid.
    """
    return available_moves[np.random.randint(0, len(available_moves))]()


def get_moves_list(search_grid: Grid) -> List[Callable[[], bool]]:
    """
    Creates list of all the possible moves for a given grid.

    Parameters
    ----------
    search_grid: Grid
        Grid for which list of moves will be returned.

    Returns
    -------
    List[Callable[[], bool]]
        List of all the possible moves.
    """
    return list(search_grid.move_map.values())


class MonteCarloTreeSearch:
    """
    Class which performs Monte Carlo Tree Search for a given grid, which returns
    approximately best move for a given state of grid.

    Attributes
    ----------
    grid: Grid
        Grid for which search will be performed.
    searches_per_move: int
        Number of searches performed for each possible grid's move.
    number_of_moves: int
        Number of all possible moves.
    """
    def __init__(self, search_grid: 'Grid', *, searches_per_move: int = 25) -> None:
        """
        Parameters
        ----------
        grid: Grid
            Grid for which search will be performed.
        searches_per_move: int, optional
            Number of searches performed for each possible grid's move.
        """
        self.grid: Grid = search_grid
        self.searches_per_move: int = searches_per_move
        self.number_of_moves: int = 4

    def search_for_one_move(self, search_grid: Grid, move_index: int) -> int:
        """
        Performs search for a given number. 'searches_per_moves' iterations are performed
        and then all the acquired scores are summed.

        Parameters
        ----------
        search_grid: Grid
            Grid for which current search will be performed.
        move_index: int
            Index in a list of a first move in a search.

        Returns
        -------
        int
            Sum of scores in all simulated games.
        """
        search_score: int = 0
        search_moves: List[Callable[[], bool]] = get_moves_list(search_grid)

        is_valid: bool = search_moves[move_index]()

        if not is_valid:
            return 0

        search_grid.generate_twos(number_of_twos=1)
        current_grid: np.ndarray = np.copy(search_grid.grid)
        current_score: int = search_grid.score
        for later_move in range(self.searches_per_move):
            search_grid.grid = np.copy(current_grid)
            search_grid.score = current_score
            while not search_grid.is_win() and not search_grid.is_lose():
                is_valid = make_random_move(search_moves)
                if is_valid:
                    search_grid.generate_twos(number_of_twos=1)
            search_score += search_grid.score

        return search_score

    def __call__(self) -> int:
        """
        Execute search for each possible move. And then best move is selected.

        Returns
        -------
            Index of a move for which best score was returned.
        """
        print(self.grid)
        grids_lists = [copy.deepcopy(self.grid) for _ in range(self.number_of_moves)]
        #scores = []
        #for i in range(self.number_of_moves):
        #    scores.append(self.search_for_one_move(grids_lists[i], i))
        with Pool(processes=self.number_of_moves) as pool:
            scores = pool.starmap(self.search_for_one_move, zip(grids_lists, range(self.number_of_moves)))
        """
        t = []
        for i in range(self.number_of_moves):
            t.append(ThreadWithReturnValue(target=self.search_for_one_move, args=(grids_lists[i], i)))
            t[i].start()
        scores = []
        for th in t:
            scores.append(th.join())
        """

        return np.argmax(scores)


if __name__ == "__main__":
    grid = Grid()
    grid.generate_twos(number_of_twos=2)
    mcts = MonteCarloTreeSearch(grid, searches_per_move=25)
    all_moves = list(grid.move_map.values())
    while True:
        next_move = mcts()
        all_moves[next_move]()
        if grid.is_win():
            print('win')
            break
        if grid.is_lose():
            print('lost')
            break
        grid.generate_twos(number_of_twos=1)
        print(grid)

    print(grid)
