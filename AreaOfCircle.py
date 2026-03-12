#This program will calculate the area of a circle based on user input for the radius.
import math
#This program will calculate the area of a circle based on user input for the radius.
radius = float(input("Enter the radius of the circle: "))
#calculating the area of the circle using the formula A = πr^2 and printing the result to the user
area = math.pi * radius**2
#printing the area of the circle to the user
print("The area of the circle is: ", area)
