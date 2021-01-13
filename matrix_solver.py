"""
0-8 = normal numbers
9 = unknown
10 = bomb

What does it do?
-gets every space that borders anything 0-8
-creates all possible permutations of bombs or not
-checks through every possibility to see if they're valid using logic

"""
from math import floor
from constants import *
from itertools import product
from emoji_to_matrix import matrix_to_pretty

letters = ["A", "B", "C", "D", "E", "F", "G", "H"]


class MatrixSolver:

    def __init__(self, matrix, debug = False):
        self.matrix = matrix
        self.col_length = len(matrix)
        self.row_length = len(matrix[0])
        self.debug = debug
        self.coords = product(range(self.row_length), range(self.col_length))

    def get_command(self):
        result = self.solve()
        if not result is None: return f"{result[2]}{letters[result[0]]}{result[1] + 1}"
        return None

    # returns x, y, string
    def solve(self):

        # gets every blank tile adjacent to a numbered tile and every numbered tile
        blank_tiles = []
        numbered_tiles = []
        for x, y in self.coords:

            if self.matrix[y][x] == BLANK_TILE:
                if self.count_in_radius(self.matrix, x, y, 1, 2, 3, 4, 5, 6, 7, 8) > 0:
                    blank_tiles.append((x, y))

            elif self.matrix[y][x] in range(1, 9):
                numbered_tiles.append((x, y))


        if self.debug: print(f"blank tiles: {str(blank_tiles)[1:len(str(blank_tiles))-1]}\n"
              f"tiles: {str(numbered_tiles)[1:len(str(numbered_tiles))-1]}")


        # creates every possible mine value for the length of spaces given
        values = list(product((True, False), repeat=len(blank_tiles)))
        value_lengths = len(blank_tiles)

        # this is the total number of spaces for probabilities
        total = 0
        # this is the spaces and totals for each space
        # spaces_and_totals = [[(tup[0], tup[1]), 0] for tup in blank_tiles]
        totals = [0 for _ in range(value_lengths)]

        for value in values:

            # creates and fills the pseudo_matrix assuming what's dictated as bombs are bombs
            temp_matrix = self.matrix
            for i, (x, y) in enumerate(blank_tiles):
                if value[i]: temp_matrix[y][x] = BOMB
                else: temp_matrix[y][x] = BLANK_TILE

            # checks every numbered tile for incorrectness
            invalid = False
            for x, y in numbered_tiles:
                if self.count_in_radius(temp_matrix, x, y, BOMB) != self.matrix[y][x]:
                    invalid = True
                    break

            # if it's not incorrect adds to totals
            if not invalid:
                total += 1
                for i in range(value_lengths):
                    # spaces_and_totals[i][1] += 1 if value[i] else 0
                    if value[i]: totals[i] += 1
                    if self.debug: matrix_to_pretty(temp_matrix)

        # prints the thing if it's debugging
        if self.debug: print(f"totals: {str(totals)[1:len(str(totals))-1]}\n\n")

        # gets all items that are min
        probabilities = [i/total for i in totals]
        items = list(filter(
            lambda j: j[2] == min(probabilities),
            [(x, y, probabilities[i]) for i, x, y in enumerate(blank_tiles)]
        ))

        # returns the smallest value and also the chance if it's not 0
        if len(items) == 0:
            return int(self.row_length / 2), int(self.col_length / 2), ""
        return items[0][0], items[0][1], f"{items[0][2]*100}% confident: " if items[0][2] != 0 else ""




    def count_in_radius(self, matrix, x, y, *accepted):
        result = 0
        for i in range(8):
            new_x, new_y = self.generate_new_coords(i)
            # if anything is out of bounds, ignores it
            if len(matrix) > y + new_y >= 0 and len(matrix[0]) > x + new_x >= 0:
                if matrix[y + new_y][x + new_x] in accepted:
                    result += 1

        return result

    @staticmethod
    def generate_new_coords(i):
        return i % 3 - 1 if i < 4 else (i + 1) % 3 - 1, min(floor(max(0, i - 1) / 2) - 1, 1)
