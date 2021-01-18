class MonteCarloTreeSearch:
    def __init__(self, grid: 'Grid', searches_per_move, search_length) -> None:
        self.grid: 'Grid' = grid
        self.searches_per_move: int = searches_per_move
        self.search_length: int = search_length

    def __call__(self):
        all_moves = list(self.grid.move_map.values())
        for first_index in range(len(all_moves)):
            pass

