
#take the value of N as input from the user
N = int(input("Enter the value of N: "))
#initialize the sum variable
sum = 0
#calculate the sum of the series
for i in range(1, N + 1):
    sum += 1 / i
#display the result
print(f"The sum of the series 1 + 1/2 + 1/3 + ... + 1/{N} is: {sum:.4f}")
