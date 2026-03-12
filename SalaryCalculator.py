"""
Create a salary calculator:
•	Input: basic salary
•	Calculate:
o	HRA = 10% of basic
o	DA = 5% of basic
•	Display gross salary
Note: House Rental Allowance , Dearness Allowance

"""
# Salary Calculator takes the basic salary as input, calculates the HRA and DA,
#  and then computes the gross salary by summing up the basic salary, HRA, and DA. 
# Finally, it displays the gross salary formatted to two decimal places.
basic_salary = float(input("Enter the basic salary: "))
hra = 0.10 * basic_salary
da = 0.05 * basic_salary
# Calculate gross salary
gross_salary = basic_salary + hra + da
print(f"Gross Salary: {gross_salary:.2f}")