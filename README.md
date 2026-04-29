MedStore Wholesale Management System
📌 Project Overview

The MedStore Wholesale Management System is a Python-based console application developed to manage medicine inventory, sales transactions, and restocking operations for a wholesale pharmaceutical distributor.

The system is designed to:

Maintain real-time stock updates
Process medicine sales (per tablet or per strip)
Apply automatic bulk discount logic
Generate unique invoice files for every transaction
Ensure data consistency using file handling techniques

This project demonstrates the practical application of programming fundamentals including file operations, data structures, modular programming, input validation, and exception handling.

🎯 Objectives
To develop a modular and loop-based inventory system.
To implement real-time stock updates using file handling.
To generate automated invoices for both sales and restocking.
To apply business logic such as 5% discount on strip purchases (2 or more strips).
To validate user input and handle runtime exceptions.
To demonstrate the use of appropriate data structures in Python.
🏗 System Features
1️⃣ Inventory Management
Reads medicine data from a text file.
Displays available medicines with stock details.
Updates stock immediately after each transaction.
2️⃣ Sales Processing
Allows sale per tablet or per strip.
Applies 5% discount when 2 or more strips are purchased.
Supports multiple medicine purchases in one transaction.
Automatically generates VAT invoice (.txt file).
3️⃣ Restocking System
Allows restocking from suppliers.
Updates inventory file after stock addition.
Generates supplier invoice with transaction details.
4️⃣ Invoice Generation

Each invoice contains:

Medicine name
Brand
Unit type (tablet/strip)
Quantity
Discount (if applicable)
Total cost
Customer/Supplier name
Date of transaction
Unique file name
🧠 Technologies Used
Programming Language: Python 3
Concepts Applied:
File Handling (read/write/update)
Lists and Dictionaries
String Processing
Modular Programming
Exception Handling
Loop Control Structures
📂 Project Structure
MedStore/
│
├── inventory.txt
├── main.py
├── invoices/
│   ├── sales_invoice_001.txt
│   └── restock_invoice_001.txt
└── README.md
🗃 Data Structure Design

The system uses:

Dictionary → To store medicine details for efficient lookup.
List → To manage multiple transaction items.
String Processing → To handle file data parsing.
Functions → For modularity (reading file, updating stock, generating invoice, etc.)

This approach ensures scalability, readability, and maintainability.

🔄 Program Flow
Load inventory file.
Display available medicines.
Prompt administrator for action:
Sell medicine
Restock medicine
Exit system
Validate inputs.
Process transaction.
Generate invoice.
Update inventory file.
Return to main menu.

The program runs continuously until the administrator chooses to exit.

⚠️ Business Logic Implementation
Strip discount:
If strips ≥ 2 → 5% discount applied automatically.
Stock validation:
System prevents selling more than available quantity.
Error handling:
Invalid inputs trigger appropriate error messages.
🧪 Testing

The system was tested for:

Valid and invalid input handling
Discount calculation accuracy
Multiple item transactions
Real-time stock updates
Unique invoice generation

Test cases were verified with sample data to ensure correctness and reliability.

📈 Learning Outcomes

Through this project, the following competencies were developed:

Practical understanding of Python file handling
Application of structured algorithm design
Development of modular programs
Implementation of real-world business logic
Experience in debugging and exception handling
Understanding of software usability principles
🏁 Conclusion

The MedStore Wholesale Management System successfully simulates a real-world wholesale pharmacy operation. The system ensures accurate inventory tracking, automated discount application, structured invoice generation, and modular code implementation.

This project bridges theoretical computing concepts with practical business logic, demonstrating the effective use of data structures and algorithmic thinking in solving real-world problems.
