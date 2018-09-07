
from datetime import datetime, date

from bokeh.io import curdoc
from bokeh.layouts import widgetbox, layout
from bokeh.models import ColumnDataSource, FactorRange, LabelSet
from bokeh.models.formatters import NumeralTickFormatter
from bokeh.models.widgets import DateRangeSlider, Select, Button, Div, CheckboxGroup
from bokeh.plotting import figure

from generate_data import generate_df

dataset = generate_df()
dataset['Data'] = [i.to_pydatetime().date() for i in dataset['Data']]

#==================================================
# Main plot
#==================================================

# Defining the data
anos = ['2017', '2018']
meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
         'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

options = ["Vendas", "Margem_Operacional", "EBITDA"]
colors = ['#c6dbef', '#6baed6', '#084594']
colormapper = dict(zip(options,colors))

source = ColumnDataSource(data=dict(x=[], y=[], labels=[], color=[]))
# initialize widgets
select = Select(value="Vendas", options=options)
dates = DateRangeSlider(start=date(2017, 1, 1),
                        end=date(2018, 9, 1),
                        value=(date(2017, 1, 1), date(2018, 9, 1)), step=1)
produtos = CheckboxGroup(labels=["Produto A", "Produto B", "Produto C"],
                         active=[0, 1, 2])
div1 = Div(text="<br><h5>Medida</h5>")
div2 = Div(text="<br><h5>Datas</h5>")
div3 = Div(text="<br><h5>Produtos</h5>")
# hover = HoverTool(tooltips=[("word", "@words")])

def refresh_data(dataset):
    dataset = dataset.groupby('Ano/Mês')[select.value].sum().reset_index()
    x = dataset['Ano/Mês']
    y = dataset[select.value]
    labels = ["{}m €".format(int(i)) for i in y]
    color = [colormapper[select.value] for i in y]
    source.data = {'x': x,
                   'y': y,
                   'labels': labels,
                   'color': color}
    print("Is the Error here?\n")
refresh_data(dataset) # initialize data


# Creating the figure
x_range = [(ano, mes) for ano in anos for mes in meses]
x_range = x_range[:len(x_range)-4] # remove last 4 months, no data

plot = figure(x_range=FactorRange(*x_range), y_range=(0, max(source.data['y'])*1.2),
              title=select.value,
              # tools=[hover],
              plot_height=500, plot_width=800,
              sizing_mode='stretch_both',
              toolbar_location=None)

# Adding the vertical bars
plot.vbar(x='x', top='y', width=0.7, source=source, fill_color='color')

# Adding custom labels
labels = LabelSet(x='x', y='y', text='labels', source=source, level='glyph',render_mode='css',
                 text_font='times',text_font_size='11px',text_font_style='bold',
                 y_offset=5,text_align='center',text_color='black')
plot.add_layout(labels)


# Function to generate new data on button click
def generate_data():
    dataset = generate_df()
    refresh_data(dataset=dataset)

button = Button(label="Gerar novos dados", button_type="primary")
button.on_click(generate_data)

# Function to update dropdown on change
def update_medida(attrname, old, new):
    plot.title.text = select.value
    source.data = refresh_data(dataset)

select.on_change('value', update_medida)

# Function to update dropdown on change
def update_data(attrname, old, new):
    start_date = datetime.fromtimestamp(dates.value[0]/1000).date()
    end_date = datetime.fromtimestamp(dates.value[0]/1000).date()
    global dataset
    dataset = dataset[(dataset['Data']>=start_date)&(dataset['Data']<=end_date)]

    source.data = refresh_data(dataset)

dates.on_change('value', update_data)

# Define static layouts
plot.sizing_mode = 'scale_width'
plot.xgrid.grid_line_color = None
plot.ygrid.grid_line_color = None

plot.outline_line_color = None
plot.yaxis.minor_tick_line_color = None
plot.yaxis.axis_label = "Valor em m€"
plot.yaxis[0].formatter = NumeralTickFormatter(format="€ 0,0")

controls = [button, div1, select, div2, dates, div3, produtos]

inputs = widgetbox(*controls, width=300, height=200, sizing_mode='fixed')
plot_layout = layout([
    [plot, inputs],
])

curdoc().add_root(plot_layout)
