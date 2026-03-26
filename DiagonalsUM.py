'''
Write a progarm  to store the values of the  matrix  given below in a 2d list . Then, calculate the sum of the diagonal  elements , the sum of all elements  above the diagonal  and the sum of all the elements below the diagonal .Also find out the Max and min elemnts from the matrix .
A=[1 2 3
  8 9 4
  7 6 5
]

B = [2 7 6
     9 5 1
     4 3 8]
'''
A = [
    [1, 2, 3],
    [8, 9, 4],
    [7, 6, 5]
]

B = [
    [2, 7, 6],
    [9, 5, 1],
    [4, 3, 8]
]

# A stats
n = len(A)
diag_sum_A = 0
above_sum_A = 0
below_sum_A = 0
max_A = A[0][0]
min_A = A[0][0]

for i in range(n):
    for j in range(n):
        v = A[i][j]
        if i == j:
            diag_sum_A += v
        elif i < j:
            above_sum_A += v
        else:
            below_sum_A += v
        if v > max_A:
            max_A = v
        if v < min_A:
            min_A = v

print("--- Matrix A ---")
print("Diagonal sum:", diag_sum_A)
print("Above diagonal sum:", above_sum_A)
print("Below diagonal sum:", below_sum_A)
print("Max:", max_A)
print("Min:", min_A)

# B stats
n = len(B)
diag_sum_B = 0
above_sum_B = 0
below_sum_B = 0
max_B = B[0][0]
min_B = B[0][0]

for i in range(n):
    for j in range(n):
        v = B[i][j]
        if i == j:
            diag_sum_B += v
        elif i < j:
            above_sum_B += v
        else:
            below_sum_B += v
        if v > max_B:
            max_B = v
        if v < min_B:
            min_B = v

print("--- Matrix B ---")
print("Diagonal sum:", diag_sum_B)
print("Above diagonal sum:", above_sum_B)
print("Below diagonal sum:", below_sum_B)
print("Max:", max_B)
print("Min:", min_B)