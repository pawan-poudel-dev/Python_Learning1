#swapping the numbers
#This program will swap the values of two numbers provided by the user.
#Ask the user for the first number
num1 = int(input("Enter the first number: "))
#Ask the user for the second number
num2 = int(input("Enter the second number: "))
#Swapping the values of num1 and num2 using a temporary variable
temp = num1
num1 = num2
num2 = temp
#Printing the swapped values to the user
print("After swapping:")
print("First number: ", num1,num2)
#code runs well and the values of num1 and num2 are swapped successfully.