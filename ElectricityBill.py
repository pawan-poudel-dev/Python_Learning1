
# The program prompts the user to enter the number of units consumed, calculates the cost by multiplying the units by 12, adds a fixed service charge of 100, and then displays the total bill formatted to two decimal places.
units_consumed = float(input("Enter the number of units consumed: "))
# Calculate cost based on units consumed
cost = units_consumed * 12
# Fixed service charge
service_charge = 100
# Calculate total bill
total_bill = cost + service_charge
print(f"Total Electricity Bill: {total_bill:.2f}")