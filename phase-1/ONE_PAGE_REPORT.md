# One-Page Report: E-Commerce Sales Performance Analysis

**Project:** Phase 1 Mini Project — EDA
**Dataset:** Brazilian E-Commerce Public Dataset by Olist (Kaggle)
**Analyst:** AI/ML Cohort Student

---

## Objective

Perform a complete Exploratory Data Analysis on Olist's multi-table e-commerce transaction
data to identify which product categories, regions, customer segments, and time periods
drive the most revenue — and translate those findings into actionable business
recommendations.

---

## Dataset Description

| Table | Key Columns |
|---|---|
| `olist_orders` | order_id, customer_id, order_status, order_purchase_timestamp |
| `olist_order_items` | order_id, product_id, seller_id, price, freight_value |
| `olist_customers` | customer_id, customer_city, customer_state |
| `olist_products` | product_id, product_category_name |
| `olist_sellers` | seller_id, seller_city, seller_state |
| `olist_order_payments` | order_id, payment_type, payment_installments, payment_value |
| `olist_order_reviews` | order_id, review_score |

Seven files were merged into one master dataset using `order_id`, `customer_id`,
`product_id`, and `seller_id` as join keys. Merge key coverage was ≥99% across all tables
with no unexpected fan-out or record loss.

---

## Data Cleaning Summary

| Issue Found | Action Taken |
|---|---|
| Null `product_category_name` values (~5% of product rows) | Filled with `'unknown'` to preserve row counts |
| Null `review_score` values (~10% of reviews) | Dropped — imputation would introduce bias |
| Canceled orders present in order items | Excluded from all revenue analyses |
| `price`, `freight_value`, `payment_value` stored as object | Cast to `float64` with `pd.to_numeric` |
| Timestamp columns stored as string | Parsed to `datetime64` with `pd.to_datetime` |
| Duplicate records | None found across all tables |

All cleaning decisions were documented before any analysis was performed.

---

## Analysis Findings

**Q1 – Revenue by Category**
*Bed Bath Table*, *Health Beauty*, and *Watches Gifts* are the top three categories,
collectively driving ~40% of total delivered revenue. *Office Furniture* and *Garden
Tools* lag behind and represent growth opportunities.

**Q2 – Regional Sales**
São Paulo (SP) accounts for ~30% of all orders and revenue. The Southeast region (SP, RJ,
MG) contributes over 55% of total revenue. The Northeast states — CE (Ceará) and BA
(Bahia) — are emerging markets where logistics investment could unlock significant growth.

**Q3 – Customer Segments**
Customers were segmented by total spend into High, Medium, and Low tiers using 33rd/66th
percentile thresholds. The High segment (~34% of customers) generates ~71% of revenue;
Medium (~33%) contributes ~20%; and Low (~33%) contributes only ~8%. Revenue is
heavily concentrated in the top spend tier.

**Q4 – Purchase Patterns**
Peak buying occurs on weekdays (Monday–Thursday) during afternoon hours (10:00–17:00).
Approximately 70% of orders contain only one item, indicating specific-purpose purchasing
rather than large basket behaviour. Flash deals timed for weekday afternoons could
capture this peak window effectively.

**Q5 – Top Products**
Top revenue SKUs belong to *Health Beauty*, *Computers & Accessories*, *Bed Bath Table*,
*Watches Gifts*, and *Furniture Decor*. A clear split exists between high-volume
low-margin products and low-volume high-value products — each requiring a distinct
pricing and promotion strategy.

**Q6 – Payment Methods**
Credit card handles ~74% of transactions with an average of ~5 installments per order.
Boleto (bank slip) accounts for ~19%, serving customers without credit card access.
The strong installment culture suggests "0% installment" promotions could materially
increase average order value.

**Q7 – Seller Performance**
A classic Pareto pattern exists — the top 10 sellers generate a disproportionate share
of total revenue. A strong positive correlation between order count and revenue was
confirmed. Mid-tier sellers with high order counts but below-average revenue could
benefit from pricing or product-mix coaching.

**Q8 – Review Scores**
Most categories maintain scores above 4.0, reflecting strong overall customer satisfaction.
Categories scoring below 3.8 (typically Electronics and Telephony) signal quality or
delivery experience gaps. Regional scores are relatively uniform, indicating that issues
are product-driven rather than logistics-driven.

**Q9 – Sales Over Time**
A clear upward growth trend is visible from early 2017 through mid-2018, with seasonal
peaks around November (Black Friday / Cyber Monday) and Q1. Pre-positioning inventory
and increasing ad spend 4–6 weeks ahead of the November peak is strongly recommended.

**Q10 – Repeat vs One-Time Customers**
Virtually all customers in this dataset are one-time buyers (100% in the sample).
This represents the single largest retention opportunity — converting even 10% of
one-time buyers to repeat customers would significantly improve Customer Lifetime Value.

**Q11 – Data Quality**
The primary issues were null product categories (~5%) and null review scores (~10%),
both handled conservatively. No duplicate order-item records were found, and all prices
were positive. The dataset is reasonably clean for a real-world multi-file source.

**Q12 – Merge Reliability**
All key joins maintained ≥99% coverage. The multi-file master dataset merges cleanly
with no significant data loss. Unmatched category translations fell back to the raw
(underscore-formatted) category name. The merged dataset is reliable for analysis.

---

## Key Visualizations

| Chart File | Question Answered |
|---|---|
| `q1_revenue_by_category.png` | Revenue by product category (horizontal bar) |
| `q2_regional_sales.png` | Revenue and order count by state (dual bar) |
| `q3_customer_segments.png` | Customer count and revenue by spend segment |
| `q4_purchase_patterns.png` | Orders by day-of-week and hour-of-day |
| `q4c_basket_size.png` | Distribution of items per order |
| `q5_top_products.png` | Top-10 products by revenue and by units sold |
| `q6_payment_methods.png` | Transaction share, revenue, and avg value by payment method |
| `q7_seller_performance.png` | Top-15 sellers by revenue + orders vs revenue scatter |
| `q8_review_scores.png` | Avg review score by category and by state |
| `q9_sales_over_time.png` | Monthly order volume and revenue trend lines |
| `q10_repeat_customers.png` | Repeat vs one-time customer pie + order frequency distribution |
| `q11_data_quality.png` | Missing value % across master dataset columns |
| `q12_merge_reliability.png` | Key coverage % across all table joins |

---

## Final Conclusion & Recommendations

| Priority | Recommendation | Rationale |
|---|---|---|
| 🔴 High | Launch a post-purchase loyalty programme | ~100% one-time buyers — retention is the highest-ROI lever |
| 🔴 High | Increase marketing spend on Bed Bath Table, Health Beauty & Watches Gifts | Top revenue categories with strong review scores |
| 🔴 High | Expand logistics partnerships in CE, BA, PE (Northeast) | Emerging demand with under-served delivery infrastructure |
| 🟠 Medium | Pre-stock and ramp ad spend 6 weeks before November | Clear Black Friday seasonal peak confirmed |
| 🟠 Medium | Offer "0% installment" promotions on high-ticket items | Credit card installment behaviour drives purchase decisions |
| 🟡 Low | Investigate quality issues in Electronics & Telephony | Below-average review scores risk brand reputation |
| 🟡 Low | Coach mid-tier sellers on pricing and product mix | High order count but below-average revenue per seller |

**Bottom line:** The business has strong product-market fit in the Southeast, led by home,
health, and lifestyle categories. The most urgent untapped opportunity is **customer
retention** — building a loyalty loop around the one-time buyer majority would compound
revenue growth without requiring proportional increases in acquisition spend.
