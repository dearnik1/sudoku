#!/usr/bin/python3
import copy

import sys
import itertools

class Element:
    def __init__(self):
        self.value = 0
        self.is_empty = True
        self.impossible_values = set()

    # print(element) would print its value
    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)


    def change_element(self, number):
        if not self.is_empty:
            return False
        self.value = number
        self.is_empty = False
        return True


class Sudoku:
    def __init__(self, file_name):
        self.size = 0   # How many elements completed. Should be 81 to finish the sudoku
        self.elements = [[Element() for i in range(9)] for j in range(9)]     # initiate the 2D array
        file = open(file_name, 'r')
        Lines = file.readlines()
        row = -1
        for line in Lines:
            row += 1
            column = -1
            for character in line:
                if character == '|':
                    column+=1   # go to the next column
                elif character.isnumeric():
                    self.fill(row, column, int(character))
                

    def fill(self, row, column, number):
        self.size += 1
        if not self.elements[row][column].is_empty:
            print("The element <{},{}> already exists".format(row, column))
            return False
        adjacent = self.get_adjacent_elements_coordinates(row, column)
        for r, c in adjacent:
            if self.elements[r][c].value == number:
                print("{} at <{},{}> conflicts with <{},{}>".format(number,row,column,r,c))
                return False
            else:
                self.elements[r][c].impossible_values.add(number)
        print('Adding {} to [{},{}]'.format(number, row, column))
        return self.elements[row][column].change_element(number)

    def get_adjacent_elements_coordinates(self, row, column):
        res = set()
        res.update(self.get_adjacent_in_column(row, column))
        res.update(self.get_adjacent_in_row(row, column))
        res.update(self.get_adjacent_in_subgrid(row, column))
        return res

    def get_adjacent_in_row(self, row, column):
        res = set()
        for i in range(9):
            pair = (row, i)
            res.add(pair)
        return res

    def get_adjacent_in_column(self, row, column):

        res = set()
        for i in range(9):
            pair = (i, column)
            res.add(pair)
        return res

    def get_adjacent_in_subgrid(self, row, column):
        x = int(row / 3)
        y = int(column / 3)
        res = set()
        for i in range(9):
            pair = (x * 3 + int(i / 3), y * 3 + i % 3)
            res.add(pair)
        return res

    # fill out the most obvious elements
    def upgrade(self):
        changes_made = True
        while changes_made:
            changes_made = False
            # fill elements that have the only 1 possible value remaining
            for row in range(9):
                for column in range(9):
                    el = self.elements[row][column]
                    if el.is_empty and len(el.impossible_values) == 8:
                        changes_made = True
                        for x in range(1, 10):
                            if x not in el.impossible_values:
                                if not self.fill(row, column, x):
                                    return False
                                break
            # fill elements that can have a number that adjacent elements cannot...
            for row in range(9):
                for column in range(9):
                    el = self.elements[row][column]
                    if el.is_empty:
                        for x in range(1, 10):
                            if x not in el.impossible_values:
                                # for each possible value check if it is impossible in adjacent elements:
                                counter = 0
                                # traverse in row
                                for r,c in self.get_adjacent_in_row(row, column):
                                    if x in self.elements[r][c].impossible_values or \
                                            not self.elements[r][c].is_empty:
                                        counter += 1
                                if counter == 8:
                                    if not self.fill(row, column, x):
                                        return False
                                    changes_made = True
                                    break
                                counter = 0
                                # traverse in column
                                for r, c in self.get_adjacent_in_column(row, column):
                                    if x in self.elements[r][c].impossible_values or\
                                            not self.elements[r][c].is_empty:
                                        counter += 1
                                if counter == 8:
                                    if not self.fill(row, column, x):
                                        return False
                                    changes_made = True
                                    break
                                counter = 0
                                # traverse in subgrid
                                for r, c in self.get_adjacent_in_subgrid(row, column):
                                    if x in self.elements[r][c].impossible_values or \
                                            not self.elements[r][c].is_empty:
                                        counter += 1
                                if counter == 8:
                                    if not self.fill(row, column, x):
                                        return False
                                    changes_made = True
                                    break
        return True

    # when stuck, just pick a random digit and check if it works
    def guess(self):
        if not self.upgrade():
            return False        # mistake found
        if self.size == 81:
            return True     # done
        else:
            print('Guessing...')
            print(self.elements[0][5].impossible_values)
            # make a copy of sudoku
            # fill 1 random element
            # call guess()
            # if false - try another element


    def display(self):
        for row in self.elements:
            for el in row:
                if el.value == 0:
                    print('| ', end='')
                else:
                    print('|' + str(el), end='')
            print('|')


class Sudoku2:
    _ALL_VALUES = set(range(1, 10))

    def __init__(self, file_name):
        self.grid = self._read_sudoku_from_file(file_name)

    def display(self):
        for row in self.grid:
            row_str = '|'.join([str(v) if v != 0 else ' '
                                for v in row])
            print(f"|{row_str}|")
        print('-' * 20)

    @staticmethod
    def _read_sudoku_from_file(file_name):
        with open(file_name, 'r') as file:
            rows = []
            for line in file.readlines():
                # trim extra elements because of leading and trailing seperator
                line = line.split('|')[1:-1]
                row = [int(value) if value.isdigit() else 0
                       for value in line]
                rows.append(row)
            return rows

    def solve(self):
        counter = 1000
        while counter and not self._solved:
            self._try_to_solve()
            counter -= 1

        if self._solved:
            print("Finally, solved!")
        else:
            print("I'm stupid, sorry :(")

        self.display()

    def _try_to_solve(self):
        if not self.update_values_for_obvious_cases():
            if not self.update_values_for_50_percent_cases():
                return
                # if not self.update_values_for_33_percent_cases():
                #     break

    def update_values_for_obvious_cases(self):
        updated = False
        for i, row in enumerate(self.grid):
            for j, value in enumerate(row):
                if value == 0:
                    row_values = self._get_row_values(i)
                    col_values = self._get_col_values(j)
                    subgrid_values = self._get_subgrid_values(i, j)
                    existing_values = row_values | col_values | subgrid_values
                    existing_values.remove(0)

                    if len(existing_values) == 8:
                        new_value = (self._ALL_VALUES - existing_values).pop()
                        self.grid[i][j] = new_value
                        print(f"Uhhu, value at [{i}][{j}] updated to {new_value}")
                        updated = True
        return updated

    def update_values_for_50_percent_cases(self):
        for i, row in enumerate(self.grid):
            for j, value in enumerate(row):
                if value == 0:
                    row_values = self._get_row_values(i)
                    col_values = self._get_col_values(j)
                    subgrid_values = self._get_subgrid_values(i, j)
                    existing_values = row_values | col_values | subgrid_values
                    existing_values.remove(0)

                    if len(existing_values) == 7:
                        left_value, right_value = (self._ALL_VALUES - existing_values)
                        data = {
                            'left_value': left_value,
                            'right_value': right_value
                        }
                        grid_temp = copy.deepcopy(self.grid)
                        self.grid[i][j] = left_value
                        self._try_to_solve()

                        if not self._solved:
                            self.grid = grid_temp
                            self.grid[i][j] = right_value
                            self._try_to_solve()

                        if not self._solved:
                            self.grid = grid_temp
        return self._solved

    @property
    def _solved(self):
        for row in self.grid:
            for value in row:
                if not value:
                    return False
        return True

    def _get_row_values(self, row_index):
        return set(self.grid[row_index])

    def _get_col_values(self, col_index):
        result = set()
        for row in self.grid:
            result.add(row[col_index])
        return result

    def _get_subgrid_values(self, row_index, col_index):
        result = set()
        for i in self._get_index_range_for_subgrid(row_index):
            for j in self._get_index_range_for_subgrid(col_index):
                result.add(self.grid[i][j])
        return result

    @staticmethod
    def _get_index_range_for_subgrid(index):
        return [i + index - index % 3 for i in range(3)]


if __name__ == '__main__':
    sudoku = Sudoku('input.txt')
    # sudoku = Sudoku('input_hard.txt')
    # sudoku.display()
    # sudoku.guess()
    # sudoku.display()

    sudoku2 = Sudoku2('input.txt')
    sudoku2.display()
    sudoku2.solve()


