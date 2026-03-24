#WAP that take diameter as input and calculate the area of a circle
diameter = float(input("Diameter is :"))
# first method is using the formula pi* d^2/2
pi = 3.14
area = (pi* diameter**2)/4
print(f"Area of circle is : {area}")