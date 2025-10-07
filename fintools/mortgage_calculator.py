#!/usr/bin/python3
#pythonscratchspace.py

from datetime import date
from datetime import datetime

def get_interest(outstanding,interest_rate,days_per_month):
	interest = outstanding * (interest_rate / 365) * days_per_month
	return round(interest,2)


def do_the_math(additional = None, verbose=True):
	working_principal = outstanding
	add_payment_monthly = additional or globals().get('add_payment_monthly',0)
	months_counter = 0
	total_interest = 0
	days_per_month = 30.4 # I'm skipping annoying datetime stuff sue me
	while working_principal > 0:
		months_interest = get_interest(working_principal,interest_rate,days_per_month)
		total_interest += months_interest
		applied_principal = monthly_payment - escrow - months_interest
		if float(add_payment_monthly) > 0:
			applied_principal += add_payment_monthly
		applied_principal = round(applied_principal,2)
		months_counter += 1
		new_principal = round(working_principal - applied_principal,2)
		if verbose:
			months_interest = str(f'{months_interest:.2f}')
			print(f'[Month: {str(months_counter).rjust(3)}]\tP: {working_principal}\tI: {months_interest.rjust(6)}\tpaid {applied_principal}')
		working_principal = new_principal
	print(f'\nTotal Months to Payoff: {months_counter} / Years {int(months_counter/12)}')
	print(f'Total Interest Paid: {round(total_interest,2)} with +Principal payment of: {add_payment_monthly}')
	return total_interest, months_counter


def calculate_investment_growth(monthly_payment, average_return_rate, months):
    monthly_return_rate = (1 + average_return_rate) ** (1 / 12) - 1
    investment_value = 0
    
    for _ in range(months):
        investment_value += monthly_payment
        investment_value *= (1 + monthly_return_rate)
    
    return investment_value


### SET CURRENT LOAN VALUES
outstanding = 146295.57
monthly_payment = 1350.54
interest_rate = 0.0375
escrow = 372.27
add_payment_monthly = 300
avg_investment_return = 0.05 # Yearly


total_interest, time_of_loan = do_the_math(verbose=False)

result = calculate_investment_growth(add_payment_monthly,avg_investment_return,(12*11))
print(f'Investment of ${add_payment_monthly} over {time_of_loan} months at {avg_investment_return} is ${result:.2f}')