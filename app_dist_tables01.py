"""
app1.py illustrates use of pitaxcalc-demo release 2.0.0 (India version).
USAGE: python app2.py
"""
import locale
from taxcalc import *


locale.setlocale(locale.LC_ALL, '')

# create Records object containing pit.csv and pit_weights.csv input data
recs = Records(data='pit.csv', weights='pit_weights.csv')

# create Policy object containing current-law policy
pol = Policy()

# specify Calculator object for current-law policy
calc1 = Calculator(policy=pol, records=recs, verbose=False)

# specify Calculator object for reform in JSON file
reform = Calculator.read_json_param_objects('app14_reform.json', None)
pol.implement_reform(reform['policy'])
calc2 = Calculator(policy=pol, records=recs, verbose=False)
# loop through years 2017, 2018, and 2019 and print out pitax
for year in range(2017, 2020):
    calc1.advance_to_year(year)
    calc2.advance_to_year(year)
    calc1.calc_all()
    calc2.calc_all()
    weighted_tax1 = calc1.weighted_total('pitax')
    weighted_tax2 = calc2.weighted_total('pitax')
    total_weights = calc1.total_weight()
    print(f'Tax 1 for {year}: {weighted_tax1 * 1e-9:,.2f}')
    print(f'Tax 2 for {year}: {weighted_tax2 * 1e-9:,.2f}')
    print(f'Total weight for {year}: {total_weights * 1e-6:,.2f}')
    #dt1, dt2 = calc1.distribution_tables(calc2, 'weighted_deciles')
    dt1, dt2 = calc1.distribution_tables(calc2, 'standard_income_bins')
    print('Current-Law Distribution Table for ', year)
    print(dt1)
    print('Policy-Reform Distribution Table for ', year)
    print(dt2)
    # print text version of each complete distribution table to a file
    with open('dist-table-all-clp.txt', 'w') as dfile:
        dt1.to_string(dfile)
    with open('dist-table-all-ref.txt', 'w') as dfile:
        dt2.to_string(dfile)
    # print text version of each partial distribution table to a file
    to_include = ['weight', 'GTI', 'TTI', 'pitax']
    with open('dist-table-part-clp.txt', 'w') as dfile:
        dt1.to_string(dfile, columns=to_include)
    with open('dist-table-part-ref.txt', 'w') as dfile:
        dt2.to_string(dfile, columns=to_include)
