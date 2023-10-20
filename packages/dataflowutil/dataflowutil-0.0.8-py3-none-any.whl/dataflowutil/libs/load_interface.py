from dash import Dash, html, Input, Output, ctx, callback, dcc, State, dependencies
import dash_bootstrap_components as dbc
import sys
import yaml
from io import StringIO
import os
assets_path = os.getcwd() +'/assets'

class LoadInterface():
    def __init__(self,main):
        self.app = Dash(__name__,external_stylesheets=[dbc.themes.COSMO],suppress_callback_exceptions=True,assets_folder=assets_path)
        self.title_tab_new,self.title_info,self.markdown= {},{},{}
        self.icon_theme = None
        self.color_theme = None
        self.title_general = None

        self.main = main

        self.app.callback(dependencies.Output('tabs-example-content-1', 'children'),
              dependencies.Input('tabs-inline', 'value'))(self.render_content)
        
        self.app.callback(dependencies.Output('console-output', 'children'),
              dependencies.Input('run_process', 'n_clicks'),dependencies.State('tabs-inline', 'value'))(self.run_process_button)


    def load_interface(self,yaml_archive):
        with open(yaml_archive, 'r') as file:
            load_yml = yaml.safe_load(file)
        
        self.title_tab_new,self.title_info,self.markdown= {},{},{}
        self.icon_theme = None
        self.color_theme = None
        self.title_general = None

        for key,value in load_yml.items():
            if "config_general" in  key:
                self.title_general = value["title_general"]
                self.icon_theme = value["icon"]
                self.color_theme = value["color"]
            else:
                self.title_tab_new[key] = value["title_tab_new"]
                self.title_info[key] = value["title_info"]
                self.markdown[key] = value["descrip_tab_page"]


        self.load_process()

    def load_process(self):
        tabs_styles = {
            'height': '44px'
        }

        tab_style = {
            'padding': '10px',
            'fontWeight': 'bold',
            "color":"#9E9E9E",
        }

        tab_selected_style = {
            'borderBottom': f'3px solid {self.color_theme}',
            'padding': '10px',
            'fontWeight': 'bold',
            "background": "white",
            "color": f"{self.color_theme}",
        }


        elements_tab = [
            dcc.Tab(label=f'{value}', value=f'{key}', style=tab_style, selected_style=tab_selected_style)
            for key,value in self.title_tab_new.items()
        ]
        
        self.app.layout = dbc.Container([

            dbc.Row(
                [
                    dbc.Col(html.Img(src=self.app.get_asset_url(self.icon_theme),style={"width":"65px","margin-left":"20px"}), width=3,style={"background-color": self.color_theme,"padding": "17px"}),
                    dbc.Col(
                        html.H1(self.title_general,style={"color":"white","margin-left":"20px"}
                    ), width=9,style={"background-color": self.color_theme,"padding": "15px"})
                ],
            ),

            dcc.Tabs(id='tabs-inline', value=list(self.title_tab_new.keys())[0], children=elements_tab,style=tabs_styles,colors={
                "background": "white"
            }),
            
            html.Div(style={'margin': '100px'}),
            html.Div(id='tabs-example-content-1'),
            dcc.Loading(
                    id="loading-output",
                    type="circle",  # También puedes probar con "default", "circle", "dot", "default", "pacman"
                    children=[html.Div(id="console-output",style={'textAlign': 'center'})],fullscreen=True,
                )  
        ],fluid=True)


    def render_content(self,tab):
        get_title = self.title_info[tab]
        return html.Div([
            html.H1(get_title, style={'textAlign': 'center'}),
            dcc.Markdown(self.markdown[tab]),
            dbc.Button("Run Process",id="run_process", style={"background-color":self.color_theme}),
            html.Div(style={'margin': '7px'}),
            
        ],className="d-grid gap-3 col-6 mx-auto")
    

    def run_process_button(self,n_clicks,state):
        if n_clicks is not None:
            # Redirect stdout to a variable
            sys.stdout = mystdout = StringIO()

            self.main.load(state)

            # Get the output
            sys.stdout = sys.__stdout__
            output = mystdout.getvalue()

            return html.Pre(output)