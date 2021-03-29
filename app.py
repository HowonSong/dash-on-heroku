
import os
import jinja2.ext
import dash_core_components as dcc
import dash_html_components as html
import dash 
from dash.dependencies import Output, Input
import plotly 
import plotly.graph_objs as go
from collections import deque
from random import randint
import pymysql
import pandas as pd  
import flask

old=[0]
accum_w=deque(maxlen = 5)
accum_c=deque(maxlen = 5)
server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))
app = dash.Dash(__name__, server=server)
app.layout = html.Div( 
    [
        html.Label('Dataset'),
        dcc.Dropdown(
        id='dataset',
        options=[
            {'label': 'house_hold_1', 'value': 1},{'label': 'house_hold_2', 'value': 2},
            {'label': 'house_hold_3', 'value': 3},{'label': 'house_hold_4', 'value': 4},
            {'label': 'house_hold_5', 'value': 5},{'label': 'house_hold_6', 'value': 6},
            {'label': 'house_hold_7', 'value': 7},{'label': 'house_hold_8', 'value': 8},
            {'label': 'house_hold_9', 'value': 9},{'label': 'house_hold_10', 'value': 10},
            {'label': 'house_hold_11', 'value': 11},{'label': 'house_hold_12', 'value': 12},
            {'label': 'house_hold_13', 'value': 13},{'label': 'house_hold_14', 'value': 14},
            {'label': 'house_hold_15', 'value': 15},{'label': 'house_hold_16', 'value': 16},
            {'label': 'house_hold_17', 'value': 17},{'label': 'house_hold_18', 'value': 18},
            {'label': 'house_hold_19', 'value': 19},{'label': 'house_hold_20', 'value': 20},
            {'label': 'house_hold_21', 'value': 21},{'label': 'house_hold_22', 'value': 22},
            {'label': 'house_hold_23', 'value': 23},{'label': 'house_hold_24', 'value': 24},
            {'label': 'house_hold_25', 'value': 25},{'label': 'house_hold_26', 'value': 26},
            {'label': 'house_hold_27', 'value': 27},{'label': 'house_hold_28', 'value': 28},
            {'label': 'house_hold_29', 'value': 29},{'label': 'house_hold_30', 'value': 30},
            {'label': 'house_hold_31', 'value': 31},{'label': 'house_hold_32', 'value': 32},
            {'label': 'house_hold_33', 'value': 33},{'label': 'house_hold_34', 'value': 34},
            {'label': 'house_hold_35', 'value': 35},{'label': 'house_hold_36', 'value': 36},
            {'label': 'house_hold_37', 'value': 37},{'label': 'house_hold_38', 'value': 38},
            {'label': 'house_hold_39', 'value': 39},{'label': 'house_hold_40', 'value': 40},
            {'label': 'house_hold_41', 'value': 41},{'label': 'house_hold_42', 'value': 42},
            {'label': 'house_hold_43', 'value': 43},{'label': 'house_hold_44', 'value': 44},
            {'label': 'house_hold_45', 'value': 45},{'label': 'house_hold_46', 'value': 46},
            {'label': 'house_hold_47', 'value': 47},{'label': 'house_hold_48', 'value': 48},
            {'label': 'house_hold_49', 'value': 49},{'label': 'house_hold_50', 'value': 50},
            {'label': 'house_hold_51', 'value': 51},{'label': 'house_hold_52', 'value': 52},
            {'label': 'house_hold_53', 'value': 53},{'label': 'house_hold_54', 'value': 54},
            {'label': 'house_hold_55', 'value': 55},{'label': 'house_hold_56', 'value': 56},
            {'label': 'house_hold_57', 'value': 57},{'label': 'house_hold_58', 'value': 58},
            {'label': 'house_hold_59', 'value': 59},{'label': 'house_hold_60', 'value': 60},

        ],
        value=1),
        dcc.Graph(id = 'live-graph', animate = False), 
        dcc.Interval(id = 'graph-update',interval = 2000,n_intervals = 0) 
    ] ) 
  
@app.callback( 
    Output('live-graph', 'figure'), 
    [ Input('graph-update', 'n_intervals'),Input('dataset', 'value') ] 
) 
  
def update_graph_scatter(n,dataset):
    name=[]
    name.append('index')
    name.append('datetime')
    for i in range (1,61):
        name.append(i)
    connect = pymysql.connect(host='127.0.0.1', user='root', password='2243', db='db',charset='utf8mb4')
    cur = connect.cursor()
    query = "SELECT * FROM working ORDER BY 1 DESC limit 1"
    cur.execute(query)
    rows= cur.fetchone()
    cur2 = connect.cursor()
    query1 = "SELECT * FROM credits1 ORDER BY 1 DESC limit 1"
    cur2.execute(query1)
    rows1= cur2.fetchone()
    if rows[0]>old[0]:
        rows=list(rows)
        rows1=list(rows1)
        accum_w.append(rows)
        accum_c.append(rows1)
        df=pd.DataFrame(list(accum_w),columns=name)
        df1=pd.DataFrame(list(accum_c),columns=name)
    else:
        df=pd.DataFrame(list(accum_w),columns=name)
        df1=pd.DataFrame(list(accum_c),columns=name)
    old[0]=rows[0]
    connect.close()
    data = plotly.graph_objs.Scatter(x= df['datetime'], y=df[dataset],name = "consumption", mode= 'lines+markers',yaxis='y1')
    data1 = plotly.graph_objs.Scatter(x= df1['datetime'], y=df1[dataset],name="credit", mode= 'lines+markers',yaxis='y2')
    layout= go.Layout(title = "Consumption and Credit",
                      legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
                      xaxis=dict(title='Time(hr:min:sec)',tickformat='%H:%M:%S'),
                      yaxis1 = dict(title = 'Concumption (kwh)',range = [0,1000]),
                      yaxis2 = dict(title = 'Credit (TZS)',range = [0,1000],overlaying='y1',side='right'))
    return {'data': [data,data1],'layout':layout}

if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)







