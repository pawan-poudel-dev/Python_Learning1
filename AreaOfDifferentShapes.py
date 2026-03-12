
# The program calculates the area of a circle and a rectangle based on user input for the radius, length, and width. It then sums the areas to display the total area formatted to two decimal places.
import math 
# Take input for circle radius
radius = float(input("Enter the radius of the circle: "))
# Take input for rectangle length and width
length = float(input("Enter the length of the rectangle: "))
width = float(input("Enter the width of the rectangle: "))
# Calculate area of the circle
area_circle = math.pi * radius ** 2
# Calculate area of the rectangle
area_rectangle = length * width
# Calculate total area
total_area = area_circle + area_rectangle
# Display the areas
print(f"Area of Circle: {area_circle:.2f}")
print(f"Area of Rectangle: {area_rectangle:.2f}")
print(f"Total Area: {total_area:.2f}")