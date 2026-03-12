
#function to calculate GCD using Euclidean algorithm
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a    
#taking input from the user
num1 = int(input("Enter the first number: "))
num2 = int(input("Enter the second number: "))
#calculating GCD
result = gcd(num1, num2)
#printing the result
print(f"The GCD of {num1} and {num2} is: {result}")
