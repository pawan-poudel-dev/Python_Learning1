"""
utils.py  —  Constants, validators, bill-counter, table builder, display helpers.
             MedStore Pvt. Ltd. Wholesale Medicine Management System
"""

import os
import re
from datetime import datetime

# ═══════════════════════════════════════════════════════
#  COMPANY CONSTANTS
# ═══════════════════════════════════════════════════════
COMPANY_NAME    = "MedStore Pvt. Ltd."
COMPANY_SUB     = "Wholesale Medicine Distributor"
COMPANY_ADDRESS = "New Road, Pokhara-8, Gandaki Pradesh, Nepal"
COMPANY_PHONE   = "+977-61-123456  |  +977-9856-123456"
COMPANY_EMAIL   = "info@medstore.com.np"
COMPANY_PAN     = "PAN No: 300456789"
COMPANY_REGD    = "Regd. No: 123/078-79"

VAT_RATE       = 0.13   # 13% VAT on taxable amount
STRIP_DISCOUNT = 0.05   # 5% discount when buying 2+ strips of same medicine

# ═══════════════════════════════════════════════════════
#  PATHS
# ═══════════════════════════════════════════════════════
BASE_DIR       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR       = os.path.join(BASE_DIR, "data")
INVOICES_DIR   = os.path.join(BASE_DIR, "invoices")
INVENTORY_FILE = os.path.join(DATA_DIR, "inventory.txt")
COUNTER_FILE   = os.path.join(DATA_DIR, "bill_counter.txt")
SALES_DIR      = os.path.join(INVOICES_DIR, "sales")
RESTOCK_DIR    = os.path.join(INVOICES_DIR, "restock")

# ═══════════════════════════════════════════════════════
#  BILL COUNTER
# ═══════════════════════════════════════════════════════

def _read_counters() -> dict:
    c = {"INV": 0, "PO": 0}
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "=" in line:
                    k, v = line.split("=", 1)
                    if k in c:
                        try:   c[k] = int(v)
                        except ValueError: pass
    return c

def _write_counters(c: dict):
    with open(COUNTER_FILE, "w", encoding="utf-8") as f:
        for k, v in c.items():
            f.write(f"{k}={v}\n")

def next_invoice_number() -> str:
    c = _read_counters(); c["INV"] += 1; _write_counters(c)
    return f"MS-INV-{c['INV']:04d}"

def next_po_number() -> str:
    c = _read_counters(); c["PO"] += 1; _write_counters(c)
    return f"MS-PO-{c['PO']:04d}"


# ═══════════════════════════════════════════════════════
#  TABLE BUILDER
#
#  Row formula: '  │' + join(' cell │')
#  Rendered width = 3 + sum(w+2 per col) + ncols
#                 = 3 + sum(w) + 2*ncols + ncols
#                 = 3 + sum(w) + 3*ncols
#
#  For console width 72:  sum(w) + 3*ncols = 69
#  For invoice file 80:   sum(w) + 3*ncols = 77
# ═══════════════════════════════════════════════════════
W_CONSOLE = 72   # console output width

def tbl_row(cells: list, widths: list, align: list = None) -> str:
    """Build one table row with hard-truncation and alignment."""
    if align is None:
        align = ["l"] * len(widths)
    parts = []
    for i, (cell, w) in enumerate(zip(cells, widths)):
        s = str(cell)
        if len(s) > w:
            s = s[:w - 1] + "…"
        a = align[i] if i < len(align) else "l"
        parts.append(" " + (s.rjust(w) if a == "r" else s.ljust(w)) + " ")
    return "  │" + "│".join(parts) + "│"

def tbl_top(cols: list)      -> str: return "  ┌" + "┬".join("─"*(c+2) for c in cols) + "┐"
def tbl_head_sep(cols: list) -> str: return "  ╞" + "╪".join("═"*(c+2) for c in cols) + "╡"
def tbl_mid(cols: list)      -> str: return "  ├" + "┼".join("─"*(c+2) for c in cols) + "┤"
def tbl_bot(cols: list)      -> str: return "  └" + "┴".join("─"*(c+2) for c in cols) + "┘"

def tbl_span(text: str, cols: list) -> str:
    """Full-width span row (no cell dividers) inside the table."""
    # inner text area width = total inner table width - 2 (for the space after/before │)
    # total inner = sum(c+2) + (ncols-1) border chars
    inner = sum(c + 2 for c in cols) + (len(cols) - 1) - 2
    s = str(text)
    if len(s) > inner:
        s = s[:inner - 1] + "…"
    return "  │ " + s.ljust(inner) + " │"

def tbl_width(cols: list) -> int:
    """Return the full rendered width of a table row."""
    return 3 + sum(c + 2 for c in cols) + len(cols)


# ═══════════════════════════════════════════════════════
#  INPUT HELPERS
# ═══════════════════════════════════════════════════════

def ask_int(prompt: str, min_val: int = 1, max_val: int = None) -> int:
    """Keep asking until a valid integer in [min_val, max_val] is received."""
    while True:
        raw = input(prompt).strip()
        if not raw:
            print("  ⚠  You didn't enter anything. Please type a number.")
            continue
        if not re.fullmatch(r"\d+", raw):
            print(f"  ⚠  '{raw}' is not a valid number. Please enter digits only.")
            continue
        val = int(raw)
        if val < min_val:
            print(f"  ⚠  That's too low — minimum is {min_val}. Try again.")
            continue
        if max_val is not None and val > max_val:
            print(f"  ⚠  That's too high — maximum is {max_val}. Try again.")
            continue
        return val

def ask_str(prompt: str) -> str:
    """Keep asking until a non-empty string with at least one letter is received."""
    while True:
        raw = input(prompt).strip()
        if not raw:
            print("  ⚠  This field cannot be empty. Please enter a name.")
            continue
        if not re.search(r"[a-zA-Z]", raw):
            print("  ⚠  The name must contain at least one letter. Please try again.")
            continue
        return raw

def ask_yn(prompt: str) -> bool:
    """Ask yes/no. Returns True for yes, False for no."""
    while True:
        raw = input(prompt + " [yes/no]: ").strip().lower()
        if raw in ("y", "yes"): return True
        if raw in ("n", "no"):  return False
        print("  ⚠  Please type 'yes' or 'no'  (or 'y' / 'n').")

def ask_choice(prompt: str, options: list) -> str:
    """Ask until one of the options is chosen. Returns lowercased match."""
    opts_lower = [o.lower() for o in options]
    display    = " / ".join(options)
    while True:
        raw = input(f"{prompt} [{display}]: ").strip().lower()
        if raw in opts_lower: return raw
        print(f"  ⚠  '{raw}' is not valid. Please choose one of: {display}")


# ═══════════════════════════════════════════════════════
#  TIME
# ═══════════════════════════════════════════════════════
def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d  %H:%M:%S")


# ═══════════════════════════════════════════════════════
#  CONSOLE DISPLAY HELPERS
# ═══════════════════════════════════════════════════════
def banner(title: str):
    W = W_CONSOLE - 4
    print()
    print("  ╔" + "═" * (W_CONSOLE - 2) + "╗")
    print("  ║  " + title.upper().ljust(W) + "  ║")
    print("  ╚" + "═" * (W_CONSOLE - 2) + "╝")

def rule(char: str = "─"):
    print("  " + char * (W_CONSOLE - 2))

def box_top(w: int)  -> str: return "  ╔" + "═" * (w - 2) + "╗"
def box_sep(w: int)  -> str: return "  ╠" + "═" * (w - 2) + "╣"
def box_bot(w: int)  -> str: return "  ╚" + "═" * (w - 2) + "╝"
def box_line(text: str, w: int, align: str = "l") -> str:
    inner = w - 4  # subtract '  ║ ' and ' ║'
    s = str(text)
    if len(s) > inner: s = s[:inner - 1] + "…"
    return "  ║ " + (s.center(inner) if align == "c" else s.ljust(inner)) + " ║"

def ok(msg: str):   print(f"  ✔  {msg}")
def warn(msg: str): print(f"  ⚠  {msg}")
def info(msg: str): print(f"  ℹ  {msg}")
