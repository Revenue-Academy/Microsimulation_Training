"""
app1.py illustrates use of pitaxcalc-demo release 2.0.0 (India version).
USAGE: python app1.py > app1.res
CHECK: Use your favorite Windows diff utility to confirm that app1.res is
       the same as the app1.out file that is in the repository.
"""
from taxcalc import *
import numpy as np
import matplotlib.pyplot as plt

# create Records object containing pit.csv and pit_weights.csv input data
recs = Records()

# create GSTRecords object containing gst.csv and gst_weights.csv input data
grecs = GSTRecords()

assert isinstance(grecs, GSTRecords)
assert grecs.data_year == 2017
assert grecs.current_year == 2017

# create CorpRecords object containing cit.csv and cit_weights.csv input data
crecs = CorpRecords()

assert isinstance(crecs, CorpRecords)
assert crecs.data_year == 2017
assert crecs.current_year == 2017

# create Policy object containing current-law policy
pol = Policy()

# specify Calculator object for current-law policy
calc1 = Calculator(policy=pol, records=recs, gstrecords=grecs,
                   corprecords=crecs, verbose=False)
calc1.calc_all()

# specify Calculator object for reform in JSON file
reform = Calculator.read_json_param_objects('app1_reform.json', None)
pol.implement_reform(reform['policy'])
calc2 = Calculator(policy=pol, records=recs, gstrecords=grecs,
                   corprecords=crecs, verbose=False)
calc2.calc_all()


# compare aggregate results from two calculators
weighted_tax1 = calc1.weighted_total('pitax')
weighted_tax2 = calc2.weighted_total('pitax')
total_weights = calc1.total_weight()
weighted_tax_diff= weighted_tax2-weighted_tax1
print(f'Tax under Current Law: {weighted_tax1 * 1e-9:,.2f} billions')
print(f'Tax under Reform: {weighted_tax2 * 1e-9:,.2f} billions')
print(f'Total Returns: {total_weights * 1e-6:,.2f} million')
print(f'Change in taxes due to reform: {weighted_tax_diff * 1e-6:,.2f} million')

output_categories = 'standard_income_bins'
dt1, dt2 = calc1.distribution_tables(calc2, output_categories, 
                                     averages = True,
                                     scaling = True)
dt1 = dt1.fillna(0)
print(dt1)
dt2['pitax_diff'] = dt2['pitax'] - dt1['pitax']
dt2['etr'] = (dt2['pitax']/dt2['GTI'])*100
dt2 = dt2.fillna(0)    
print(dt2)
dt2[['pitax', 'pitax_diff']].plot.bar()
plt.show()

dt2['etr'].plot.line()
