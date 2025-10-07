#!/usr/bin/python3
#pythonscratchspace.py

from datetime import date
from datetime import datetime

'''
Simulation Setup - Compare Mortage costs vs. Investment returns
'''
outstanding = 146295.57
monthly_payment = 1350.54
interest_rate = 0.0375
escrow = 372.27
add_principal = 300
avg_investment_return = 0.05 # Yearly


def comp_total_mortgage(
        principal: float,
        monthly: float,
        rate: float,
        escrow: float,
        add_principal: float = 0,
        verbose: bool = False,
        report: bool = False
):
    working_principal = principal
    loan_term = 0
    total_interest = 0
    days_per_month = 30.4 # Skipping dealing with datetime stuff, sue me
    # loop through the loan term
    while working_principal > 0:
        current_month_interest = get_interest(
            outstanding = working_principal, 
            interest_rate = rate, 
            days_per_month = days_per_month
        )
        total_interest += current_month_interest
        loan_term += 1 # Increment total loan term by a month
        applied_principal = (
            monthly_payment + add_principal - escrow - current_month_interest
        )
        new_principal = round(working_principal - applied_principal,2)
        if verbose: # Trigger the monthly output report
            print(
                f'[Month: {str(loan_term).rjust(3)}\t'
                f'Principal: {working_principal:.2f}\t'
                f'Term Interest: {str(current_month_interest).rjust(6)}\t'
                f'PrincplPaid: {applied_principal}'
            )
        working_principal = new_principal
    if report:  # Output a completed report
        print(
            f'Months to Payoff: {loan_term} / Years {int(loan_term/12)}\n'
            f'Total Interest Paid: {round(total_interest,2)} with Add Principal payment of {add_principal:.2f}'
        )
    return loan_term, total_interest


def get_interest(outstanding,interest_rate,days_per_month):
	interest = outstanding * (interest_rate / 365) * days_per_month
	return round(interest,2)

def calculate_investment_growth(monthly_payment, average_return_rate, months):
    monthly_return_rate = (1 + average_return_rate) ** (1 / 12) - 1
    investment_value = 0
    
    for _ in range(months):
        investment_value += monthly_payment
        investment_value *= (1 + monthly_return_rate)
    
    return investment_value


# Get no-additional-princ loan details
original_loan_term, total_interest = comp_total_mortgage(
    outstanding, monthly_payment, interest_rate, escrow, 0
)
# Get Details if we applie the add_principal value every month
reduced_loan_term, reduced_interest = comp_total_mortgage(
    outstanding, monthly_payment, interest_rate, escrow, add_principal
)

# Get Investment Return Projection over reduced Loan Period
investment_gain = calculate_investment_growth(add_principal, avg_investment_return, reduced_loan_term)
long_investment_gain = calculate_investment_growth(add_principal, avg_investment_return, original_loan_term)

print(
    f'== Mortgage Simulation Results ==\n'
    f'  Principal: {outstanding:,}\n'
    f'  Monthly Payment: {monthly_payment:,}\n'
    f'  Interest Rate: {interest_rate}\n'
    f'  Escrow Payment: {escrow:,}\n'
    f'  Additional Payments: {add_principal:,.2f}\n'
    f'  Avg. Investment Return: {avg_investment_return}\n\n'
    f'== Loan Comparisons:\n'
    f'  - No Addtl Payments:\n'
    f'    Loan of {original_loan_term} months, Total interest cost: {round(total_interest,2)}\n'
    f'  - Addtl Principal Pyament of ${add_principal:,.2f}\n'
    f'    Loan of {reduced_loan_term} months, Total interest cost: {round(reduced_interest,2)}\n'
    f'    . Savings of {round(total_interest - reduced_interest,2):,} and {original_loan_term - reduced_loan_term} months.\n\n'
    f'== Investment Projects/Comparisons:\n'
    f'  - Investing {add_principal:,.2f}/month for reduced term of {reduced_loan_term} at {avg_investment_return} rate:\n'
    f'    Return of {round(investment_gain,2)} / {round(investment_gain - reduced_interest,2)} compared to interest reduction in mortgage loan\n'
    f'  - Investing {add_principal}/month for full loan term {original_loan_term} at {avg_investment_return} rate:\n'
    f'    Return of {round(long_investment_gain,2)} / {round(long_investment_gain - total_interest,2)} as compared to full mortgage term\n'
)

# result = calculate_investment_growth(add_payment_monthly,avg_investment_return,(12*11))
# print(f'Investment of ${add_payment_monthly} over {time_of_loan} months at {avg_investment_return} is ${result:.2f}')
