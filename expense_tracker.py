"""Project 1: Command-line expense tracker.

Stores expenses in a local JSON file.

Usage:
    python expense_tracker.py add 12.50 food "Lunch"
    python expense_tracker.py list
    python expense_tracker.py summary
    python expense_tracker.py delete 3
"""

import argparse
import json
from collections import defaultdict
from datetime import date
from pathlib import Path

DATA_FILE = Path("expenses.json")


def load():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return []


def save(expenses):
    DATA_FILE.write_text(json.dumps(expenses, indent=2))


def add(args):
    expenses = load()
    next_id = max((e["id"] for e in expenses), default=0) + 1
    expenses.append(
        {
            "id": next_id,
            "date": args.date or date.today().isoformat(),
            "amount": args.amount,
            "category": args.category.lower(),
            "note": args.note,
        }
    )
    save(expenses)
    print(f"Added #{next_id}: {args.amount:.2f} on {args.category}")


def list_all(_args):
    expenses = load()
    if not expenses:
        print("No expenses yet.")
        return
    print(f"{'ID':<4}{'Date':<12}{'Category':<12}{'Amount':>9}  Note")
    for e in sorted(expenses, key=lambda e: e["date"]):
        print(f"{e['id']:<4}{e['date']:<12}{e['category']:<12}{e['amount']:>9.2f}  {e['note']}")


def summary(_args):
    expenses = load()
    if not expenses:
        print("No expenses yet.")
        return
    totals = defaultdict(float)
    for e in expenses:
        totals[e["category"]] += e["amount"]
    grand = sum(totals.values())
    for cat, amt in sorted(totals.items(), key=lambda kv: -kv[1]):
        print(f"{cat:<12}{amt:>10.2f}  {amt / grand:>5.0%}")
    print("-" * 30)
    print(f"{'total':<12}{grand:>10.2f}")


def delete(args):
    expenses = load()
    remaining = [e for e in expenses if e["id"] != args.id]
    if len(remaining) == len(expenses):
        print(f"No expense with id {args.id}.")
        return
    save(remaining)
    print(f"Deleted #{args.id}")


def main():
    parser = argparse.ArgumentParser(description="Simple expense tracker")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="add an expense")
    p_add.add_argument("amount", type=float)
    p_add.add_argument("category")
    p_add.add_argument("note", nargs="?", default="")
    p_add.add_argument("--date", help="YYYY-MM-DD (defaults to today)")
    p_add.set_defaults(func=add)

    sub.add_parser("list", help="list all expenses").set_defaults(func=list_all)
    sub.add_parser("summary", help="totals by category").set_defaults(func=summary)

    p_del = sub.add_parser("delete", help="delete by id")
    p_del.add_argument("id", type=int)
    p_del.set_defaults(func=delete)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
