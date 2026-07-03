"""
=================================================================
  Personal Finance Analyzer
  File  : transactions_analyzer.py
  Author: github.com/amanattar

  Phases:
    Phase 1 ✅  Read CSV
    Phase 2 ✅  Validate Data  (7 checks, detailed per-row output)
    Phase 2b ✅ Clean Data     (drop / fix bad rows, save cleaned CSV)
    Phase 3 ✅  Categorize Expenses  (totals + out-of-budget alerts)
    Phase 4 ✅  Monthly Summary      (table + CSV export)
    Phase 5 ✅  Report Generation    (TXT report)
    Phase 6 ✅  argparse CLI
    Phase 7 ✅  README               (shown via --readme or --help)

  Usage:
    python transactions_analyzer.py
    python transactions_analyzer.py --input myfile.csv
    python transactions_analyzer.py --input myfile.csv --output cleaned.csv
    python transactions_analyzer.py --input myfile.csv --report report.txt --summary monthly.csv
    python transactions_analyzer.py --month Jan
    python transactions_analyzer.py --month Jan Jun
    python transactions_analyzer.py --month Jan Feb Mar
    python transactions_analyzer.py --no-clean
    python transactions_analyzer.py --no-report
    python transactions_analyzer.py --readme
=================================================================
"""

# stdlib only — no pip install needed
import csv
import os
import argparse
from datetime import datetime
from copy import deepcopy
from collections import defaultdict

# =================================================================
# CONFIG  (overridden by CLI args at runtime)
# =================================================================

DEFAULT_INPUT   = "transactions_2025_updated.csv"
DEFAULT_OUTPUT  = "transactions_2025_cleaned.csv"
DEFAULT_REPORT  = "report.txt"
DEFAULT_SUMMARY = "monthly_summary.csv"
DATE_FORMAT     = "%d/%m/%Y"

VALID_CATEGORIES = {
    "Income", "Food", "Transport", "Rent",
    "Entertainment", "Utilities", "Savings",
    "Shopping", "Medical", "Subscriptions"
}

# Category budget ranges (min, max) in ₹ — for out-of-budget alerts
BUDGET_RANGES = {
    "Food":          (200,    6000),
    "Entertainment": (1000,   3000),
    "Shopping":      (500,   10000),
    "Medical":       (100,    2000),
    "Transport":     (100,    3000),
    "Utilities":     (200,    3000),
    "Subscriptions": (50,     1000),
    "Rent":          (5000,  30000),
}

# =================================================================
# HELPERS
# =================================================================

def separator(title, width=65):
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)

def is_numeric(value):
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False

def is_valid_date(value):
    try:
        datetime.strptime(value.strip(), DATE_FORMAT)
        return True
    except (ValueError, AttributeError):
        return False

def parse_date(value):
    return datetime.strptime(value.strip(), DATE_FORMAT)

def month_label(date_str):
    """'01/03/2025'  →  'Mar-2025'"""
    return parse_date(date_str).strftime("%b-%Y")

def month_sort_key(label):
    """Sort 'Jan-2025' labels chronologically."""
    return datetime.strptime(label, "%b-%Y")

def parse_month_args(month_args):
    """
    Convert CLI month inputs to canonical 3-letter abbreviations.
    Accepts: Jan, January, jan, 1, 01  ->  'Jan'
    Returns a set like {'Jan', 'Jun'}
    """
    abbr_map = {}
    for i in range(1, 13):
        dt = datetime(2000, i, 1)
        abbr_map[dt.strftime("%b").lower()] = dt.strftime("%b")
        abbr_map[dt.strftime("%B").lower()] = dt.strftime("%b")
        abbr_map[str(i)]                    = dt.strftime("%b")
        abbr_map[f"{i:02d}"]               = dt.strftime("%b")
    result = set()
    for m in month_args:
        key = m.strip().lower()
        if key in abbr_map:
            result.add(abbr_map[key])
        else:
            print(f"  WARNING: Unrecognised month '{m}' - skipping. Use e.g. Jan, February, 3")
    return result

def filter_rows_by_months(rows, month_set):
    """Return only rows whose month abbreviation is in month_set. Skips invalid dates."""
    result = []
    for r in rows:
        if not is_valid_date(r.get("date", "")):
            continue
        if month_label(r["date"]).split("-")[0] in month_set:
            result.append(r)
    return result

def parse_category_args(cat_args):
    """
    Normalize category inputs to canonical form (case-insensitive).
    e.g. food -> Food, FOOD -> Food, entertainment -> Entertainment
    Returns a set of matched valid category strings, warns on unknown ones.
    """
    lower_map = {c.lower(): c for c in VALID_CATEGORIES}
    lower_map["unknown"] = "Unknown"
    result = set()
    for c in cat_args:
        key = c.strip().lower()
        if key in lower_map:
            result.add(lower_map[key])
        else:
            print(f"  WARNING: Unrecognised category '{c}' - skipping.")
            print(f"    Valid: {sorted(VALID_CATEGORIES)}")
    return result

def filter_rows_by_categories(rows, cat_set):
    """Return only rows whose category is in cat_set."""
    return [r for r in rows if r.get("category", "").strip() in cat_set]

# =================================================================
# PHASE 1 — READ CSV
# =================================================================

def phase1_read(filepath):
    separator("PHASE 1 — READ CSV")
    if not os.path.exists(filepath):
        print(f"  [ERROR] File not found: '{filepath}'")
        exit(1)
    with open(filepath, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    print(f"  ✅ Loaded {len(rows)} rows from '{filepath}'")
    # Show first 3 rows as preview
    print(f"\n  Preview (first 3 rows):")
    print(f"  {'date':<14} {'category':<16} {'description':<28} {'amount':>8}")
    print(f"  {'-'*68}")
    for r in rows[:3]:
        print(f"  {r.get('date',''):<14} {r.get('category',''):<16} "
              f"{r.get('description',''):<28} {r.get('amount',''):>8}")
    return rows

# =================================================================
# PHASE 2 — VALIDATE DATA
# =================================================================

# ── Individual check functions (return list of (row_num, row) tuples) ──

def _check_missing_amounts(rows):
    return [(i + 2, r) for i, r in enumerate(rows)
            if not r.get("amount", "").strip()]

def _check_non_numeric_amounts(rows):
    return [(i + 2, r) for i, r in enumerate(rows)
            if r.get("amount", "").strip() and not is_numeric(r["amount"].strip())]

def _check_missing_descriptions(rows):
    return [(i + 2, r) for i, r in enumerate(rows)
            if not r.get("description", "").strip()]

def _check_missing_categories(rows):
    return [(i + 2, r) for i, r in enumerate(rows)
            if not r.get("category", "").strip()]

def _check_invalid_dates(rows):
    return [(i + 2, r) for i, r in enumerate(rows)
            if not is_valid_date(r.get("date", ""))]

def _check_duplicates(rows):
    seen, dupes = {}, []
    for i, r in enumerate(rows):
        key = (
            r.get("date", "").strip(),
            r.get("category", "").strip(),
            r.get("description", "").strip(),
            r.get("amount", "").strip(),
        )
        if key in seen:
            dupes.append((i + 2, r, seen[key] + 2))
        else:
            seen[key] = i
    return dupes

def _check_unknown_categories(rows):
    return [(i + 2, r) for i, r in enumerate(rows)
            if r.get("category", "").strip()
            and r["category"].strip() not in VALID_CATEGORIES]

# ── Main validate function ──────────────────────────────────────────

def phase2_validate(rows):
    separator("PHASE 2 — VALIDATE DATA")

    missing_amounts = _check_missing_amounts(rows)
    non_numeric     = _check_non_numeric_amounts(rows)
    missing_descs   = _check_missing_descriptions(rows)
    missing_cats    = _check_missing_categories(rows)
    invalid_dates   = _check_invalid_dates(rows)
    duplicates      = _check_duplicates(rows)
    unknown_cats    = _check_unknown_categories(rows)

    # ── 1. Missing Amounts ───────────────────────────────────────
    print(f"\n  {'1. MISSING AMOUNTS':}")
    if not missing_amounts:
        print("    ✅ No missing amounts found.")
    else:
        for row_num, r in missing_amounts:
            print(f"    ❌ Row {row_num}: date={r['date']} | cat={r['category']} "
                  f"| desc={r['description']} | amount='{r['amount']}'")

    # ── 2. Non-Numeric Amounts ───────────────────────────────────
    print(f"\n  {'2. NON-NUMERIC AMOUNTS':}")
    if not non_numeric:
        print("    ✅ All amounts are numeric.")
    else:
        for row_num, r in non_numeric:
            print(f"    ❌ Row {row_num}: amount='{r['amount']}' is not a number "
                  f"| desc={r['description']}")

    # ── 3. Missing Descriptions ──────────────────────────────────
    print(f"\n  {'3. MISSING DESCRIPTIONS':}")
    if not missing_descs:
        print("    ✅ No missing descriptions.")
    else:
        for row_num, r in missing_descs:
            print(f"    ❌ Row {row_num}: date={r['date']} | cat={r['category']} "
                  f"| description is empty")

    # ── 4. Missing Categories ────────────────────────────────────
    print(f"\n  {'4. MISSING CATEGORIES':}")
    if not missing_cats:
        print("    ✅ No missing categories.")
    else:
        for row_num, r in missing_cats:
            print(f"    ❌ Row {row_num}: date={r['date']} | desc={r['description']} "
                  f"| category is empty")

    # ── 5. Invalid Dates ─────────────────────────────────────────
    print(f"\n  {'5. INVALID DATES':}")
    if not invalid_dates:
        print("    ✅ All dates are valid.")
    else:
        for row_num, r in invalid_dates:
            print(f"    ❌ Row {row_num}: date='{r['date']}' is not a valid DD/MM/YYYY "
                  f"| desc={r['description']}")

    # ── 6. Duplicate Rows ────────────────────────────────────────
    print(f"\n  {'6. DUPLICATE ROWS':}")
    if not duplicates:
        print("    ✅ No duplicate rows found.")
    else:
        for row_num, r, orig in duplicates:
            print(f"    ❌ Row {row_num} is a duplicate of Row {orig}: "
                  f"{r['date']} | {r['category']} | {r['description']} | {r['amount']}")

    # ── 7. Unknown Categories ────────────────────────────────────
    print(f"\n  {'7. UNKNOWN CATEGORIES':}")
    if not unknown_cats:
        print("    ✅ All categories are valid.")
    else:
        for row_num, r in unknown_cats:
            print(f"    ❌ Row {row_num}: category='{r['category']}' not recognised "
                  f"| desc={r['description']}")
        print(f"    Valid categories: {sorted(VALID_CATEGORIES)}")

    # ── Summary table ─────────────────────────────────────────────
    total_issues = (len(missing_amounts) + len(non_numeric) + len(missing_descs) +
                    len(missing_cats) + len(invalid_dates) + len(duplicates) + len(unknown_cats))

    print(f"\n  {'─'*50}")
    print(f"  {'Check':<30} {'Issues':>6}")
    print(f"  {'─'*50}")
    print(f"  {'1. Missing Amounts':<30} {len(missing_amounts):>6}")
    print(f"  {'2. Non-Numeric Amounts':<30} {len(non_numeric):>6}")
    print(f"  {'3. Missing Descriptions':<30} {len(missing_descs):>6}")
    print(f"  {'4. Missing Categories':<30} {len(missing_cats):>6}")
    print(f"  {'5. Invalid Dates':<30} {len(invalid_dates):>6}")
    print(f"  {'6. Duplicate Rows':<30} {len(duplicates):>6}")
    print(f"  {'7. Unknown Categories':<30} {len(unknown_cats):>6}")
    print(f"  {'─'*50}")
    print(f"  {'TOTAL ISSUES':<30} {total_issues:>6}")

    return (missing_amounts, non_numeric, missing_descs,
            missing_cats, invalid_dates, duplicates, unknown_cats)

# =================================================================
# PHASE 2b — CLEAN DATA
# =================================================================

def phase2b_clean(rows, missing_amounts, non_numeric, missing_descs,
                  missing_cats, invalid_dates, duplicates, unknown_cats):
    separator("PHASE 2b — CLEAN DATA")

    drop = set()

    # Drop: missing amount
    for row_num, r in missing_amounts:
        drop.add(row_num - 2)
        print(f"  🗑  Row {row_num}: dropped — missing amount")

    # Drop: non-numeric amount
    for row_num, r in non_numeric:
        drop.add(row_num - 2)
        print(f"  🗑  Row {row_num}: dropped — non-numeric amount ('{r['amount']}')")

    # Drop: invalid date
    for row_num, r in invalid_dates:
        drop.add(row_num - 2)
        print(f"  🗑  Row {row_num}: dropped — invalid date ('{r['date']}')")

    # Drop: duplicate (keep first, remove later copy)
    for row_num, r, orig in duplicates:
        drop.add(row_num - 2)
        print(f"  🗑  Row {row_num}: dropped — duplicate of Row {orig}")

    # Fix: missing description → placeholder
    for row_num, r in missing_descs:
        idx = row_num - 2
        if idx not in drop:
            rows[idx]["description"] = "No description"
            print(f"  ✏️  Row {row_num}: description → 'No description'")

    # Fix: missing category → 'Unknown'
    for row_num, r in missing_cats:
        idx = row_num - 2
        if idx not in drop:
            rows[idx]["category"] = "Unknown"
            print(f"  ✏️  Row {row_num}: category → 'Unknown'")

    # Fix: unknown category → 'Unknown'
    for row_num, r in unknown_cats:
        idx = row_num - 2
        if idx not in drop:
            old = rows[idx]["category"]
            rows[idx]["category"] = "Unknown"
            print(f"  ✏️  Row {row_num}: category '{old}' → 'Unknown'")

    cleaned = [r for i, r in enumerate(rows) if i not in drop]
    print(f"\n  ✅ Cleaning done — {len(rows)} → {len(cleaned)} rows "
          f"(removed {len(drop)}, fixed {len(missing_descs) + len(missing_cats) + len(unknown_cats)})")
    return cleaned

def save_cleaned_csv(rows, filepath):
    fieldnames = ["date", "category", "description", "amount"]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  💾 Cleaned CSV saved → '{filepath}'")

# =================================================================
# PHASE 3 — CATEGORIZE EXPENSES
# =================================================================

def phase3_categorize(rows):
    separator("PHASE 3 — CATEGORIZE EXPENSES")

    category_totals = defaultdict(float)
    category_counts = defaultdict(int)
    out_of_range    = []

    for r in rows:
        cat    = r["category"].strip()
        amount = float(r["amount"])
        category_totals[cat] += amount
        category_counts[cat] += 1

        if cat in BUDGET_RANGES:
            lo, hi = BUDGET_RANGES[cat]
            if not (lo <= abs(amount) <= hi):
                out_of_range.append((r, abs(amount), lo, hi))

    income_total  = category_totals.get("Income", 0)
    savings_total = abs(category_totals.get("Savings", 0))
    expense_total = abs(sum(v for k, v in category_totals.items()
                            if k not in ("Income", "Savings")))

    print(f"\n  {'Category':<18} {'Txns':>5}  {'Total (₹)':>12}  {'Avg (₹)':>10}")
    print(f"  {'─'*52}")
    for cat in sorted(category_totals):
        total = category_totals[cat]
        count = category_counts[cat]
        avg   = total / count if count else 0
        print(f"  {cat:<18} {count:>5}  {total:>12,.0f}  {avg:>10,.0f}")
    print(f"  {'─'*52}")
    print(f"  {'TOTAL INCOME':<18} {'':>5}  {income_total:>12,.0f}")
    print(f"  {'TOTAL EXPENSES':<18} {'':>5}  {-expense_total:>12,.0f}")
    print(f"  {'TOTAL SAVINGS':<18} {'':>5}  {-savings_total:>12,.0f}")
    print(f"  {'NET CASH FLOW':<18} {'':>5}  {income_total - expense_total - savings_total:>12,.0f}")

    if out_of_range:
        print(f"\n  ⚠️  Out-of-budget transactions ({len(out_of_range)}):")
        for r, amt, lo, hi in out_of_range:
            print(f"     Row: {r['date']}  {r['category']:<14} ₹{amt:,.0f}  "
                  f"(expected ₹{lo}–₹{hi})  → {r['description']}")
    else:
        print("\n  ✅ All transactions within expected budget ranges.")

    return category_totals, category_counts

# =================================================================
# PHASE 4 — MONTHLY SUMMARY
# =================================================================

def phase4_monthly_summary(rows):
    separator("PHASE 4 — MONTHLY SUMMARY")

    monthly = defaultdict(lambda: defaultdict(float))
    for r in rows:
        label  = month_label(r["date"])
        cat    = r["category"].strip()
        amount = float(r["amount"])
        monthly[label][cat] += amount

    months   = sorted(monthly.keys(), key=month_sort_key)
    all_cats = sorted({cat for m in monthly.values() for cat in m})

    col_w  = 12
    header = f"  {'Month':<10}" + "".join(f"{c:>{col_w}}" for c in all_cats)
    print(header)
    print("  " + "─" * (10 + col_w * len(all_cats)))

    for month in months:
        row_str = f"  {month:<10}"
        for cat in all_cats:
            val = monthly[month].get(cat, 0)
            row_str += f"{val:>{col_w},.0f}"
        print(row_str)

    print("\n  ✅ Monthly summary complete.")
    return monthly, months, all_cats

def save_monthly_summary_csv(monthly, months, all_cats, filepath):
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Month"] + all_cats + ["Net"])
        for month in months:
            income   = monthly[month].get("Income", 0)
            expenses = sum(v for k, v in monthly[month].items()
                           if k not in ("Income", "Savings"))
            net      = income + expenses
            row      = [month] + [f"{monthly[month].get(c, 0):.0f}"
                                   for c in all_cats] + [f"{net:.0f}"]
            writer.writerow(row)
    print(f"  💾 Monthly summary CSV saved → '{filepath}'")

# =================================================================
# PHASE 5 — REPORT GENERATION
# =================================================================

def phase5_report(rows, category_totals, category_counts, monthly, months, report_path):
    separator("PHASE 5 — REPORT GENERATION")

    income_total  = category_totals.get("Income", 0)
    savings_total = abs(category_totals.get("Savings", 0))
    expense_total = abs(sum(v for k, v in category_totals.items()
                            if k not in ("Income", "Savings")))
    net           = income_total - expense_total - savings_total
    savings_rate  = (savings_total / income_total * 100) if income_total else 0

    month_expenses = {
        m: abs(sum(v for k, v in monthly[m].items() if k not in ("Income", "Savings")))
        for m in months
    }
    top3 = sorted(month_expenses, key=lambda x: month_expenses[x], reverse=True)[:3]

    W = 65
    lines = []
    lines.append("=" * W)
    lines.append("  PERSONAL FINANCE REPORT — 2025")
    lines.append(f"  Generated : {datetime.now().strftime('%d %b %Y  %H:%M')}")
    lines.append(f"  Total rows: {len(rows)}")
    lines.append("=" * W)

    # Overview
    lines.append("\n  OVERVIEW")
    lines.append(f"  {'─'*W}")
    lines.append(f"  {'Total Income':<30} ₹{income_total:>12,.0f}")
    lines.append(f"  {'Total Expenses':<30} ₹{expense_total:>12,.0f}")
    lines.append(f"  {'Total Savings (SIP/FD)':<30} ₹{savings_total:>12,.0f}")
    lines.append(f"  {'Net Cash Flow':<30} ₹{net:>12,.0f}")
    lines.append(f"  {'Savings Rate':<30}  {savings_rate:>11.1f}%")

    # Expense breakdown
    lines.append(f"\n  EXPENSE BREAKDOWN BY CATEGORY")
    lines.append(f"  {'─'*W}")
    lines.append(f"  {'Category':<18} {'Txns':>5}  {'Total (₹)':>12}  {'Avg (₹)':>10}  {'% of Exp':>9}")
    lines.append(f"  {'─'*W}")
    for cat in sorted(category_totals):
        if cat in ("Income", "Savings"):
            continue
        total = abs(category_totals[cat])
        count = category_counts[cat]
        avg   = total / count if count else 0
        pct   = (total / expense_total * 100) if expense_total else 0
        lines.append(f"  {cat:<18} {count:>5}  {total:>12,.0f}  {avg:>10,.0f}  {pct:>8.1f}%")

    # Month-by-month
    lines.append(f"\n  MONTH-BY-MONTH NET CASH FLOW")
    lines.append(f"  {'─'*W}")
    lines.append(f"  {'Month':<12} {'Income':>10}  {'Expenses':>10}  {'Savings':>10}  {'Net':>10}")
    lines.append(f"  {'─'*W}")
    for month in months:
        inc  = monthly[month].get("Income", 0)
        sav  = abs(monthly[month].get("Savings", 0))
        exp  = abs(sum(v for k, v in monthly[month].items()
                       if k not in ("Income", "Savings")))
        nm   = inc - exp - sav
        lines.append(f"  {month:<12} {inc:>10,.0f}  {exp:>10,.0f}  {sav:>10,.0f}  {nm:>10,.0f}")

    # Top 3 expense months
    lines.append(f"\n  TOP 3 HIGHEST EXPENSE MONTHS")
    lines.append(f"  {'─'*W}")
    for i, m in enumerate(top3, 1):
        lines.append(f"  {i}. {m:<14} ₹{month_expenses[m]:,.0f}")

    lines.append("\n" + "=" * W)
    report_text = "\n".join(lines)

    print(report_text)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(f"\n  💾 Report saved → '{report_path}'")

# =================================================================
# PHASE 6 — argparse CLI
# =================================================================

def build_cli():
    parser = argparse.ArgumentParser(
        prog="transactions_analyzer.py",
        description="💰 Personal Finance Analyzer — validate, clean, categorize & report on transaction CSVs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  python transactions_analyzer.py
  python transactions_analyzer.py --input myfile.csv
  python transactions_analyzer.py --input myfile.csv --output cleaned.csv
  python transactions_analyzer.py --input myfile.csv --report rep.txt --summary monthly.csv
  python transactions_analyzer.py --no-clean
  python transactions_analyzer.py --no-report
  python transactions_analyzer.py --readme
        """
    )
    parser.add_argument("--input",     default=DEFAULT_INPUT,
                        help=f"Input CSV (default: {DEFAULT_INPUT})")
    parser.add_argument("--output",    default=DEFAULT_OUTPUT,
                        help=f"Cleaned CSV output (default: {DEFAULT_OUTPUT})")
    parser.add_argument("--report",    default=DEFAULT_REPORT,
                        help=f"Text report path (default: {DEFAULT_REPORT})")
    parser.add_argument("--summary",   default=DEFAULT_SUMMARY,
                        help=f"Monthly summary CSV (default: {DEFAULT_SUMMARY})")
    parser.add_argument("--no-clean",  action="store_true",
                        help="Validate only — skip cleaning and saving output")
    parser.add_argument("--no-report", action="store_true",
                        help="Skip phases 3-5 (categorize / summary / report)")
    parser.add_argument("--readme",    action="store_true",
                        help="Print the README and exit")
    parser.add_argument("--month",     nargs="+", metavar="MONTH", default=None,
                        help="Filter report to specific month(s). e.g. --month Jan  or  --month Jan Jun Dec")
    parser.add_argument("--category",  nargs="+", metavar="CATEGORY", default=None,
                        help="Filter report to specific category/categories. e.g. --category Food  or  --category Food Shopping Transport")
    return parser

# =================================================================
# PHASE 7 — README
# =================================================================

README = """
╔══════════════════════════════════════════════════════════════════╗
║          💰  PERSONAL FINANCE ANALYZER  — README                ║
╚══════════════════════════════════════════════════════════════════╝

DESCRIPTION
  Reads a personal transaction CSV, validates it for 7 types of
  errors, cleans it, categorizes expenses, builds a monthly summary,
  and generates a plain-text finance report.  No third-party libraries
  required — pure Python 3.7+ stdlib.

──────────────────────────────────────────────────────────────────
REQUIRED CSV FORMAT
──────────────────────────────────────────────────────────────────
  date,category,description,amount
  01/01/2025,Income,Salary January,55000
  02/01/2025,Food,Swiggy order,-450

  Column       Format           Notes
  ─────────    ──────────────   ──────────────────────────────────
  date         DD/MM/YYYY       e.g. 15/03/2025
  category     see list below   must match exactly (case-sensitive)
  description  free text        leave blank → filled as 'No description'
  amount       integer/float    income = positive, expense = negative

──────────────────────────────────────────────────────────────────
VALID CATEGORIES
──────────────────────────────────────────────────────────────────
  Income | Food | Transport | Rent | Entertainment
  Utilities | Savings | Shopping | Medical | Subscriptions

──────────────────────────────────────────────────────────────────
BUDGET RANGES  (out-of-range amounts are flagged in Phase 3)
──────────────────────────────────────────────────────────────────
  Category        Min (₹)   Max (₹)
  ─────────────   ───────   ───────
  Food               200     6,000
  Entertainment    1,000     3,000
  Shopping           500    10,000
  Medical            100     2,000
  Transport          100     3,000
  Utilities          200     3,000
  Subscriptions       50     1,000
  Rent             5,000    30,000

──────────────────────────────────────────────────────────────────
PHASES
──────────────────────────────────────────────────────────────────
  Phase 1   Read CSV            Load & preview input file
  Phase 2   Validate Data       7 checks with per-row detail
  Phase 2b  Clean Data          Drop bad rows, fix missing fields
  Phase 3   Categorize          Totals per category, outlier alerts
  Phase 4   Monthly Summary     Month-by-month table + CSV export
  Phase 5   Report Generation   Full finance report saved as .txt
  Phase 6   argparse CLI        All options via terminal flags
  Phase 7   README              This screen (--readme)

──────────────────────────────────────────────────────────────────
VALIDATION CHECKS  (Phase 2 / 2b)
──────────────────────────────────────────────────────────────────
  Check                  Action
  ──────────────────     ──────────────────────────────────────────
  Missing Amount         🗑  Row dropped
  Non-Numeric Amount     🗑  Row dropped
  Invalid Date           🗑  Row dropped
  Duplicate Row          🗑  Later copy dropped
  Missing Description    ✏️  Filled → 'No description'
  Missing Category       ✏️  Filled → 'Unknown'
  Unknown Category       ✏️  Renamed → 'Unknown'

──────────────────────────────────────────────────────────────────
OUTPUT FILES
──────────────────────────────────────────────────────────────────
  transactions_2025_cleaned.csv   cleaned version of input
  monthly_summary.csv             one row per month × category
  report.txt                      income / expense / savings report

──────────────────────────────────────────────────────────────────
CLI FLAGS
──────────────────────────────────────────────────────────────────
  --input   FILE    Input CSV              (default: transactions_2025_updated.csv)
  --output  FILE    Cleaned CSV output     (default: transactions_2025_cleaned.csv)
  --report  FILE    Text report            (default: report.txt)
  --summary FILE    Monthly summary CSV    (default: monthly_summary.csv)
  --no-clean        Validate only, skip cleaning & saving
  --no-report       Skip phases 3-5
  --readme          Print this page and exit

──────────────────────────────────────────────────────────────────
QUICK-START EXAMPLES
──────────────────────────────────────────────────────────────────
  python transactions_analyzer.py
  python transactions_analyzer.py --input myfile.csv
  python transactions_analyzer.py --no-clean
  python transactions_analyzer.py --no-report
  python transactions_analyzer.py --readme
"""

def phase7_readme():
    print(README)

# =================================================================
# MAIN
# =================================================================

def main():
    parser = build_cli()
    args   = parser.parse_args()

    # Phase 7 — README
    if args.readme:
        phase7_readme()
        return

    print("\n" + "=" * 65)
    print("   💰  PERSONAL FINANCE ANALYZER")
    print("=" * 65)
    print(f"  Input   : {args.input}")
    print(f"  Output  : {args.output}")
    print(f"  Report  : {args.report}")
    print(f"  Summary : {args.summary}")

    # Phase 1 — Read
    rows = phase1_read(args.input)

    # Phase 2 — Validate
    (missing_amounts, non_numeric, missing_descs,
     missing_cats, invalid_dates, duplicates, unknown_cats) = phase2_validate(rows)

    # Phase 2b — Clean
    if args.no_clean:
        print("\n  ⚠️  --no-clean: skipping clean & save.")
        cleaned = deepcopy(rows)
    else:
        cleaned = phase2b_clean(
            deepcopy(rows),
            missing_amounts, non_numeric, missing_descs,
            missing_cats, invalid_dates, duplicates, unknown_cats
        )
        save_cleaned_csv(cleaned, args.output)

    # ── Apply --month and/or --category filters (phases 3-5 only) ──────
    report_rows = cleaned
    active_filters = []

    if args.month:
        month_set = parse_month_args(args.month)
        if month_set:
            ordered = sorted(month_set, key=lambda m: datetime.strptime(m, "%b").month)
            active_filters.append(f"Month = {', '.join(ordered)}")
            report_rows = filter_rows_by_months(report_rows, month_set)
        else:
            print("  ERROR: No valid months parsed — month filter skipped.")

    if args.category:
        cat_set = parse_category_args(args.category)
        if cat_set:
            active_filters.append(f"Category = {', '.join(sorted(cat_set))}")
            report_rows = filter_rows_by_categories(report_rows, cat_set)
        else:
            print("  ERROR: No valid categories parsed — category filter skipped.")

    if active_filters:
        print(f"\n  ACTIVE FILTERS: {' | '.join(active_filters)}")
        print(f"  Rows after filter: {len(report_rows)} / {len(cleaned)}")
        if not report_rows:
            print("  ERROR: No rows matched the given filters. Check spelling.")
            return

    if args.no_report:
        print("\n  WARNING: --no-report: skipping phases 3-5.")
    else:
        # Phase 3 — Categorize
        category_totals, category_counts = phase3_categorize(report_rows)

        # Phase 4 — Monthly Summary
        monthly, months, all_cats = phase4_monthly_summary(report_rows)
        save_monthly_summary_csv(monthly, months, all_cats, args.summary)

        # Phase 5 — Report
        phase5_report(report_rows, category_totals, category_counts,
                      monthly, months, args.report)

    print("\n" + "=" * 65)
    print("  ✅  All phases complete!")
    if not args.no_clean:
        print(f"  📄 Cleaned CSV   → {args.output}")
    if not args.no_report:
        print(f"  📊 Monthly CSV   → {args.summary}")
        print(f"  📝 Report TXT    → {args.report}")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    main()