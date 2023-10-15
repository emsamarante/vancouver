import dash
from dash import html, dcc
import dash_bootstrap_components as dbc


texto = """ Vancouver is one of the most ethnically and linguistically diverse cities in Canada: 49.3 percent of its residents are
 not native English speakers, 47.8 percent are native speakers of neither English nor French, and 54.5 percent of residents belong 
 to visible minority groups. It has been consistently ranked one of the most livable cities in Canada and in the world.
 In terms of housing affordability, Vancouver is also one of the most expensive cities in Canada and in the world.
 Vancouver plans to become the greenest city in the world. Vancouverism is the city's urban planning design philosophy. """


texto_project_1 = """ Not all areas of Vancouver are as safe as others. Vancouver has been been voted one of the best cities in the 
world to live in, but crime statistics clearly indicate that there are some areas where you want to have your wits about you. These areas are often 
referred to as "hot spots" of crime. """

texto_project_2 = """In this project I analyse data of crimes in Vancouver and show the results in the attractive way. This dashboard is compound
by four screens: """



tab_card = {'height': '98vh', "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 5px 6px 15px 0 rgba(0, 0, 0, 0.19)"}


layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.CardImg(src="/static/images/vancouver.jpg",style={"object-fit": "cover", "object-position": "100% 65%",
                                                                               "width": "100%", "height": "400px"}),
                        html.H2("Is Vancouver dangerous?", style={'margin-top':'15px'}),
                        dbc.Col([
                            html.H4("Overview", style={"margin-top":"15px"}),
                            html.P(texto, style={"text-align": "justify"})
                        ], sm=6),
                        dbc.Col([
                            html.Div([
                                html.H4("About the project", style={"margin-top":"15px"}),
                                html.P(texto_project_1),
                                html.P(texto_project_2),
                                html.Li("Home - You see a brief overview of Vancouver and the project. (This page)", style={'margin-left':'15px'} ),
                                html.Li("Maps - The analysis of crimes in georeferencing perspective.", style={'margin-left':'15px'} ),
                                html.Li("Analysis - Analysis of crimes and some metrics.", style={'margin-left':'15px'} ),
                            ], style={"text-align": "justify"} ),
                            
                        ], sm=6),
                    ])
                ])
            ], style=tab_card)
        ], lg=12)
    ], className='g-2 my-auto', style={"margin-top":"9px"}),
    
], fluid=True)