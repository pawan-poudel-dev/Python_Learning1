
# Profit Margin takes the cost price per item, selling price per item, and quantity as input, calculates the total cost, total selling, total profit, and profit percentage, and then displays the results formatted to two decimal places.
cost_price_per_item = float(input("Enter the cost price per item: "))
selling_price_per_item = float(input("Enter the selling price per item: "))
quantity = int(input("Enter the quantity: "))
# Calculate total cost, total selling, total profit, and profit percentage
total_cost = cost_price_per_item * quantity
#total selling is calculated by multiplying the selling price per item with the quantity
total_selling = selling_price_per_item * quantity
#totalprofit is calculated by subtracting the total cost from the total selling
total_profit = total_selling - total_cost
#pprofit percentage is calculated by dividing the total profit by the total cost and multiplying by 100
profit_percentage = (total_profit / total_cost) * 100
# Display results
print(f"Total Cost: {total_cost:.2f}")
print(f"Total Selling: {total_selling:.2f}")
print(f"Total Profit: {total_profit:.2f}")
print(f"Profit Percentage: {profit_percentage:.2f}%")
