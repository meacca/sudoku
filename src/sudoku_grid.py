import numpy as np


class SudokuGrid:
    def __init__(self, size: int = 3):
        self.size = size
        self.grid = np.zeros((self.size * self.size, self.size * self.size), dtype=np.int32)

    def check_grid_correctness(self) -> bool:
        standard = np.arange(1, len(self.grid) + 1)
        equal = True
        # check row/column correctness
        for i in range(len(self.grid)):
            # check i-th row
            equal = equal and all(np.sort(self.grid[i]) == standard)
            # check i-th column
            equal = equal and all(np.sort(self.grid[:, i]) == standard)
        # check squares correctness
        for i in range(self.size):
            for j in range(self.size):
                square = self.grid[i * self.size:(i + 1) * self.size, j * self.size:(j + 1) * self.size]
                equal = equal and all(np.sort(square.ravel()) == standard)
        return equal

    def __generate_base_array(self):
        for i in range(self.size):
            base_row = np.roll(np.arange(1, len(self.grid) + 1), shift=-i)
            for j in range(self.size):
                new_row = np.roll(base_row, shift=-j * self.size)
                row_number = i * self.size + j
                self.grid[row_number] = new_row

    def __swap_rows(self, row_1, row_2):
        self.grid[[row_1, row_2]] = self.grid[[row_2, row_1]]

    def __random_rows_swap(self):
        # calculating numbers of changing rows
        row_square = np.random.randint(0, self.size)
        row_1, row_2 = np.random.choice(np.arange(self.size), 2, replace=False)
        row_1 = self.size * row_square + row_1
        row_2 = self.size * row_square + row_2
        self.__swap_rows(row_1, row_2)

    def __random_columns_swap(self):
        self.__transposing()
        self.__random_rows_swap()
        self.__transposing()

    def __random_square_rows_swap(self):
        row_square_1, row_square_2 = np.random.choice(np.arange(self.size), 2, replace=False)
        for i in range(self.size):
            row_1 = self.size * row_square_1 + i
            row_2 = self.size * row_square_2 + i
            self.__swap_rows(row_1, row_2)

    def __random_square_columns_swap(self):
        self.__transposing()
        self.__random_square_rows_swap()
        self.__transposing()

    def __transposing(self):
        self.grid = self.grid.T

    def __invariant_changing(self, n: int = 20):
        change_functions = [self.__random_rows_swap,
                            self.__random_columns_swap,
                            self.__random_square_rows_swap,
                            self.__random_square_columns_swap,
                            self.__transposing]
        for func_number in np.random.choice(np.arange(5), n):
            change_functions[func_number]()

    def generate_true_grid(self):
        self.__generate_base_array()
        self.__invariant_changing()

    def init_game(self):
        self.generate_true_grid()
