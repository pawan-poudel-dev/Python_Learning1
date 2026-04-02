a, b, c=45,67,89
if a>b and a>c:
    print("A is greater than B and C")
elif b>c and b>a:
    print("B os greater than A and C")
else:
    print("C is greater than A and B")
    print(max(a,b,c)) 