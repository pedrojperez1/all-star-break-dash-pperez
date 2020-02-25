# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import re
import os
import numpy as np 
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = app.server

data = pd.read_csv('C:/Users/pedro/Downloads/ibp_pitcher.csv')
##########################################################
# data needs to be cleaned a bit (e.g. bs_count is mistaken for dates)
##########################################################
temp = [re.sub(r'Jan', '1', x) for x in data.bs_count]
temp = [re.sub(r'Feb', '2', x) for x in temp]
temp = [re.sub(r'Mar', '3', x) for x in temp]
temp = [re.sub(r'00', '0', x) for x in temp]
data['bs_count'] = temp
new = data['bs_count'].str.split('-', n=1, expand=True)
data['ball_count'] = new[0]
data['strike_count'] = new[1]
data['walk'] = [row.pitch_result == 'ball' and row.ball_count == '3' for index, row in data.iterrows()]
data = data[data.pitch_type != 'FT']
##########################################################
def init_kde(df, pitcher, pitch_type, metric):
    filtered_df_init = df[df.pitcherid == pitcher].copy()
    filtered_df_init = filtered_df_init[filtered_df_init.pitch_type == pitch_type]
    before_init = filtered_df_init[filtered_df_init['all_star'] == 'before'][metric].dropna()
    after_init = filtered_df_init[filtered_df_init['all_star'] == 'after'][metric].dropna()

    hist_data_init = [before_init, after_init]
    group_labels_init = ['before', 'after']
    colors = ['#636EFA', '#EF553B']
    fig = ff.create_distplot(hist_data_init, group_labels_init, colors=colors)
    fig.update_layout(
        legend=dict(
            orientation='h',
            yanchor='top',
            xanchor='center',
            x=0.5,
            y=-0.15
        ),
    )

    return fig

def init_bar_graph(df, before_after, pitcherid):
    to_graph = df.groupby(['pitcherid', 'pitch_type', 'pitch_result', 'all_star']).apply(lambda x: x.count())['x'].reset_index()
    temp = to_graph[to_graph['pitcherid'] == pitcherid]
    temp = temp[temp['all_star'] == before_after].sort_values(by=['x'])
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=temp[temp['pitch_result'] == 'ball']['pitch_type'],
        x=temp[temp['pitch_result'] == 'ball']['x'],
        name='ball',
        orientation='h',
    ))
    fig.add_trace(go.Bar(
        y=temp[temp['pitch_result'] == 'called_strike']['pitch_type'],
        x=temp[temp['pitch_result'] == 'called_strike']['x'],
        name='called_strike',
        orientation='h',
    ))

    fig.update_layout(
        barmode='stack', 
        title={
            'text': before_after.capitalize(),
            'x': 0.5,
            'xanchor': 'center'
        },
        legend=dict(
            orientation='h',
            yanchor='top',
            xanchor='center',
            x=0.5,
            y=-0.15
        ),
    )

    return fig

def init_pitch_scatter(df, before_after, pitcher, pitch_type):
    data = df[df.pitcherid == pitcher]
    data = data[df.all_star == before_after]
    data = data[data.pitch_type == pitch_type]
    fig = px.scatter(
        data, 
        x="x", 
        y="z", 
        color="pitch_result", 
        # colorscale=[['called_strike', '#636EFA'], ['ball', '#EF553B']],
        opacity=0.80)
    fig.add_shape(
                type="rect",
                x0=-10,
                y0=18,
                x1=10,
                y1=42,
                line=dict(
                    color="Black",
                    width=2,
                ),
                layer='below',
            )
    fig.update_xaxes(autorange='reversed')
    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        # autosize=False,
        # width=500,
        # height=500,
        legend=dict(
            orientation='h',
            yanchor='top',
            xanchor='center',
            x=0.5,
            y=-0.15,
            title=''
        ),
    )
    fig.update_xaxes(range=[-45, 45])
    fig.update_yaxes(range=[-15, 75])

    return fig



app = dash.Dash(external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.Div([
        html.H2('What happened after the All-Star break?')
    ], style={'margin': 'auto', 'text-align': 'center'}),
    html.Div([
        html.H5('Choose a pitcher to get started...')
    ], style={'margin': 'auto', 'text-align': 'center'}),
    html.Div([
        dcc.Dropdown(
            id='pitcher_drop',
            options=[
                {'label': 'Pitcher 1', 'value': 1},
                {'label': 'Pitcher 2', 'value': 2},
                {'label': 'Pitcher 3', 'value': 3}
            ],
            value=1
        )  
    ], style={'width': '25%', 'margin': 'auto', 'text-align': 'center'}
    ),
    html.Div([
        html.Div([
            dcc.Graph(
                id='before_bar',
                figure=init_bar_graph(data, 'before', 1)
            )
        ], className='six columns'),
        html.Div([
            dcc.Graph(
                id='after_bar',
                figure=init_bar_graph(data, 'after', 1)
            )
        ], className='six columns'),
    ], className='row'),
    html.Div([
        html.Div([
            html.H6('Did placement change for different pitch types?')
        ], style={'margin': 'auto', 'text-align': 'center'}),
        html.Div([
            dcc.Dropdown(
                id='pitch_type_drop',
                options=[
                    {'label': 'FF', 'value': 'FF'},
                    {'label': 'CB', 'value': 'CB'},
                    {'label': 'CH', 'value': 'CH'},
                    {'label': 'SL', 'value': 'SL'},
                    {'label': 'CT', 'value': 'CT'},
                    {'label': 'FT', 'value': 'FT'}
                ],
                value='FF'
            ) 
        ], style={'width': '20%', 'margin': 'auto', 'text-align': 'center'}),
        html.Div([
            html.Div([
                dcc.Graph(
                    id='before_pitch_scatter',
                    figure=init_pitch_scatter(data, 'before', 1, 'FF')
                )
            ], className='six columns'),
            html.Div([
                dcc.Graph(
                    id='after_pitch_scatter',
                    figure=init_pitch_scatter(data, 'after', 1, 'FF')
                )
            ], className='six columns'),
        ], className='row'),
        html.Div([
            html.Div([
                html.H6('How did distribution of biometric measures change after the break? ')
            ], style={'margin': 'auto', 'text-align': 'center'}),
            html.Div([
                dcc.Dropdown(
                    id='metric_drop',
                    options=[
                        {'label': 'spin_rate', 'value': 'spin_rate'},
                        {'label': 'release_velocity', 'value': 'release_velo'},
                        {'label': 'pfx_x', 'value': 'pfx_x'},
                        {'label': 'pfx_z', 'value': 'pfx_z'},
                        {'label': 'extension', 'value': 'extension'},
                        {'label': 'release_x', 'value': 'release_x'},
                        {'label': 'release_y', 'value': 'release_y'},
                        {'label': 'release_z', 'value': 'release_z'}
                    ],
                    value='release_velo'
                )
            ], style={'width': '25%', 'margin': 'auto', 'text-align': 'center'}),
        ]),
        dcc.Graph(
            id='g1',
            figure=init_kde(data, 1, 'FF', 'release_velo')
        )
    ], style={'margin': 'auto'}),
    html.Footer(
        html.Div(
            id='footer-copyright',
            className='container-fluid text-center',
            children=[
                html.Span(
                    'Copyright © 2020 Pedro Perez',
                    className='text-muted'),
                html.H5(),
            ]),
        className='page-footer',
        style={
            'textAlign': 'center',
            'position': 'relative',
            'bottom': 0,
            'width': '100%',
            'padding': '60px 15px 0',
        }, 
    )
])

@app.callback(
    [
        Output('g1', 'figure'),
        Output('before_bar', 'figure'),
        Output('after_bar', 'figure'),
        Output('before_pitch_scatter', 'figure'),
        Output('after_pitch_scatter', 'figure')
    ],
    [
        Input('pitcher_drop', 'value'),
        Input('metric_drop', 'value'),
        Input('pitch_type_drop', 'value')
    ]
)
def update_figure(selected_pitcher, selected_metric, selected_pitch_type):

    output1 = init_kde(data, selected_pitcher, selected_pitch_type, selected_metric)
    output2 = init_bar_graph(data, 'before', selected_pitcher)
    output3 = init_bar_graph(data, 'after', selected_pitcher)
    output4 = init_pitch_scatter(data, 'before', selected_pitcher, selected_pitch_type)
    output5 = init_pitch_scatter(data, 'after', selected_pitcher, selected_pitch_type)

    return output1, output2, output3, output4, output5


if __name__ == '__main__':
    app.run_server(debug=True)