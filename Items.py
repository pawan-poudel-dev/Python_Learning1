# Input
item_name = input("Enter Item 1 Name: ")
item_price = float(input("Enter Item 1 Price: "))

item_name1 = input("Enter Item 2 Name: ")
item_price1 = float(input("Enter Item 2 Price: "))

item_name2 = input("Enter Item 3 Name: ")
item_price2 = float(input("Enter Item 3 Price: "))

# Calculation
total = item_price + item_price1 + item_price2
tax = total * 0.13
final_total = total + tax

# Receipt Output
print("\n====================================================")
print("                 RECEIPT")
print("====================================================")

print("Item Name\t\tPrice")
print("----------------------------------------------------")
print(item_name, "\t\tRs.", item_price)
print(item_name1, "\t\tRs.", item_price1)
print(item_name2, "\t\tRs.", item_price2)

print("----------------------------------------------------")
print("Total Amount:\t\tRs.", total)
print("Tax (13%):\t\tRs.", tax)
print("Final Total:\t\tRs.", final_total)
print("====================================================")