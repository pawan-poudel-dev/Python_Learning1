#write a program that will compute the value of an algebraic expression. The program should ask the user for the values of x and y, and then compute the value of the expression x^3 + 3*x^2*y + 3*x*y^2+ y^3. The program should then print the result to the user.
#This program will compute the value of an algebraic expression based on user input for x and y.
#Ask the user for the value of x and y
x = float(input("Enter the value of x: "))
y = float(input("Enter the value of y: "))
#Compute the value of the expression x^3 + 3*x^2*y + 3*x*y^2 + y^3
result = x**3 + 3*x**2*y + 3*x*y**2 + y**3
#Print the result to the user
print("The value of the expression x^3 + 3*x^2*y + 3*x*y^2 + y^3 is: ", result)