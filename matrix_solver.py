"""
0-8 = normal numbers
9 = unknown
10 = bomb
"""
from math import floor
from constants import *
from random import choice

letters = ["A", "B", "C", "D", "E", "F", "G", "H"]


class MatrixSolver:

    def __init__(self, matrix):
        self.matrix = matrix
        self.col_length = len(matrix)
        self.row_length = len(matrix[0])
        self.probabilities = []

    def get_command(self):
        result = self.solve()
        return f"{result[2] if len(result) == 3 else ''}{letters[result[0]]}{result[1] + 1}" if not result is None else None

    # returns x, y and whether it's a chance or not
    def solve(self):
        # if first move, choose the middle
        if self.count_all_of(BLANK_TILE) == self.col_length * self.row_length:
            return floor((len(self.x(0))) / 2), floor((len(self.y(0))) / 2)

        # finds bombs from numbers
        for y in range(len(self.matrix)):
            for x in range(len(self.matrix[y])):
                if self.matrix[y][x] in range(1, 9):

                    # Safe values around the number
                    safe = [False, False, False, False, False, False, False, False]

                    # checks if it's in the far corners anywhere
                    if x == 0:
                        safe[0], safe[3], safe[5] = [True for _ in range(3)]
                    elif x == self.row_length - 1:
                        safe[2], safe[4], safe[7] = [True for _ in range(3)]
                    if y == 0:
                        safe[0], safe[1], safe[2] = [True for _ in range(3)]
                    elif y == self.col_length - 1:
                        safe[5], safe[6], safe[7] = [True for _ in range(3)]

                    # checks for other blank spaces
                    for i in range(8):
                        if not safe[i]:
                            # get the coord increments
                            new_x, new_y = self.generate_new_coords(i)

                            # if it's <= 8 it's a tile from 0-8
                            if self.coords(x + new_x, y + new_y) <= 8:
                                safe[i] = True

                    # converts any unknown spaces into bombs if it can
                    if safe.count(False) <= self.matrix[y][x]:
                        for i in range(8):
                            if not safe[i]:
                                # get the coord increments
                                new_x, new_y = self.generate_new_coords(i)

                                # changes unknown to bomb
                                if self.coords(x + new_x, y + new_y) == BLANK_TILE:
                                    self.matrix[y + new_y][x + new_x] = BOMB

                    # now that it knows bombs in the area, gives a move that would convert unknown into known if it can
                    if self.count_in_radius(x, y, [BOMB]) == self.matrix[y][x]:
                        for i in range(8):
                            # get the coord increments
                            new_x, new_y = self.generate_new_coords(i)

                            if x + new_x in range(0, self.row_length) \
                                    and y + new_y in range(0, self.col_length) \
                                    and self.coords(x + new_x, y + new_y) == BLANK_TILE:
                                return x + new_x, y + new_y

                    # gets bomb count and available count for probabilities
                    bomb_count = self.count_in_radius(x, y, [BOMB])
                    available_count = self.count_in_radius(x, y, [BLANK_TILE])
                    # adds probabilities to the list if it can't do anything else
                    for i in range(8):
                        # get the coord increments
                        new_x, new_y = self.generate_new_coords(i)
                        if x + new_x in range(0, self.row_length) \
                                and y + new_y in range(0, self.col_length) \
                                and self.coords(x + new_x, y + new_y) == BLANK_TILE:

                            denominator = available_count - bomb_count if available_count != bomb_count else 1
                            probability_tuple = ((self.matrix[y][x] - bomb_count) / denominator, x + new_x, y + new_y)
                            others = list(filter(
                                lambda item: probability_tuple[1] == item[1] and probability_tuple[2] == item[2],
                                self.probabilities
                            ))

                            # if there's already the same coords in there, use the highest probability.
                            if len(others) != 0:
                                if others[0][0] <= probability_tuple[0]:
                                    self.probabilities[self.probabilities.index(others[0])] = probability_tuple
                            else:
                                self.probabilities.append(probability_tuple)

        if len(self.probabilities) != 0:
            min_probability = min(map(lambda item: item[0], self.probabilities))
            final = choice(list(filter(lambda prob: prob[0] == min_probability, self.probabilities)))
            return final[1], final[2], f"{int(min_probability * 100)}% chance of bomb: "
        return None

    # counts total values
    def count_all_of(self, number):
        result = 0
        for i in self.matrix:
            for j in i:
                if j == number:
                    result += 1
        return result

    # gets column list at index
    def y(self, index):
        result = []
        for i in self.matrix:
            result.append(i[index])
        return result

    # gets row list at index
    def x(self, index):
        return self.matrix[index]

    # gets the value at the coords
    def coords(self, x, y):
        return self.matrix[y][x]

    # gets the coords from row and item
    # 0 is x, 1 is y
    def get_coords(self, row, item):
        row_index = self.matrix.index(row)
        return row.index(item), row_index

    def count_in_radius(self, x, y, accepted):
        result = 0
        for i in range(8):
            new_x, new_y = self.generate_new_coords(i)
            # try/excepts in case it picks something that's out of bounds
            try:
                if self.coords(x + new_x, y + new_y) in accepted:
                    result += 1
            except IndexError:
                pass
        return result

    # generates x and y increments
    @staticmethod
    def generate_new_coords(i):
        return i % 3 - 1 if i < 4 else (i + 1) % 3 - 1, min(floor(max(0, i - 1) / 2) - 1, 1)
