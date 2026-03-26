'''Write a program that creates a 2D list having m number of rows and n number of columns.
# All elements in the diagonal should be 0, the elements above the diagonal should be 1, and the elements below the diagonal should be -1.
# Values for m and n should be taken from the user.
011
10-1
-1-10'''
# Taking input from the user
m = int(input("Enter the number of rows (m): "))
n = int(input("Enter the number of columns (n): "))

# Initialize the 2D list
matrix = []
for i in range(m):
    row = []
    for j in range(n):
        if i == j:
            row.append(0)
        elif i < j:
            row.append(1)
        else:
            row.append(-1)
    matrix.append(row)

# Print the matrix
for row in matrix:
    print(' '.join(map(str, row)))

