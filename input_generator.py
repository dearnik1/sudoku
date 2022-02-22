# https://qqwing.com/generate.html


file = open("input_unsupported.txt", 'r')
Lines = file.readlines()
output_string = []
for line in Lines:
    output_string.append(f"|{'|'.join([c if c != '.' else ' ' for c in line.rstrip()])}|\n")
    # print(output_string)
with open("input_test.txt", 'w') as file:
    file.writelines(output_string)
