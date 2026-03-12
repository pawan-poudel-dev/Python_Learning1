#calculating the factorial of a number
#using the while loop
num = int(input("Enter a number: "))
factorial = 1
if num < 0:
    print("Factorial does not exist for negative numbers")
elif num == 0:
    print("The factorial of 0 is 1")
else:
    while num > 0:
        factorial *= num
        num -= 1
    print(f"The factorial of the number is: {factorial}")