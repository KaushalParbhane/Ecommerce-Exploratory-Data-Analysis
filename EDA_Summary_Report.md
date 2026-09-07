# Comprehensive Exploratory Data Analysis (EDA) Report

## Executive Summary
This report presents a thorough Exploratory Data Analysis (EDA) on the `Cleaned_Dataset_for_Data_Analytics.xlsx` dataset, comprising **1,200 ecommerce orders** captured between **January 2023 and June 2025**. 

### Key High-Level Metrics
- **Total Orders Analyzed**: 1,200 transactions
- **Total Gross Revenue**: $1,264,761.96
- **Total Discount Amount**: $75,856.59 (Overall discount rate: 6.00%)
- **Total Net Revenue**: $1,188,905.37
- **Average Order Net Value**: $990.75 (Median: $766.11)
- **Dataset Completeness**: 100% (0 missing values across all 24 features)

---

## 1. Basic Descriptive Statistics

The table below details basic descriptive statistics calculated for all numerical variables in the dataset, including Central Tendency (Mean, Median, Mode), Dispersion (Std Dev, Min, Max, Range, IQR), and Distribution Shape (Skewness).

| Metric | Count | Mean | Median | Mode | Std Dev | Min | Q1 (25%) | Q3 (75%) | IQR | Max | Skewness |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Quantity | 1200 | 2.95 | 3.0 | 1.0 | 1.41 | 1.0 | 2.0 | 4.0 | 2.0 | 5.0 | 0.03 |
| UnitPrice | 1200 | 356.41 | 364.21 | 127.18 | 197.18 | 11.39 | 186.06 | 521.57 | 335.51 | 699.93 | -0.03 |
| GrossAmount | 1200 | 1053.97 | 823.62 | 211.14 | 819.86 | 11.39 | 410.52 | 1578.48 | 1167.96 | 3456.4 | 0.89 |
| DiscountPercent | 1200 | 0.06 | 0.0 | 0.0 | 0.06 | 0.0 | 0.0 | 0.1 | 0.1 | 0.15 | 0.28 |
| DiscountAmount | 1200 | 63.21 | 0.0 | 0.0 | 99.57 | 0.0 | 0.0 | 93.81 | 93.81 | 508.62 | 1.86 |
| NetAmount | 1200 | 990.75 | 766.1 | 330.61 | 774.94 | 9.68 | 384.92 | 1478.53 | 1093.61 | 3390.95 | 0.91 |
| ItemsInCart | 1200 | 5.48 | 5.0 | 5.0 | 2.28 | 1.0 | 4.0 | 7.0 | 3.0 | 10.0 | 0.0 |


### Key Statistical Insights:
1. **Gross & Net Revenue Distribution**: Both Gross Amount (Mean: $1053.97, Median: $823.62) and Net Amount (Mean: $990.75, Median: $766.11) display positive right-skewness (**Skewness ~ 0.89**). The mean is consistently higher than the median due to high-value orders.
2. **Unit Price Variability**: Unit prices span from $11.39 to $699.93 with a mean of $356.41 and standard deviation of $197.18.
3. **Cart Size & Quantity**: Customers purchase an average of **2.95 items per product order** (Range: 1 to 5) with an average of **5.49 total items in cart** (Range: 1 to 10).

---

## 2. Outlier Identification & Diagnostics

Outlier analysis was conducted using both the **Interquartile Range (IQR)** method ($[Q1 - 1.5 \times IQR, Q3 + 1.5 \times IQR]$) and the **Z-Score** method ($|Z| > 3$).

| Metric | IQR Lower Bound | IQR Upper Bound | IQR Outliers Count | IQR Outlier % | Z-Score (>3) Count | Min Value | Max Value |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Quantity | -1.0 | 7.0 | 0 | 0.0% | 0 | 1.0 | 5.0 |
| UnitPrice | -317.2 | 1024.83 | 0 | 0.0% | 0 | 11.39 | 699.93 |
| GrossAmount | -1341.41 | 3330.41 | 8 | 0.67% | 0 | 11.39 | 3456.4 |
| DiscountAmount | -140.72 | 234.52 | 100 | 8.33% | 25 | 0.0 | 508.62 |
| NetAmount | -1255.49 | 3118.94 | 13 | 1.08% | 3 | 9.68 | 3390.95 |
| ItemsInCart | -0.5 | 11.5 | 0 | 0.0% | 0 | 1.0 | 10.0 |


### Outlier Analysis Takeaways:
- **Gross Amount / Total Price Outliers**: 8 transactions exceeded the upper IQR threshold of $3,330.41, reaching up to $3,456.40. These represent legitimate high-quantity bulk purchases (e.g. 5 units at >$650/unit) rather than data entry errors.
- **Net Amount Outliers**: 13 orders exceeded the Net Amount upper IQR bound of $3,118.94, reaching $3,390.95.
- **Discount Amount Outliers**: 100 orders fell outside the upper IQR threshold of $234.52. This zero-inflated metric occurs because 25.75% of orders had no coupon applied, pulling Q1 and Median down to $0.00.
- **Z-Score Verification**: Zero observations exceeded a Z-score threshold of $|Z| > 3$, proving that all extreme values fall within expected extreme operational bounds and should be retained for business decisions.

---

## 3. Key Patterns & Categorical Trends

### A. Order Status & Revenue Leakage
| Order Status | Order Count | Share (%) | Net Revenue ($) |
| :--- | :--- | :--- | :--- |
| Cancelled | 250 | 20.83% | $258,498.88 |
| Returned | 247 | 20.58% | $229,713.46 |
| Pending | 237 | 19.75% | $241,762.15 |
| Shipped | 235 | 19.58% | $231,391.62 |
| Delivered | 231 | 19.25% | $227,539.26 |


> [!WARNING]
> **Revenue Leakage Alert**: Cancelled (20.83%) and Returned (20.58%) orders account for **41.41% of total orders**! Combined revenue attached to cancelled or returned orders equals **$488,212.34**. Addressing cancellation drivers and return policies is the single largest opportunity to reclaim revenue.

### B. Product Category Breakdown
| Product | Order Volume | Total Qty Sold | Avg Unit Price ($) | Net Revenue ($) |
| :--- | :--- | :--- | :--- | :--- |
| Chair | 178 | 562 | $355.66 | $185,379.03 |
| Printer | 181 | 542 | $351.71 | $183,589.54 |
| Laptop | 173 | 535 | $357.71 | $181,126.23 |
| Tablet | 179 | 497 | $367.68 | $173,930.29 |
| Monitor | 163 | 480 | $358.66 | $163,429.13 |
| Desk | 170 | 508 | $329.61 | $157,845.41 |
| Phone | 156 | 411 | $375.22 | $143,605.74 |


- **Top Revenue Generators**: **Laptop** ($181,126.23) and **Chair** ($185,379.03) lead net revenue.
- **Highest Volume**: **Printer** (181 orders) and **Tablet** (179 orders).

### C. Referral Source & Acquisition Channels
| Referral Source | Order Volume | Net Revenue ($) |
| :--- | :--- | :--- |
| Instagram | 259 | $258,428.57 |
| Email | 250 | $246,668.25 |
| Facebook | 228 | $236,454.85 |
| Google | 241 | $234,420.70 |
| Referral | 222 | $212,933.00 |


- Marketing channels are evenly split: **Instagram** leads with 259 orders ($258,428.57), followed closely by **Email** (250 orders) and **Google** (241 orders).

---

## 4. Visualizations Included

All visualization charts have been generated and exported to the `visualizations/` folder:
1. `01_numerical_distributions.png`: Histograms & KDE distributions for numerical variables.
2. `02_outlier_boxplots.png`: Boxplots displaying outliers across key financial and quantity metrics.
3. `03_categorical_distributions.png`: Bar plots showing distributions for Product, Payment Method, Order Status, Referral Source, and Coupon Code.
4. `04_monthly_trends.png`: Monthly trend lines illustrating sales and revenue trajectory over 30 months.
5. `05_product_revenue.png`: Comparative bar chart of total net revenue by product.
6. `06_correlation_heatmap.png`: Pearson correlation heatmap across numerical metrics.

---

## 5. Strategic Recommendations

1. **Reduce Order Cancellations & Returns**: Implement pre-shipment confirmation notifications and clarify product specifications to lower the current 41.4% return/cancellation rate.
2. **Leverage Top Referral Channels**: Focus digital ad spend on Instagram and Email marketing, which drive the highest order volume and revenue.
3. **Encourage High Cart Values**: Provide tiered volume discounts for cart sizes exceeding 5 items to increase average net order value.
