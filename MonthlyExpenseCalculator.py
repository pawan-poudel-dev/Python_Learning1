
# Monthly Expense Calculator takes the house rent, food expense, transport expense, and other expense as input, calculates the total monthly expense by summing up all the expenses, and then computes the yearly expense by multiplying the total monthly expense by 12. Finally, it displays both the total monthly expense and yearly expense formatted to two decimal places.
house_rent = float(input("Enter house rent: "))
food_expense = float(input("Enter food expense: "))
transport_expense = float(input("Enter transport expense: "))
other_expense = float(input("Enter other expense: "))
# Calculate total monthly expense
total_monthly_expense = house_rent + food_expense + transport_expense + other
# Calculate yearly expense
yearly_expense = total_monthly_expense * 12
# Display total monthly expense and yearly expense
print(f"Total Monthly Expense: {total_monthly_expense:.2f}")
print(f"Yearly Expense: {yearly_expense:.2f}")
