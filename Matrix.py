'''A = [
    [2, 3, 24, 30],
    [8, 9, 10, 45],
    [5, 88, 90, 112]
]
Given is the 3/ 4 matrix use 2d list to represent the matrix  in a python script.The n find out the elements of the matrix which are divisible by 2 and 3 also find out the max and min  elements of the matrix '''

A =[[2, 3, 24, 30], [8, 9, 10, 45], [5, 88, 90, 112]]
divisible_by_2_and_3 = []
max_element = A[0][0]
min_element = A[0][0]
for row in A:
    for element in row:
        if element % 2 == 0 and element % 3 == 0:
            divisible_by_2_and_3.append(element)
        if element > max_element:
            max_element = element
        if element < min_element:
            min_element = element
print("Elements divisible by 2 and 3:",divisible_by_2_and_3)
print("Maximum element present  in the matrix:", max_element)
print("Minimum element present in the matrix:", min_element)
