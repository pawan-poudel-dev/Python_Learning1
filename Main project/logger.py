"""
logger.py  —  Append-only activity log for MedStore Pvt. Ltd.

Every sale and restock is recorded in data/log.txt with:
  - Timestamp
  - Event type  (SALE / RESTOCK)
  - Bill / PO number
  - Party name  (customer or supplier)
  - Item count
  - Grand total
  - Per-item detail lines

Format (human-readable, also machine-parseable):
────────────────────────────────────────────────
[2026-04-22  10:45:01]  SALE  MS-INV-0001
  Customer   : Ram Bahadur Shrestha
  Items      : 2
  Grand Total: Rs. 402.56
  ─ Paracetamol 500mg  ×  3 Strip(s)  →  Rs. 128.25  (disc Rs.6.75)
  ─ Cetirizine 10mg    ×  7 Tablet(s) →  Rs.  28.00
────────────────────────────────────────────────
"""

import os
import traceback
from modules.utils import DATA_DIR, now_str, VAT_RATE, warn

LOG_FILE = os.path.join(DATA_DIR, "log.txt")
_SEP     = "─" * 62


def _append(text: str):
    """Low-level append to log.txt with full exception handling."""
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(text + "\n")
    except PermissionError:
        warn("Log: permission denied — could not write to log.txt.")
    except OSError as e:
        warn(f"Log: OS error while writing log — {e}")
    except Exception as e:
        warn(f"Log: unexpected error — {e}")


def log_sale(bill_no: str, customer_name: str, items: list[dict]):
    """Record a completed sale transaction."""
    sub   = sum(it["subtotal_before_discount"]  for it in items)
    disc  = sum(it["discount_amount"]            for it in items)
    tax   = round(sub - disc, 2)
    vat   = round(tax * VAT_RATE, 2)
    grand = round(tax + vat, 2)

    lines = [
        _SEP,
        f"[{now_str()}]  SALE  {bill_no}",
        f"  Customer    : {customer_name}",
        f"  Items       : {len(items)}",
        f"  Subtotal    : Rs. {sub:.2f}",
        f"  Discount    : Rs. {disc:.2f}",
        f"  VAT (13%)   : Rs. {vat:.2f}",
        f"  Grand Total : Rs. {grand:.2f}",
        "  Items detail:",
    ]
    for it in items:
        unit  = "Strip(s)"  if it["unit_type"] == "strip" else "Tablet(s)"
        disc_ = f"  [disc Rs.{it['discount_amount']:.2f}]" if it["discount_amount"] > 0 else ""
        lines.append(
            f"    • {it['name']:<22}  x{it['quantity']:>3} {unit:<9}"
            f"  Rs.{it['subtotal_after_discount']:>8.2f}{disc_}"
        )

    _append("\n".join(lines))


def log_restock(po_no: str, supplier_name: str, items: list[dict]):
    """Record a completed restock / purchase order."""
    grand      = sum(it["subtotal"]       for it in items)
    total_tabs = sum(it["total_tablets"]  for it in items)

    lines = [
        _SEP,
        f"[{now_str()}]  RESTOCK  {po_no}",
        f"  Supplier    : {supplier_name}",
        f"  Items       : {len(items)}",
        f"  Tablets added to stock: {total_tabs}",
        f"  Total Cost  : Rs. {grand:.2f}",
        "  Items detail:",
    ]
    for it in items:
        unit = "Strip(s)" if it["unit_type"] == "strip" else "Tablet(s)"
        lines.append(
            f"    • {it['name']:<22}  x{it['quantity']:>3} {unit:<9}"
            f"  Rs.{it['subtotal']:>8.2f}  (+{it['total_tablets']} tabs)"
        )

    _append("\n".join(lines))


def log_session_start():
    _append(f"\n{'═'*62}\nSESSION STARTED  [{now_str()}]\n{'═'*62}")


def log_session_end():
    _append(f"SESSION ENDED    [{now_str()}]\n{'═'*62}\n")


def view_log(last_n: int = 20):
    """Print the last `last_n` log entries to the console."""
    if not os.path.exists(LOG_FILE):
        warn("No activity log found yet. Make some transactions first!")
        return
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        # Split on the separator and take the last n blocks
        blocks = [b.strip() for b in content.split(_SEP) if b.strip()]
        if not blocks:
            warn("The log file is empty.")
            return
        shown = blocks[-last_n:]
        print()
        print("  " + "═" * 70)
        print("  " + f" ACTIVITY LOG  (last {len(shown)} of {len(blocks)} entries) ".center(70, "═"))
        print("  " + "═" * 70)
        for block in shown:
            print()
            print("  " + _SEP)
            for line in block.splitlines():
                print("  " + line)
        print()
        print("  " + _SEP)
        print(f"  Log file: {LOG_FILE}")
        print()
    except OSError as e:
        warn(f"Could not read log file — {e}")
    except Exception as e:
        warn(f"Unexpected error reading log — {e}")
