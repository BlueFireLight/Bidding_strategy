''' # PnL Integration over Global Mean Second Bid

## Overview
This tool numerically integrates the expected PnL curve over all possible values of the global market mean second bid (`avg_b2`), assuming `avg_b2` is **uniformly distributed** across the market range (700–920). The resulting area under the curve serves as a single scalar metric representing total expected PnL under market uncertainty.

This metric enables direct comparison across bid pairs — the optimal `(b1, b2)` strategy is the one that **maximizes this integral**.

---

## Motivation
In practice, the true market mean `avg_b2` is not known in advance. If it is equally likely to fall anywhere in the range, the expected PnL is:

$$E[\text{PnL}] = \frac{1}{920 - 700} \int_{700}^{920} \text{PnL}(\text{avg\_b2}) \, d(\text{avg\_b2})$$

The raw integral (before dividing by range width) preserves the same ordering across strategies, making it directly usable for optimization.

---

## Computation

### Step 1 — Sweep avg_b2
Samples 110 evenly spaced values of `avg_b2` from 700 to 918 (step 2).

### Step 2 — Evaluate PnL at Each Point
For each `avg_b2`, calls the core auction model which averages expected PnL across 49 uniformly distributed reserve prices (675–915, step 5).

### Step 3 — Numerical Integration
Applies the **trapezoidal rule** to approximate the area under the PnL curve:
```python
area = np.trapezoid(pnl_values, mean_range)
```
Includes fallback to `np.trapz` for older NumPy versions.

---

## Output
- **Blue curve** — Expected PnL at each `avg_b2` value
- **Shaded area** — Visual representation of the integral
- **Red dashed line** — Critical `b2` threshold where PnL collapses
- **Printed value** — Total area under the curve

---

## Usage
```bash
python pnl_integrator.py
```
Enter your first bid (`b1`) and second bid (`b2`) when prompted. The tool computes and displays the integral area alongside the PnL curve.

---

## Optimization Application
To find the optimal bid pair, run a grid search:
```python
best_area = 0
best_bids = (0, 0)
for b1 in range(700, 900, 5):
    for b2 in range(b1, 920, 5):
        area = compute_integral(b1, b2)
        if area > best_area:
            best_area = area
            best_bids = (b1, b2)
```
The `(b1, b2)` pair with the highest integral is the optimal strategy under uniform market uncertainty.

---

## Known Limitations
- `mean_range` ends at 918 rather than 920 — marginally underestimates the tail area
- Raw integral is not normalized by range width — divide by 220 to obtain true expected PnL
- Uniform distribution of `avg_b2` is an assumption — results shift if the true distribution is skewed

---

## Dependencies
- `numpy`
- `matplotlib`

---

## Parameters

| Parameter | Description |
|---|---|
| `b1` | Primary bid |
| `b2` | Secondary bid |
| `mean_range` | 700 to 918, step 2 (110 sample points) |
| Integration method | Trapezoidal rule |
| Intrinsic value | 920 |
'''



import numpy as np
import matplotlib.pyplot as plt

def calculate_pnl_integral_for_mean():
    print("--- PnL vs Mean Bid 2 Integrator ---")
    try:
        b1 = float(input("Enter the first bid: "))
        b2 = float(input("Enter the second bid: "))
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        return

    # Range for Global Mean (avg_b2)
    mean_range = np.arange(700, 920, 2)
    
    # Calculate PnL values for each mean in the range
    pnl_values = np.array([calculate_expected_pnl_for_mean(b1, b2, m) for m in mean_range])

    # Calculate the integral using the trapezoidal rule
    try:
        area = np.trapezoid(pnl_values, mean_range)
    except AttributeError:
        area = np.trapz(pnl_values, mean_range)

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(mean_range, pnl_values, color='blue', linewidth=2, label='Expected PnL')
    plt.fill_between(mean_range, pnl_values, color='skyblue', alpha=0.4, label=f'Integral Area: {area:.2f}')
    
    plt.title(f'PnL Integration over Global Mean\n(b1={b1}, b2={b2})')
    plt.xlabel('Global Mean Second Bid (avg_b2)')
    plt.ylabel('Expected PnL')
    plt.axvline(x=b2, color='red', linestyle='--', label=f'b2 threshold ({b2})')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()

    print(f'Total Area under the curve: {area:.2f}')

if __name__ == "__main__":
    calculate_pnl_integral_for_mean()
