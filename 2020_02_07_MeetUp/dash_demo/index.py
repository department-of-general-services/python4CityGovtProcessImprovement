import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from apps import app1, app2, app3


app.layout = html.Div([

    dcc.Location(id='url', refresh=False),

    html.Div([
        html.Div([
            html.Img(
                src="//www.baltimorecity.gov/sites/all/themes/custom/flight_city/images/uber/logo-big.png",
                style={'float': 'left'},
                className="mr-3"
            ),
            html.H2([
                html.Small([''' City of '''], style={'color': '#deb64b'}),
                html.Br(),
                ''' Baltimore '''
            ], style={'color': '#FFF'})
        ], className="container pt-4 pb-4")
    ], className="container-fluid", style={'background': '#31363c'}),

    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Ul([
                        html.Li([
                            dcc.Link('Dashboard 1', href='/app1')
                        ], className="list-group-item"),
                        html.Li([
                            dcc.Link('Dashboard 2', href='/app2')
                        ], className="list-group-item"),
                        html.Li([
                            dcc.Link('Dashboard 3', href='/app3')
                        ], className="list-group-item")
                    ], className="list-group")
                ])
            ], className="col-md-3"),
            html.Div([
                html.Div(id='page-content')
            ], className="col-md-9")
        ], className="row mt-5 mb-5")
    ], className="container"),

    html.Div([
        html.Div([
            html.P(children='''Copyright © 2018 City of Baltimore''', className="m-0", style={"line-height": "1em"}),
            html.Br(),
            html.P(children='''All Rights Reserved.''', className="m-0")
        ], className="container pt-3 pb-3")
    ], className="container-fluid", style={'background': '#deb64b'})

])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/app1':
        return app1.layout
    elif pathname == '/app2':
        return app2.layout
    elif pathname == '/app3':
        return app3.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)