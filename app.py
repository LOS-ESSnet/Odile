# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import gettext
from dash.dependencies import Input, Output

import queries
import config


language = gettext.translation('base',
                               localedir='locales',
                               languages=[config.language])
language.install()
_ = language.gettext


app = dash.Dash()
server = app.server

# Import of CSS stylesheet
app.css.append_css({"external_url": config.css_url})

app.layout = html.Div(children=[
    html.H1(children=_('Odil ou Odette')),
    html.H2(children=_('Paramètres du diagnostic local')),
    html.Div(children=_('Sélection de la commune')),
    html.Label(_('Département')),
    dcc.Dropdown(
        id='dep_id',
        options=queries.department_list(),
        value=queries.department_list()[0]['value']
    ),

    html.Label(_('Commune')),
    dcc.Dropdown(
        id='com_id',
        value=[],
        multi=True
    ),

    html.Div(children=_('Sélection de l\'activité')),
    dcc.Input(id='activity_str', value='', type='text'),
    dcc.Dropdown(
        id='activity_selection',
        value=[],
        multi=True
    ),

    html.H2(children=_('Résultats')),
    dcc.Graph(
        id='graphpop'
       ),
    html.Div(children=_('Filtrer sur un sexe')),
    dcc.RadioItems(
        id='gender_selection',
        options=[
            {'label': _('Hommes'), 'value': '1'},
            {'label': _('Femmes'), 'value': '2'}
        ],
        value='2'
    ),
    dcc.Graph(
        id='popstructure'
        )
])


@app.callback(
    Output(component_id='com_id',
           component_property='options'),
    [Input(component_id='dep_id',
           component_property='value')]
)
def update_municipality_list(department):
    return queries.liste_communes(department)


@app.callback(
    Output(component_id='activity_selection',
           component_property='options'),
    [Input(component_id='activity_str',
           component_property='value')]
)
def update_output_div(input_value):
    return queries.activity_list(input_value)


@app.callback(
    Output(component_id='graphpop',
           component_property='figure'),
    [Input(component_id='com_id',
           component_property='value')]
)
def update_pop_evolution(communes):
    return {
            'data': [queries.population(codecom)
                     for codecom in communes],
            'layout': {'title': _('Evolution démographique')}
    }


@app.callback(
    Output(component_id='popstructure',
           component_property='figure'),
    [Input(component_id='com_id',
           component_property='value'),
     Input(component_id='gender_selection',
           component_property='value')
     ]
)
def update_pop_structure(communes, gender):
    return {
            'data': [queries.population_structure(codecom, gender)
                     for codecom in communes],
            'layout': {'title': _('Structure de la population en 2015')}
    }


if __name__ == '__main__':
    app.run_server(debug=True)
