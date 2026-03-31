#take a numeric  string and find its sum 
def sum_of_digits(num_str):
    total = 0
    for char in num_str:
        if char.isdigit():
            total += int(char)
    return total
input_str = input("Enter a numeric string: ")
result = sum_of_digits(input_str)
print(f"The sum of the digits in the string is: {result}")
