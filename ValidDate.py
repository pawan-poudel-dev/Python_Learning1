
#take the date as input from the user
date = input("Enter a date (dd/mm/yyyy): ")
#split the date into day, month and year
day, month, year = map(int, date.split('/'))
#check if the date is valid
if (month < 1 or month > 12) or (day < 1 or day > 31):
    print("Invalid date")
elif month in [4, 6, 9, 11] and day > 30:
    print("Invalid date")
elif month == 2:    
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        if day > 29:
            print("Invalid date")
        else:
            print("Valid date")
    else:
        if day > 28:
            print("Invalid date")
        else:
            print("Valid date")
else:
    print("Valid date")