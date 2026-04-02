'''#creating an empty set 
empty_set=set()
#creating an empty dictionary
empty_dict={}
#check data type of empty_set
print("Data type of empty_set:",type(empty_set))
print("Data type of empty_dictionary:", type(empty_dict))
  '''
numbers = {21,34,54,122}
num1 = {1,2,3,4,5,56,7,8,8,9,9,9}
'''print("Initial sets is :" , numbers)
#using add()method
numbers.add(32)
print(numbers)
#for the update purpose 
numbers.update(num1)
print(numbers)'''
'''a = num1.discard(7)
print(num1)'''
#iterate through loops 
for number in numbers:
    print(number)

print(len(numbers))