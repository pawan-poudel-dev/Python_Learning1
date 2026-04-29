"""
invoice.py  —  Generate VAT sales invoices and restock purchase orders.
               Both are printed to console AND saved as .txt files.
               MedStore Pvt. Ltd. — CS4051NP Coursework SP26

Invoice layout:
  ╔══ Company Header ══╗
  ╠══ Invoice Details ══╣
  ╟── Item Table ──────╢
  ╟── Discount Block ──╢
  ╠══ Totals ══════════╣
  ╚════════════════════╝
"""

import os
from modules.utils import (
    COMPANY_NAME, COMPANY_SUB, COMPANY_ADDRESS, COMPANY_PHONE,
    COMPANY_EMAIL, COMPANY_PAN, COMPANY_REGD,
    VAT_RATE, STRIP_DISCOUNT,
    SALES_DIR, RESTOCK_DIR,
    next_invoice_number, next_po_number, now_str, write_file
)

# ── Invoice box inner width ──────────────────────────────────────────────────
IW = 72     # characters between the box walls

def _L(text: str = "", align: str = "l") -> str:
    """One line inside the double-border invoice box."""
    s = str(text)
    if len(s) > IW:
        s = s[:IW - 1] + "…"
    padded = s.center(IW) if align == "c" else s.ljust(IW)
    return "║ " + padded + " ║"

def _top()  -> str: return "╔" + "═" * (IW + 2) + "╗"
def _sep()  -> str: return "╠" + "═" * (IW + 2) + "╣"
def _thin() -> str: return "╟" + "─" * (IW + 2) + "╢"
def _bot()  -> str: return "╚" + "═" * (IW + 2) + "╝"


# ── Item table column widths inside invoice ──────────────────────────────────
#   Medicine | Brand | Unit | Qty | Rate | Disc(Rs.) | Amount
_TW  = [20, 14, 7, 4, 8, 10, 10]
_TAL = ["l", "l", "l", "r", "r", "r",  "r"]
_THD = ["Medicine", "Brand", "Unit", "Qty", "Rate", "Disc(Rs.)", "Amount"]


def _tbl_row(cells, widths, aligns) -> str:
    parts = []
    for cell, w, a in zip(cells, widths, aligns):
        s = str(cell)
        if len(s) > w:
            s = s[:w - 1] + "…"
        parts.append(" " + (s.rjust(w) if a == "r" else s.ljust(w)) + " ")
    return "│" + "│".join(parts) + "│"


def _tbl_top(cols)      -> str: return "┌" + "┬".join("─" * (c + 2) for c in cols) + "┐"
def _tbl_hsep(cols)     -> str: return "╞" + "╪".join("═" * (c + 2) for c in cols) + "╡"
def _tbl_mid(cols)      -> str: return "├" + "┼".join("─" * (c + 2) for c in cols) + "┤"
def _tbl_bot(cols)      -> str: return "└" + "┴".join("─" * (c + 2) for c in cols) + "┘"


def _build_company_header(doc_title: str, bill_ref: str, date_str: str, party_label: str, party_name: str) -> list:
    """Build the standard company header block shared by all invoice types."""
    return [
        _top(),
        _L(),
        _L(COMPANY_NAME, "c"),
        _L(COMPANY_SUB, "c"),
        _L(),
        _L(f"  Address  :  {COMPANY_ADDRESS}"),
        _L(f"  Phone    :  {COMPANY_PHONE}"),
        _L(f"  Email    :  {COMPANY_EMAIL}"),
        _L(f"  {COMPANY_PAN}   |   {COMPANY_REGD}"),
        _L(),
        _sep(),
        _L(doc_title, "c"),
        _thin(),
        _L(f"  Reference No :  {bill_ref}"),
        _L(f"  Date & Time  :  {date_str}"),
        _L(f"  {party_label:<13}:  {party_name}"),
        _thin(),
    ]


# ════════════════════════════════════════════════════════════════════════════
#  SALES INVOICE
# ════════════════════════════════════════════════════════════════════════════

def generate_sales_invoice(customer_name: str, items: list) -> tuple:
    """
    Build a VAT sales invoice and save as .txt file.

    Each item dict must have:
      name, brand, unit, qty, rate, disc_rs (discount in Rs.), amt, tabs

    Returns (invoice_number, file_path).
    """
    bill_no   = next_invoice_number()
    timestamp = now_str()

    lines = _build_company_header(
        doc_title    = "OFFICIAL VAT INVOICE — CUSTOMER SALE",
        bill_ref     = bill_no,
        date_str     = timestamp,
        party_label  = "Customer",
        party_name   = customer_name,
    )

    # ── Item table ────────────────────────────────────────────────────────
    lines.append(_tbl_top(_TW))
    lines.append(_tbl_row(_THD, _TW, _TAL))
    lines.append(_tbl_hsep(_TW))

    subtotal_rs   = 0.0
    disc_total_rs = 0.0

    for i, it in enumerate(items):
        gross    = it["qty"] * it["rate"]
        disc_rs  = it.get("disc_rs", 0.0)
        net      = gross - disc_rs

        disc_str = f"Rs.{disc_rs:.2f}" if disc_rs > 0 else "—"
        cells = [
            it["name"], it["brand"], it["unit"],
            str(it["qty"]),
            f"Rs.{it['rate']:.2f}",
            disc_str,
            f"Rs.{net:.2f}",
        ]
        lines.append(_tbl_row(cells, _TW, _TAL))
        if i < len(items) - 1:
            lines.append(_tbl_mid(_TW))

        subtotal_rs   += gross
        disc_total_rs += disc_rs

    lines.append(_tbl_bot(_TW))

    # ── Discount note ─────────────────────────────────────────────────────
    if disc_total_rs > 0:
        lines.append(_thin())
        lines.append(_L(f"  Strip Discount (5% on 2+ strips of same medicine applied above)", "l"))

    # ── Totals ────────────────────────────────────────────────────────────
    taxable  = round(subtotal_rs - disc_total_rs, 2)
    vat_amt  = round(taxable * VAT_RATE, 2)
    grand    = round(taxable + vat_amt, 2)

    lines.append(_thin())
    lines.append(_L(f"  Gross Subtotal              :  Rs. {subtotal_rs:>10.2f}"))
    if disc_total_rs > 0:
        lines.append(_L(f"  Total Strip Discount (5%)   :  Rs. {disc_total_rs:>10.2f}"))
    lines.append(_L(f"  Taxable Amount              :  Rs. {taxable:>10.2f}"))
    lines.append(_L(f"  VAT @ 13.0%                 :  Rs. {vat_amt:>10.2f}"))
    lines.append(_sep())
    lines.append(_L(f"  GRAND TOTAL PAYABLE         :  Rs. {grand:>10.2f}", "l"))
    lines.append(_sep())
    lines.append(_L())
    lines.append(_L("Thank you for your purchase!  —  E. & O. E.", "c"))
    lines.append(_L())
    lines.append(_bot())

    return _output(bill_no, lines, SALES_DIR)


# ════════════════════════════════════════════════════════════════════════════
#  RESTOCK PURCHASE ORDER
# ════════════════════════════════════════════════════════════════════════════

def generate_restock_invoice(supplier: str, items: list) -> tuple:
    """
    Build a purchase-order invoice and save as .txt file.

    Each item dict must have: name, brand, unit, qty, rate

    Returns (po_number, file_path).
    """
    po_no     = next_po_number()
    timestamp = now_str()

    lines = _build_company_header(
        doc_title    = "PURCHASE ORDER — RESTOCK FROM SUPPLIER",
        bill_ref     = po_no,
        date_str     = timestamp,
        party_label  = "Supplier",
        party_name   = supplier,
    )

    # ── Item table (simpler — no discount on restocks) ────────────────────
    PO_TW  = [22, 16, 7, 6, 10, 11]
    PO_AL  = ["l", "l", "l", "r", "r", "r"]
    PO_HDR = ["Medicine", "Brand", "Unit", "Qty", "Rate", "Amount"]

    lines.append(_tbl_top(PO_TW))
    lines.append(_tbl_row(PO_HDR, PO_TW, PO_AL))
    lines.append(_tbl_hsep(PO_TW))

    total_cost = 0.0
    for i, it in enumerate(items):
        cost = it["qty"] * it["rate"]
        total_cost += cost
        cells = [
            it["name"], it["brand"], it["unit"],
            str(it["qty"]),
            f"Rs.{it['rate']:.2f}",
            f"Rs.{cost:.2f}",
        ]
        lines.append(_tbl_row(cells, PO_TW, PO_AL))
        if i < len(items) - 1:
            lines.append(_tbl_mid(PO_TW))

    lines.append(_tbl_bot(PO_TW))
    lines.append(_thin())
    lines.append(_L(f"  Total Items Ordered         :  {len(items)} line(s)"))
    lines.append(_sep())
    lines.append(_L(f"  TOTAL PURCHASE COST         :  Rs. {total_cost:>10.2f}", "l"))
    lines.append(_sep())
    lines.append(_L())
    lines.append(_L("Authorised by MedStore Management.  —  E. & O. E.", "c"))
    lines.append(_L())
    lines.append(_bot())

    return _output(po_no, lines, RESTOCK_DIR)


# ════════════════════════════════════════════════════════════════════════════
#  OUTPUT HELPER  (print + save)
# ════════════════════════════════════════════════════════════════════════════

def _output(ref_no: str, lines: list, directory: str) -> tuple:
    """Save invoice to .txt file only. Console already showed checkout preview."""
    content = "\n".join(lines)
    path = write_file(directory, f"{ref_no}.txt", content)
    return ref_no, path
