"""
main.py  —  MedStore Pvt. Ltd. Wholesale Medicine Management System
            Run:  python main.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.utils import (
    COMPANY_NAME, COMPANY_SUB, COMPANY_ADDRESS,
    COMPANY_PHONE, COMPANY_EMAIL, COMPANY_PAN, COMPANY_REGD,
    ask_int, ask_yn,
    box_top, box_sep, box_bot, box_line,
    rule, ok, warn, info,
    now_str, W_CONSOLE,
    SALES_DIR, RESTOCK_DIR,
)
from modules.inventory import load_inventory, display_inventory
from modules.sales    import run_sales
from modules.restock  import run_restock
from modules.logger   import log_session_start, log_session_end


# ════════════════════════════════════════════════════════
#  STARTUP BANNER
# ════════════════════════════════════════════════════════

def _startup():
    BW = W_CONSOLE
    print()
    print(box_top(BW))
    print(box_line("", BW))
    print(box_line(COMPANY_NAME, BW, "c"))
    print(box_line(COMPANY_SUB,  BW, "c"))
    print(box_line("", BW))
    print(box_line("─" * 50, BW, "c"))
    print(box_line(f"Address : {COMPANY_ADDRESS}", BW))
    print(box_line(f"Phone   : {COMPANY_PHONE}",   BW))
    print(box_line(f"Email   : {COMPANY_EMAIL}",   BW))
    print(box_line(f"{COMPANY_PAN}    {COMPANY_REGD}", BW))
    print(box_line("", BW))
    print(box_sep(BW))
    print(box_line("WHOLESALE MEDICINE MANAGEMENT SYSTEM", BW, "c"))
    print(box_bot(BW))
    print(f"  Session started : {now_str()}")
    print()


# ════════════════════════════════════════════════════════
#  MAIN MENU
# ════════════════════════════════════════════════════════

def _menu():
    BW = W_CONSOLE
    print()
    print(box_top(BW))
    print(box_line("MAIN MENU", BW, "c"))
    print(box_sep(BW))
    print(box_line("  1.  View Medicine Inventory",             BW))
    print(box_line("  2.  Process a Sale  (Customer Purchase)", BW))
    print(box_line("  3.  Restock  (Purchase from Supplier)",   BW))
    print(box_line("  4.  View Past Invoices / Purchase Orders",BW))
    print(box_line("  5.  Exit",                                BW))
    print(box_bot(BW))


# ════════════════════════════════════════════════════════
#  PAST INVOICE VIEWER
# ════════════════════════════════════════════════════════

def _view_invoices():
    from modules.utils import banner
    banner("Past Invoices")
    print()
    print("  Which type of records would you like to browse?")
    print("    1.  Sales Invoices       (MS-INV-XXXX)")
    print("    2.  Purchase Orders      (MS-PO-XXXX)")
    print()
    choice    = ask_int("  Enter choice [1 or 2]: → ", min_val=1, max_val=2)
    directory = SALES_DIR if choice == 1 else RESTOCK_DIR
    label     = "Sales Invoices" if choice == 1 else "Purchase Orders"

    os.makedirs(directory, exist_ok=True)
    files = sorted(f for f in os.listdir(directory) if f.endswith(".txt"))

    if not files:
        warn(f"No {label} have been generated yet.")
        return

    print()
    rule()
    print(f"  {label}  —  {len(files)} record(s) found")
    rule()
    for i, fname in enumerate(files, 1):
        size = os.path.getsize(os.path.join(directory, fname))
        print(f"    {i:>3}.  {fname:<22}  ({size} bytes)")
    rule()
    print()

    if not ask_yn("  Would you like to open and read one of these?"):
        return

    idx    = ask_int(f"  Enter the record number [1–{len(files)}]: → ", min_val=1, max_val=len(files))
    fpath  = os.path.join(directory, files[idx - 1])
    print()
    rule("═")
    print()
    with open(fpath, "r", encoding="utf-8") as f:
        print(f.read())
    rule("═")
    print()


# ════════════════════════════════════════════════════════
#  MAIN LOOP
# ════════════════════════════════════════════════════════

def main():
    _startup()
    log_session_start()

    medicines = load_inventory()
    if not medicines:
        warn("Could not load inventory. Please check data/inventory.txt")
        sys.exit(1)

    ok(f"Inventory loaded — {len(medicines)} medicines on record.")
    print()

    while True:
        _menu()
        choice = ask_int("  Please enter your choice [1–5]: → ", min_val=1, max_val=5)

        if   choice == 1: display_inventory(medicines)
        elif choice == 2: run_sales(medicines)
        elif choice == 3: run_restock(medicines)
        elif choice == 4: _view_invoices()
        elif choice == 5:
            print()
            log_session_end()
            BW = W_CONSOLE
            print(box_top(BW))
            print(box_line("Thank you for using MedStore Management System!", BW, "c"))
            print(box_line("Session ended. Goodbye!", BW, "c"))
            print(box_bot(BW))
            print()
            sys.exit(0)


if __name__ == "__main__":
    main()
