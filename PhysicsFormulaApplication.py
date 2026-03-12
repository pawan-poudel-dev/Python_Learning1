# Physics Formula Application: Final Velocity and Distance Calculation
# Input for initial velocity, acceleration, and time
initial_velocity = float(input("Enter the initial velocity (u) in m/s: "))
acceleration = float(input("Enter the acceleration (a) in m/s²: "))
time = float(input("Enter the time (t) in seconds: "))
# Calculate final velocity
final_velocity = initial_velocity + (acceleration * time)
# Calculate distance
distance = (initial_velocity * time) + (0.5 * acceleration * (time ** 2))
# Display final velocity and distance
print(f"Final Velocity (v): {final_velocity:.2f} m/s")
print(f"Distance (s): {distance:.2f} meters")   
