import numpy as np


class Grid:
    def __init__(self, *, grid_size: int = 4, max_tile: int = 2048) -> None:
        self.grid_size = grid_size
        self.max_tile = max_tile

        self.grid = np.zeros((grid_size, grid_size), dtype=np.int16)

    def move(self, direction: str) -> np.ndarray:
        if direction == 'w':
            return self.moveUp()
        elif direction == 's':
            return self.moveDown()
        elif direction == 'a':
            return self.moveLeft()
        elif direction == 'd':
            return self.moveRight()

    def get_status(self) -> str:
        if self.max_tile in self.grid:
            return "WIN"

        for i in range(4):
            for j in range(4):
                # is marge possible
                if j != 3 and self.grid[i, j] == self.grid[i, j + 1] or \
                   i != 3 and self.grid[i, j] == self.grid[i + 1, j]:
                    return "PLAY"

        if 0 not in self.grid:
            return "LOSE"
        else:
            return "PLAY"

    def generate_twos(self, iters: int = 1) -> None:
        for _ in range(iters):
            x, y = np.random.randint(0, len(self.grid), size=2)
            while self.grid[x, y] != 0:
                x, y = np.random.randint(0, len(self.grid), size=2)

            if self.grid.sum() in (0, 2):
                self.grid[x, y] = 2
            else:
                self.grid[x, y] = np.random.choice((2, 4))

    def moveLeft(self) -> None:
        self.shiftLeft()

        for i in range(4):
            for j in range(3):
                if self.grid[i, j] == self.grid[i, j + 1] and self.grid[i, j] != 0:
                    self.grid[i, j] *= 2
                    self.grid[i, j + 1] = 0
                    j = 0

        self.shiftLeft()

    def moveUp(self) -> None:
        self.rotateLeft()
        self.moveLeft()
        self.rotateRight()

    def moveRight(self) -> None:
        self.shiftRight()

        for i in range(4):
            for j in range(3, 0, -1):
                if self.grid[i, j] == self.grid[i, j - 1] and self.grid[i, j] != 0:
                    self.grid[i, j] *= 2
                    self.grid[i, j - 1] = 0
                    j = 0

    def moveDown(self) -> None:
        self.rotateLeft()
        self.moveLeft()
        self.shiftRight()
        self.rotateRight()

    def shiftLeft(self) -> None:
        for i in range(4):
            nums, count = [], 0
            for j in range(4):
                if self.grid[i, j] != 0:
                    nums.append(self.grid[i, j])
                    count += 1
            # nums.extend([0] * (4 - count))
            self.grid[i] = np.array(nums + ([0] * (4 - count)))

    def shiftRight(self) -> None:
        for i in range(4):
            nums, count = [], 0
            for j in range(4):
                if self.grid[i, j] != 0:
                    nums.append(self.grid[i, j])
                    count += 1

            self.grid[i] = np.array(([0] * (4 - count)) + nums)

    def rotateLeft(self) -> None:
        self.grid = np.rot90(self.grid)

    def rotateRight(self) -> None:
        self.grid = np.rot90(self.grid, k=3)

    def __str__(self) -> str:
        return str(self.grid)

    def __getitem__(self, item) -> np.int16:
        return self.grid[item[0], item[1]]


if __name__ == "__main__":
    grid = Grid()
    print(grid)
    print(str(grid[0, 2]))
