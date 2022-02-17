#!/usr/bin/python3
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
        if not self.elements[row][column].is_empty:
            print("The element <{},{}> already exists".format(row, column))
            return False
        # traverse in row
        # for i in range(9):
        #     if self.elements[i][column].value == number:
        #         print("{} at <{},{}> conflicts with <{},{}>".format(number,row,column,i,column))
        #         return False
        #     else:
        #         self.elements[i][column].impossible_values.add(number)
        # # traverse in column
        # for i in range(9):
        #     if self.elements[row][i].value == number:
        #         print("{} at <{},{}> conflicts with <{},{}>".format(number,row,column,row,i))
        #         return False
        #     else:
        #         self.elements[row][i].impossible_values.add(number)
        # # TODO: traverse in subgrid
        adjacent = self.get_adjacent_elements_coordinates(row, column)
        for r, c in adjacent:
            if self.elements[r][c].value == number:
                print("{} at <{},{}> conflicts with <{},{}>".format(number,row,column,r,c))
                return False
            else:
                self.elements[r][c].impossible_values.add(number)

        self.elements[row][column].change_element(number)
        return 1

    def get_adjacent_elements_coordinates(self, row, column):

        # res = set()
        # for i in range(9):
        #     pair = (i, column)
        #     res.add(pair)
        #     pair = (row, i)
        #     res.add(pair)
        # x = int(row / 3)
        # y = int(column / 3)
        # for i in range(9):
        #     pair = (x * 3 + int(i / 3), y * 3 + i % 3)
        #     res.add(pair)
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
                                self.fill(row, column, x)
                                print('Adding {} to {},{}'.format(x, row, column))
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
                                    self.fill(row, column, x)
                                    print('Adding {} to {},{}'.format(x, row, column))
                                    changes_made = True
                                    break
                                counter = 0
                                # traverse in column
                                for r, c in self.get_adjacent_in_column(row, column):
                                    if x in self.elements[r][c].impossible_values or\
                                            not self.elements[r][c].is_empty:
                                        counter += 1
                                if counter == 8:
                                    self.fill(row, column, x)
                                    print('Adding {} to {},{}'.format(x, row, column))
                                    changes_made = True
                                    break
                                counter = 0
                                # traverse in subgrid
                                for r, c in self.get_adjacent_in_subgrid(row, column):
                                    if x in self.elements[r][c].impossible_values or \
                                            not self.elements[r][c].is_empty:
                                        counter += 1
                                if counter == 8:
                                    self.fill(row, column, x)
                                    print('Adding {} to {},{}'.format(x, row, column))
                                    changes_made = True
                                    break


    def display(self):
        for row in self.elements:
            for el in row:
                if el.value == 0:
                    print('| ', end='')
                else:
                    print('|' + str(el), end='')
            print('|')
            


sudoku = Sudoku('input.txt')
sudoku.display()
sudoku.upgrade()
sudoku.display()

