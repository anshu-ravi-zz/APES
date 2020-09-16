import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
from data_functions import get_adobe_data, get_student_names
import pandas as pd

external_stylesheets = [dbc.themes.BOOTSTRAP]

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

def create_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=external_stylesheets)

    comment_df = get_adobe_data()
    student_names = get_student_names(comment_df)
    comment_df.sort_values('num_comments', ascending=False, inplace=True)

    def sidebar():
        return html.Div(
                    [
                        html.H2("BDBA Group B", className="display-4"),
                        html.Hr(),
                        html.P(
                            "Individual Student Analysis", className="lead"
                        ),
                        html.Div([dcc.Dropdown(
                            id='student_name',
                            options=[
                                {'label':student_name, 'value': student_name} for student_name in student_names
                            ], placeholder='Select student...'
                        )], style={'width': '100%', 'display': 'inline-block'}),

                        html.Hr(),

                        dbc.Nav(
                            [
                                dbc.NavLink("Number of Comments", href="/dashapp/page-1", id="page-1-link"),
                                dbc.NavLink("Similarity", href="/dashapp/page-2", id="page-2-link"),
                                dbc.NavLink("Overall Score", href="/dashapp/page-3", id="page-3-link"),
                            ],
                            vertical=True,
                            pills=True,
                        ),
                        html.Div([html.A('Go back', href='/home')], style={'position' : 'absolute', 'bottom' : '25px', 'left' : '40px'})
                    ],
                    style=SIDEBAR_STYLE,
                )
    
    def content():
        return html.Div(id="page-content", style=CONTENT_STYLE)

    def page1():
        return html.Div(
            dcc.Graph(id='graph1')
        )


    dash_app.layout = html.Div([
        dcc.Location(id='url'),
        sidebar(),
        content(),
    ])

    @dash_app.callback(
        Output('graph1','figure'),
        [Input(component_id='student_name', component_property='value')]
    )
    def update_graph1(value):
        def set_color(name):
            if name == value:
                return '#047cfc'
            return('#D3D3D3')
        fig = go.Figure(
            data=[go.Bar(x=comment_df['num_comments'], y=comment_df['student'], 
            orientation="h")])
        fig.layout.template = 'plotly_white'
        fig.update_traces(marker_color=list(map(set_color, comment_df['student'])))
        fig.update_xaxes(title_text='Number of Comments')
        fig.update_yaxes(title_text='', automargin=True)
        fig.update_layout(autosize=True, width=1000, height=800, margin=dict(
            l=50,
            r=50,
            b=50,
            t=50,
            pad=4
        ))
        fig['layout']['yaxis']['autorange'] = "reversed"
        return fig

    @dash_app.callback(
        [Output(f"page-{i}-link", "active") for i in range(1, 4)],
        [Input("url", "pathname")],
    )
    def toggle_active_links(pathname):
        if pathname == "/dashapp/":
            return True, False, False
        return [pathname == f"/dashapp/page-{i}" for i in range(1, 4)]

    @dash_app.callback(Output("page-content", "children"), [Input("url", "pathname")])
    def render_page_content(pathname):
        if pathname in ["/dashapp/", "/dashapp/page-1"]:
            return page1()
        elif pathname == "/dashapp/page-2":
            return html.P("Similarity Score.")
        elif pathname == "/dashapp/page-3":
            return html.P("Normal Distribution to compare.")
        # If the user tries to reach a different page, return a 404 message
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ]
        )

    return dash_app.server


