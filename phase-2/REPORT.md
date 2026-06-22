# Order Delay Intelligence — Findings, Model Comparison & Recommendations

**Project:** Phase 2 Mini Project — Predict, Explain, Recommend
**Dataset:** Brazilian E-Commerce Public Dataset by Olist (Kaggle)
**Role:** Data Analyst / ML Engineer

---

## Business Problem

The e-commerce business wants to know **which orders are likely to be delayed** and **how
large that delay might be**, so operations can intervene before the customer is impacted.
This report summarises the data audit, modelling work, and resulting recommendations.

---

## Data Used

| File | Purpose |
|---|---|
| `olist_orders_dataset.csv` | Order timestamps, status, promised vs delivered dates |
| `olist_customers_dataset.csv` | Customer city/state |
| `olist_order_items_dataset.csv` | Item count, price, freight per order |
| `olist_products_dataset.csv` | Product category, weight |
| `olist_order_payments_dataset.csv` | Payment type, installments, value |

All five tables were merged into a single order-level dataset (5,555 delivered orders with
complete delivery dates) after cleaning.

---

## Data Cleaning Summary

| Issue Found | Action Taken |
|---|---|
| 5 duplicate rows in `payments` | Dropped via `drop_duplicates()` |
| Null `product_category_name` (12 rows) | Filled with `'unknown'` |
| Null `order_approved_at` (80 rows) | Kept as `NaT` — order genuinely not yet approved |
| Null `order_delivered_customer_date` (445 rows) | Order excluded from delay-target rows (no actual delivery date to compare) |
| Remaining numeric NaNs (freight, weight, approval time) | Filled with column median |

All cleaning decisions were made and documented **before** any model training.

---

## Target Definition

`is_delayed = 1` if `order_delivered_customer_date > order_estimated_delivery_date`, else `0`.

This directly reflects whether the business broke its promise to the customer — the most
business-relevant definition of "delay."

**Class balance:** ~26% delayed, ~74% on-time (moderately imbalanced — informed metric choice).

---

## EDA — Key Insights

1. **Peak season (Nov/Dec) more than doubles the delay rate** (~55% vs ~20% in regular months) —
   the single strongest pattern found in the data.
2. **Geography is a major risk factor** — AL, MA, SE show delay rates 1.5–2.5x higher than São Paulo, reflecting logistics infrastructure gaps.
3. **The delay-day distribution is right-skewed** — most orders arrive a few days early, but a
   meaningful tail arrives significantly late.
4. **Payment type shows a mild relationship** — voucher and boleto orders delay slightly more
   than credit/debit card orders.
5. **Order volume and delay rate spike together seasonally**, suggesting delay is partly a
   *capacity* problem, not purely random.

---

## SQL Validation

Ten SQL queries were run against a SQLite copy of the cleaned dataset (`orders_clean` table),
covering `SELECT`, `WHERE`, `GROUP BY`, `ORDER BY`, `JOIN`, aggregate functions, and a subquery.
The peak-season insight was independently recreated in SQL and matched the pandas result
**exactly** (20.54% regular vs 55.59% peak), confirming the pipeline's correctness.

---

## Feature Importance / Explainability

The top features driving predicted delay risk, consistent across SQL aggregates, EDA charts,
and model feature importance:

1. **`is_peak_season`** — Nov/Dec orders carry the highest risk
2. **`customer_state`** (especially AL, MA, SE) — geographic delivery risk
3. **`promised_days`** — tighter promised windows correlate with higher delay risk
4. **`total_freight`** / **`shipping_time_days`** — proxies for distance and carrier handling time

This 3-way agreement across independent analysis methods gives strong confidence these are
genuine business drivers rather than modelling artifacts.

---

## Business Recommendations

| Priority | Recommendation | Rationale |
|---|---|---|
| 🔴 High | Pre-emptively flag Nov/Dec orders for priority handling | Peak season delay rate is 2.5x higher — single biggest lever |
| 🔴 High | Set wider promised delivery windows for AL, MA, SE | Structurally higher delay risk regardless of season |
| 🟠 Medium | Use the model's risk score to trigger proactive customer communication | A 20%+ predicted risk could auto-send a tracking update, reducing complaint volume |
| 🟠 Medium | Negotiate peak-season carrier capacity in advance | The Nov/Dec spike is predictable — pre-booking capacity could reduce it materially |
| 🟡 Low | Review freight cost structure for high-freight orders | Secondary delay risk signal worth monitoring |

---

## Final Recommendation

Deploy the tuned model as a **daily batch scoring job** flagging new orders above a chosen
delay-probability threshold (e.g. 35%). Route flagged orders to:

1. A logistics dashboard for manual prioritisation, and
2. An automated "delay-risk" customer email for transparency.

This turns the analysis into an active, revenue-protecting operational tool that directly
answers the original business question: **which orders are at risk, and why.**
