import numpy as np
import pandas as pd
from babel.numbers import format_currency

def remove_decimal(S):
    S = str(S)
    S = S[:-3]
    return S

def convert_df(df, cols):
    # breakup the dataframe into cols and others
    df1 = df[cols].copy(deep=True)
    cols_other = df.columns.difference(cols)
    df2 = df[cols_other].copy(deep=True)
    # strip the first row and make it into a list
    for i in range(len(df)):
        #print('i '+ str(i))
        row = df1.loc[i].values.tolist()
        #print(row)
        # take the list and build a new list element by element
        row1=[]
        for j in range(len(row)):
            #row1.append(format_it(str(row[i])))
            #row1.append(format_it(row[i]))
            value_str = format_currency(row[j], 'INR', locale='en_IN').replace(u'\xa0', u' ')
            row1.append(remove_decimal(value_str))
        # replace the row with the changed list
        df1.loc[i] =  row1
        # reassemble the dataframe
    df = pd.concat([df2, df1], axis=1)     
    return(df)

df = pd.DataFrame(np.array([[123456789, 0, 3], [4, 523456712, 6], [7, 6, 389292]]))
df.columns=['A', 'B', 'C']

# Send particular columns for changing
change_cols = ['A', 'C']

df4 = convert_df(df, change_cols)
