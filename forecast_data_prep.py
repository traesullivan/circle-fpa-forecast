import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Set random seed for reproducibility
np.random.seed(42)

# Generate a date range for last 2 years
dates = pd.date_range(start='2023-01-01', periods=24, freq='MS')

# Base assumptions from Circle's financial model
starting_subscribers = 4000  # Approximate initial paying communities in 2023
avg_subscription_fee = 99  # Weighted average of subscription tiers ($49 - $399)
growth_rate_mean = 0.06  # ~6% monthly growth
growth_rate_std = 0.015  # variability in growth
churn_rate_mean = 0.015  # 1.5% monthly churn
churn_rate_std = 0.005  # Some variability in churn

# Expense assumptions
fixed_expenses = 500000  # Fixed operating costs (staff, infrastructure, etc.)
variable_expense_ratio = 0.4  # 40% of revenue goes to operating costs

# Variables to store generated values
subscribers = [starting_subscribers]
new_subscribers = []
churned_subscribers = []
mrr = []
expenses = []
profits = []

# Simulate month-over-month financials
for date in dates:
    # Simulate new subscribers based on growth rate variability
    growth_rate = np.random.normal(growth_rate_mean, growth_rate_std)
    new_sub = int(subscribers[-1] * growth_rate)
    new_subscribers.append(new_sub)
    
    # Simulate churn based on churn rate variability
    churn_rate = np.random.normal(churn_rate_mean, churn_rate_std)
    churned = int(subscribers[-1] * churn_rate)
    churned_subscribers.append(churned)
    
    # Calculate current subscribers
    current_subscribers = subscribers[-1] + new_sub - churned
    subscribers.append(current_subscribers)
    
    # Calculate Monthly Recurring Revenue (MRR)
    current_mrr = current_subscribers * avg_subscription_fee
    mrr.append(current_mrr)
    
    # Calculate expenses
    total_expenses = fixed_expenses + (current_mrr * variable_expense_ratio)
    expenses.append(total_expenses)
    
    # Calculate profit
    profit = current_mrr - total_expenses
    profits.append(profit)

# Create DataFrame
financial_data = pd.DataFrame({
    'Date': dates,
    'Subscribers': subscribers[1:],  # Skip first value (starting point)
    'New Subscribers': new_subscribers,
    'Churned Subscribers': churned_subscribers,
    'MRR': mrr,
    'Expenses': expenses,
    'Profit': profits
})

# Set date as index
financial_data.set_index('Date', inplace=True)

# Display dataset
print(financial_data)

# Plot key metrics
plt.figure(figsize=(12, 6))

# Plot Subscribers Growth
plt.subplot(2, 1, 1)
plt.plot(financial_data.index, financial_data['Subscribers'], label="Subscribers", marker="o")
plt.ylabel("Subscribers")
plt.title("Subscribers Growth Over Time")
plt.legend()

# Plot MRR and Profit
plt.subplot(2, 1, 2)
plt.plot(financial_data.index, financial_data['MRR'], label="Monthly Recurring Revenue (MRR)", marker="o")
plt.plot(financial_data.index, financial_data['Profit'], label="Profit", marker="o", linestyle="dashed")
plt.xlabel("Date")
plt.ylabel("Revenue & Profit ($)")
plt.title("MRR & Profit Over Time")
plt.legend()

plt.tight_layout()
plt.show()
