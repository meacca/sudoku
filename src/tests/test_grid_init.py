import unittest
import numpy as np
from src.sudoku_grid import SudokuGrid


class TestGridInit(unittest.TestCase):
    def setUp(self) -> None:
        self.sudoku = SudokuGrid(size=2)

    def test_00_check_grid_correctness_1(self):
        self.sudoku.grid = np.array([[3, 4, 1, 2], [2, 1, 4, 3], [1, 3, 2, 4], [4, 2, 3, 1]])
        self.assertTrue(self.sudoku.check_grid_correctness())

    def test_01_check_grid_correctness_2(self):
        self.sudoku.grid = np.array([[3, 4, 1, 2], [2, 3, 4, 1], [4, 1, 2, 3], [1, 2, 3, 4]])
        self.assertFalse(self.sudoku.check_grid_correctness())

    def test_02_base_array_correctness(self):
        self.sudoku._SudokuGrid__generate_base_array()
        self.assertTrue(self.sudoku.check_grid_correctness())

    def test_03_random_rows_swap_check_correctness(self):
        self.sudoku._SudokuGrid__generate_base_array()
        correct = True
        for i in range(100):
            self.sudoku._SudokuGrid__random_rows_swap()
            correct = correct and self.sudoku.check_grid_correctness()
        self.assertTrue(correct)

    def test_04_random_columns_swap_check_correctness(self):
        self.sudoku._SudokuGrid__generate_base_array()
        correct = True
        for i in range(100):
            self.sudoku._SudokuGrid__random_columns_swap()
            correct = correct and self.sudoku.check_grid_correctness()
        self.assertTrue(correct)

    def test_05_random_square_rows_swap_check_correctness(self):
        self.sudoku._SudokuGrid__generate_base_array()
        correct = True
        for i in range(100):
            self.sudoku._SudokuGrid__random_square_rows_swap()
            correct = correct and self.sudoku.check_grid_correctness()
        self.assertTrue(correct)

    def test_06_random_square_columns_swap_check_correctness(self):
        self.sudoku._SudokuGrid__generate_base_array()
        correct = True
        for i in range(100):
            self.sudoku._SudokuGrid__random_square_columns_swap()
            correct = correct and self.sudoku.check_grid_correctness()
        self.assertTrue(correct)

    def test_07_transposing_check_correctness(self):
        self.sudoku._SudokuGrid__generate_base_array()
        correct = True
        for i in range(100):
            self.sudoku._SudokuGrid__transposing()
            correct = correct and self.sudoku.check_grid_correctness()
        self.assertTrue(correct)

    def test_08_invariant_changing_check_correctness(self):
        self.sudoku._SudokuGrid__generate_base_array()
        correct = True
        for i in range(100):
            self.sudoku._SudokuGrid__invariant_changing(n=100)
            correct = correct and self.sudoku.check_grid_correctness()
        self.assertTrue(correct)


if __name__ == "__main__":
    unittest.main()
