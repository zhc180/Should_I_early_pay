import numpy as np

# Given values
principal = 200000
annual_interest_rate = 7 / 100
monthly_interest_rate = annual_interest_rate / 12
term_years = 30
term_months = term_years * 12
investment_rate = 15 / 100  # 6% investment rate
marginal_tax_rate = 27 / 100  # 32% marginal tax rate
total_cash = 100000

def calculate_total_interest_first_x_months(principal, monthly_payment, months):
    total_interest_paid = 0
    balance = principal
    
    for month in range(1, int(months) + 1):
        monthly_interest = balance * monthly_interest_rate
        monthly_principal = monthly_payment - monthly_interest
        balance -= monthly_principal
        
        total_interest_paid += monthly_interest
        
        if balance <= 0:
            break  # Loan is paid off
    
    return total_interest_paid

def calculate_saving(early_payment, least_term_months):
    # Monthly mortgage payment calculation
    monthly_payment = principal * (monthly_interest_rate * (1 + monthly_interest_rate) ** term_months) / ((1 + monthly_interest_rate) ** term_months - 1)
    
    # New principal after early payment
    new_principal = principal - early_payment
    
    # Calculate the new loan term
    new_term_months = np.log(monthly_payment / (monthly_payment - new_principal * monthly_interest_rate)) / np.log(1 + monthly_interest_rate)
    new_term_years = new_term_months / 12
    
    # Calculate the total interest paid with and without early payment
    total_interest_without_early_payment = (monthly_payment * term_months) - principal
    total_payment_with_early_payment = monthly_payment * new_term_months
    total_interest_with_early_payment_fixed_payment = total_payment_with_early_payment - new_principal
    
    # Interest saved by making early payment
    interest_saved_fixed_payment = total_interest_without_early_payment - total_interest_with_early_payment_fixed_payment
    
    # Tax saved by making early payment
    tax_saved_fixed_payment = total_interest_with_early_payment_fixed_payment * marginal_tax_rate
    
    # Investment term for new term years
    investment_term_years_shortened = new_term_years
    
    cash_principal = total_cash - early_payment
    # Future value of investment for the new term years
    future_value_investment_shortened = cash_principal * (1 + investment_rate) ** investment_term_years_shortened
    
    # Total gain from investment for the new term years
    total_gain_investment_shortened = future_value_investment_shortened - cash_principal
    
    total_gain_investment_after_tax = total_gain_investment_shortened * 0.75
    
    
    # at the end of least term month, what is the debt & earning state
    debt = monthly_payment * (new_term_months - least_term_months)
    investment_earning = (cash_principal * (1 + investment_rate) ** (least_term_months / 12) - cash_principal) * 0.75
    interest_tax_saved_by_paying_down = calculate_total_interest_first_x_months(new_principal, monthly_payment, least_term_months)
    interest_tax_saved_by_paying_max = calculate_total_interest_first_x_months(principal - total_cash, monthly_payment, least_term_months)
    interest_saved = interest_tax_saved_by_paying_down - interest_tax_saved_by_paying_max
    
    return interest_saved_fixed_payment, tax_saved_fixed_payment, total_gain_investment_after_tax, new_term_years, {"debt": debt, "money_gain": investment_earning + interest_saved, "total_balance": investment_earning + interest_saved - debt}

print(f"{'Early Payment':<15}{'Interest Saved':<20}{'Tax Saved':<15}{'Total Gain from Investment':<30}{'total_gain_per_yr':<20}{'total_term_yr':<15}")


# Get the least term length --- by making as much early payment as possible
# Monthly mortgage payment calculation
monthly_payment = principal * (monthly_interest_rate * (1 + monthly_interest_rate) ** term_months) / ((1 + monthly_interest_rate) ** term_months - 1)

# New principal after early payment
new_principal = principal - total_cash

# Calculate the new loan term
least_term_months = np.log(monthly_payment / (monthly_payment - new_principal * monthly_interest_rate)) / np.log(1 + monthly_interest_rate)

x = []
y1 = []
y2 = []
y3 = []
for i in range(0, total_cash + 10000, 10000):
    interest_saved, tax_saved, investment_gain, new_term_years, state_at_least_term_end = calculate_saving(i, least_term_months)
    total_gain_per_yr = (investment_gain + tax_saved + interest_saved) / new_term_years
    print(f"${i:<15,.2f}${interest_saved:<18,.2f}${tax_saved:<15,.2f}${investment_gain:<30,.2f}${total_gain_per_yr:<20,.2f}{new_term_years:<15,.2f}{state_at_least_term_end}")
    x.append(i)
    y1.append(interest_saved / new_term_years)
    y2.append((tax_saved + investment_gain) / new_term_years)
    y3.append(total_gain_per_yr)
    
import matplotlib.pyplot as plt
plt.figure(figsize=(12, 6))
plt.plot(x, y1, label='Interest Saved')
plt.plot(x, y2, label='Investment Gain + tax saved')
plt.plot(x, y3, label='Total Saved')

plt.xlabel('Early Payment Amount ($)')
plt.ylabel('Amount ($)')
plt.title('Comparison of Interest Savings and Investment Gains')
plt.legend()
plt.grid(True)
plt.show()