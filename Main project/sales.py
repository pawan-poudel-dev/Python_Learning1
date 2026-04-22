"""
sales.py  —  Complete sales transaction flow.

Discount:  5% off item subtotal  when unit_type == 'strip' AND qty >= 2
VAT:       13% on (subtotal - total_discount)
"""

from modules.utils import (
    VAT_RATE, STRIP_DISCOUNT,
    ask_int, ask_str, ask_yn, ask_choice,
    tbl_row, tbl_top, tbl_head_sep, tbl_bot, tbl_mid, tbl_span,
    box_top, box_sep, box_bot, box_line,
    banner, rule, ok, warn, info,
    W_CONSOLE,
)
from modules.inventory import display_inventory, find_by_index, update_stock
from modules.invoice import generate_sales_invoice
from modules.logger import log_sale

# ── Cart display table columns (console, width = 72) ──────────────────────────
# 6 cols: sum(w) + 3*6 = 69  →  sum = 51
# [14, 6, 4, 9, 8, 10]  sum=51  ✓
# Worst: 'Levofloxaci…'(truncated ok), Rs.228.00=9 ✓, Rs.1083.00=10 ✓
_C_W   = [14, 6, 4, 9, 8, 10]
_C_AL  = ["l", "l", "r", "r", "r", "r"]
_C_HDR = ["Medicine", "Unit", "Qty", "Rate(Rs)", "Disc(Rs)", "Amt(Rs)"]


# ════════════════════════════════════════════════════════
#  PRICING HELPER
# ════════════════════════════════════════════════════════

def _build_item(med: dict, unit_type: str, quantity: int) -> dict:
    """
    Compute all price fields for one cart line.
    Discount rule: 5% off subtotal when unit=strip AND qty >= 2.
    """
    tps = med["tablets_per_strip"]
    if unit_type == "tablet":
        rate_per_unit = med["rate_tablet"]
        tablets_sold  = quantity
    else:
        rate_per_unit = med["rate_strip"]
        tablets_sold  = quantity * tps

    subtotal_before = round(rate_per_unit * quantity, 2)
    eligible        = (unit_type == "strip" and quantity >= 2)
    discount_amount = round(subtotal_before * STRIP_DISCOUNT, 2) if eligible else 0.0
    subtotal_after  = round(subtotal_before - discount_amount, 2)

    return {
        "name"                    : med["name"],
        "brand"                   : med["brand"],
        "unit_type"               : unit_type,
        "quantity"                : quantity,
        "rate_per_unit"           : rate_per_unit,
        "tablets_per_strip"       : tps,
        "tablets_sold"            : tablets_sold,
        "subtotal_before_discount": subtotal_before,
        "discount_amount"         : discount_amount,
        "subtotal_after_discount" : subtotal_after,
    }


# ════════════════════════════════════════════════════════
#  CART DISPLAY
# ════════════════════════════════════════════════════════

def _show_cart(cart: list):
    BW = W_CONSOLE  # box width
    print()
    print(box_top(BW))
    print(box_line("CART SUMMARY", BW, "c"))
    print(box_sep(BW))

    print(tbl_top(_C_W))
    print(tbl_row(_C_HDR, _C_W, _C_AL))
    print(tbl_head_sep(_C_W))

    for i, it in enumerate(cart, 1):
        unit_lbl = "Strip" if it["unit_type"] == "strip" else "Tablet"
        cells = [
            it["name"],
            unit_lbl,
            str(it["quantity"]),
            f"Rs.{it['rate_per_unit']:.2f}",
            f"Rs.{it['discount_amount']:.2f}",
            f"Rs.{it['subtotal_after_discount']:.2f}",
        ]
        print(tbl_row(cells, _C_W, _C_AL))

        detail_parts = [f"Brand: {it['brand']}"]
        if it["unit_type"] == "strip":
            detail_parts.append(
                f"{it['quantity']} strip(s) x {it['tablets_per_strip']} tabs"
                f" = {it['tablets_sold']} tablets"
            )
            if it["discount_amount"] > 0:
                detail_parts.append("5% bulk discount")
        print(tbl_span("  " + "  |  ".join(detail_parts), _C_W))

        if i < len(cart):
            print(tbl_mid(_C_W))

    print(tbl_bot(_C_W))

    sub_total  = sum(it["subtotal_before_discount"] for it in cart)
    disc_total = sum(it["discount_amount"]           for it in cart)
    taxable    = round(sub_total - disc_total, 2)
    vat        = round(taxable * VAT_RATE, 2)
    grand      = round(taxable + vat, 2)

    rule()
    lw = 43  # label width
    print(f"  {'Subtotal':<{lw}}  Rs. {sub_total:>10.2f}")
    print(f"  {'Total Discount  (5% on 2+ strips)':<{lw}}  Rs. {disc_total:>10.2f}")
    print(f"  {'Taxable Amount':<{lw}}  Rs. {taxable:>10.2f}")
    print(f"  {'VAT @ 13%':<{lw}}  Rs. {vat:>10.2f}")
    rule("═")
    print(f"  {'GRAND TOTAL':<{lw}}  Rs. {grand:>10.2f}")
    print(box_bot(BW))
    print()


# ════════════════════════════════════════════════════════
#  MAIN SALES FLOW  —  human-like conversation
# ════════════════════════════════════════════════════════

def run_sales(medicines: list):
    banner("New Sales Transaction")
    print("  Hello! Let's record a new sale.")
    print("  I'll walk you through it step by step.\n")

    customer_name = ask_str("  What is the customer's full name? → ")
    print(f"\n  Got it! Starting sale for: {customer_name}\n")

    cart = []

    while True:
        display_inventory(medicines)

        if all(m["stock"] == 0 for m in medicines):
            warn("All medicines are currently out of stock. Cannot process this sale.")
            return

        print("  Which medicine would you like to add to the cart?")
        med_idx = ask_int(
            f"  Enter the medicine number [1–{len(medicines)}]: → ",
            min_val=1, max_val=len(medicines)
        )
        med = find_by_index(medicines, med_idx)

        if med["stock"] == 0:
            warn(f"'{med['name']}' is out of stock right now. Please choose another.")
            continue

        tps        = med["tablets_per_strip"]
        max_tabs   = med["stock"]
        max_strips = max_tabs // tps

        print()
        rule()
        print(f"  Medicine  : {med['name']}")
        print(f"  Brand     : {med['brand']}")
        print(f"  In Stock  : {max_tabs} tablets  ({max_strips} full strip(s) of {tps} tablets each)")
        print(f"  Per Tablet: Rs. {med['rate_tablet']:.2f}")
        print(f"  Per Strip : Rs. {med['rate_strip']:.2f}"
              f"   ← Buy 2 or more strips to get a 5% discount!")
        rule()
        print()

        # ── Unit type ────────────────────────────────────────────────
        print("  How would the customer like to buy this medicine?")
        unit_type = ask_choice("  Sell as", ["tablet", "strip"])

        # ── Quantity ─────────────────────────────────────────────────
        if unit_type == "tablet":
            print(f"\n  How many tablets does the customer need?")
            print(f"  (Max available: {max_tabs} tablets)")
            quantity = ask_int("  Enter quantity (tablets): → ", min_val=1, max_val=max_tabs)

            # Tip when buying enough for 2+ strips
            if max_strips >= 2 and quantity >= 2 * tps:
                possible = quantity // tps
                saving   = round(possible * med["rate_strip"] * STRIP_DISCOUNT, 2)
                info(f"Tip: {possible} strips cover {possible*tps} tablets "
                     f"and would save Rs.{saving:.2f} with the 5% bulk discount.")

        else:   # strip
            if max_strips == 0:
                warn(f"Not enough stock to complete even 1 strip "
                     f"(need {tps} tablets, only {max_tabs} left).")
                print("  Switching to tablet mode for this item.\n")
                unit_type = "tablet"
                quantity  = ask_int(
                    f"  Enter quantity (tablets) [max {max_tabs}]: → ",
                    min_val=1, max_val=max_tabs
                )
            else:
                print(f"\n  How many strips does the customer need?")
                print(f"  (Max available: {max_strips} strips  |  each = {tps} tablets)")
                if max_strips >= 2:
                    info("Buying 2 or more strips gives a 5% discount on this item!")
                quantity = ask_int("  Enter quantity (strips): → ", min_val=1, max_val=max_strips)

        # ── Build item & preview ──────────────────────────────────────
        item = _build_item(med, unit_type, quantity)
        print()
        rule()
        print(f"  ✔  Added to cart:")
        u_str = (f"{quantity} strip(s)  =  {item['tablets_sold']} tablets"
                 if unit_type == "strip" else f"{quantity} tablet(s)")
        print(f"     {med['name']}  ({med['brand']})")
        print(f"     Quantity : {u_str}")
        print(f"     Rate     : Rs.{item['rate_per_unit']:.2f} per {unit_type}")
        print(f"     Subtotal : Rs.{item['subtotal_before_discount']:.2f}", end="")
        if item["discount_amount"] > 0:
            print(f"  −  Rs.{item['discount_amount']:.2f} discount"
                  f"  =  Rs.{item['subtotal_after_discount']:.2f}  (5% strip discount!)")
        else:
            print()
        rule()
        cart.append(item)

        print()
        if not ask_yn("  Would the customer like to add another medicine?"):
            break

    if not cart:
        warn("Cart is empty. No transaction was recorded.")
        return

    # ── Review & confirm ──────────────────────────────────────────────
    _show_cart(cart)
    print("  Please review the cart summary above.")
    if not ask_yn("  Confirm and finalise this sale?"):
        warn("Transaction cancelled. No changes have been saved.")
        return

    # ── Deduct stock & generate invoice ──────────────────────────────
    for it in cart:
        update_stock(medicines, it["name"], -it["tablets_sold"])

    bill_no, path = generate_sales_invoice(customer_name, cart)
    log_sale(bill_no, customer_name, cart)

    print()
    rule("═")
    ok("Sale completed successfully!")
    ok(f"Invoice No  : {bill_no}")
    ok(f"Saved to    : {path}")
    ok(f"Stock updated for {len(cart)} item(s).")
    rule("═")
    print()
