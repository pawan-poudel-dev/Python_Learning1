num1 = int(input("enter your first number:"))
num2 = int(input("enter your second number:"))


#using while loop
while num2 != 0:
    temp = num2
    num2 = num1 % num2
    num1 = temp
print("the GCD of the two numbers is:",num1)