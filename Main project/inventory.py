"""
inventory.py  —  Load, save, and display the MedStore medicine inventory.

Medicine dict keys:
  name, brand, stock (int tablets), rate_tablet (float),
  rate_strip (float), tablets_per_strip (int)
"""

import os
from modules.utils import (
    INVENTORY_FILE,
    tbl_row, tbl_top, tbl_head_sep, tbl_mid, tbl_bot, tbl_width,
    warn,
)

# ── Inventory table ─────────────────────────────────────────────────────────
# 7 cols.  Width computed automatically via tbl_width().
# [3, 20, 16, 10, 10, 11, 10]  →  tbl_width = 3 + sum(w+2)*7 + 7 = 3+80*2+? 
# Just use the function.
_I_W   = [3, 20, 16, 10, 10, 11, 10]
_I_AL  = ["r", "l", "l", "r", "r", "r", "r"]
_I_HDR = ["No", "Medicine Name", "Brand", "Stock(tab)", "Rate/Tab", "Rate/Strip", "Tabs/Strip"]


# ════════════════════════════════════════════════════════
#  LOAD
# ════════════════════════════════════════════════════════

def load_inventory() -> list:
    medicines = []
    if not os.path.exists(INVENTORY_FILE):
        warn(f"Inventory file not found: {INVENTORY_FILE}")
        return medicines
    with open(INVENTORY_FILE, "r", encoding="utf-8") as f:
        for ln, raw in enumerate(f, 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split(",")]
            if len(parts) != 6:
                warn(f"Line {ln} skipped — expected 6 fields, got {len(parts)}.")
                continue
            try:
                medicines.append({
                    "name"             : parts[0],
                    "brand"            : parts[1],
                    "stock"            : int(parts[2]),
                    "rate_tablet"      : float(parts[3]),
                    "rate_strip"       : float(parts[4]),
                    "tablets_per_strip": int(parts[5]),
                })
            except ValueError as e:
                warn(f"Line {ln} skipped — {e}")
    return medicines


# ════════════════════════════════════════════════════════
#  SAVE
# ════════════════════════════════════════════════════════

def save_inventory(medicines: list):
    with open(INVENTORY_FILE, "w", encoding="utf-8") as f:
        for m in medicines:
            f.write(
                f"{m['name']}, {m['brand']}, {m['stock']}, "
                f"{int(m['rate_tablet'])}, {int(m['rate_strip'])}, "
                f"{m['tablets_per_strip']}\n"
            )


# ════════════════════════════════════════════════════════
#  DISPLAY
# ════════════════════════════════════════════════════════

def display_inventory(medicines: list):
    TW = tbl_width(_I_W)   # actual rendered width of one row
    banner_w = TW - 2      # subtract the 2-char indent

    print()
    print("  " + "═" * banner_w)
    print("  " + " CURRENT STOCK — MEDSTORE PVT. LTD. ".center(banner_w, "═"))
    print("  " + "═" * banner_w)

    if not medicines:
        print("  (No medicines found in inventory.)")
        print()
        return

    print(tbl_top(_I_W))
    print(tbl_row(_I_HDR, _I_W, _I_AL))
    print(tbl_head_sep(_I_W))

    for i, m in enumerate(medicines, 1):
        cells = [
            str(i),
            m["name"],
            m["brand"],
            str(m["stock"]),
            f"Rs.{m['rate_tablet']:.2f}",
            f"Rs.{m['rate_strip']:.2f}",
            str(m["tablets_per_strip"]),
        ]
        row = tbl_row(cells, _I_W, _I_AL)
        if m["stock"] == 0:
            print(row + "  ◄ OUT OF STOCK")
        else:
            print(row)
        if i < len(medicines):
            print(tbl_mid(_I_W))

    print(tbl_bot(_I_W))
    in_s  = sum(1 for m in medicines if m["stock"] > 0)
    out_s = len(medicines) - in_s
    print(f"  {len(medicines)} medicines listed  |  {in_s} in stock  |  {out_s} out of stock")
    print()


# ════════════════════════════════════════════════════════
#  HELPERS
# ════════════════════════════════════════════════════════

def find_by_index(medicines: list, index: int):
    if 1 <= index <= len(medicines):
        return medicines[index - 1]
    return None

def update_stock(medicines: list, name: str, delta: int):
    """Apply delta (negative=sold, positive=restocked) then save immediately."""
    for m in medicines:
        if m["name"] == name:
            m["stock"] = max(0, m["stock"] + delta)
            break
    save_inventory(medicines)
