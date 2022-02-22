#!/usr/bin/python3
import sys
import itertools
import copy

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
    # the domain [1..9]
    _ALL_VALUES = set(range(1, 10))

    # the constructor
    def __init__(self, file_name):
        self.size = 0   # How many elements completed. Should be 81 to finish the sudoku
        self.elements = [[Element() for i in range(9)] for j in range(9)]     # initiate the 2D array
        file = open(file_name, 'r')
        Lines = file.readlines()
        # start with -1 because first '|' does not count
        row = -1
        # read the imput from a file
        for line in Lines:
            row += 1
            column = -1
            # looks weird but it works both with spaces and without
            for character in line:
                if character == '|':
                    column += 1   # go to the next column
                elif character.isnumeric():
                    self.fill(row, column, int(character))
                
    # try to fill the number at a certain row and column
    # returns false if errors occured, true if filled successfully
    def fill(self, row, column, number):
        self.size += 1
        if not self.elements[row][column].is_empty:
            print("The element <{},{}> already exists".format(row, column))
            return False
        adjacent = self.get_adjacent_elements_coordinates(row, column)
        adjacent.remove((row, column))
        for r, c in adjacent:
            el = self.elements[r][c]
            if el.value == number:
                print("{} at <{},{}> conflicts with <{},{}>".format(number,row,column,r,c))
                return False
            else:
                el.impossible_values.add(number)
                if el.is_empty and len(el.impossible_values) >= 9:
                    print("no possible values at <{},{}>".format(r, c))
                    return False
        # print('Adding {} to [{},{}]'.format(number, row, column))
        return self.elements[row][column].change_element(number)

    # returns a set of pairs of coordinates for adjacent elements for the given position
    # adjacent are those who are in the same row or column or the subgrid
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
        #letsgomath
        for i in range(9):
            pair = (x * 3 + int(i / 3), y * 3 + i % 3)
            res.add(pair)
        return res

    # fill out the most obvious elements with 100% accuracy
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
            return False        # mistakes found
        elif self.size == 81:
            self.display()
            return True     # done
        else:
            desired_number_of_impossible_values = 7
            while desired_number_of_impossible_values:
                for i in range(9):
                    for j in range(9):
                        el = self.elements[i][j]
                        if el.is_empty and len(el.impossible_values) >= desired_number_of_impossible_values:
                            possible_values = self._ALL_VALUES - el.impossible_values
                            for value in possible_values:
                                # make a copy of sudoku
                                new_sudoku = copy.deepcopy(self)
                                # print(f'Guessing {value} at [{i},{j}]')
                                new_sudoku.fill(i, j, value)
                                if new_sudoku.guess():
                                    return True
                                del new_sudoku
                            return False
                # if we are here that means there are no elements with 2 possible values
                # search for elements with 3 possible solutions...
                desired_number_of_impossible_values -= 1
        return False


    # print the sudoku in console and in a file
    def display(self):
        with open("solution2.txt", 'w') as file:
            output_string = ''
            for row in self.elements:
                for el in row:
                    if el.value == 0:
                        output_string += '| '
                        print('| ', end='')
                    else:
                        output_string += '|' + str(el)

                        print('|' + str(el), end='')
                output_string += '|\n'
                print('|')
                file.write(output_string)
                output_string = ''


if __name__ == '__main__':
    sudoku = Sudoku('input.txt')
    sudoku.guess()


