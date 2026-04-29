"""
main.py  —  MedStore Pvt. Ltd. Wholesale Medicine Management System
            Entry point: startup screen → main menu loop.
            CS4051NP Fundamentals of Computing — Coursework SP26

Run:
    python main.py
"""

import sys
import os

# Ensure the project root is on sys.path so 'modules' package resolves.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.utils import (
    COMPANY_NAME, COMPANY_SUB, COMPANY_ADDRESS, COMPANY_PHONE,
    COMPANY_EMAIL, W_CONSOLE,
    ask_int, banner, ok, warn, info,
    box_top, box_sep, box_bot, box_line, box_thin, now_str, append_log
)
from modules.inventory import (
    load_inventory, display_inventory,
    add_new_medicine, delete_medicine
)
from modules.sales         import run_sales
from modules.restock       import run_restock
from modules.search        import run_search, search_by_letter
from modules.invoice_viewer import view_past_invoices


# ════════════════════════════════════════════════════════════════════════════
#  STARTUP SCREEN
# ════════════════════════════════════════════════════════════════════════════

def startup_screen():
    """Display a formatted startup banner with company details."""
    print()
    print(box_top(W_CONSOLE))
    print(box_line("", W_CONSOLE))
    print(box_line(COMPANY_NAME, W_CONSOLE, "c"))
    print(box_line(COMPANY_SUB, W_CONSOLE, "c"))
    print(box_line("", W_CONSOLE))
    print(box_sep(W_CONSOLE))
    print(box_line("", W_CONSOLE))
    print(box_line("WHOLESALE MEDICINE MANAGEMENT SYSTEM", W_CONSOLE, "c"))
    print(box_line("CS4051NP  —  Fundamentals of Computing  —  SP26", W_CONSOLE, "c"))
    print(box_line("", W_CONSOLE))
    print(box_thin(W_CONSOLE))
    print(box_line(f"  Address :  {COMPANY_ADDRESS}", W_CONSOLE))
    print(box_line(f"  Phone   :  {COMPANY_PHONE}", W_CONSOLE))
    print(box_line(f"  Email   :  {COMPANY_EMAIL}", W_CONSOLE))
    print(box_thin(W_CONSOLE))
    print(box_line(f"  Session started :  {now_str()}", W_CONSOLE, "c"))
    print(box_line("", W_CONSOLE))
    print(box_bot(W_CONSOLE))
    print()


# ════════════════════════════════════════════════════════════════════════════
#  MAIN MENU
# ════════════════════════════════════════════════════════════════════════════

def main_menu():
    """Print the numbered main menu."""
    print()
    print(box_top(W_CONSOLE))
    print(box_line("  M A I N   M E N U", W_CONSOLE, "c"))
    print(box_sep(W_CONSOLE))
    print(box_line("  1.  View Medicine Inventory", W_CONSOLE))
    print(box_line("  2.  Search Medicine  (by Name / Brand)", W_CONSOLE))
    print(box_line("  3.  Search Medicine  (by Letter Pattern — Fuzzy)", W_CONSOLE))
    print(box_sep(W_CONSOLE))
    print(box_line("  4.  Process a Sale  (Customer Purchase)", W_CONSOLE))
    print(box_line("  5.  Restock Inventory  (Purchase from Supplier)", W_CONSOLE))
    print(box_sep(W_CONSOLE))
    print(box_line("  6.  Add New Medicine to Inventory", W_CONSOLE))
    print(box_line("  7.  Delete Medicine from Inventory", W_CONSOLE))
    print(box_sep(W_CONSOLE))
    print(box_line("  8.  View Past Invoices / Records", W_CONSOLE))
    print(box_line("  9.  Exit", W_CONSOLE))
    print(box_bot(W_CONSOLE))


# ════════════════════════════════════════════════════════════════════════════
#  MAIN LOOP
# ════════════════════════════════════════════════════════════════════════════

def main():
    """Program entry point — display startup, load inventory, run menu loop."""
    startup_screen()

    # Load inventory
    medicines = load_inventory()

    if not medicines:
        warn("Inventory file is empty or missing.")
        info(f"Please ensure data/inventory.txt exists with at least one medicine.")
    else:
        ok(f"Inventory loaded: {len(medicines)} medicine(s) ready.")

    append_log("SESSION STARTED")

    # ── Menu loop ─────────────────────────────────────────────────────────
    while True:
        main_menu()
        choice = ask_int("  Enter your choice [1-9]: ", min_val=1, max_val=9)

        if   choice == 1: display_inventory(medicines)
        elif choice == 2: run_search(medicines)
        elif choice == 3: search_by_letter(medicines)
        elif choice == 4: run_sales(medicines)
        elif choice == 5: run_restock(medicines)
        elif choice == 6: add_new_medicine(medicines)
        elif choice == 7: delete_medicine(medicines)
        elif choice == 8: view_past_invoices()
        elif choice == 9:
            append_log("SESSION ENDED")
            print()
            print(box_top(W_CONSOLE))
            print(box_line("Thank you for using MedStore Pvt. Ltd. Management System!", W_CONSOLE, "c"))
            print(box_line("Have a great day.  —  Goodbye!", W_CONSOLE, "c"))
            print(box_bot(W_CONSOLE))
            print()
            sys.exit(0)


if __name__ == "__main__":
    main()
