# Write a program that creates a 2D list having m number of rows and n number of columns.
# All elements in the diagonal should be 1, the elements above the diagonal should be 2, and the elements below the diagonal should be 3.
# Values for m and n should be taken from the user.
# Example for 3x3:
# 1 2 2
# 3 1 2
# 3 3 1

# Taking input from the user
m = int(input("Enter the number of rows (m): "))
n = int(input("Enter the number of columns (n): "))

# Initialize the 2D list
matrix = []

for i in range(m):
    row = []
    for j in range(n):
        if i == j:
            row.append(1)
        elif i < j:
            row.append(2)
        else:
            row.append(3)
    matrix.append(row)

# Print the matrix
for row in matrix:
    print(' '.join(map(str, row)))


