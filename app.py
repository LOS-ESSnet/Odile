# -*- coding: utf-8 -*-
import os,os.path
os.environ['HTTP_PROXY']="http://proxy-rie.http.insee.fr:8080"
os.environ['HTTPS_PROXY']="http://proxy-rie.http.insee.fr:8080"


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import queries

app = dash.Dash()
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.layout = html.Div(children=[
    html.H1(children='Odil ou Odette'),

    html.H2(children='Paramètres du diagnostic local'),
    html.Div(children='Sélection de la commune'),
    html.Label('Département'),
    dcc.Dropdown(
        id = 'dep_id',
        options=queries.liste_departements(),
        value=queries.liste_departements()[0]['value']
    ),

    html.Label('Commune'),
    dcc.Dropdown(
        id = 'com_id',
        value=[],
        multi=True
    ),
        
    html.Div(children='Sélection de l\'activité'),            
    dcc.Input(id='activity_str', value='', type='text'),
    dcc.Dropdown(
        id = 'activity_selection',
        value=[],
        multi=True
    ),
            
    html.H2(children='Résultats'),
    dcc.Graph(
        id='graphpop'
       ),
    html.Div(children = 'Filtrer sur un sexe'),
    dcc.RadioItems(
        id = 'gender_selection',
        options=[
            {'label': 'Hommes', 'value': '1'},
            {'label': 'Femmes', 'value': '2'}
        ],
        value='2'
    ),
    dcc.Graph(
        id = 'popstructure'
        )
])




@app.callback(
    Output(component_id='com_id', component_property='options'),
    [Input(component_id='dep_id', component_property='value')]
)
def update_liste_communes(departement):
    return queries.liste_communes(departement)

@app.callback(
    Output(component_id='activity_selection', component_property='options'),
    [Input(component_id='activity_str', component_property='value')]
)
def update_output_div(input_value):
    return queries.list_activities(input_value)

@app.callback(
    Output(component_id='graphpop', component_property='figure'),
    [Input(component_id='com_id', component_property='value')]
)
def update_pop_evolution(communes):
    return {
            'data': [queries.population(codecom) for codecom in communes],
            'layout': {'title': 'Evolution démographique'}
    }

@app.callback(
    Output(component_id='popstructure', component_property='figure'),
    [Input(component_id='com_id', component_property='value'),
     Input(component_id='gender_selection', component_property='value')
]
)
def update_pop_structure(communes,gender):
    return {
            'data': [queries.population_structure(codecom,gender) for codecom in communes],
            'layout': {'title': 'Structure de la population en 2015'}
    }
      

if __name__ == '__main__':
    app.run_server(debug=True)