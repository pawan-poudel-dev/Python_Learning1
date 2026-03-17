n = int(input("Enter number of terms: "))

a = 1
b = 1

print("Fibonacci sequence:")

print(a, b, end=" ")

for i in range(2, n):
    c = a + b
    print(c, end=" ")
    
    a = b
    b = c