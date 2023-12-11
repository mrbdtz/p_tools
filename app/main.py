from dash import Dash, Input, Output, State, html, dcc, callback, callback_context
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_auth
from app.database.postgres import PtoolsDB
from app.core.config import settings

from datetime import datetime

# App create
VALID_USERNAME_PASSWORD_PAIRS = {settings.DASH_USERNAME: settings.DASH_PASSWORD}
app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])
auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)
server = app.server
app.title = "Platform Tools"
app._favicon = ('icons8-steam-32.png')

# Layout elements
title = html.H1('Followers Dumper', id='title1')
input_dropdown = dcc.Dropdown(id='input_dropdown', clearable=False)
btn_download = dbc.Button('Download Data', id='btn_download', color="info", outline=True, n_clicks=0,
                          style = {'width':'180px'})
progress = html.Div(
    [
        dcc.Interval(id="progress-interval", n_intervals=0, interval=500),
        dbc.Progress(id="progress", striped=True, animated=True),
    ]
)

# Layout body
tab1_content = dbc.Container(
html.Div([
    # Title
    dbc.Row([title], style = {'margin-left':'7px', 'margin-top':'40px'}),

    # Download
    dbc.Row([dbc.Col([input_dropdown], width=9),
             dbc.Col([btn_download])], style = {'margin-top':'14px'}, align="center"),
             dcc.Download(id='download_data'),
    dbc.Row(id='table_last', children=[], style = {'margin-top':'14px'}),
    dbc.Row(progress),
    dbc.Row(id='table_followers_data', children=[], style = {'margin-top':'14px'})
    ]
),style={"height": "100vh", "width": "70%", "font-family":"Motiva Sans, Sans-serif"})

# Layout
app.layout = html.Div([tab1_content])

# Functions
def create_table(followers_data):
    # Create table with followers data
    use_cols = ['#', 'dump', 'date', 'followers', 'minutes to dump']
    order_cols = [4, 1, 2, 3]
    table_th = []
    for c in use_cols:
        table_th.append(html.Th(c))
    table_header = [html.Thead(html.Tr(table_th))]
    table_rows = []
    for i, row in enumerate(followers_data):
        row = [row[i] for i in order_cols]
        row[1] = row[1].strftime('%d-%m-%Y')
        row[3] = round(row[3] / 60, 1)
        table_td = []
        table_td.append(html.Td(i+1))
        for col in row:
            table_td.append(html.Td(col))
        table_rows.append(html.Tr(table_td))
    table_body = [html.Tbody(table_rows)]
    table = dbc.Table(table_header + table_body, bordered=True)
    return table

# Callbacks
# Update data on page load
@callback(Output('table_followers_data', 'children'), Output('input_dropdown', 'options'), Output('input_dropdown', 'value'),
          Input('btn_download', 'n_clicks'))
def retrun_dropdown(n_clicks):
    if n_clicks == 0:
        ptools_db = PtoolsDB()
        followers_data = ptools_db.select_followers_data_table()
        ptools_db.conn.close()
        table = create_table(followers_data)
        options = [v[-1] for v in followers_data]
        return table, options, options[0]
    else:
        raise PreventUpdate
    
# Download all data for choosen database
@callback(Output("download_data", "data"), Input("btn_download", 'n_clicks'), State('input_dropdown', 'value'), 
          prevent_initial_call=True)
def all_comments(n_clicks, table_name):
    if n_clicks == 0:
        raise PreventUpdate
    else:
        ptools_db = PtoolsDB()
        followers_steamids = ptools_db.select_followers_table(table_name)
        ptools_db.conn.close()
        content = 'steamid\n'
        if followers_steamids is not None:
            content = content + '\n'.join([str(v[0]) for v in followers_steamids])
            filename = table_name + '.csv'
            return dict(content=content, filename=filename)

if __name__ == "__main__":
    app.run_server(debug=True)