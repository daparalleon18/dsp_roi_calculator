# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 08:46:33 2022

@author: dparalleon
"""
#%%
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Output,Input,State
from dash.exceptions import PreventUpdate
from app import app, server 
from apps import dashboard
import sqlite3
import pandas as pd

colors = {
    'c1': 'rgb(0, 123, 255)',
    'c2': 'rgb(134, 169, 189)',
    'c3': 'rgb(255, 59, 60)',
    'c4': 'rgb(44, 82, 103)',
    'c5': 'rgb(242, 217, 187)',
    'c6': 'rgba(44, 82, 103, .70)',
    'c7': 'rgba(255, 59, 60, .70)'
}
hstyle = {
    'color': colors['c1']    
}



app = dash.Dash(__name__,suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'userid', children = ''),
    html.Div(id = 'page-content')
])

login_page = html.Div([
    html.H1('ROI Calculator', style = {'margin-left':'45%'}),
    html.Div([
        dcc.Input(
            id = 'username'
            , type = 'text'
            , placeholder = 'Username'
            , className = "inputbox1"
            , style = {'margin-left':'40%','width':'350px','height':'35px'
                       ,'padding':'10px','margin-top':'60px', 'font-size':'16px'
                       ,'border-width':'3px'}
            ),
        ]),
    html.Div(
        dcc.Input(
            id = 'password'
            , type = 'password'
            , placeholder = 'Password'
            , className = 'inputbox2'
            , style = {'margin-left':'40%','width':'350px','height':'35px'
                       ,'padding':'10px','margin-top':'10px', 'font-size':'16px'
                       ,'border-width':'3px'}
            ),
        ),
    html.Div(
        html.Button(
            'Log In'
            , id = 'login'
            , n_clicks = 0
            , style = {'backgroundColor': colors['c1'],
                       'color': 'white',
                       'height': '40px',
                       'width': '100px'}

            
            )
        , style={'margin-left':'47%','padding-top':'30px'}
        )
])

@app.callback(
    [Output('url', 'pathname'),
     Output('userid', 'children')
     ],    
    [Input('login', 'n_clicks')],
    [State('username', 'value'),
     State('password', 'value')]
)
def login(n_clicks, username, password):
    db = sqlite3.connect('scenarios_tab.db')
    cur = db.cursor()
    sql = 'SELECT DISTINCT userid, username, password FROM user_form'
    cur.execute(sql, [])
    utab = pd.DataFrame(cur.fetchall(), columns=['userid', 'username', 'password'])
    db.close()

    if username == '' or username == None:
        pathname = '/'
        uid = ['']
        return [pathname, uid]
    elif password in utab[utab['username'] == username]['password'].to_list():
        pathname = '/dashboard'
        uid = [utab[utab['username'] == username]['userid'].to_list()[0]]
        return [pathname, uid]
    else:
        pathname = '/'
        uid = ['']
        return [pathname, uid]

####################################################################################



@app.callback(
    [Output('tab-1-tpar', 'children'),
     Output('tab-2-uor', 'children'),
     Output('tab-3-cr', 'children'),
     Output('tab-4-mas', 'children'),
     Output('tab-5-msh', 'children'),
     Output('tab-6-nps', 'children')
     ],
    [Input('button-calc', 'n_clicks'),
     ],
    [State('input-0-id', 'value'),
     State('input-1-th', 'value'),
     State('input-2-cr', 'value'),
     State('input-3-rpp', 'value'),
     State('input-4-ntpc', 'value'),         
     State('input-5-sc', 'value'),
     State('input-6-sb', 'value')               
     ]   
)  
def update_tabs(n_clicks, sid, th, cr, rpp, ntpc, sc, sb):
    tpar = th * rpp * ntpc
    uor = (1 - (cr / 100) ) * tpar
    crev = (cr / 100) * tpar 
    np = crev - sc
    mas = (sb / 100) * np
    msh = mas / th
    nps = (1 - (sb / 100) ) * np
    return ['Php {:,.2f}'.format(x) for x in [tpar, uor, crev, mas, msh, nps] ]          


@app.callback(
    [Output('chart-pie', 'figure')
     ],
    [Input('button-calc', 'n_clicks')
     ],
    [
     State('input-1-th', 'value'),
     State('input-2-cr', 'value'),
     State('input-3-rpp', 'value'),
     State('input-4-ntpc', 'value'),  
     State('input-5-sc', 'value'),            
     State('input-6-sb', 'value')               
     ]       
)  

def update_pie(n_clicks, th, cr, rpp, ntpc, sc, sb):    
    tpar = th * rpp * ntpc
    uor = (1 - (cr / 100) ) * tpar
    crev = (cr / 100) * tpar     
    np = crev - sc    
    mas = (sb / 100) * np    
    nps = (1 - (sb / 100) ) * np

    figure = {
        'data': [
            go.Pie(
                labels = ['Unconverted Revenue, Php',
                          'Max Allowable Spend, Php',
                          'Net Profit Not For Sampling, Php',
                          'Sampling Cost, Php'
                          ],
                values = [uor, mas, nps, sc],
                textinfo ='label, value',
                textposition = 'outside',                            
                showlegend = False,
                hole = .4,
                marker_colors = [colors['c5'], colors['c2'], colors['c3'], colors['c4']],
                marker = dict(line=dict(color='black', width=.8))                                                        
                )
            ]                        
        }           
    return [figure]


@app.callback(
    [Output('chart-wf', 'figure')
     ],
    [Input('button-calc', 'n_clicks')
     ],
    [State('input-1-th', 'value'),
     State('input-2-cr', 'value'),
     State('input-3-rpp', 'value'),
     State('input-4-ntpc', 'value'),         
     State('input-5-sc', 'value'),
     State('input-6-sb', 'value')  
     ]   
)  


def update_wf(n_clicks, th, cr, rpp, ntpc, sc, sb): 
 
    tpar = th * rpp * ntpc
    uor = (1 - (cr / 100) ) * tpar
    crev = (cr / 100) * tpar 
    np = crev - sc    
    nps = (1 - (sb / 100) ) * np
            
    figure = {
        'data': [
            go.Waterfall(
                x = ["Total Potential Annual Revenue", 
                     "Unconverted Opportunity Revenue", 
                     "Converted Revenue", 
                     "Sampling Cost", 
                     "Net Profit", 
                     "Net Profit Not for Sampling",
                     "Max Allowable Spend"
                     ],
                y = [tpar, -uor, 0, -sc, 0, -nps, 0],
                measure = ["absolute", "relative", "total", "relative", "total","relative", "total"],
                orientation = 'v', textposition = 'outside',   
                decreasing = {'marker':{'color':colors['c7']}},
                totals = {'marker':{'color':colors['c6']}}                                                
                )
            ],
        
        }           
                    
    return [figure]


@app.callback(
    [Output('combo-scenario', 'options'),
     Output('combo-scenario', 'value')],
    [Input('button-save', 'n_clicks'),
     Input('button-del', 'n_clicks'),
     Input('mode-edit','value')],    
    [State('input-0-id', 'value'),   
     State('input-1-th', 'value'),     
     State('input-2-cr', 'value'),
     State('input-3-rpp', 'value'),
     State('input-4-ntpc','value'),
     State('input-5-sc', 'value'),
     State('input-6-sb', 'value'),
     State('combo-scenario', 'value'),
     State('userid', 'children')]
)
def save_scenario(button_save, button_del, mode_edit, 
                  scenario_name, total_hits, conversion_rate, revenue, 
                  purchase_per_user, sampling_cost, sampling_budget, scenario_combo, userid):
   ctx = dash.callback_context
   userid = int(userid[0])
   if ctx.triggered:
       eventid = ctx.triggered[0]['prop_id'].split('.')[0]
       if eventid =="button-save":
            if 1 not in mode_edit:
                sql = "SELECT max(scenario_id) as scenario_id FROM scenarios_tab"
                df = querydatafromdatabase(sql,[],["scenario_id"])
            
                if not df['scenario_id'][0]:
                    scenario_id=1
                else:
                    scenario_id = int(df['scenario_id'][0])+1
                sqlinsert = '''INSERT INTO 
                scenarios_tab(scenario_id, scenario_name, total_hits, 
                               conversion_rate, revenue, 
                               purchase_per_user, sampling_cost, 
                               sampling_budget, userid) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
                modifydatabase(sqlinsert, (scenario_id, scenario_name, total_hits, conversion_rate, revenue,
                                          purchase_per_user, sampling_cost, sampling_budget, userid))                                                
            else:
                sqledit = '''UPDATE scenarios_tab SET scenario_name= ?, total_hits = ?, 
                               conversion_rate = ?, revenue = ?, 
                               purchase_per_user = ?, sampling_cost = ?, 
                               sampling_budget = ?, userid = ?
                               WHERE scenario_id = ?'''
                modifydatabase(sqledit, (scenario_name, total_hits, conversion_rate, revenue,
                                          purchase_per_user, sampling_cost, sampling_budget, scenario_combo, userid)) 
                          
                
       elif eventid =="button-del":
            sqlinsert = '''DELETE FROM scenarios_tab WHERE scenario_id = ?'''
            modifydatabase(sqlinsert, (scenario_combo,))
       sql = "SELECT scenario_name, scenario_id, userid FROM scenarios_tab"
       df = querydatafromdatabase(sql,[],["label","value", "userid"])
       df = df[df['userid'] == userid][['label', 'value']]
       return [df.to_dict('records'), 
               df.to_dict('records')[0]['value']]
   else:
       sql = "SELECT scenario_name, scenario_id, userid FROM scenarios_tab"
       df = querydatafromdatabase(sql,[],["label","value", "userid"])   
       df = df[df['userid'] == userid][['label', 'value']]
       return [df.to_dict('records'), 
               df.to_dict('records')[0]['value']]


@app.callback(
    [Output('input-0-id', 'value'),   
     Output('input-1-th', 'value'),     
     Output('input-2-cr', 'value'),
     Output('input-3-rpp', 'value'),
     Output('input-4-ntpc','value'),
     Output('input-5-sc', 'value'),
     Output('input-6-sb', 'value')],
    [Input('combo-scenario', 'value'),
     Input('userid', 'children')]
)
def load_scenario(scenario_combo, userid):
    userid = int(userid[0])
    if scenario_combo:
        sql = "SELECT * FROM scenarios_tab WHERE scenario_id = ?"
        df = querydatafromdatabase(sql,[scenario_combo],
                                   ['scenario_id','scenario_name','total_hits','conversion_rate',
                                    'revenue', 'purchase_per_user', 'sampling_cost', 'sampling_budget', 'userid'])
        df = df[df['userid'] == userid]
        scenario_name = df['scenario_name'][0]
        total_hits = df['total_hits'][0]
        conversion_rate = df['conversion_rate'][0]
        revenue = df['revenue'][0]
        purchase_per_user = df['purchase_per_user'][0]
        sampling_cost = df['sampling_cost'][0]
        sampling_budget = df['sampling_budget'][0]
        return [scenario_name, total_hits, conversion_rate, revenue, 
                purchase_per_user, sampling_cost, sampling_budget]
    else:
        raise PreventUpdate

def querydatafromdatabase(sql, values,dbcolumns):
    db = sqlite3.connect('scenarios_tab.db')
    cur = db.cursor()
    cur.execute(sql, values)
    rows = pd.DataFrame(cur.fetchall(), columns=dbcolumns)
    db.close()
    return rows

def modifydatabase(sqlcommand, values):
    db = sqlite3.connect('scenarios_tab.db')
    cursor = db.cursor()
    cursor.execute(sqlcommand, values)
    db.commit()
    db.close()


####################################################################################
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)    
def display_page(pathname):    
    if pathname == '/login':
        return login_page
    elif pathname == '/dashboard':
        return dashboard.dashboard_page
    else:
        return login_page

    

if __name__ == '__main__':
    app.run_server()
    
