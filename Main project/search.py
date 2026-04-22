"""
search.py  —  Medicine search feature for MedStore Pvt. Ltd.

Supports:
  • Search by medicine name  (partial, case-insensitive)
  • Search by brand name     (partial, case-insensitive)
  • Combined query matches either field

Also displays low-stock warnings for any results with stock < LOW_STOCK_THRESHOLD.
"""

from modules.utils import (
    ask_str, ask_choice,
    tbl_row, tbl_top, tbl_head_sep, tbl_bot, tbl_mid,
    banner, rule, warn, info,
    W_CONSOLE,
)

LOW_STOCK_THRESHOLD = 20   # tablets

# ── Search result table — same column spec as inventory display ──────────────
_SR_W   = [3, 20, 16, 10, 10, 11, 10]
_SR_AL  = ["r", "l", "l", "r", "r", "r", "r"]
_SR_HDR = ["No", "Medicine Name", "Brand", "Stock(tab)", "Rate/Tab", "Rate/Strip", "Tabs/Strip"]


def _match(medicine: dict, query: str, field: str) -> bool:
    """Return True if the query matches the specified field (case-insensitive)."""
    q = query.lower().strip()
    if field == "name":
        return q in medicine["name"].lower()
    if field == "brand":
        return q in medicine["brand"].lower()
    # "both": match either
    return q in medicine["name"].lower() or q in medicine["brand"].lower()


def _show_results(results: list[tuple[int, dict]]):
    """Display search results in a formatted table with low-stock flags."""
    W = _SR_W
    print()
    print(tbl_top(W))
    print(tbl_row(_SR_HDR, W, _SR_AL))
    print(tbl_head_sep(W))

    for rank, (orig_idx, m) in enumerate(results, 1):
        stock_str = str(m["stock"])
        cells = [
            str(orig_idx),
            m["name"],
            m["brand"],
            stock_str,
            f"Rs.{m['rate_tablet']:.2f}",
            f"Rs.{m['rate_strip']:.2f}",
            str(m["tablets_per_strip"]),
        ]
        row = tbl_row(cells, W, _SR_AL)
        if m["stock"] == 0:
            print(row + "  ◄ OUT OF STOCK")
        elif m["stock"] < LOW_STOCK_THRESHOLD:
            print(row + f"  ◄ LOW STOCK")
        else:
            print(row)
        if rank < len(results):
            print(tbl_mid(W))

    print(tbl_bot(W))


def run_search(medicines: list[dict]):
    """Interactive search loop — keeps searching until the user exits."""
    banner("Search Medicine")

    while True:
        print()
        print("  How would you like to search?")
        print("    1.  Search by medicine name")
        print("    2.  Search by brand name")
        print("    3.  Search both (name or brand)")
        print("    4.  Back to main menu")
        print()

        from modules.utils import ask_int
        choice = ask_int("  Enter your choice [1-4]: → ", min_val=1, max_val=4)

        if choice == 4:
            break

        field_map = {1: "name", 2: "brand", 3: "both"}
        field     = field_map[choice]
        field_lbl = {"name": "medicine name", "brand": "brand name", "both": "name or brand"}[field]

        query = ask_str(f"  Enter {field_lbl} to search for: → ")

        # ── Run search ────────────────────────────────────────────────────
        results = [
            (i + 1, m)
            for i, m in enumerate(medicines)
            if _match(m, query, field)
        ]

        print()
        if not results:
            warn(f"No medicines found matching '{query}' in {field_lbl}.")
            print("  Try a shorter keyword or check the spelling.")
        else:
            rule()
            print(f"  Found {len(results)} result(s) for '{query}':")
            rule()
            _show_results(results)

            # ── Low-stock alerts in results ───────────────────────────────
            low = [(idx, m) for idx, m in results if 0 < m["stock"] < LOW_STOCK_THRESHOLD]
            out = [(idx, m) for idx, m in results if m["stock"] == 0]
            if out:
                print()
                for idx, m in out:
                    warn(f"[#{idx}] {m['name']} ({m['brand']}) — OUT OF STOCK!")
            if low:
                print()
                for idx, m in low:
                    warn(f"[#{idx}] {m['name']} ({m['brand']}) — LOW STOCK: only {m['stock']} tablet(s) left.")
                info("Consider restocking these items soon.")

        print()
        from modules.utils import ask_yn
        if not ask_yn("  Would you like to search again?"):
            break
