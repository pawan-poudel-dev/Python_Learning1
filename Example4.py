#For input [1, 2, 9, 4, 5], the return value should be 9.
names = int(input("Enter numbers: "))
list = []
for i in range(names):
    num = int(input())
    list.append(num)
print(list)
max_num = max(list)
print("The maximum number is:", max_num)
