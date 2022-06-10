import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import panel as pn
import hvplot.pandas

data = pd.read_csv('test.csv')
field_col_name = 'field'
df = pd.DataFrame(data,columns =['cycle','entity',field_col_name,'pass percent'])
print(df)

## Create Dashboard Components ##
def color_negative_red(val):
    if type(val) == int:
        if val >= 90:   color = 'green' 
        elif val >= 70: color = 'orange'
        else:           color = 'red'
        return 'background-color: %s' % color

# pn.bind binds widget and parameter values to a function and complex filtering can be achieved
entity_filter = pn.widgets.TextInput(name='entity filter', value='Cycle 1')
# entity_filter = pn.widgets.MultiChoice(name='entity',options=list(df.entity.unique()))

def contains_filter(df, pattern, column):
    if not pattern:
        return df
    return df[df[column].str.contains(pattern)]

## Create template and organise components together ##
template = pn.template.BootstrapTemplate(title='Data Dashboard')#,sidebar_width=200)
template.main.append(entity_filter)
row_1 = pn.Row()

# Inline notes for each row in each table
content_fn = lambda row: pn.pane.Markdown(f'{row["field"]} Notes; Description; Defect Details')

# Create Components in loop
for entity in list(df.entity.unique()):
    # Filter df on entity
    df_edit = df[df['entity']==entity]
    df_edit = df_edit.drop(columns=['entity'])
    
    # Create table for each entity
    table = pn.widgets.Tabulator(df_edit, pagination='remote', layout='fit_data', 
        widths={'pass percent': 50},
        row_content=content_fn, 
        embed_content=True,
        show_index=False,
        hidden_columns=['cycle']
        )
    
    # Apply styling - Add to template -  Add dynamic filter
    table.style.applymap(color_negative_red)
    row_1.append(pn.Column(pn.pane.Markdown("## "+entity), table))
    table.add_filter(pn.bind(contains_filter, pattern=entity_filter, column='cycle'))  

template.main.append(row_1)

df_plot = df.groupby(['cycle'])['pass percent'].mean()
row_2 = pn.Row(df_plot.hvplot(x='cycle',y='pass percent',title='Average Pass Percentage Over Cycles'))

template.main.append(row_2)

template.servable()
