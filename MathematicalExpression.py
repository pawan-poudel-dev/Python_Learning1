# This program calculates the result of the expression (a + b)² + (b + c)² + (c + d)² + (a + d)²
# Input for four numbers
a = float(input("Enter the first number (a): "))
b = float(input("Enter the second number (b): "))
c = float(input("Enter the third number (c): "))
d = float(input("Enter the fourth number (d): "))
# Calculate the result of the expression
result = (a + b)**2 + (b + c)**2 + (c + d)**2 + (a + d)**2
# Calculate the average of the four numbers
average = (a + b + c + d) / 4
# Display the results
print(f"The result of the expression (a + b)² + (b + c)² + (c + d)² + (a + d)² is: {result:.2f}")
print(f"The average of the four numbers is: {average:.2f}")