#WPA to find the greatest of 3 numbes entered by the user 
num1 = int(input("Enter your first Number: "))
num2 = int(input("Enter your second Number: "))
num3 = int(input('Enter your Third digit: '))
if (num1>=num2 and num1>= num3):
    print("Num1 is greater")
elif(num2>= num1 and num2>=num3):
    print("Num2 is greater")
else:
    print("Num3 is greater.")
print("Greatest number is :",max(num1,num2,num3))
print("Smallest number is:",min(num1,num2,num3))