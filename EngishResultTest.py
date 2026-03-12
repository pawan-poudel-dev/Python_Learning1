
# Exam Result Sheet takes the marks of English, Math, Science, and Computer as input, calculates the total marks by summing up the individual marks, computes the percentage by dividing the total marks by the maximum possible marks (400) and multiplying by 100, and then calculates the average marks by dividing the total marks by the number of subjects (4). Finally, it displays the total marks, percentage formatted to two decimal places, and average marks formatted to two decimal places.
english_marks = float(input("Enter marks for English: "))
math_marks = float(input("Enter marks for Math: "))
science_marks = float(input("Enter marks for Science: "))
computer_marks = float(input("Enter marks for Computer: "))
# Calculate total marks
total_marks = english_marks + math_marks + science_marks + computer_marks
# Calculate percentage
percentage = (total_marks / 400) * 100
# Calculate average marks
average_marks = total_marks / 4
# Display results
print(f"Total Marks: {total_marks:.2f}")
print(f"Percentage: {percentage:.2f}%")
print(f"Average Marks: {average_marks:.2f}")
