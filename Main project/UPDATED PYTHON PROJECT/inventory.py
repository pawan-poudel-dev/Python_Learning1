"""
inventory.py  —  Load, save, display, add, and delete medicines.
                 MedStore Pvt. Ltd. — CS4051NP Coursework SP26

Inventory file format (CSV per line):
  Name, Brand, Stock(tablets), Rate/Tablet, Rate/Strip, Tablets/Strip
"""

import os
from modules.utils import (
    INVENTORY_FILE, DATA_DIR,
    tbl_row, tbl_top, tbl_head_sep, tbl_mid, tbl_bot, tbl_width,
    warn, ok, info, err, ask_yn, ask_int, ask_float, ask_str,
    W_CONSOLE, box_top, box_sep, box_bot, box_line, append_log
)

# ── Table column widths and alignment ───────────────────────────────────────
# Widths chosen so nothing truncates: Rs.150.00=9, Tab/Strip=9, R/Strip=10
_COL_W   = [3, 22, 16, 7, 9, 10, 9]
_COL_AL  = ["r", "l", "l", "r", "r", "r", "r"]
_COL_HDR = ["No", "Medicine Name", "Brand", "Stock", "R/Tab", "R/Strip", "Tab/Strip"]


# ════════════════════════════════════════════════════════════════════════════
#  LOAD
# ════════════════════════════════════════════════════════════════════════════

def load_inventory() -> list:
    """
    Read inventory.txt and return a list of medicine dictionaries.
    Skips blank lines and comment lines starting with '#'.
    """
    medicines = []
    if not os.path.exists(INVENTORY_FILE):
        warn(f"Inventory file not found: {INVENTORY_FILE}")
        return medicines

    with open(INVENTORY_FILE, "r", encoding="utf-8") as f:
        for line_no, raw in enumerate(f, 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split(",")]
            if len(parts) < 6:
                warn(f"Line {line_no}: too few fields, skipped.")
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
            except (ValueError, IndexError) as exc:
                warn(f"Line {line_no}: parse error ({exc}), skipped.")
    return medicines


# ════════════════════════════════════════════════════════════════════════════
#  SAVE
# ════════════════════════════════════════════════════════════════════════════

def save_inventory(medicines: list):
    """Persist the current in-memory inventory list back to inventory.txt."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(INVENTORY_FILE, "w", encoding="utf-8") as f:
        f.write("# MedStore Pvt. Ltd. — Inventory File\n")
        f.write("# Format: Name, Brand, Stock(tablets), Rate/Tablet, Rate/Strip, Tablets/Strip\n")
        for m in medicines:
            f.write(
                f"{m['name']}, {m['brand']}, {m['stock']}, "
                f"{m['rate_tablet']:.2f}, {m['rate_strip']:.2f}, {m['tablets_per_strip']}\n"
            )


# ════════════════════════════════════════════════════════════════════════════
#  DISPLAY
# ════════════════════════════════════════════════════════════════════════════

def display_inventory(medicines: list):
    """Print a formatted inventory table to the console."""
    TW = tbl_width(_COL_W)

    print()
    print("  " + "═" * (TW - 2))
    print("  " + " MEDSTORE Pvt. Ltd. — MEDICINE INVENTORY ".center(TW - 2, "═"))
    print("  " + "═" * (TW - 2))

    if not medicines:
        print("  (Inventory is empty — no medicines loaded)")
        return

    print(tbl_top(_COL_W))
    print(tbl_row(_COL_HDR, _COL_W, _COL_AL))
    print(tbl_head_sep(_COL_W))

    alerts = []

    for i, m in enumerate(medicines, 1):
        tags = []

        # Stock alert flags
        if m["stock"] == 0:
            tags.append("OUT OF STOCK")
        elif m["stock"] < 20:
            tags.append("LOW STOCK")
            alerts.append(f"  ⚠  Low stock: {m['name']} — only {m['stock']} tablet(s) left.")

        tag_str = "  ◄ " + " | ".join(tags) if tags else ""

        cells = [
            str(i),
            m["name"],
            m["brand"],
            str(m["stock"]),
            f"Rs.{m['rate_tablet']:.2f}",
            f"Rs.{m['rate_strip']:.2f}",
            str(m["tablets_per_strip"]),
        ]
        print(tbl_row(cells, _COL_W, _COL_AL) + tag_str)
        if i < len(medicines):
            print(tbl_mid(_COL_W))

    print(tbl_bot(_COL_W))

    if alerts:
        print()
        for a in alerts:
            print(a)

    print(f"\n  Total medicines in inventory: {len(medicines)}")
    print()


# ════════════════════════════════════════════════════════════════════════════
#  ADD NEW MEDICINE
# ════════════════════════════════════════════════════════════════════════════

def add_new_medicine(medicines: list):
    """
    Smart add / restock logic:

      Case 1 — Same name AND same brand already exists
               → Update (add to) existing stock. Optionally update rates.
               → No new row is created.

      Case 2 — Same name BUT different brand
               → Inform the user that this name exists under other brand(s).
               → Add as a brand-new separate row in the inventory.

      Case 3 — Completely new name
               → Add as a new row directly.
    """
    from modules.utils import banner
    banner("Add / Update Medicine")

    name  = ask_str("  Medicine name : ")
    brand = ask_str("  Brand name    : ")

    name_key  = name.lower().strip()
    brand_key = brand.lower().strip()

    # ── Find all rows that share the same name ────────────────────────────
    same_name = [m for m in medicines if m["name"].lower().strip() == name_key]

    # ── CASE 1: Exact match — same name AND same brand ────────────────────
    exact = next(
        (m for m in same_name if m["brand"].lower().strip() == brand_key),
        None
    )

    if exact:
        print()
        print(box_top(W_CONSOLE))
        print(box_line("EXISTING ENTRY FOUND — SAME NAME & BRAND", W_CONSOLE, "c"))
        print(box_sep(W_CONSOLE))
        print(box_line(f"  Medicine  : {exact['name']}", W_CONSOLE))
        print(box_line(f"  Brand     : {exact['brand']}", W_CONSOLE))
        print(box_line(f"  Stock now : {exact['stock']} tablet(s)", W_CONSOLE))
        print(box_line(f"  R/Tablet  : Rs.{exact['rate_tablet']:.2f}", W_CONSOLE))
        print(box_line(f"  R/Strip   : Rs.{exact['rate_strip']:.2f}  ({exact['tablets_per_strip']} tabs/strip)", W_CONSOLE))
        print(box_bot(W_CONSOLE))

        info("This medicine (same name & brand) already exists.")
        info("Stock will be added to the existing entry — no duplicate row will be created.")
        print()

        add_qty = ask_int("  Tablets to add to existing stock [0 to cancel]: ", min_val=0)
        if add_qty == 0:
            warn("No stock added. Operation cancelled.")
            return

        # Optionally update rates
        if ask_yn("  Do you want to update the rates as well?"):
            rate_tablet = ask_float(
                f"  New rate per tablet (Rs.) [current Rs.{exact['rate_tablet']:.2f}]: ",
                min_val=0.01
            )
            tabs_per_strip = exact["tablets_per_strip"]
            rate_strip = ask_float(
                f"  New rate per strip (Rs.) [{tabs_per_strip} tabs, current Rs.{exact['rate_strip']:.2f}]: ",
                min_val=0.01
            )
            exact["rate_tablet"] = rate_tablet
            exact["rate_strip"]  = rate_strip

        old_stock     = exact["stock"]
        exact["stock"] += add_qty
        new_stock      = exact["stock"]

        # Preview
        print()
        print(box_top(W_CONSOLE))
        print(box_line("STOCK UPDATE PREVIEW", W_CONSOLE, "c"))
        print(box_sep(W_CONSOLE))
        print(box_line(f"  Medicine     : {exact['name']}  ({exact['brand']})", W_CONSOLE))
        print(box_line(f"  Stock Before : {old_stock} tablet(s)", W_CONSOLE))
        print(box_line(f"  Added        : {add_qty} tablet(s)", W_CONSOLE))
        print(box_line(f"  Stock After  : {new_stock} tablet(s)", W_CONSOLE))
        print(box_line(f"  R/Tablet     : Rs.{exact['rate_tablet']:.2f}", W_CONSOLE))
        print(box_line(f"  R/Strip      : Rs.{exact['rate_strip']:.2f}", W_CONSOLE))
        print(box_bot(W_CONSOLE))

        if ask_yn("  Confirm and save this stock update?"):
            save_inventory(medicines)
            append_log(
                f"STOCK UPDATE: {exact['name']} ({exact['brand']})  "
                f"{old_stock} + {add_qty} = {new_stock} tablets"
            )
            ok(f"Stock updated! '{exact['name']}' ({exact['brand']}) now has {new_stock} tablet(s).")
        else:
            # Rollback the in-memory change
            exact["stock"] = old_stock
            exact["rate_tablet"] = exact["rate_tablet"]
            warn("Update cancelled. No changes saved.")
        return

    # ── CASE 2: Same name, different brand ───────────────────────────────
    if same_name:
        print()
        info(f"'{name}' already exists under different brand(s):")
        for m in same_name:
            print(f"    • {m['brand']:<20} — Stock: {m['stock']} tablets")
        print()
        info(f"Brand '{brand}' is NEW — this will be added as a separate row.")
        print()

    # ── CASE 2 & 3: Collect details and add new row ───────────────────────
    stock             = ask_int("  Initial stock (tablets): ", min_val=0)
    rate_tablet       = ask_float("  Rate per tablet (Rs.)  : ", min_val=0.01)
    tablets_per_strip = ask_int("  Tablets per strip      : ", min_val=1)
    rate_strip        = ask_float(
        f"  Rate per strip (Rs.)   [{tablets_per_strip} tabs, suggested Rs.{rate_tablet * tablets_per_strip:.2f}]: ",
        min_val=0.01
    )

    new_med = {
        "name"             : name,
        "brand"            : brand,
        "stock"            : stock,
        "rate_tablet"      : rate_tablet,
        "rate_strip"       : rate_strip,
        "tablets_per_strip": tablets_per_strip,
    }

    # Preview
    action = "RESTOCK — NEW BRAND VARIANT" if same_name else "NEW MEDICINE PREVIEW"
    print()
    print(box_top(W_CONSOLE))
    print(box_line(action, W_CONSOLE, "c"))
    print(box_sep(W_CONSOLE))
    print(box_line(f"  Name          : {name}", W_CONSOLE))
    print(box_line(f"  Brand         : {brand}", W_CONSOLE))
    print(box_line(f"  Initial Stock : {stock} tablet(s)", W_CONSOLE))
    print(box_line(f"  R/Tablet      : Rs.{rate_tablet:.2f}", W_CONSOLE))
    print(box_line(f"  R/Strip       : Rs.{rate_strip:.2f}  ({tablets_per_strip} tabs/strip)", W_CONSOLE))
    print(box_bot(W_CONSOLE))

    if ask_yn("  Confirm and save?"):
        medicines.append(new_med)
        save_inventory(medicines)
        append_log(f"ADD: {name} ({brand}), stock={stock}")
        if same_name:
            ok(f"'{name}' ({brand}) added as a new brand variant — separate row created.")
        else:
            ok(f"'{name}' ({brand}) added to inventory.")
    else:
        warn("Operation cancelled.")


# ════════════════════════════════════════════════════════════════════════════
#  DELETE MEDICINE
# ════════════════════════════════════════════════════════════════════════════

def delete_medicine(medicines: list):
    """Prompt the user to select and confirm deletion of a medicine."""
    from modules.utils import banner
    banner("Delete Medicine")
    display_inventory(medicines)

    if not medicines:
        return

    idx = ask_int(
        "  Enter medicine No. to delete [0 = cancel]: ",
        min_val=0, max_val=len(medicines)
    )
    if idx == 0:
        info("Delete cancelled.")
        return

    med = medicines[idx - 1]
    print()
    warn(f"You are about to permanently delete: '{med['name']}' ({med['brand']})")

    if ask_yn("  Are you sure?"):
        removed = medicines.pop(idx - 1)
        save_inventory(medicines)
        append_log(f"DELETE medicine: {removed['name']} ({removed['brand']})")
        ok(f"'{removed['name']}' has been deleted from the inventory.")
    else:
        info("Delete cancelled.")


# ════════════════════════════════════════════════════════════════════════════
#  HELPERS FOR OTHER MODULES
# ════════════════════════════════════════════════════════════════════════════

def find_by_index(medicines: list, index: int) -> dict | None:
    """Return the medicine at 1-based index, or None if out of range."""
    if 1 <= index <= len(medicines):
        return medicines[index - 1]
    return None


def update_stock(medicines: list, name: str, delta: int):
    """
    Adjust stock for a medicine by delta (positive = add, negative = deduct).
    Saves inventory after update.
    """
    for m in medicines:
        if m["name"] == name:
            m["stock"] = max(0, m["stock"] + delta)
            break
    save_inventory(medicines)
