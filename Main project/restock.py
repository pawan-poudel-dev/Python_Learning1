"""
restock.py  —  Restock / Purchase Order flow for MedStore Pvt. Ltd.
"""

from modules.utils import (
    ask_int, ask_str, ask_yn, ask_choice,
    tbl_row, tbl_top, tbl_head_sep, tbl_bot, tbl_mid, tbl_span,
    box_top, box_sep, box_bot, box_line,
    banner, rule, ok, warn, info,
    W_CONSOLE,
)
from modules.inventory import display_inventory, find_by_index, update_stock
from modules.invoice import generate_restock_invoice
from modules.logger import log_restock

# ── Order summary table (console, width = 72) ────────────────────────────────
# 5 cols: sum(w) + 3*5 = 69  →  sum = 54
# [20, 6, 4, 10, 14]  sum=54  ✓
# Total=14: 'Rs.13200.00'=11 ✓, Rate=10: 'Rs.228.00'=9 ✓
_O_W   = [20, 6, 4, 10, 14]
_O_AL  = ["l", "l", "r", "r", "r"]
_O_HDR = ["Medicine", "Unit", "Qty", "Rate(Rs)", "Total(Rs)"]


# ════════════════════════════════════════════════════════
#  ORDER SUMMARY DISPLAY
# ════════════════════════════════════════════════════════

def _show_order(items: list):
    BW = W_CONSOLE
    print()
    print(box_top(BW))
    print(box_line("RESTOCK ORDER SUMMARY", BW, "c"))
    print(box_sep(BW))

    print(tbl_top(_O_W))
    print(tbl_row(_O_HDR, _O_W, _O_AL))
    print(tbl_head_sep(_O_W))

    for i, it in enumerate(items, 1):
        unit_lbl = "Strip" if it["unit_type"] == "strip" else "Tablet"
        cells = [
            it["name"],
            unit_lbl,
            str(it["quantity"]),
            f"Rs.{it['rate_per_unit']:.2f}",
            f"Rs.{it['subtotal']:.2f}",
        ]
        print(tbl_row(cells, _O_W, _O_AL))

        detail_parts = [f"Brand: {it['brand']}"]
        if it["unit_type"] == "strip":
            detail_parts.append(
                f"{it['quantity']} x {it['tablets_per_strip']} tabs"
                f" = {it['total_tablets']} tablets"
            )
        else:
            detail_parts.append(f"{it['total_tablets']} tablets to stock")
        print(tbl_span("  " + "  |  ".join(detail_parts), _O_W))

        if i < len(items):
            print(tbl_mid(_O_W))

    print(tbl_bot(_O_W))

    grand      = sum(it["subtotal"]      for it in items)
    total_tabs = sum(it["total_tablets"] for it in items)

    rule()
    lw = 43
    print(f"  {'Total tablets to be added to stock':<{lw}}  {total_tabs:>14}")
    print(f"  {'TOTAL PURCHASE AMOUNT':<{lw}}  Rs. {grand:>10.2f}")
    print(box_bot(BW))
    print()


# ════════════════════════════════════════════════════════
#  MAIN RESTOCK FLOW  —  human-like conversation
# ════════════════════════════════════════════════════════

def run_restock(medicines: list):
    banner("Restock / Purchase Order")
    print("  Let's create a new restock order from a supplier.")
    print("  I'll guide you through each step.\n")

    supplier_name = ask_str("  What is the supplier or vendor's name? → ")
    print(f"\n  Creating purchase order for supplier: {supplier_name}\n")

    order_items = []

    while True:
        display_inventory(medicines)

        print("  Which medicine would you like to restock?")
        med_idx = ask_int(
            f"  Enter the medicine number [1–{len(medicines)}]: → ",
            min_val=1, max_val=len(medicines)
        )
        med = find_by_index(medicines, med_idx)
        tps = med["tablets_per_strip"]

        print()
        rule()
        print(f"  Medicine       : {med['name']}")
        print(f"  Brand          : {med['brand']}")
        print(f"  Current Stock  : {med['stock']} tablets  ({med['stock']//tps} strips)")
        print(f"  Stored Rate/Tab: Rs.{med['rate_tablet']:.2f}")
        print(f"  Stored Rate/Str: Rs.{med['rate_strip']:.2f}  ({tps} tablets per strip)")
        rule()
        print()

        # ── Unit type ────────────────────────────────────────────────
        print("  In what unit is the supplier providing this medicine?")
        unit_type = ask_choice("  Restock in", ["tablet", "strip"])

        # ── Quantity ─────────────────────────────────────────────────
        if unit_type == "tablet":
            print(f"\n  How many tablets are you purchasing from the supplier?")
            quantity = ask_int("  Enter quantity (tablets): → ", min_val=1)
        else:
            print(f"\n  How many strips are you purchasing?  (1 strip = {tps} tablets)")
            quantity = ask_int("  Enter quantity (strips): → ", min_val=1)

        # ── Purchase rate ────────────────────────────────────────────
        stored_rate = med["rate_tablet"] if unit_type == "tablet" else med["rate_strip"]
        print(f"\n  The stored rate is Rs.{stored_rate:.2f} per {unit_type}.")
        if ask_yn("  Is the supplier charging the same rate?"):
            rate_per_unit = stored_rate
        else:
            print(f"  What rate is the supplier charging per {unit_type}?")
            rate_per_unit = float(ask_int("  Enter rate (Rs., whole number): → ", min_val=1))

        # ── Build order line ──────────────────────────────────────────
        total_tablets = quantity if unit_type == "tablet" else quantity * tps
        subtotal      = round(rate_per_unit * quantity, 2)

        item = {
            "name"             : med["name"],
            "brand"            : med["brand"],
            "unit_type"        : unit_type,
            "quantity"         : quantity,
            "rate_per_unit"    : rate_per_unit,
            "tablets_per_strip": tps,
            "total_tablets"    : total_tablets,
            "subtotal"         : subtotal,
        }
        order_items.append(item)

        print()
        rule()
        print(f"  ✔  Added to order:")
        u_str = (f"{quantity} strip(s)  =  {total_tablets} tablets"
                 if unit_type == "strip" else f"{quantity} tablet(s)")
        print(f"     {med['name']}  ({med['brand']})")
        print(f"     Quantity : {u_str}")
        print(f"     Rate     : Rs.{rate_per_unit:.2f} per {unit_type}")
        print(f"     Subtotal : Rs.{subtotal:.2f}")
        rule()
        print()

        if not ask_yn("  Do you want to add another medicine to this order?"):
            break

    if not order_items:
        warn("Order is empty. Restock cancelled.")
        return

    # ── Review & confirm ──────────────────────────────────────────────
    _show_order(order_items)
    print("  Please review the order summary above.")
    if not ask_yn("  Confirm and complete this restock order?"):
        warn("Restock cancelled. No changes have been saved.")
        return

    # ── Add stock & generate PO ───────────────────────────────────────
    for it in order_items:
        update_stock(medicines, it["name"], it["total_tablets"])

    po_no, path = generate_restock_invoice(supplier_name, order_items)
    log_restock(po_no, supplier_name, order_items)

    print()
    rule("═")
    ok("Restock completed successfully!")
    ok(f"Purchase Order No : {po_no}")
    ok(f"Saved to          : {path}")
    ok(f"Stock updated for {len(order_items)} medicine(s).")
    rule("═")
    print()
