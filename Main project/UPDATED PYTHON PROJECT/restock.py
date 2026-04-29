"""
restock.py  —  Restock / Purchase-Order flow (buying from a supplier).
               MedStore Pvt. Ltd. — CS4051NP Coursework SP26
"""

from modules.utils import (
    ask_int, ask_float, ask_str, ask_yn, ask_choice,
    banner, ok, warn, info, append_log
)
from modules.inventory import display_inventory, find_by_index, save_inventory
from modules.invoice import generate_restock_invoice


def run_restock(medicines: list):
    """
    Full restock workflow:
      1. Collect supplier name
      2. Let user pick medicines and quantities (tablet or strip)
      3. Optionally update the purchase rate
      4. Confirm → update stock → generate PO invoice (console + file)
    """
    banner("Restock Inventory — Purchase from Supplier")

    supplier = ask_str("  Enter supplier / vendor name: ")
    order_items = []

    while True:
        display_inventory(medicines)

        idx = ask_int(
            "  Select medicine No. to restock  [0 = done]: ",
            min_val=0, max_val=len(medicines)
        )
        if idx == 0:
            break

        med = find_by_index(medicines, idx)

        # ── Choose unit ──────────────────────────────────────────────────
        unit = ask_choice("  Restock unit", ["tablet", "strip"])

        qty = ask_int(f"  Quantity to order ({unit}s): ", min_val=1)

        # ── Confirm or update purchase rate ──────────────────────────────
        stored_rate = med["rate_tablet"] if unit == "tablet" else med["rate_strip"]
        info(f"Current rate on record: Rs.{stored_rate:.2f} per {unit}.")
        if ask_yn("  Is this purchase rate still valid?"):
            rate = stored_rate
        else:
            rate = ask_float(f"  Enter new purchase rate per {unit} (Rs.): ", min_val=0.01)

        # Tablets added to stock
        tabs_added = qty if unit == "tablet" else qty * med["tablets_per_strip"]

        order_items.append({
            "name" : med["name"],
            "brand": med["brand"],
            "unit" : unit,
            "qty"  : qty,
            "rate" : rate,
            "tabs" : tabs_added,
        })

        cost = qty * rate
        ok(f"Added to PO: {qty} {unit}(s) of '{med['name']}' @ Rs.{rate:.2f}  =  Rs.{cost:.2f}")

        if not ask_yn("  Add another medicine to this purchase order?"):
            break

    if not order_items:
        warn("No items selected. Restock cancelled.")
        return

    # ── Summary ───────────────────────────────────────────────────────────
    total_cost = sum(it["qty"] * it["rate"] for it in order_items)
    print()
    info(f"Purchase Order Summary: {len(order_items)} line(s), Total: Rs.{total_cost:.2f}")

    if ask_yn("  Confirm and finalise this purchase order?"):
        # Update stock for each ordered medicine
        for it in order_items:
            for m in medicines:
                if m["name"] == it["name"]:
                    m["stock"] += it["tabs"]
                    break

        save_inventory(medicines)

        po_no, path = generate_restock_invoice(supplier, order_items)
        append_log(
            f"RESTOCK  PO:{po_no}  Supplier:{supplier}  "
            f"Items:{len(order_items)}  Total:Rs.{total_cost:.2f}"
        )
        ok(f"Restock complete!  PO No: {po_no}")
        info(f"PO saved at  : {path}")
    else:
        warn("Restock cancelled. Stock was not modified.")
