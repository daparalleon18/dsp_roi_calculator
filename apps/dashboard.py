
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 12:46:51 2022

@author: dparalleon
"""


#%%


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

from dash.dependencies import Input, Output, State
import pandas as pd
import dash_table
import sqlite3
from dash.exceptions import PreventUpdate
from app import app

app = dash.Dash()
server = app.server

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


app.layout = html.Div([
    html.Div(children = [
        html.H3('Return of Investment Inputs: ', style = hstyle),
        html.Table([
            html.Tr([
                    html.Td('Scenario Name: ', style = {'font-weight': 'bold'}),
                    html.Td(
                        dcc.Input(
                            id = 'input-0-id',
                            type = 'text',
                            value = 'Scenario 1'
                            ),                                        
                        )
                
                ]),
            html.Tr([
                    html.Td('Total Hits: ', style={'font-weight': 'bold'}),
                    html.Td(
                        dcc.Input(
                            id = 'input-1-th',
                            type = 'number',
                            value = 1000000.00
                            ),                                        
                        )
                ]),
            html.Tr([
                    html.Td('Conversion Rate: ', style={'font-weight': 'bold'}),
                    html.Td(
                        dcc.Input(
                            id = 'input-2-cr',
                            type = 'number',
                            value = 60.00
                            ),                                        
                        )
                ]), 
            html.Tr([
                    html.Td('Revenue Per Purchase (PhP): ', style={'font-weight': 'bold'}),
                    html.Td(
                        dcc.Input(
                            id = 'input-3-rpp',
                            type = 'number',
                            value = 50.00
                            ),                                        
                        )
                ]),
            html.Tr([
                    html.Td('Number of Times of Purchase per Converter User Per Year: ', style={'font-weight': 'bold'}),
                    html.Td(
                        dcc.Input(
                            id = 'input-4-ntpc',
                            type = 'number',
                            value = 2.00
                            ),                                        
                        )
                ]),
            html.Tr([
                    html.Td('Total Cost of Sampling (Php): ', style={'font-weight': 'bold'}),
                    html.Td(
                        dcc.Input(
                            id = 'input-5-sc' ,
                            type = 'number',
                            value = 25000000.00
                            ),                                        
                        )
                ]),
            html.Tr([
                    html.Td('% of Potential Revenue You Are Willing to Allocate for Sampling: ', style={'font-weight': 'bold'}),
                    html.Td(
                        dcc.Input(
                            id = 'input-6-sb',
                            type = 'number',
                            value = 50.00                       
                            ),                                        
                        )
                ]), 
            html.Tr([
                    html.Td(
                       html.Button('Calculate ROI', 
                                   id = 'button-calc', 
                                   style = {'backgroundColor': colors['c1'],
                                            'color': 'white',
                                            'height': '40px',
                                            'width': '100px'
                                            
                                            })                           
                        ),
                    html.Td('')
                ]),
            
            
            html.Tr([
                    html.Td('Select Scenario: ', style = {'font-weight': 'bold'}),
                    html.Td(
                        dcc.Dropdown(
                            id = 'combo-scenario'
                            )
                        )
                
                ]),
            
            html.Tr([
                    html.Td(
                       html.Button('Save Settings', 
                                   id = 'button-save', 
                                   style = {'backgroundColor': colors['c1'],
                                            'color': 'white',
                                            'height': '40px',
                                            'width': '100px'
                                            
                                            })                           
                        ),
                    html.Td(
                        dcc.Checklist(
                            id = 'mode-edit',
                            value = [],
                            options = [
                                {'label': 'Edit Mode', 'value': 1}
                                ]
                            )
                        )
                ]),
            html.Tr([
                    html.Td(
                       html.Button('Delete the Scenario', 
                                   id = 'button-del', 
                                   style = {'backgroundColor': colors['c1'],
                                            'color': 'white',
                                            'height': '40px',
                                            'width': '100px'
                                            
                                            })                           
                        ),
                    html.Td('')
                ]),
            html.Tr([

                html.A(html.Button('Log Out', 
                        id = 'logout', 
                        style = {'backgroundColor': colors['c1'],
                                 'color': 'white',
                                 'height': '40px',
                                 'width': '100px',                                                 
                                 }       
                            ), href = '/login'
                       ),
                ])
            
            
            
                             
        ])
        
        
    ], style={'width': '25%', 'display': 'inline-block', 
              'vertical-align': 'top', 'horizontal-align': 'left', 
              'fontSize': 14}),
    
    html.Div(children = [
        html.Div(children = [
            html.H3('Investment/Income Breakdown', style = hstyle),
            dcc.Graph(
                id = 'chart-pie', 
                figure = {
                    'data': [
                        go.Pie(
                            labels = ['Unconverted Revenue, Php',
                                      'Max Allowable Spend, Php',
                                      'Net Profit Not For Sampling, Php',
                                      'Sampling Cost, Php'],
                            values = [40000000, 17500000, 17500000, 25000000],
                            textinfo='label, value',
                            textposition = 'outside',                            
                            showlegend = False,
                            hole = .4,
                            marker_colors = [colors['c5'], colors['c2'], colors['c3'], colors['c4']],
                            marker = dict(line=dict(color='black', width=.8))
                                                        
                            )
                        ]
                        
                    }, style = {'height': '300px', 'width': '500px', 'marginTop': 'auto',
                                'marginLeft': 'auto', 'marginRight': 'auto',
                                'marginTop': '0px'}                     
                )
            ]
        ), 
        
        html.Div(children = [
            html.H3('ROI Parameters Computed: ', style = hstyle),
            html.Table([
                html.Tr([
                        html.Td('Total Potential Annual Revenue: ', 
                                style = {'textAlign': 'left',
                                         'border': 'solid', 'border-width': '0.2px'}), 
                        html.Td(id = 'tab-1-tpar', 
                                style = {'textAlign': 'right',
                                         'border': 'solid', 'border-width': '0.2px'})                                            
                    ]), 
                html.Tr([
                        html.Td('Unconverted Opportunity Revenue: ', 
                                style = {'textAlign': 'left',
                                         'border': 'solid', 'border-width': '0.2px'}),
                        html.Td(id = 'tab-2-uor', 
                                style = {'textAlign': 'right',
                                         'border': 'solid', 'border-width': '0.2px'})                                                
                    ]), 
                html.Tr([
                        html.Td('Converted Revenue: ', 
                                style = {'textAlign': 'left',
                                         'border': 'solid', 'border-width': '0.2px'}),
                        html.Td(id = 'tab-3-cr', 
                                style = {'textAlign': 'right',
                                         'border': 'solid', 'border-width': '0.2px'})                                                
                    ]), 
                html.Tr([
                        html.Td('Maximum Allowable Spend: ', 
                                style = {'textAlign': 'left',
                                         'border': 'solid', 'border-width': '0.2px'}),
                        html.Td(id = 'tab-4-mas', 
                                style = {'textAlign': 'right',
                                         'border': 'solid', 'border-width': '0.2px'})                                                
                    ]), 
                html.Tr([
                        html.Td('Maximum Spend per Hit: ', 
                                style = {'textAlign': 'left',
                                         'border': 'solid', 'border-width': '0.2px'}),
                        html.Td(id = 'tab-5-msh', 
                                style = {'textAlign': 'right',
                                         'border': 'solid', 'border-width': '0.2px'})                                                
                    ])
                ], style = {#'border': 'solid', 'border-width': '0.2px',
                            'height': '100px', 'width': '500px', 'border-collapse': 'collapse',
                            'marginLeft': 'auto', 'marginRight': 'auto'})
            
            
            ]), 
        
        
        
        
        
        html.Div(children = [
            html.H3('Estimated Net Profit from Sampling: ', style = hstyle),
            html.Table([ 
                html.Tr([
                        html.Td('Net Profit: ', 
                                style = {'textAlign': 'left',
                                         'border': 'solid', 'border-width': '0.2px'}),
                        html.Td(id = 'tab-6-nps', 
                                style = {'textAlign': 'right',
                                         'border': 'solid', 'border-width': '0.2px'}) 
                ])
            ], style = {#'border': 'solid', 'border-width': '0.2px', 
                        'height': '20px', 'width': '500px', 'border-collapse': 'collapse',
                        'marginLeft': 'auto', 'marginRight': 'auto'})
            
            
            
            ]), 
        
    ], style={'width': '40%', 'display': 'inline-block', 
              'vertical-align': 'top', 'textAlign': 'center', 'fontSize': 14}),
    
    html.Div(children = [                
        html.H3('Waterfall Chart', style = hstyle),
        dcc.Graph(
            id = 'chart-wf', 
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
                        y = [100000000, -40000000, 0, -25000000, 0, -17500000, 0],
                        measure = ["absolute", "relative", "total", "relative", "total","relative", "total"],
                        orientation = 'v', textposition = 'outside',   
                        decreasing = {'marker':{'color':colors['c7']}},
                        totals = {'marker':{'color':colors['c6']}}                                                
                        )
                    ],
                    
                }, style = {'height': '550px', 'width': '600px', 
                            'marginTop': '0px', 'paddingTop': '0px'}  
            )
        
    ], style={'width': '35%',  'display': 'inline-block', 
              #'marginLeft': 'auto', 'marginRight': 'auto',
              'vertical-align': 'top', 'textAlign': 'center',
              'fontSize': 14})                                           
         
])
                          
dashboard_page = app.layout

if __name__ == '__main__':
    app.run_server()
