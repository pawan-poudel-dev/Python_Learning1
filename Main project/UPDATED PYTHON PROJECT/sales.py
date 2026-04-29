"""
sales.py  —  Sales transaction flow.
             Handles tablet and strip sales, applies 5% strip discount
             for 2+ strips, converts tablets to strips for discount check.
             MedStore Pvt. Ltd. — CS4051NP Coursework SP26
"""

from modules.utils import (
    ask_int, ask_str, ask_yn, ask_choice,
    banner, ok, warn, info,
    STRIP_DISCOUNT, VAT_RATE, W_CONSOLE,
    box_top, box_sep, box_bot, box_line, box_thin,
    append_log
)
from modules.inventory import display_inventory, find_by_index, update_stock
from modules.invoice import generate_sales_invoice


def run_sales(medicines: list):
    """
    Full sales workflow:
      1. Display inventory
      2. Let cashier pick medicines and quantities
      3. Apply 5% strip discount where eligible
         (also checks if tablet qty >= 1 strip worth → auto-flag discount eligibility)
      4. Show checkout preview with itemised discounts
      5. Confirm → update stock → generate invoice (console + file)
    """
    banner("Process Customer Sale")
    cart = []

    while True:
        display_inventory(medicines)

        if not medicines:
            warn("Inventory is empty. Cannot process a sale.")
            return

        idx = ask_int(
            "  Select medicine No. to add to cart  [0 = done]: ",
            min_val=0, max_val=len(medicines)
        )
        if idx == 0:
            break

        med = find_by_index(medicines, idx)

        if med["stock"] <= 0:
            warn(f"'{med['name']}' is currently OUT OF STOCK.")
            continue

        # ── Choose unit ──────────────────────────────────────────────────
        unit = ask_choice("  Sell as", ["tablet", "strip"])

        if unit == "strip":
            max_strips = med["stock"] // med["tablets_per_strip"]
            if max_strips <= 0:
                warn(f"Not enough stock to form even one strip ({med['tablets_per_strip']} tablets needed).")
                continue
            qty = ask_int(
                f"  Quantity (strips)  [max {max_strips}]: ",
                min_val=1, max_val=max_strips
            )
            rate      = med["rate_strip"]
            tabs_used = qty * med["tablets_per_strip"]
        else:
            max_tabs = med["stock"]
            qty = ask_int(
                f"  Quantity (tablets) [max {max_tabs}]: ",
                min_val=1, max_val=max_tabs
            )
            rate      = med["rate_tablet"]
            tabs_used = qty

        # ── Discount logic ───────────────────────────────────────────────
        gross   = qty * rate
        disc_rs = 0.0
        disc_note = ""

        if unit == "strip" and qty >= 2:
            # Direct strip discount: 2+ strips of same medicine
            disc_rs   = round(gross * STRIP_DISCOUNT, 2)
            disc_note = f"5% strip discount ({qty} strips)"
        elif unit == "tablet":
            # Check if tablet qty is equivalent to 2+ strips → apply discount
            equivalent_strips = qty // med["tablets_per_strip"]
            if equivalent_strips >= 2:
                # Calculate the equivalent strip value and apply discount
                equivalent_gross = equivalent_strips * med["rate_strip"]
                disc_rs   = round(equivalent_gross * STRIP_DISCOUNT, 2)
                disc_note = f"5% discount (tablets ≡ {equivalent_strips} strips)"

        net_amt = round(gross - disc_rs, 2)

        cart.append({
            "name"    : med["name"],
            "brand"   : med["brand"],
            "unit"    : unit,
            "qty"     : qty,
            "rate"    : rate,
            "disc_rs" : disc_rs,
            "disc_note": disc_note,
            "amt"     : net_amt,
            "tabs"    : tabs_used,
        })

        # Confirmation line
        disc_info = f"  Discount: Rs.{disc_rs:.2f} ({disc_note})" if disc_rs > 0 else "  No discount applicable."
        ok(f"Added {qty} {unit}(s) of '{med['name']}' to cart.")
        info(disc_info)

        if not ask_yn("  Add another medicine?"):
            break

    if not cart:
        warn("Cart is empty. Sale cancelled.")
        return

    # ── Customer name (collected at end) ─────────────────────────────────
    print()
    customer = ask_str("  Enter customer's full name: ")

    # ── Checkout preview ──────────────────────────────────────────────────
    subtotal_rs   = sum(it["qty"] * it["rate"] for it in cart)
    disc_total_rs = sum(it["disc_rs"] for it in cart)
    taxable       = round(subtotal_rs - disc_total_rs, 2)
    vat_amt       = round(taxable * VAT_RATE, 2)
    grand         = round(taxable + vat_amt, 2)

    print()
    print(box_top(W_CONSOLE))
    print(box_line("SALE CHECKOUT PREVIEW", W_CONSOLE, "c"))
    print(box_sep(W_CONSOLE))
    print(box_line(f"  Customer : {customer}", W_CONSOLE))
    print(box_thin(W_CONSOLE))

    for it in cart:
        line = (
            f"  {it['name']:<22} {it['qty']:>3} {it['unit']:<7}"
            f"  Rate: Rs.{it['rate']:>7.2f}   Net: Rs.{it['amt']:>9.2f}"
        )
        print(box_line(line, W_CONSOLE))
        if it["disc_rs"] > 0:
            disc_line = f"    └─ Disc: Rs.{it['disc_rs']:.2f}  ({it['disc_note']})"
            print(box_line(disc_line, W_CONSOLE))

    print(box_thin(W_CONSOLE))
    print(box_line(f"  {'Gross Subtotal':<38}  Rs. {subtotal_rs:>10.2f}", W_CONSOLE))
    print(box_line(f"  {'Total Strip Discount (5%)':<38}  Rs. {disc_total_rs:>10.2f}", W_CONSOLE))
    print(box_line(f"  {'Taxable Amount':<38}  Rs. {taxable:>10.2f}", W_CONSOLE))
    print(box_line(f"  {'VAT @ 13.0%':<38}  Rs. {vat_amt:>10.2f}", W_CONSOLE))
    print(box_sep(W_CONSOLE))
    print(box_line(f"  {'GRAND TOTAL PAYABLE':<38}  Rs. {grand:>10.2f}", W_CONSOLE, "c"))
    print(box_bot(W_CONSOLE))

    # ── Confirm ───────────────────────────────────────────────────────────
    if ask_yn("  Confirm and finalise this sale?"):
        for it in cart:
            update_stock(medicines, it["name"], -it["tabs"])

        bill_no, path = generate_sales_invoice(customer, cart)
        append_log(
            f"SALE  Invoice:{bill_no}  Customer:{customer}  "
            f"Items:{len(cart)}  Total:Rs.{grand:.2f}"
        )
        ok(f"Sale complete!  Invoice No: {bill_no}")
        info(f"Invoice saved : {path}")
    else:
        warn("Sale cancelled. Stock was not modified.")
