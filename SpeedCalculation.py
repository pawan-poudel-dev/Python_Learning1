
# Speed is calculated using the formula: Speed = Distance / Time
# The program prompts the user to enter the distance in kilometers and the time in hours, then it calculates the speed and displays it formatted to two decimal places.
distance = float(input("Enter the distance in kilometers: "))
time = float(input("Enter the time in hours: "))
# Calculate speed
speed = distance / time
print(f"Speed: {speed:.2f} km/h")
