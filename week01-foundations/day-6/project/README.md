# 💰 Personal Finance Analyzer

A command-line tool to validate, clean, categorize, and summarize personal transaction CSVs — no pip installs needed, pure Python stdlib.

---

## 📁 Project Structure

```
project/
├── transactions_analyzer.py       ← main script (all 7 phases)
├── transactions_2025_updated.csv  ← your raw input CSV
├── transactions_2025_cleaned.csv  ← auto-generated cleaned CSV
├── monthly_summary.csv            ← auto-generated monthly breakdown
├── report.txt                     ← auto-generated finance report
└── README.md
```

---

## 🚀 How to Run

### Default run (uses built-in file names)
```bash
python transactions_analyzer.py
```

### Custom input file
```bash
python transactions_analyzer.py --input my_data.csv
```

### Full custom paths
```bash
python transactions_analyzer.py \
  --input my_data.csv \
  --output cleaned.csv \
  --report finance_report.txt \
  --summary monthly.csv
```

### Validate only (no cleaning, no report)
```bash
python transactions_analyzer.py --no-clean --no-report
```

### Skip report generation only
```bash
python transactions_analyzer.py --no-report
```

---

## 📋 CSV Format

Your input CSV must have these exact column headers:

```
date,category,description,amount
01/01/2025,Income,Salary January,55000
02/01/2025,Food,Swiggy order,-450
```

| Column        | Format               | Example            |
|---------------|----------------------|--------------------|
| `date`        | `DD/MM/YYYY`         | `15/03/2025`       |
| `category`    | One of valid list    | `Food`             |
| `description` | Free text            | `Swiggy order`     |
| `amount`      | Positive=credit, Negative=debit | `-450` / `55000` |

---

## ✅ Valid Categories

```
Income | Food | Transport | Rent | Entertainment
Utilities | Savings | Shopping | Medical | Subscriptions
```

---

## 🔍 What Each Phase Does

| Phase | Name               | What it does |
|-------|--------------------|--------------|
| 1     | Read CSV           | Loads the file, counts rows |
| 2     | Validate & Clean   | Finds 7 types of errors, fixes or drops bad rows |
| 3     | Categorize         | Totals per category, flags out-of-budget amounts |
| 4     | Monthly Summary    | Month-by-month breakdown table + CSV |
| 5     | Report Generation  | Full finance report saved as `.txt` |
| 6     | argparse CLI       | All options controllable via terminal flags |
| 7     | README             | This file |

---

## 🛡️ Validation Checks (Phase 2)

| Check                | Action taken |
|----------------------|--------------|
| Missing Amount       | 🗑 Row dropped |
| Non-Numeric Amount   | 🗑 Row dropped |
| Invalid Date         | 🗑 Row dropped |
| Duplicate Row        | 🗑 Later copy dropped |
| Missing Description  | ✏️ Filled → `"No description"` |
| Missing Category     | ✏️ Filled → `"Unknown"` |
| Unknown Category     | ✏️ Renamed → `"Unknown"` |

---

## 💸 Budget Ranges (Phase 3 Outlier Detection)

| Category      | Min (₹) | Max (₹) |
|---------------|---------|---------|
| Food          | 200     | 6,000   |
| Entertainment | 1,000   | 3,000   |
| Shopping      | 500     | 10,000  |
| Medical       | 100     | 2,000   |
| Transport     | 100     | 3,000   |
| Utilities     | 200     | 3,000   |
| Subscriptions | 50      | 1,000   |
| Rent          | 5,000   | 30,000  |

---

## 📤 Output Files

| File                             | Contents |
|----------------------------------|----------|
| `transactions_2025_cleaned.csv`  | Cleaned version of your input |
| `monthly_summary.csv`            | One row per month, one column per category |
| `report.txt`                     | Income, expenses, savings rate, top expense months |

---git 

## ⚙️ CLI Reference

```
usage: transactions_analyzer.py [-h] [--input INPUT] [--output OUTPUT]
                                 [--report REPORT] [--summary SUMMARY]
                                 [--no-clean] [--no-report]

options:
  -h, --help         show this help message and exit
  --input  INPUT     Input CSV file         (default: transactions_2025_updated.csv)
  --output OUTPUT    Cleaned CSV output     (default: transactions_2025_cleaned.csv)
  --report REPORT    Text report path       (default: report.txt)
  --summary SUMMARY  Monthly summary CSV    (default: monthly_summary.csv)
  --no-clean         Validate only, skip cleaning and saving
  --no-report        Skip report and summary generation
```

---

## 🐍 Requirements

- Python 3.7+
- No external libraries needed
