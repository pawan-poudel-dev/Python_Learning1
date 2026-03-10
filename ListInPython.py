# write a program that takes  n umbers  as input  from a user and puts them in a list then the program should find out the sum of all the even numbers and  sum of all the odd numbers from the list 
num= int(input("enter n number:"))
numbers= []
for i in range(num):
    number = int(input("enter a number:"))
    numbers.append(number)
even_sum = 0
odd_sum = 0
for number in numbers:  
    if number % 2 == 0:  
        even_sum += number  
    else:  
        odd_sum += number
print("the sum of even numbers is:",even_sum)
print("the sum of odd numbers is:",odd_sum)