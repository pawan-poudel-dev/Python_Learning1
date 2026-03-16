choice = -1

while choice != 0:
    print("Please choose a number for a rainbow color:")
    print("1. Red")
    print("2. Orange")
    print("3. Yellow")
    print("4. Green")
    print("5. Blue")
    print("6. Indigo")
    print("7. Violet")
    print("Enter 0 to exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        print("You chose Red")
    elif choice == 2:
        print("You chose Orange")
    elif choice == 3:
        print("You chose Yellow")
    elif choice == 4:
        print("You chose Green")
    elif choice == 5:
        print("You chose Blue")
    elif choice == 6:
        print("You chose Indigo")
    elif choice == 7:
        print("You chose Violet")
    elif choice == 0:
        print("Program exited.")
    else:
        print("Invalid choice")

    print()