# P-Value : What & Why ?

## What is a p-value?
The p-value helps you decide whether the effect you observed is statistically significant or just happened by random chance. The p-value gives you a number between 0 and 1 that tells you how surprising your results are.

## Interpret the p-value:
Let’s assume, we set the probability benchmark at 5%:
If the p-value is higher than 5%, the results are likely due to chance and we do not reject the null hypothesis.
However, if the p-value is equal to or less than 5% (very low), the results are unlikely due to chance. We may reject the null hypothesis in this case.

## When is p-value used?
In A/B testing or marketing experiments, such as:
Testing two versions of an email campaign
Comparing conversion rates before and after a new website layout
Evaluating impact of an ad on sales

## Real-World Example: Marketing Campaign Effectiveness
Your company runs a new email campaign to improve purchases.
- Group A: Sent the standard email
- Group B: Sent the new marketing email

## Hypotheses:
- Null hypothesis (H₀): The new campaign has no effect on sales.
- Alternative hypothesis (H₁): The new campaign increases sales.

After one week:

You want to test if the new email led to significantly higher sales

### You find:
- Email B generated $110 average sales.
- Email A generated $100 average sales.
- p-value = 0.02

### This means:
“If both emails were equally effective (null is true), there’s only a 2% chance I would’ve seen this big a difference just by luck.”

So, you reject the null hypothesis and say:

“The new email is likely more effective.”

## Let's simulate synthetic data using Python
### Python Code:

```
import numpy as np
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt

# Set seed for reproducibility
np.random.seed(42)

# Simulate daily sales (in $) over 50 users
# Group A: Standard campaign
group_A_sales = np.random.normal(loc=100, scale=15, size=50)

# Group B: New campaign (better performance)
group_B_sales = np.random.normal(loc=110, scale=15, size=50)

# Perform two-sample t-test
t_stat, p_val = ttest_ind(group_B_sales, group_A_sales)

# Print summary
print("Average Sales - Group A (Standard): $", round(np.mean(group_A_sales), 2))
print("Average Sales - Group B (New): $", round(np.mean(group_B_sales), 2))
print("t-statistic:", round(t_stat, 2))
print("p-value:", round(p_val, 5))

# Visualize
plt.figure(figsize=(8, 5))
plt.hist(group_A_sales, bins=10, alpha=0.6, label='Standard Campaign (Group A)')
plt.hist(group_B_sales, bins=10, alpha=0.6, label='New Campaign (Group B)')
plt.axvline(np.mean(group_A_sales), color='blue', linestyle='dashed')
plt.axvline(np.mean(group_B_sales), color='green', linestyle='dashed')
plt.legend()
plt.title("Sales Distribution: Standard vs New Campaign")
plt.xlabel("Sales ($)")
plt.ylabel("Number of Customers")
plt.grid(True)
plt.tight_layout()
plt.show()
```

### Sample Output:
```
Average Sales - Group A (Standard): $99.61
Average Sales - Group B (New): $109.91
t-statistic: 3.49
p-value: 0.00078
```

## Interpretation:
- The average sales in the new campaign group is significantly higher.
- The p-value = 0.00078, which is much less than 0.05.
- We reject the null hypothesis → The new campaign is statistically more effective.

## What p-value is not:

- It’s not the chance that your hypothesis is true.
- It’s not a guarantee — just evidence based on probability.
- A p-value of 0.02 doesn’t mean 98% chance the new email works — it means 2% chance this result came from random noise.

## Summary
- P-Value is used to decide whether a result is statistically significant.
- A low p-value (typically ≤ 0.05) means your result is unlikely due to chance, so you reject the null hypothesis.
- A high p-value means the result could easily happen by chance — so you don’t reject the null.
- Smaller p-value = stronger evidence that there’s a real effect.