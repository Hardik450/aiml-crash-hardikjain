# aiml-crash-hardikjain

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Status](https://img.shields.io/badge/status-work%20in%20progress-yellow)
![License](https://img.shields.io/badge/license-MIT-green)

Self-practice tasks from the CodeTrade.io AI/ML Crash Course — Days 2 & 4.  
Each file is standalone, requires no third-party packages unless noted, and runs with a single `python` command.

---

## Setup

```bash
git clone https://github.com/hardik450/aiml-crash-hardikjain.git
cd aiml-crash-hardikjain
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
.venv\Scripts\activate         # Windows
pip install pandas             # required for Task 07 only
```

---

## Day 2 — Python Basics

| File | What it does | Run |
|---|---|---|
| `intro.py` | Prints a 4-line self-introduction using a dict and f-strings | `python intro.py` |
| `skills_counter.py` | Prints a numbered skill list using `enumerate()` and shows the total count | `python skills_counter.py` |
| `even_odd.py` | Asks for a number and classifies it as even, odd, or zero; handles bad input with `try/except` | `python even_odd.py` |
| `tip_calculator.py` | Calculates tip and total for 3 test bills via a function that returns a dict | `python tip_calculator.py` |
| `word_frequency.py` | Counts word frequency in a sentence; compares a manual approach with `collections.Counter` | `python word_frequency.py` |
| `calculator.py` | Interactive 4-operation calculator using dict-based function dispatch; handles division by zero | `python calculator.py` |
| `grade_classifier.py` | Classifies 5 students' grades and prints them sorted highest to lowest using `sorted()` + `lambda` | `python grade_classifier.py` |
| `guessing_game.py` | Random number guessing game (1–100) with a 7-attempt maximum | `python guessing_game.py` |
| `contact_book.py` | Case-insensitive contact search over a list of dicts | `python contact_book.py` |

---

## Day 4 — OOP, File I/O & Pandas

| File | What it does | Run |
|---|---|---|
| `student_report.py` | OOP — `Student` class with `average()`, `grade()`, and `__str__()`; uses a class variable for school name | `python student_report.py` |
| `comprehension_drills.py` | Four list comprehension drills — filtering, title case, Celsius→Fahrenheit, flattening; plus dict & set comprehension examples | `python comprehension_drills.py` |
| `file_records.py` | Creates `students.csv`, reads it back to compute averages, then writes `results.csv` using `csv.DictWriter` | `python file_records.py` |
| `typed_calculator.py` | Upgraded calculator with full type hints, docstrings, `power()`, `modulo()`, and `Optional[float]` on `divide()` | `python typed_calculator.py` |
| `library_system.py` | OOP inheritance — `LibraryItem` base class with `Book` and `EBook` children; demonstrates `isinstance()` | `python library_system.py` |
| `config_manager.py` | JSON config manager with `save_config()`, `load_config()`, and `update_config()`; explains `json.dump` vs `json.dumps` | `python config_manager.py` |
| `pandas_explore.py` | Pandas DataFrame of 10 students — average per subject, top scorer, city counts, score filter, top-3 with `nlargest()` | `python pandas_explore.py` |
| `fraction_class.py` | Custom `Fraction` class with `__str__`, `__add__`, `__eq__`, `__lt__` and GCD simplification; notes on `@total_ordering` | `python fraction_class.py` |
| `inventory.py` | OOP + CSV — `Product` and `Inventory` classes with add, search, total value, save/load; explains `@staticmethod` vs `@classmethod` | `python inventory.py` |

---

## Generated Files

| File | Created by |
|---|---|
| `students.csv` | `file_records.py` |
| `results.csv` | `file_records.py` |
| `config.json` | `config_manager.py` |
| `inventory.csv` | `inventory.py` |

---

## .gitignore Highlights

```
.venv/
__pycache__/

```
