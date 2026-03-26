''' Write a proigram that takes as  input  the names  and marks  obtaines  on a certain  subject  of N Students . Then  the data must be stored  in a  dictionary  with the names as keys and marks  as values .
 Then find out the highest , lowest and averahge marks obtained  and print them out ..'''
# read number of students
n = int(input("Enter number of students: ").strip())

marks_dict = {}
for i in range(n):
    name = input(f"Student #{i+1} name: ").strip()
    mark = float(input(f"Student #{i+1} mark: ").strip())
    marks_dict[name] = mark

if len(marks_dict) == 0:
    print("No students provided.")
else:
    values = list(marks_dict.values())
    highest = max(values)
    lowest = min(values)
    average = sum(values) / len(values)

    # find students with highest/lowest
    highest_names = [name for name, score in marks_dict.items() if score == highest]
    lowest_names = [name for name, score in marks_dict.items() if score == lowest]

    print("\n--- Results ---")
    print("Data:", marks_dict)
    print(f"Highest mark: {highest} (students: {', '.join(highest_names)})")
    print(f"Lowest mark: {lowest} (students: {', '.join(lowest_names)})")
    print(f"Average mark: {average:.2f}")