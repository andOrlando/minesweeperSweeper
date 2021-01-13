import unittest
from matrix_solver import MatrixSolver


class MatrixTest(unittest.TestCase):
    def test_basic_matrix(self):
        matrix = [[9, 9, 9, 9, 9, 9, 9],
                  [1, 2, 3, 4, 9, 9, 9],
                  [0, 0, 0, 1, 3, 9, 9],
                  [0, 0, 0, 0, 2, 9, 9],
                  [1, 1, 1, 2, 3, 9, 9],
                  [9, 9, 9, 9, 9, 9, 9]]
        self.assertEqual(MatrixSolver(matrix, debug=True).get_command(), "A1")


if __name__ == '__main__':
    unittest.main()
