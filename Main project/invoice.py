"""
invoice.py  —  Generate formatted .txt invoice files.

  Sales    →  invoices/sales/MS-INV-XXXX.txt
  Restock  →  invoices/restock/MS-PO-XXXX.txt

VAT (sales only):
  Subtotal       = sum(rate × qty)          per item
  Discount       = 5% × subtotal            when unit=strip AND qty >= 2
  Taxable Amount = Subtotal − Total Discount
  VAT (13%)      = Taxable Amount × 0.13
  Grand Total    = Taxable Amount + VAT
"""

import os
from modules.utils import (
    COMPANY_NAME, COMPANY_SUB, COMPANY_ADDRESS,
    COMPANY_PHONE, COMPANY_EMAIL, COMPANY_PAN, COMPANY_REGD,
    VAT_RATE,
    SALES_DIR, RESTOCK_DIR,
    next_invoice_number, next_po_number,
    now_str,
)

# ═══════════════════════════════════════════════════════════════════════
#  OUTER BOX  ── all invoice text sits inside a double-line box
#  IW  = inner content width  (chars between "║ " and " ║")
#  BOX = full line width      (IW + 4 for "║ " + " ║")
# ═══════════════════════════════════════════════════════════════════════
IW  = 72   # inner content width
BOX = IW + 4   # = 76  (full line: "║ " + 72 + " ║")

def _L(text: str = "", align: str = "l") -> str:
    """A box line: '║ ' + padded text + ' ║'."""
    s = str(text)
    if len(s) > IW: s = s[:IW - 1] + "…"
    return "║ " + (s.center(IW) if align == "c" else s.ljust(IW)) + " ║"

def _otop()  -> str: return "╔" + "═" * (IW + 2) + "╗"
def _osep()  -> str: return "╠" + "═" * (IW + 2) + "╣"
def _othin() -> str: return "╟" + "─" * (IW + 2) + "╢"
def _obot()  -> str: return "╚" + "═" * (IW + 2) + "╝"


# ═══════════════════════════════════════════════════════════════════════
#  INNER ITEM TABLE
#
#  Row formula:  "  │" + join(" cell │")
#  width = 3 + sum(w+2 per col) + ncols
#        = 3 + sum(w) + 3*ncols
#
#  Invoice file: target width = 80
#    sum(w) + 3*ncols = 77
#
#  Sales   6 cols: sum = 77 - 18 = 59  →  [20, 7, 5, 9, 8, 10]  ✓
#    Medicine(20) Unit(7) Qty(5) Rate(9) Disc(8) Amt(10)
#    Worst values: 'Levofloxacin 500mg'=18≤20 ✓  'Rs.228.00'=9≤9 ✓  'Rs.1083.00'=10≤10 ✓
#
#  Restock 5 cols: sum = 77 - 15 = 62  →  [22, 7, 5, 12, 16]
#    But we want tighter for readability. 5 cols width=80:
#    sum=62: [22, 7, 5, 12, 16] → Total col 16 is wastefully wide.
#    Better: [22, 7, 5, 14, 14] sum=62 ✓  or even use 6 cols at width 78:
#    6 cols width=78: sum = 78-3-18 = 57  →  [20, 7, 5, 9, 8, 8] sum=57, width=78
#    Amt=8: Rs.6840.00=10>8 ✗.  [20, 7, 5, 9, 6, 10]=57, Disc=6 but no disc for restock.
#    Restock: just 5 cols. sum for width 78 = 78-3-15=60. [22,7,5,12,14] sum=60 ✓
#    Total=14: 'Rs.13200.00'=11≤14 ✓
# ═══════════════════════════════════════════════════════════════════════

_S_W   = [20, 7, 5, 9, 8, 10]   # Sales: Medicine|Unit|Qty|Rate|Disc|Amt
_S_AL  = ["l", "l", "r", "r", "r", "r"]
_S_HDR = ["Medicine", "Unit", "Qty", "Rate(Rs)", "Disc(Rs)", "Amt(Rs)"]

_P_W   = [22, 7, 5, 12, 14]     # Restock: Medicine|Unit|Qty|Rate|Total
_P_AL  = ["l", "l", "r", "r", "r"]
_P_HDR = ["Medicine", "Unit", "Qty", "Rate(Rs)", "Total(Rs)"]


def _trow(cells, cols, align):
    parts = []
    for i, (cell, w) in enumerate(zip(cells, cols)):
        s = str(cell)
        if len(s) > w: s = s[:w-1] + "…"
        a = align[i] if i < len(align) else "l"
        parts.append(" " + (s.rjust(w) if a == "r" else s.ljust(w)) + " ")
    return "  │" + "│".join(parts) + "│"

def _ttop(c)  -> str: return "  ┌" + "┬".join("─"*(w+2) for w in c) + "┐"
def _thsep(c) -> str: return "  ╞" + "╪".join("═"*(w+2) for w in c) + "╡"
def _tmid(c)  -> str: return "  ├" + "┼".join("─"*(w+2) for w in c) + "┤"
def _tbot(c)  -> str: return "  └" + "┴".join("─"*(w+2) for w in c) + "┘"

def _tspan(text: str, cols: list) -> str:
    inner = sum(w + 2 for w in cols) + (len(cols) - 1) - 2
    s = str(text)
    if len(s) > inner: s = s[:inner-1] + "…"
    return "  │ " + s.ljust(inner) + " │"


# ═══════════════════════════════════════════════════════════════════════
#  FILE WRITER
# ═══════════════════════════════════════════════════════════════════════

def _write(directory: str, filename: str, content: str) -> str:
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


# ═══════════════════════════════════════════════════════════════════════
#  SHARED COMPANY HEADER
# ═══════════════════════════════════════════════════════════════════════

def _header(bill_no: str, bill_type: str, timestamp: str) -> list:
    return [
        _otop(),
        _L(COMPANY_NAME, "c"),
        _L(COMPANY_SUB,  "c"),
        _L(),
        _L(f"  Address : {COMPANY_ADDRESS}"),
        _L(f"  Phone   : {COMPANY_PHONE}"),
        _L(f"  Email   : {COMPANY_EMAIL}"),
        _L(f"  {COMPANY_PAN}    {COMPANY_REGD}"),
        _osep(),
        _L(bill_type, "c"),
        _othin(),
        _L(f"  Bill No : {bill_no}"),
        _L(f"  Date    : {timestamp}"),
        _othin(),
    ]


# ═══════════════════════════════════════════════════════════════════════
#  SALES INVOICE  →  MS-INV-XXXX
# ═══════════════════════════════════════════════════════════════════════

def generate_sales_invoice(customer_name: str, items: list) -> tuple:
    """
    items: each dict must have:
      name, brand, unit_type, quantity, rate_per_unit,
      tablets_per_strip, tablets_sold,
      subtotal_before_discount, discount_amount, subtotal_after_discount
    Returns (bill_no, file_path).
    """
    bill_no   = next_invoice_number()
    timestamp = now_str()

    L = _header(bill_no, "VAT SALES INVOICE", timestamp)
    L.append(_L(f"  Customer : {customer_name}"))
    L.append(_othin())

    C, A = _S_W, _S_AL
    L.append(_ttop(C))
    L.append(_trow(_S_HDR, C, A))
    L.append(_thsep(C))

    sub_total  = 0.0
    disc_total = 0.0

    for idx, it in enumerate(items, 1):
        unit = "Strip" if it["unit_type"] == "strip" else "Tablet"
        cells = [
            f"{idx}. {it['name']}",
            unit,
            str(it["quantity"]),
            f"Rs.{it['rate_per_unit']:.2f}",
            f"Rs.{it['discount_amount']:.2f}",
            f"Rs.{it['subtotal_after_discount']:.2f}",
        ]
        L.append(_trow(cells, C, A))

        # Detail / sub-info row
        detail_parts = [f"Brand: {it['brand']}"]
        if it["unit_type"] == "strip":
            tps = it["tablets_per_strip"]
            detail_parts.append(
                f"{it['quantity']} strip(s) x {tps} tabs = {it['tablets_sold']} tablets"
            )
            if it["discount_amount"] > 0:
                detail_parts.append("5% bulk-strip discount applied")
        L.append(_tspan("   " + "   |   ".join(detail_parts), C))

        if idx < len(items):
            L.append(_tmid(C))

        sub_total  += it["subtotal_before_discount"]
        disc_total += it["discount_amount"]

    L.append(_tbot(C))

    taxable = round(sub_total - disc_total, 2)
    vat     = round(taxable * VAT_RATE, 2)
    grand   = round(taxable + vat, 2)

    L.append(_othin())
    L.append(_L(f"  {'Subtotal':<38}  Rs. {sub_total:>10.2f}"))
    L.append(_L(f"  {'Total Discount  (5% on 2+ strips)':<38}  Rs. {disc_total:>10.2f}"))
    L.append(_L(f"  {'Taxable Amount':<38}  Rs. {taxable:>10.2f}"))
    L.append(_L(f"  {'VAT @ 13%':<38}  Rs. {vat:>10.2f}"))
    L.append(_osep())
    L.append(_L(f"  {'GRAND TOTAL':<38}  Rs. {grand:>10.2f}"))
    L.append(_othin())
    L.append(_L())
    L.append(_L("Thank you for your purchase!", "c"))
    L.append(_L("This is a system-generated VAT invoice.", "c"))
    L.append(_L())
    L.append(_obot())

    content = "\n".join(L) + "\n"
    return bill_no, _write(SALES_DIR, f"{bill_no}.txt", content)


# ═══════════════════════════════════════════════════════════════════════
#  RESTOCK / PURCHASE ORDER  →  MS-PO-XXXX
# ═══════════════════════════════════════════════════════════════════════

def generate_restock_invoice(supplier_name: str, items: list) -> tuple:
    """
    items: each dict must have:
      name, brand, unit_type, quantity, rate_per_unit,
      tablets_per_strip, total_tablets, subtotal
    Returns (po_no, file_path).
    """
    po_no     = next_po_number()
    timestamp = now_str()

    L = _header(po_no, "PURCHASE ORDER / RESTOCK NOTE", timestamp)
    L.append(_L(f"  Supplier : {supplier_name}"))
    L.append(_othin())

    C, A = _P_W, _P_AL
    L.append(_ttop(C))
    L.append(_trow(_P_HDR, C, A))
    L.append(_thsep(C))

    grand      = 0.0
    total_tabs = 0

    for idx, it in enumerate(items, 1):
        unit  = "Strip" if it["unit_type"] == "strip" else "Tablet"
        cells = [
            f"{idx}. {it['name']}",
            unit,
            str(it["quantity"]),
            f"Rs.{it['rate_per_unit']:.2f}",
            f"Rs.{it['subtotal']:.2f}",
        ]
        L.append(_trow(cells, C, A))

        detail = [f"Brand: {it['brand']}"]
        if it["unit_type"] == "strip":
            detail.append(
                f"{it['quantity']} x {it['tablets_per_strip']} tabs = {it['total_tablets']} tablets added"
            )
        else:
            detail.append(f"{it['total_tablets']} tablets added to stock")
        L.append(_tspan("   " + "   |   ".join(detail), C))

        if idx < len(items):
            L.append(_tmid(C))

        grand      += it["subtotal"]
        total_tabs += it["total_tablets"]

    L.append(_tbot(C))

    L.append(_othin())
    L.append(_L(f"  {'Total tablets added to stock':<38}  {'':>10}{total_tabs:>6} tablets"))
    L.append(_L(f"  {'TOTAL PURCHASE AMOUNT':<38}  Rs. {grand:>10.2f}"))
    L.append(_othin())
    L.append(_L())
    L.append(_L("Stock has been updated in the inventory.", "c"))
    L.append(_L("This is a system-generated purchase order.", "c"))
    L.append(_L())
    L.append(_obot())

    content = "\n".join(L) + "\n"
    return po_no, _write(RESTOCK_DIR, f"{po_no}.txt", content)
