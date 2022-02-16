#!/usr/bin/python3
import sys
import os

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


    def fill(self, number):
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
        for i in range(9):
            if self.elements[i][column].value == number:
                print("{} at <{},{}> conflicts with <{},{}>".format(number,row,column,i,column))
                return False
            else:
                self.elements[i][column].impossible_values.add(number)
        # traverse in column
        for i in range(9):
            if self.elements[row][i].value == number:
                print("{} at <{},{}> conflicts with <{},{}>".format(number,row,column,row,i))
                return False
            else:
                self.elements[row][i].impossible_values.add(number)
        # TODO: traverse in subgrid

        self.elements[row][column].fill(number)

        return 1

    def display(self):
        for row in self.elements:
            for el in row:
                # if el.value == 0:
                print('|' + str(el), end='')
            print('|')
            


cwd = os.getcwd()
sudoku = Sudoku('input.txt')
sudoku.display()



