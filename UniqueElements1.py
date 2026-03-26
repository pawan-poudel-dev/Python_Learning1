# Write a program that creates a new list containing only the unique elements from the original list in descending order
# ['a','a','b','c','d','c','e','d','e']
original_list = ['a','a','b','c','d','c','e','d','e']
unique = sorted(list(set(original_list)), reverse=True)
print(unique)