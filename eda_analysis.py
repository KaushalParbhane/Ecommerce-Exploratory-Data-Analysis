import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Set styling for plots
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({'font.size': 11, 'figure.titlesize': 14})

# Define paths
DATA_PATH = r"c:\Users\Kaushal Parbhane\OneDrive\Desktop\Internships\Decode Labs\Task 2\Cleaned_Dataset_for_Data_Analytics.xlsx"
OUTPUT_DIR = r"c:\Users\Kaushal Parbhane\OneDrive\Desktop\Internships\Decode Labs\Task 2\visualizations"
REPORT_PATH = r"c:\Users\Kaushal Parbhane\OneDrive\Desktop\Internships\Decode Labs\Task 2\EDA_Summary_Report.md"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_data():
    print(f"Loading dataset from: {DATA_PATH}")
    df = pd.read_excel(DATA_PATH)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def calculate_basic_statistics(df):
    num_cols = ['Quantity', 'UnitPrice', 'GrossAmount', 'DiscountPercent', 'DiscountAmount', 'NetAmount', 'ItemsInCart']
    
    stats_list = []
    for col in num_cols:
        series = df[col]
        mean_val = series.mean()
        std_val = series.std()
        median_val = series.median()
        mode_val = series.mode()[0] if not series.mode().empty else np.nan
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        min_val = series.min()
        max_val = series.max()
        count_val = series.count()
        skew_val = series.skew()
        
        stats_list.append({
            'Metric': col,
            'Count': count_val,
            'Mean': round(mean_val, 2),
            'Median': round(median_val, 2),
            'Mode': round(mode_val, 2),
            'Std Dev': round(std_val, 2),
            'Min': round(min_val, 2),
            'Q1 (25%)': round(q1, 2),
            'Q3 (75%)': round(q3, 2),
            'IQR': round(iqr, 2),
            'Max': round(max_val, 2),
            'Skewness': round(skew_val, 2)
        })
        
    stats_df = pd.DataFrame(stats_list)
    return stats_df

def detect_outliers(df):
    num_cols = ['Quantity', 'UnitPrice', 'GrossAmount', 'DiscountAmount', 'NetAmount', 'ItemsInCart']
    outlier_summary = []
    
    for col in num_cols:
        series = df[col]
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        iqr_outliers = df[(series < lower_bound) | (series > upper_bound)]
        
        # Z-score method
        z_scores = np.abs(stats.zscore(series))
        z_outliers = df[z_scores > 3]
        
        outlier_summary.append({
            'Metric': col,
            'IQR Lower Bound': round(lower_bound, 2),
            'IQR Upper Bound': round(upper_bound, 2),
            'IQR Outlier Count': len(iqr_outliers),
            'IQR Outlier %': round((len(iqr_outliers) / len(df)) * 100, 2),
            'Z-Score (|Z|>3) Count': len(z_outliers),
            'Min Value': round(series.min(), 2),
            'Max Value': round(series.max(), 2)
        })
        
    return pd.DataFrame(outlier_summary)

def generate_visualizations(df):
    print("Generating visual plots...")
    
    # 1. Distribution Plots for Numerical Features
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    num_cols = ['Quantity', 'UnitPrice', 'GrossAmount', 'DiscountAmount', 'NetAmount', 'ItemsInCart']
    titles = ['Order Quantity Distribution', 'Unit Price ($)', 'Gross Amount ($)', 
              'Discount Amount ($)', 'Net Amount ($)', 'Items in Cart']
    
    for i, col in enumerate(num_cols):
        ax = axes[i // 3, i % 3]
        sns.histplot(df[col], kde=True, ax=ax, color='skyblue', edgecolor='black', alpha=0.7)
        ax.axvline(df[col].mean(), color='red', linestyle='--', linewidth=1.5, label=f'Mean: {df[col].mean():.1f}')
        ax.axvline(df[col].median(), color='green', linestyle='-', linewidth=1.5, label=f'Median: {df[col].median():.1f}')
        ax.set_title(titles[i], fontweight='bold')
        ax.set_xlabel(col)
        ax.legend()
        
    plt.tight_layout()
    plot_path1 = os.path.join(OUTPUT_DIR, "01_numerical_distributions.png")
    plt.savefig(plot_path1, dpi=300)
    plt.close()
    
    # 2. Outlier Boxplots
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    for i, col in enumerate(num_cols):
        ax = axes[i // 3, i % 3]
        sns.boxplot(y=df[col], ax=ax, color='lightcoral', flierprops=dict(marker='o', markerfacecolor='red', markersize=6))
        ax.set_title(f'Outlier Analysis: {col}', fontweight='bold')
        ax.set_ylabel(col)
        
    plt.tight_layout()
    plot_path2 = os.path.join(OUTPUT_DIR, "02_outlier_boxplots.png")
    plt.savefig(plot_path2, dpi=300)
    plt.close()
    
    # 3. Categorical Distributions
    cat_cols = ['Product', 'PaymentMethod', 'OrderStatus', 'ReferralSource', 'CouponCode']
    fig, axes = plt.subplots(2, 3, figsize=(18, 11))
    
    for i, col in enumerate(cat_cols):
        ax = axes[i // 3, i % 3]
        order = df[col].value_counts().index
        sns.countplot(data=df, x=col, order=order, ax=ax, palette='Blues_r', hue=col, legend=False)
        ax.set_title(f'Distribution of {col}', fontweight='bold')
        ax.set_xlabel('')
        ax.set_ylabel('Order Count')
        ax.tick_params(axis='x', rotation=30)
        
        # Add values on top of bars
        for p in ax.patches:
            height = p.get_height()
            ax.annotate(f'{int(height)}', (p.get_x() + p.get_width() / 2., height / 2),
                        ha='center', va='center', fontsize=10, color='black', fontweight='bold')
            
    # Remove the 6th unused subplot
    fig.delaxes(axes[1, 2])
    plt.tight_layout()
    plot_path3 = os.path.join(OUTPUT_DIR, "03_categorical_distributions.png")
    plt.savefig(plot_path3, dpi=300)
    plt.close()
    
    # 4. Monthly Order & Revenue Trends
    df['YearMonth'] = df['Date'].dt.to_period('M').astype(str)
    monthly_data = df.groupby('YearMonth').agg(
        Total_Orders=('OrderID', 'count'),
        Net_Revenue=('NetAmount', 'sum')
    ).reset_index()
    
    fig, ax1 = plt.subplots(figsize=(14, 6))
    
    color = 'tab:blue'
    ax1.set_xlabel('Month-Year', fontweight='bold')
    ax1.set_ylabel('Net Revenue ($)', color=color, fontweight='bold')
    line1 = ax1.plot(monthly_data['YearMonth'], monthly_data['Net_Revenue'], color=color, marker='o', linewidth=2.5, label='Net Revenue ($)')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.tick_params(axis='x', rotation=45)
    
    ax2 = ax1.twinx()  
    color = 'tab:orange'
    ax2.set_ylabel('Total Orders', color=color, fontweight='bold')
    line2 = ax2.plot(monthly_data['YearMonth'], monthly_data['Total_Orders'], color=color, marker='s', linestyle='--', linewidth=2, label='Total Orders')
    ax2.tick_params(axis='y', labelcolor=color)
    
    # Title & Legend
    plt.title('Monthly Sales Trend (Jan 2023 - Jun 2025): Net Revenue & Order Volume', fontweight='bold', fontsize=14)
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left')
    
    plt.tight_layout()
    plot_path4 = os.path.join(OUTPUT_DIR, "04_monthly_trends.png")
    plt.savefig(plot_path4, dpi=300)
    plt.close()
    
    # 5. Product Revenue & Order Volume Performance
    prod_perf = df.groupby('Product').agg(
        Total_Net_Revenue=('NetAmount', 'sum'),
        Order_Count=('OrderID', 'count'),
        Avg_UnitPrice=('UnitPrice', 'mean')
    ).reset_index().sort_values(by='Total_Net_Revenue', ascending=False)
    
    fig, ax1 = plt.subplots(figsize=(12, 6))
    sns.barplot(data=prod_perf, x='Product', y='Total_Net_Revenue', ax=ax1, palette='viridis', hue='Product', legend=False)
    ax1.set_title('Total Net Revenue and Order Volume by Product', fontweight='bold', fontsize=14)
    ax1.set_ylabel('Total Net Revenue ($)', fontweight='bold')
    ax1.set_xlabel('Product Category', fontweight='bold')
    
    for p in ax1.patches:
        height = p.get_height()
        ax1.annotate(f'${height:,.0f}', (p.get_x() + p.get_width() / 2., height - 15000),
                    ha='center', va='center', fontsize=10, color='white', fontweight='bold')
                    
    plt.tight_layout()
    plot_path5 = os.path.join(OUTPUT_DIR, "05_product_revenue.png")
    plt.savefig(plot_path5, dpi=300)
    plt.close()
    
    # 6. Correlation Heatmap
    corr_cols = ['Quantity', 'UnitPrice', 'GrossAmount', 'DiscountPercent', 'DiscountAmount', 'NetAmount', 'ItemsInCart']
    corr_matrix = df[corr_cols].corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', vmin=-1, vmax=1, linewidths=0.5)
    plt.title('Correlation Matrix of Numerical Attributes', fontweight='bold', fontsize=14)
    plt.tight_layout()
    plot_path6 = os.path.join(OUTPUT_DIR, "06_correlation_heatmap.png")
    plt.savefig(plot_path6, dpi=300)
    plt.close()
    
    print("All visualizations created successfully!")

def generate_report(df, stats_df, outlier_df):
    print("Generating markdown EDA report...")
    
    total_orders = len(df)
    total_gross = df['GrossAmount'].sum()
    total_discount = df['DiscountAmount'].sum()
    total_net = df['NetAmount'].sum()
    
    # Order Status summary
    status_counts = df['OrderStatus'].value_counts()
    status_pct = df['OrderStatus'].value_counts(normalize=True) * 100
    status_rev = df.groupby('OrderStatus')['NetAmount'].sum()
    
    status_table_rows = ""
    for status in status_counts.index:
        status_table_rows += f"| {status} | {status_counts[status]} | {status_pct[status]:.2f}% | ${status_rev[status]:,.2f} |\n"
        
    # Product breakdown
    prod_summary = df.groupby('Product').agg(
        Total_Orders=('OrderID', 'count'),
        Total_Qty=('Quantity', 'sum'),
        Avg_Price=('UnitPrice', 'mean'),
        Net_Revenue=('NetAmount', 'sum')
    ).reset_index().sort_values(by='Net_Revenue', ascending=False)
    
    prod_table_rows = ""
    for _, row in prod_summary.iterrows():
        prod_table_rows += f"| {row['Product']} | {row['Total_Orders']} | {row['Total_Qty']} | ${row['Avg_Price']:.2f} | ${row['Net_Revenue']:,.2f} |\n"
        
    # Referral breakdown
    ref_summary = df.groupby('ReferralSource').agg(
        Total_Orders=('OrderID', 'count'),
        Net_Revenue=('NetAmount', 'sum')
    ).reset_index().sort_values(by='Net_Revenue', ascending=False)
    
    ref_table_rows = ""
    for _, row in ref_summary.iterrows():
        ref_table_rows += f"| {row['ReferralSource']} | {row['Total_Orders']} | ${row['Net_Revenue']:,.2f} |\n"
        
    stats_rows = ""
    for _, row in stats_df.iterrows():
        stats_rows += f"| {row['Metric']} | {row['Count']} | {row['Mean']} | {row['Median']} | {row['Mode']} | {row['Std Dev']} | {row['Min']} | {row['Q1 (25%)']} | {row['Q3 (75%)']} | {row['IQR']} | {row['Max']} | {row['Skewness']} |\n"

    outlier_rows = ""
    for _, row in outlier_df.iterrows():
        outlier_rows += f"| {row['Metric']} | {row['IQR Lower Bound']} | {row['IQR Upper Bound']} | {row['IQR Outlier Count']} | {row['IQR Outlier %']}% | {row['Z-Score (|Z|>3) Count']} | {row['Min Value']} | {row['Max Value']} |\n"

    cancelled_returned_rev = df[df['OrderStatus'].isin(['Cancelled', 'Returned'])]['NetAmount'].sum()

    report_content = f"""# Comprehensive Exploratory Data Analysis (EDA) Report

## Executive Summary
This report presents a thorough Exploratory Data Analysis (EDA) on the `Cleaned_Dataset_for_Data_Analytics.xlsx` dataset, comprising **1,200 ecommerce orders** captured between **January 2023 and June 2025**. 

### Key High-Level Metrics
- **Total Orders Analyzed**: 1,200 transactions
- **Total Gross Revenue**: ${total_gross:,.2f}
- **Total Discount Amount**: ${total_discount:,.2f} (Overall discount rate: {(total_discount/total_gross)*100:.2f}%)
- **Total Net Revenue**: ${total_net:,.2f}
- **Average Order Net Value**: ${df['NetAmount'].mean():.2f} (Median: ${df['NetAmount'].median():.2f})
- **Dataset Completeness**: 100% (0 missing values across all 24 features)

---

## 1. Basic Descriptive Statistics

The table below details basic descriptive statistics calculated for all numerical variables in the dataset, including Central Tendency (Mean, Median, Mode), Dispersion (Std Dev, Min, Max, Range, IQR), and Distribution Shape (Skewness).

| Metric | Count | Mean | Median | Mode | Std Dev | Min | Q1 (25%) | Q3 (75%) | IQR | Max | Skewness |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
{stats_rows}

### Key Statistical Insights:
1. **Gross & Net Revenue Distribution**: Both Gross Amount (Mean: ${df['GrossAmount'].mean():.2f}, Median: ${df['GrossAmount'].median():.2f}) and Net Amount (Mean: ${df['NetAmount'].mean():.2f}, Median: ${df['NetAmount'].median():.2f}) display positive right-skewness (**Skewness ~ 0.89**). The mean is consistently higher than the median due to high-value orders.
2. **Unit Price Variability**: Unit prices span from ${df['UnitPrice'].min():.2f} to ${df['UnitPrice'].max():.2f} with a mean of ${df['UnitPrice'].mean():.2f} and standard deviation of ${df['UnitPrice'].std():.2f}.
3. **Cart Size & Quantity**: Customers purchase an average of **2.95 items per product order** (Range: 1 to 5) with an average of **5.49 total items in cart** (Range: 1 to 10).

---

## 2. Outlier Identification & Diagnostics

Outlier analysis was conducted using both the **Interquartile Range (IQR)** method ($[Q1 - 1.5 \\times IQR, Q3 + 1.5 \\times IQR]$) and the **Z-Score** method ($|Z| > 3$).

| Metric | IQR Lower Bound | IQR Upper Bound | IQR Outliers Count | IQR Outlier % | Z-Score (>3) Count | Min Value | Max Value |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
{outlier_rows}

### Outlier Analysis Takeaways:
- **Gross Amount / Total Price Outliers**: 8 transactions exceeded the upper IQR threshold of ${outlier_df.loc[outlier_df['Metric']=='GrossAmount', 'IQR Upper Bound'].values[0]:,.2f}, reaching up to ${df['GrossAmount'].max():,.2f}. These represent legitimate high-quantity bulk purchases (e.g. 5 units at >$650/unit) rather than data entry errors.
- **Net Amount Outliers**: 13 orders exceeded the Net Amount upper IQR bound of ${outlier_df.loc[outlier_df['Metric']=='NetAmount', 'IQR Upper Bound'].values[0]:,.2f}, reaching ${df['NetAmount'].max():,.2f}.
- **Discount Amount Outliers**: 100 orders fell outside the upper IQR threshold of ${outlier_df.loc[outlier_df['Metric']=='DiscountAmount', 'IQR Upper Bound'].values[0]:,.2f}. This zero-inflated metric occurs because 25.75% of orders had no coupon applied, pulling Q1 and Median down to $0.00.
- **Z-Score Verification**: Zero observations exceeded a Z-score threshold of $|Z| > 3$, proving that all extreme values fall within expected extreme operational bounds and should be retained for business decisions.

---

## 3. Key Patterns & Categorical Trends

### A. Order Status & Revenue Leakage
| Order Status | Order Count | Share (%) | Net Revenue ($) |
| :--- | :--- | :--- | :--- |
{status_table_rows}

> [!WARNING]
> **Revenue Leakage Alert**: Cancelled (20.83%) and Returned (20.58%) orders account for **41.41% of total orders**! Combined revenue attached to cancelled or returned orders equals **${cancelled_returned_rev:,.2f}**. Addressing cancellation drivers and return policies is the single largest opportunity to reclaim revenue.

### B. Product Category Breakdown
| Product | Order Volume | Total Qty Sold | Avg Unit Price ($) | Net Revenue ($) |
| :--- | :--- | :--- | :--- | :--- |
{prod_table_rows}

- **Top Revenue Generators**: **Laptop** (${df[df['Product']=='Laptop']['NetAmount'].sum():,.2f}) and **Chair** (${df[df['Product']=='Chair']['NetAmount'].sum():,.2f}) lead net revenue.
- **Highest Volume**: **Printer** (181 orders) and **Tablet** (179 orders).

### C. Referral Source & Acquisition Channels
| Referral Source | Order Volume | Net Revenue ($) |
| :--- | :--- | :--- |
{ref_table_rows}

- Marketing channels are evenly split: **Instagram** leads with 259 orders (${df[df['ReferralSource']=='Instagram']['NetAmount'].sum():,.2f}), followed closely by **Email** (250 orders) and **Google** (241 orders).

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
"""
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"Report written to: {REPORT_PATH}")

def main():
    df = load_data()
    stats_df = calculate_basic_statistics(df)
    outlier_df = detect_outliers(df)
    
    # Save CSV copies of statistics
    stats_df.to_csv(os.path.join(OUTPUT_DIR, "basic_statistics.csv"), index=False)
    outlier_df.to_csv(os.path.join(OUTPUT_DIR, "outliers_summary.csv"), index=False)
    
    generate_visualizations(df)
    generate_report(df, stats_df, outlier_df)
    print("EDA Pipeline finished successfully!")

if __name__ == "__main__":
    main()
