import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import panel as pn

data = [
    ['customer','name',90],
    ['customer','address',80],
    ['customer','email',30],
    ['account','type',90],
    ['account','type',90],
    ['account','type',90]
]
df = pd.DataFrame(data,columns =['entity','field','pass percent'])

# select = pn.widgets.MultiChoice(name='Entity',options=list(df.entity.unique()))
# tabulator = pn.widgets.Tabulator(df, height=450)

def color_negative_red(val):
    if type(val) == int:
        if val >= 90:   color = 'green' 
        elif val >= 70: color = 'orange'
        else:           color = 'red'
        return 'background-color: %s' % color


movies_df = df

movies_table = pn.widgets.Tabulator(movies_df, pagination='remote', layout='fit_columns', width=800)
# By using the pn.bind function, which binds widget and parameter values to a function, complex filtering can be achieved. E.g. here we will add a filter function that uses tests whether the string or regex is contained in the ‘Director’ column of a listing of thousands of movies:
movies_table.style.applymap(color_negative_red)

director_filter = pn.widgets.TextInput(name='Director filter', value='')

def contains_filter(df, pattern, column):
    if not pattern:
        return df
    return df[df[column].str.contains(pattern)]
    
movies_table.add_filter(pn.bind(contains_filter, pattern=director_filter, column='entity'))    

pn.Row(director_filter, movies_table).servable()