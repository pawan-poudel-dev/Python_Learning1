
# Average Speed takes the distance and time for two segments of a trip as input, calculates the total distance and total time, and then computes the average speed by dividing the total distance by the total time. Finally, it displays the average speed formatted to two decimal places.
# Input for first segment
distance1 = float(input("Enter the distance for segment 1 (in km): "))
time1 = float(input("Enter the time for segment 1 (in hours): "))
# Input for second segment
distance2 = float(input("Enter the distance for segment 2 (in km): "))
time2 = float(input("Enter the time for segment 2 (in hours): "))
# Calculate total distance and total time
total_distance = distance1 + distance2
total_time = time1 + time2
# Calculate average speed
average_speed = total_distance / total_time
# Display average speed
print(f"Average Speed: {average_speed:.2f} km/h")