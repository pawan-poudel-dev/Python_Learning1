
# Travel Cost Calculator takes the distance, cost per km, and number of days as input, calculates the daily cost by multiplying the distance with the cost per km, and then computes the total trip cost by multiplying the daily cost with the number of days. Finally, it displays both the daily cost and total trip cost formatted to two decimal places.
distance = float(input("Enter the distance in km: "))
cost_per_km = float(input("Enter the cost per km: "))
number_of_days = int(input("Enter the number of days: "))
# Calculate daily cost
daily_cost = distance * cost_per_km
# Calculate total trip cost
total_trip_cost = daily_cost * number_of_days
# Display daily cost and total trip cost
print(f"Daily Cost: {daily_cost:.2f}")
print(f"Total Trip Cost: {total_trip_cost:.2f}")
