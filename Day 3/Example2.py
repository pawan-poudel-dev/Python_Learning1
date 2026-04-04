languages = ["Python","Java","Javascript"]
#accessing the first element
print('Languages[0]=',languages[0])
print(languages[2])
#negative indexing in python
print("Negative indexing of Languages[-2]=",languages[-2])
print("Negative indexing of Languages[-3]=",languages[-3])

#slicing in list 
#there are a lot of methods to slice the list 
my_list = ['p','r','o','g','r','a','m','m','i','n','g']
print("My_List=",my_list)
#turn to slicing the list 
print("my_list= ",my_list[2:4])
print("My_list =",my_list[3:-3])
print("My_List =",my_list[0:3])
#Omitting start and end slicing 
print("My_list =",my_list[5:])
print("My_List =",my_list[:-4])
print("My-list=",my_list[:])
# adding the  new element in  to the list using the append() inbuilt function 
my_list.append("Java")
print(my_list)
# add  elements at the specified index using the insert() ffunction 
my_list.insert(2,"python")
print(my_list)

# add the list elements using the extend  or using the + operator
num1 = [1,2,3,4,5]
num2= [6,7,8,9,10]
num3 = num1 + num2
print(num3)
num1.extend(num2)
print(num1)
# change the list of the item 
my_list[5]="pawan poudel"
print(my_list)
#  change  the list of the item to the next index 
my_list[6]="AAyusha  subedi"
print(my_list)
# remove an item from the  list 
num1.remove(3)
print(num1)