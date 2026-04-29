"""
utils.py  —  Constants, validators, bill-counter, table builder, display helpers.
             MedStore Pvt. Ltd. Wholesale Medicine Management System
             CS4051NP Fundamentals of Computing — Coursework SP26
"""

import os
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════
#  COMPANY CONSTANTS
# ═══════════════════════════════════════════════════════════════════
COMPANY_NAME    = "MedStore Pvt. Ltd."
COMPANY_SUB     = "Wholesale Medicine Distributor"
COMPANY_ADDRESS = "New Road, Pokhara-8, Gandaki Pradesh, Nepal"
COMPANY_PHONE   = "+977-61-123456  |  +977-9856-123456"
COMPANY_EMAIL   = "info@medstore.com.np"
COMPANY_PAN     = "PAN No: 300456789"
COMPANY_REGD    = "Regd. No: 123/078-79"

VAT_RATE       = 0.13   # 13% VAT applied on taxable (post-discount) amount
STRIP_DISCOUNT = 0.05   # 5% discount when buying 2+ strips of same medicine

# ═══════════════════════════════════════════════════════════════════
#  FILE PATHS
# ═══════════════════════════════════════════════════════════════════
BASE_DIR       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR       = os.path.join(BASE_DIR, "data")
INVOICES_DIR   = os.path.join(BASE_DIR, "invoices")
INVENTORY_FILE = os.path.join(DATA_DIR, "inventory.txt")
COUNTER_FILE   = os.path.join(DATA_DIR, "bill_counter.txt")
LOG_FILE       = os.path.join(DATA_DIR, "log.txt")
SALES_DIR      = os.path.join(INVOICES_DIR, "sales")
RESTOCK_DIR    = os.path.join(INVOICES_DIR, "restock")

# ═══════════════════════════════════════════════════════════════════
#  CONSOLE DISPLAY WIDTH
# ═══════════════════════════════════════════════════════════════════
W_CONSOLE = 100  # Total console width for boxes and banners

# ═══════════════════════════════════════════════════════════════════
#  BILL COUNTER  (persistent INV / PO numbering)
# ═══════════════════════════════════════════════════════════════════

def _read_counters() -> dict:
    """Read invoice/PO counters from the counter file."""
    counters = {"INV": 0, "PO": 0}
    if os.path.exists(COUNTER_FILE):
        try:
            with open(COUNTER_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if "=" in line:
                        key, _, val = line.partition("=")
                        if key in counters:
                            try:
                                counters[key] = int(val)
                            except ValueError:
                                pass
        except OSError:
            pass
    return counters


def _write_counters(counters: dict):
    """Persist updated counters back to the counter file."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(COUNTER_FILE, "w", encoding="utf-8") as f:
        for key, val in counters.items():
            f.write(f"{key}={val}\n")


def next_invoice_number() -> str:
    """Increment and return the next formatted invoice number."""
    c = _read_counters()
    c["INV"] += 1
    _write_counters(c)
    return f"MS-INV-{c['INV']:04d}"


def next_po_number() -> str:
    """Increment and return the next formatted purchase-order number."""
    c = _read_counters()
    c["PO"] += 1
    _write_counters(c)
    return f"MS-PO-{c['PO']:04d}"


# ═══════════════════════════════════════════════════════════════════
#  FILE WRITER HELPER
# ═══════════════════════════════════════════════════════════════════

def write_file(directory: str, filename: str, content: str) -> str:
    """Write content to a file and return the full path."""
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def append_log(entry: str):
    """Append a timestamped entry to the activity log."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{now_str()}]  {entry}\n")


# ═══════════════════════════════════════════════════════════════════
#  TABLE BUILDER
# ═══════════════════════════════════════════════════════════════════

def tbl_row(cells: list, widths: list, align: list = None) -> str:
    """Build one table row with hard truncation and alignment."""
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


def tbl_top(cols: list)      -> str: return "  ┌" + "┬".join("─" * (c + 2) for c in cols) + "┐"
def tbl_head_sep(cols: list) -> str: return "  ╞" + "╪".join("═" * (c + 2) for c in cols) + "╡"
def tbl_mid(cols: list)      -> str: return "  ├" + "┼".join("─" * (c + 2) for c in cols) + "┤"
def tbl_bot(cols: list)      -> str: return "  └" + "┴".join("─" * (c + 2) for c in cols) + "┘"

def tbl_width(cols: list) -> int:
    """Return the full rendered width of a table."""
    return 3 + sum(c + 2 for c in cols) + len(cols)


# ═══════════════════════════════════════════════════════════════════
#  BOX / BANNER HELPERS
# ═══════════════════════════════════════════════════════════════════

def box_top(w: int)  -> str: return "  ╔" + "═" * (w - 2) + "╗"
def box_sep(w: int)  -> str: return "  ╠" + "═" * (w - 2) + "╣"
def box_bot(w: int)  -> str: return "  ╚" + "═" * (w - 2) + "╝"
def box_thin(w: int) -> str: return "  ╟" + "─" * (w - 2) + "╢"


def box_line(text: str, w: int, align: str = "l") -> str:
    """One line inside a double-border box."""
    inner = w - 4
    s = str(text)
    if len(s) > inner:
        s = s[:inner - 1] + "…"
    padded = s.center(inner) if align == "c" else s.ljust(inner)
    return "  ║ " + padded + " ║"


def banner(title: str):
    """Print a prominent section banner."""
    inner = W_CONSOLE - 8   # accounts for '  ║  ◆  ' (8 chars) + '  ║' (3) 
    print()
    print("  ╔" + "═" * (W_CONSOLE - 2) + "╗")
    print("  ║  ◆  " + title.upper().ljust(inner) + "  ║")
    print("  ╚" + "═" * (W_CONSOLE - 2) + "╝")


def rule(char: str = "─"):
    print("  " + char * (W_CONSOLE - 2))


# ═══════════════════════════════════════════════════════════════════
#  INPUT / VALIDATION HELPERS
# ═══════════════════════════════════════════════════════════════════

def ask_int(prompt: str, min_val: int = None, max_val: int = None) -> int:
    """Keep asking until a valid integer within [min_val, max_val] is received."""
    while True:
        raw = input(prompt).strip()
        if not raw:
            warn("Empty input — please type a number.")
            continue
        try:
            val = int(raw)
        except ValueError:
            warn(f"'{raw}' is not a valid integer.")
            continue
        if min_val is not None and val < min_val:
            warn(f"Value must be at least {min_val}.")
            continue
        if max_val is not None and val > max_val:
            warn(f"Value must be at most {max_val}.")
            continue
        return val


def ask_float(prompt: str, min_val: float = 0.0) -> float:
    """Keep asking until a valid float >= min_val is received."""
    while True:
        raw = input(prompt).strip()
        if not raw:
            warn("Empty input — please type a number.")
            continue
        try:
            val = float(raw)
        except ValueError:
            warn(f"'{raw}' is not a valid number.")
            continue
        if val < min_val:
            warn(f"Value must be at least {min_val}.")
            continue
        return val


def ask_str(prompt: str, allow_empty: bool = False) -> str:
    """Keep asking until a non-empty string (or optionally empty) is received."""
    while True:
        raw = input(prompt).strip()
        if not raw and not allow_empty:
            warn("This field cannot be empty.")
            continue
        return raw


def ask_yn(prompt: str) -> bool:
    """Prompt yes/no — returns True for yes, False for no."""
    while True:
        raw = input(prompt + " [y/n]: ").strip().lower()
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        warn("Please type 'y' for yes or 'n' for no.")


def ask_choice(prompt: str, options: list) -> str:
    """Ask until one of the given options is chosen (case-insensitive)."""
    opts_lower = [o.lower() for o in options]
    display = " / ".join(options)
    while True:
        raw = input(f"{prompt} ({display}): ").strip().lower()
        if raw in opts_lower:
            return raw
        warn(f"Invalid choice. Please choose one of: {display}")


# ═══════════════════════════════════════════════════════════════════
#  STATUS HELPERS
# ═══════════════════════════════════════════════════════════════════

def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d  %H:%M:%S")


def ok(msg: str):   print(f"\n  ✔  {msg}")
def warn(msg: str): print(f"  ⚠  {msg}")
def info(msg: str): print(f"  ℹ  {msg}")
def err(msg: str):  print(f"  ✖  {msg}")
