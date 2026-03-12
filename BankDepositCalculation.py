
# Bank Deposit Calculation takes the deposit amount as input, calculates the interest based on a fixed interest rate of 7%, and then computes the total amount after one year by adding the interest to the original deposit. Finally, it displays the total amount formatted to two decimal places.
deposit_amount = float(input("Enter the deposit amount: "))
interest_rate = 7
# Calculate interest
interest = (deposit_amount * interest_rate) / 100
# Calculate total after 1 year
total_amount = deposit_amount + interest
# Display total amount after 1 year
print(f"Total amount after 1 year: {total_amount:.2f}")
