# This program calculates the sum, average, and a compound expression based on three numbers input by the user.
num1 = float(input("Enter the first number: "))
num2 = float(input("Enter the second number: "))
num3 = float(input("Enter the third number: "))
# Calculate the sum of the three numbers
total_sum = num1 + num2 + num3
# Calculate the average of the three numbers
average = total_sum / 3
#Now the expression is evaluated and the results are displayed
result = (num1 + num2)**2 + (num2 + num3)**2
print(f"The sum of the three numbers is: {total_sum:.2f}")
print(f"The average of the three numbers is: {average:.2f}")
print(f"The result of the expression (num1 + num2)**2 + (num2 + num3)**2 is: {result:.2f}")

