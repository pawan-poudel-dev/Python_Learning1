''' write a program that takes input as name and marks obtained on a certain subjects of n students then the data must be stored in a dictionary with the name as keys and marks as values  then print out all the a names and marks of the students '''

Students ={}
n = int(input("Enter the number of students: "))
for i in range(n):
    name = input("Enter the name of student:")
    marks = int(input("Enter the marks obtained: "))
    
    Students[name] = marks
for key, value in Students.items():
    print(f"{key}: {value}")

Students ={}
n = int(input("Enter the number of students: "))
for i in range(n):
    name = input("Enter the name of student:")
    marks = int(input("Enter the marks obtained: "))
    
    Students[name] = marks
for key, value in Students.items():
    print(f"{key}: {value}")
