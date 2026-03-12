
# Data Storage Conversion takes the size in MB as input, converts it to KB and GB using the appropriate conversion factors, and then displays the results formatted to two decimal places.
size_in_mb = float(input("Enter the size in MB: "))
# Convert MB to KB and GB
size_in_kb = size_in_mb * 1024
size_in_gb = size_in_mb / 1024
# Display the results
print(f"Size in KB: {size_in_kb:.2f} KB")
print(f"Size in GB: {size_in_gb:.2f} GB")
