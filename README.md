# sudoku

(i) For Element class:
__init__ - the constructor.
__str__ and __repr__ are for printing Element as an object. print will not give an error, but will print the value of element instead.
change_element sets the value of element to a specific number. is_empy property is also checked.
impossible_values would help us to solve the sudoku
For Sudoku Class:
__init__ - the constructor that reads the data from input file. our Sudoku will be a 9x9 matrix made of Elements from the class above. 
fill() - tries to fill a square with a specific value and checks if it made any errors on the way. The adjacent elements have added that value to their impossible_values set.
get_adjacent_elements_coordinates - returns a set of coordinates for adjacent elements - all elements in the same row / same column / same subgrid. 21 elements in total from the given point.
get_adjacent_in_row, get_adjacent_in_column, get_adjacent_in_subgrid are helper functions for the get_adjacent_elements_coordinates
upgrade() - a function that traverses each square and checks if it can fit any number in there with 100% accuracy. For example, when there are 8 impossible_values - that means only 1 remains possible. Or if adjacent elements cannot have this value, that means it only fits here. If filled successfully, traverse again because it could add another value after the change.
guess() - see below
display() - the output function. shows the sudoku in console
(ii) consistency check is implemented inside the fill() function. When filling a certain square, it performs a check if any adjacent elements contain the same number, or if any empty squares have no possible numbers inside. 
(iii) guess() is a recursive function for the backtrack search. when there is no obvious solutions, this function takes a guess at a specific empty square, making a copy of Sudoku object and continue working with that object until done or there is a conflict. If an error is detected, that means our guess was wrong. We revert to original object, guess differently and continue until finished. 


