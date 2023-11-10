from dash import html
import dash_bootstrap_components as dbc


texto = """Vancouver is recognized as one of the most ethnically and 
linguistically diverse cities in Canada, with 49.3 percent of its 
residents not being native English speakers. Additionally, 47.8 percent
 are native speakers of neither English nor French, and 54.5 percent belong
   to visible minority groups. The city has consistently earned a reputation
     as one of the most livable cities in Canada and globally. """


texto_project_1 = """
Not all areas of Vancouver are as safe as others. While Vancouver
 has been voted one of the best cities in the world 
 to live in, crime statistics clearly indicate that there are some
   areas where you need to be careful. These areas are often
     referred to as 'hot spots' of crime.
"""

texto_project_1_1 = """
The project aims to inform the citizens of Vancouver about security
 issues and share insights with the Chief of Police on the subject.
"""

texto_project_2 = """In this project, I analyze crime data in Vancouver
 and present the results in an attractive perspective. This dashboard
   is comprised of three screens:"""

texto_project_3 = """In the upcoming versions of this project, I plan
 to add more information and incorporate time series forecasting."""


tab_card_home = {'min-height': '100%',
                 "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 5px 6px 15px 0 rgba(0, 0, 0, 0.19)"}


layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.CardImg(src="/static/images/vancouver.jpg", style={"object-fit": "cover", "object-position": "100% 65%",
                                                                               "width": "100%", "height": "400px"}),
                        html.H2("Is Vancouver dangerous?",
                                style={'margin-top': '15px'}),
                        dbc.Col([
                            html.H4("Overview", style={"margin-top": "15px"}),
                            html.P(texto, style={"text-align": "justify"}),
                            html.P(texto_project_1),
                            html.P(texto_project_1_1),
                        ], sm=6),
                        dbc.Col([
                            html.Div([
                                html.H4("About the project", style={
                                        "margin-top": "15px"}),
                                html.P(texto_project_2),
                                html.Li(
                                    "Home: You see a brief overview of Vancouver and the project. (This page)", style={'margin-left': '15px'}),
                                html.Li(
                                    "Overview Analysis: Analysis by time, location and some metrics are displayed.", style={'margin-left': '15px'}),
                                html.Li(
                                    "Spatial Analysis: The analysis of crimes in georeferencing perspective.", style={'margin-left': '15px'}),
                            ], style={"text-align": "justify"}),
                            html.Br(),
                            html.P(texto_project_3),
                        ], sm=6),
                    ])
                ])
            ], style=tab_card_home)
        ], lg=12)
    ], className='g-2 my-auto', style={"margin-top": "9px"}),

], fluid=True)
