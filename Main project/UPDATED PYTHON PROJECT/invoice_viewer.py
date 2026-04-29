"""
invoice_viewer.py  —  Browse and display past sales invoices and restock POs.
                      MedStore Pvt. Ltd. — CS4051NP Coursework SP26
"""

import os
from modules.utils import (
    SALES_DIR, RESTOCK_DIR,
    banner, warn, info, ok, ask_int, ask_yn, W_CONSOLE,
    box_top, box_sep, box_bot, box_line, box_thin
)


def _list_files(directory: str) -> list:
    """Return sorted list of .txt filenames in a directory."""
    if not os.path.exists(directory):
        return []
    return sorted(
        f for f in os.listdir(directory) if f.endswith(".txt")
    )


def _display_file(filepath: str):
    """Print contents of an invoice .txt file to the console."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        print()
        for line in content.splitlines():
            print("  " + line)
        print()
    except OSError as e:
        warn(f"Could not read file: {e}")


def _browse_directory(title: str, directory: str):
    """List files in a directory and let the user pick one to view."""
    files = _list_files(directory)

    if not files:
        warn(f"No {title} records found yet.")
        return

    print()
    print(f"  ╔══ {title} — {len(files)} record(s) " + "═" * max(0, 42 - len(title) - len(str(len(files)))) + "╗")
    for i, fname in enumerate(files, 1):
        fpath = os.path.join(directory, fname)
        size  = os.path.getsize(fpath)
        print(f"    {i:>3}.  {fname:<25}  ({size} bytes)")
    print()

    idx = ask_int(
        f"  Enter record No. to view  [0 = back]: ",
        min_val=0, max_val=len(files)
    )
    if idx == 0:
        return

    fpath = os.path.join(directory, files[idx - 1])
    _display_file(fpath)


def view_past_invoices():
    """Main entry for the invoice viewer — offers Sales or Restock sub-menu."""
    banner("View Past Invoices & Records")

    while True:
        print()
        print(box_top(W_CONSOLE))
        print(box_line("RECORDS BROWSER", W_CONSOLE, "c"))
        print(box_sep(W_CONSOLE))
        print(box_line("  1.  View Sales Invoices  (Customer Purchases)", W_CONSOLE))
        print(box_line("  2.  View Restock Records  (Purchase Orders)", W_CONSOLE))
        print(box_line("  3.  Return to Main Menu", W_CONSOLE))
        print(box_bot(W_CONSOLE))

        choice = ask_int("  Choice [1-3]: ", min_val=1, max_val=3)

        if choice == 1:
            _browse_directory("Sales Invoices", SALES_DIR)
        elif choice == 2:
            _browse_directory("Restock Purchase Orders", RESTOCK_DIR)
        elif choice == 3:
            break
