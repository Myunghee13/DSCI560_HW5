import pandas as pd
import numpy as np
from bokeh.plotting import figure, show, output_notebook,ColumnDataSource,curdoc
from bokeh.models import HoverTool, Select, Div
from bokeh.layouts import row, column
from bokeh.transform import dodge

data1 = pd.read_csv('latimes-state-totals.csv')

data1['date_time']=pd.to_datetime(data1['date'])
data1 = data1[["date", "date_time", "new_confirmed_cases"]]
data1 = data1.set_index(['date_time'])
data1.sort_index(inplace=True)

df1 = data1.loc['2020-08-01':'2020-08-31']

def make_plot1():
    dates = [str(int(ele[-2:])) for ele in df1.date]
    new_cases = list(df1.new_confirmed_cases)

    data = {
        "dates": dates,
        "new_cases": new_cases
    }

    source = ColumnDataSource(data=data)

    p = figure(x_range=dates, plot_height=350, title="New Coronavirus cases in August in California",
                toolbar_location=None, y_axis_label = 'New Confirmed Cases',
                 x_axis_label = 'August, 2020')

    p.vbar(x='dates', top='new_cases', color='#FFA07A', width=0.9, source=source)


    p.add_tools(HoverTool(
        tooltips=[
            ('date', "August "+'@dates'+", 2020"),
            ("new cases", "@new_cases"),
        ]
    ))

    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    return p

plot1 = make_plot1()


data2 = pd.read_csv('cdph-race-ethnicity.csv')
data2['date_time']=pd.to_datetime(data2['date'])
data2 = data2[data2.age == "all"]
data2 = data2[["date","date_time", "race","confirmed_cases_percent", "deaths_percent","population_percent"]]
data2 = data2.set_index(['date_time'])

data2.fillna("no record", inplace = True)
data2.confirmed_cases_percent = [ele*100 for ele in data2.confirmed_cases_percent]
data2.deaths_percent = [ele*100 for ele in data2.deaths_percent]
data2.population_percent = [ele*100 for ele in data2.population_percent]

date_list = sorted(set(data2.date), reverse=True)
sel_date = date_list[0]
races = ['asian', 'black', 'cdph-other', 'latino', 'other', 'white']
def get_dataset (date):
    df2 = data2.loc[date]

    data = {'races' : races,
            'confirmed' : list(df2['confirmed_cases_percent']),
            'death' : list(df2['deaths_percent']),
            'population' : list(df2['population_percent'])
           }

    return ColumnDataSource(data=data)

def make_plot2(source):
    p = figure(x_range=races, y_range=(0, 100), plot_height=250, title="Coronavirus cases and deaths % per race in California",
               toolbar_location=None) #, tools="hover", tooltips="$name: @$name")

    p.vbar(x=dodge('races', -0.25, range=p.x_range), top='confirmed', width=0.2, source=source,
           color="#c9d9d3", legend_label="confirmed cases %")

    p.vbar(x=dodge('races',  0.0,  range=p.x_range), top='death', width=0.2, source=source,
           color="#718dbf", legend_label="death %")

    p.vbar(x=dodge('races',  0.25, range=p.x_range), top='population', width=0.2, source=source,
           color="#e84d60", legend_label="population %")

    p.add_tools(HoverTool(
        tooltips=[
            ("race", "@races"),
            ("confirmed", "@confirmed{0,0.00}"+"%"),
            ("death", "@death{0,0.00}"+"%"),
            ("population", "@population{0,0.00}"+"%"),

        ]
    ))
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"

    return p

def update_plot(attrname, old, new):
    src = get_dataset(date_select.value)
    source.data.update(src.data)

source = get_dataset (sel_date)
plot2 = make_plot2(source)

date_select = Select(value=sel_date, title='Select Date', options=date_list)
date_select.on_change('value', update_plot)


div1 = Div(text="""
<p><strong>Name: </strong>Myunghee Lee</p>
<h1>1. Source for the data</h1>
<p><strong>Source Link: </strong><a target="_blank" href="https://github.com/datadesk/california-coronavirus-data">The Los Angeles Times' independent tally of coronavirus cases in California.</a></p>
<p><strong>Used files from the data source</strong></p>
    <ol>
        <strong><li>latimes-state-totals.csv</li></strong>
        <p>The statewide total of cases and deaths logged by local public health agencies each day</p>
        <p><strong>new_confirmed_cases: </strong>the net change in confirmed cases over the previous date.</p>
        
        <strong><li>cdph-race-ethnicity.csv: </li></strong>
        <p>Statewide demographic data tallying race totals by age for both cases and deaths.</p>
        <p>Provided by the <a target="_blank" href="https://www.cdph.ca.gov/Programs/CID/DCDC/Pages/COVID-19/Race-Ethnicity.aspx">California Department of Public Health.</a></p>
        <p><strong>race: </strong>The race being tallied</pi>
        <p><strong>age: </strong>The age bracket being tallied, 0-17, 18+, 18-34, 35-49, 50-64, 65-79, 80+, <strong>all</strong>, I selected "all" for the graph.</p>       
        <p><strong>confirmed_cases_percent: </strong>The case totals percentage of the total in this age bracket</p>
        <p><strong>deaths_percent: </strong>The death totals percentage of the total in this age bracket.</p>
        <p><strong>population_percent: </strong>The race's percentage of the overall state population in this age bracket.</p>
    </ol>
<h1>2. Date of last update</h1>
<p>I downloaded the data from the source on <strong>November 5, 2020</strong>.</p>
<h1>3. New coronavirus cases in August in California</h1>
<p>You can see the number when you mouse over the bar.</p>
""")
#, width=1500, height=500)
div2 = Div(text="""
<h1>4. Cases and deaths % by race to their population %</h1>
<p>You can see the number when you mouse over the bars.</p>
<p>You can select the date by the "Select Date" button.</p>
<p><strong>No record</strong> if there is no date in the button.</p>
""")

curdoc().add_root(column(div1, plot1, div2, row(plot2, date_select)))
curdoc().title = "California Coronavirus Dashboard"
# bokeh serve --show app.py
