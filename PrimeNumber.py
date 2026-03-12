num = int(input("Enter a number:"))
"""if num>1:
    for i in range(2,num):
        if(num % i) == 0:
            print(num,"is not a prime number")
            break
    else:
        print(num,"is a prime number")
else:
    print(num,"is not a prime number")
"""

#using while loop 
if num>1:
    i = 2
    #iterating from 2 to num-1
    while i < num:
        #checking if num is divisible by any number between 2 and num-1
        if(num % i) == 0:
            print(num,"is not a prime number")# printing if num is divisible by any number between 2 and num-1
            break
        #incrementing the value of i by 1
        i += 1
    else:
        print(num,"is a prime number")
else:
    print(num,"is not a prime number")



