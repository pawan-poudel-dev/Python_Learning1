

# The program prompts the user to enter their birth year, 
# calculates their approximate age by subtracting the birth year from the current year (2026),
#  and then displays the age.
current_year = 2026
birth_year = int(input("Enter your birth year: "))
# Calculate approximate age
age = current_year - birth_year
# Display the approximate age
print(f"Your approximate age is: {age} years")
