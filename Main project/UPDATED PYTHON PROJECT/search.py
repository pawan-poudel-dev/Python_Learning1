"""
search.py  —  Medicine search: full-name fragment AND letter-pattern search.
              MedStore Pvt. Ltd. — CS4051NP Coursework SP26
"""

from modules.utils import (
    ask_str, banner, warn, info, ok,
    tbl_row, tbl_top, tbl_head_sep, tbl_bot, tbl_mid, W_CONSOLE
)

# ── Search results table columns ─────────────────────────────────────────────
_SW  = [3, 22, 16, 7, 9, 10, 9]
_SAL = ["r", "l", "l", "r", "r", "r", "r"]
_SHD = ["No", "Medicine Name", "Brand", "Stock", "R/Tab", "R/Strip", "Tab/Strip"]


def _print_results(results: list):
    """Render a list of (original_index, medicine_dict) as a table."""
    print()
    print(f"  ╔══ {len(results)} result(s) found " + "═" * (50 - len(str(len(results)))) + "╗")
    print(tbl_top(_SW))
    print(tbl_row(_SHD, _SW, _SAL))
    print(tbl_head_sep(_SW))

    for rank, (orig_idx, m) in enumerate(results, 1):
        cells = [
            str(orig_idx),
            m["name"],
            m["brand"],
            str(m["stock"]),
            f"Rs.{m['rate_tablet']:.2f}",
            f"Rs.{m['rate_strip']:.2f}",
            str(m["tablets_per_strip"]),
        ]
        print(tbl_row(cells, _SW, _SAL))
        if rank < len(results):
            print(tbl_mid(_SW))

    print(tbl_bot(_SW))
    print()


def run_search(medicines: list, _mode: str = "full"):
    """
    Search by name or brand fragment (case-insensitive substring match).
    Loops until the user presses Enter with no input.
    """
    banner("Search Medicine — by Name / Brand")
    info("Type any part of the medicine name or brand.  Press Enter alone to exit.")

    while True:
        query = ask_str(
            "  Search query (name / brand fragment): ",
            allow_empty=True
        ).strip().lower()

        if not query:
            break

        results = [
            (i + 1, m)
            for i, m in enumerate(medicines)
            if query in m["name"].lower() or query in m["brand"].lower()
        ]

        if results:
            _print_results(results)
        else:
            warn(f"No matches found for '{query}'.")
            info("Try a shorter fragment, e.g. 'para' for Paracetamol.")


def search_by_letter(medicines: list):
    """
    Letter-pattern search: matches medicines where every character in the
    query appears (in order) within the medicine name — like a fuzzy search.

    Example: 'prcml' matches 'Paracetamol'
    """
    banner("Search Medicine — by Letter Pattern (Fuzzy)")
    info("Enter letters that appear in order inside the name.")
    info("Example: 'prcm' matches 'Paracetamol'.")

    while True:
        pattern = ask_str(
            "  Letter pattern (or Enter to exit): ",
            allow_empty=True
        ).strip().lower()

        if not pattern:
            break

        results = []
        for i, m in enumerate(medicines):
            name_lower = m["name"].lower()
            # Check if all pattern chars appear in order inside name
            pos = 0
            for ch in pattern:
                found = name_lower.find(ch, pos)
                if found == -1:
                    break
                pos = found + 1
            else:
                results.append((i + 1, m))

        if results:
            ok(f"Pattern '{pattern}' matched {len(results)} medicine(s):")
            _print_results(results)
        else:
            warn(f"No medicines match the letter pattern '{pattern}'.")
