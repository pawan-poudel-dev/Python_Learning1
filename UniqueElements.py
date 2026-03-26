 # Write a program that creates a new list containing only the unique elements from the original list in descending order.
# [1,1,2,3,4,4,5,6,5,6]
original_list = [1,1,2,3,4,4,5,6,5,6]
unique_elements = sorted(list(set(original_list)), reverse=True)
print(unique_elements)