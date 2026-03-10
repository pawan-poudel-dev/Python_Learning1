#write a program that takes n number of integers  as input and put them in a list  then it should found the max. and minimum  number from the list and print them out .The whole list must be list out 
#assume that the first element of the list is max/ min element ,then iterate through the list comparing the assume value  with every elemment to find the max and min value 
num = int(input("Enter n number of integers:"))
number=  []
for i in range(num):
    numbers = int(input("enter  the number: "))
    number.append(numbers)
maximun = number[0]
minumum = number[0]
for i in number:
        if i > maximun:
            maximun = i
        elif i < minumum:
            minumum = i
print("the list of numbers is:",number)
print("the maximum number is:",maximun)
print("the minimum number is:",minumum)



