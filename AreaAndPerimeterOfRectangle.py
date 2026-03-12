# This program calculates the area and perimeter of a rectangle based on user input for length and width.
length = int(input("enter the length of the rectangle:"))
width = int(input("enter the width of the rectangle:"))
# The area is calculated by multiplying the length and width together.
area = length * width
# The perimeter is calculated by adding the length and width together and then multiplying by 2.
perimeter = 2 * (length + width)
# Finally, the program prints the results to the user.
print("the area of the rectangle is:", area)
#calculate the perimeter of a rectangle using the formula 2(l+b)
print("the perimeter of the rectangle is:", perimeter)