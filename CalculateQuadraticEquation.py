#This program will calculate the roots of a quadratic equation based on user input for the coefficients a, b, and c. The program will then print the roots to the user.
cofficent_a=float(input("Enter the value of cofficent a: "))
cofficent_b=float(input("Enter the value of cofficent b: "))
cofficent_c=float(input("Enter the value of cofficent c: "))
#calculating the value of the discriminant
discriminant = cofficent_b**2 - 4*cofficent_a*cofficent_c
#determining the nature of the roots based on the value of the discriminant and printing the result to the user
if discriminant > 0:
    #calculating the value of the roots using the quadratic formula
    root1 = (-cofficent_b + discriminant**0.5) / (2*cofficent_a)
    root2 = (-cofficent_b - discriminant**0.5) / (2*cofficent_a)
    #printing the roots to the user
    print("The roots are real and different.")
    print("Root 1: ", root1)
    print("Root 2: ", root2)
    #calculating the value of x using the quadratic formula and printing the result to the user
elif discriminant == 0:
    root = -cofficent_b / (2*cofficent_a)
    print("The roots are real and the same.")
    print("Root: ", root)
    #calculating the value of x using the quadratic formula and printing the result to the user
    x = -cofficent_b / (2*cofficent_a)
    print("The value of x is: ", x)
else:
    real_part = -cofficent_b / (2*cofficent_a)
    imaginary_part = (abs(discriminant)**0.5) / (2*cofficent_a)
    #printing the roots to the user
    print("The roots are complex and different.")
    print("Root 1: ", real_part, "+", imaginary_part, "i")
    #calculating the value of x using the quadratic formula and printing the result to the user
    print("Root 2: ", real_part, "-", imaginary_part, "i")  
    #calculating the value of x using the quadratic formula and printing the result to the user
    x1 = (-cofficent_b + discriminant**0.5) / (2*cofficent_a)
    #calculating the value of x using the quadratic formula and printing the result to the user
    x2 = (-cofficent_b - discriminant**0.5) / (2*cofficent_a)
    print("The values of x are: ", x1, " and ", x2) 
