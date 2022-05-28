import dash
import dash_bootstrap_components as dbc
from dash import html
import requests
import pandas as pd
from dash import dcc
import plotly.express as px
import numpy as np
from dash.dependencies import Input,Output
from dash import dash_table


app = dash.Dash(external_stylesheets = [ dbc.themes.BOOTSTRAP],)
IMG = "https://www.google.com/imgres?imgurl=https%3A%2F%2Fwww.ruralhealthinfo.org%2Fassets%2F4049-17150%2Fcovid-vaccination-fb.jpg&imgrefurl=https%3A%2F%2Fwww.ruralhealthinfo.org%2Ftopics%2Fcovid-19%2Fvaccination&tbnid=cPzmLKXIUihgMM&vet=12ahUKEwjWt7zHtv_3AhUQUBoKHfNwArgQMygGegUIARCNAQ..i&docid=vYNvV_CvNHsXAM&w=1200&h=628&q=covid%20vaccination%20images&ved=2ahUKEwjWt7zHtv_3AhUQUBoKHfNwArgQMygGegUIARCNAQ"

# vaccination data
url = "https://covid19.who.int/who-data/vaccination-data.csv"
df = pd.read_csv(url)



df_to_use = df[['COUNTRY','ISO3','TOTAL_VACCINATIONS','PERSONS_VACCINATED_1PLUS_DOSE','PERSONS_FULLY_VACCINATED','VACCINES_USED','NUMBER_VACCINES_TYPES_USED','PERSONS_BOOSTER_ADD_DOSE']]
country = df_to_use['COUNTRY']
iso_code = df_to_use['ISO3']
total_vaccination_doses = df_to_use['TOTAL_VACCINATIONS'][0]
single_dose = df_to_use['PERSONS_VACCINATED_1PLUS_DOSE'][0]
fully_vaccinated = df_to_use['PERSONS_FULLY_VACCINATED'][0]
vaccines_used = df_to_use['VACCINES_USED']
no_vaccine_types = df_to_use['NUMBER_VACCINES_TYPES_USED'][0]
booster_dose = df_to_use['PERSONS_BOOSTER_ADD_DOSE'][0]



def global_map(df):
    fig = px.choropleth(df, locations="ISO3", color = "TOTAL_VACCINATIONS",
                        hover_name= "COUNTRY",
                        hover_data = ['TOTAL_VACCINATIONS','PERSONS_VACCINATED_1PLUS_DOSE','PERSONS_FULLY_VACCINATED'],
                        projection="orthographic",
                        color_continuous_scale=px.colors.sequential.Plasma)

    fig.update_layout(margin = dict(l=4,r=4,t=4,b=4))

    return fig


def data_for_doses(header, total_cases):
    card_content = [
        dbc.CardHeader(header),

        dbc.CardBody(
            [
               dcc.Markdown( dangerously_allow_html = True,
                   children = ["{0} ".format(total_cases)])


                ]

            )
        ]

    return card_content
  
    
############################################ Dashboard body###########################

body_app = dbc.Container([

    dbc.Row( html.Marquee("Global"), style = {'color':'green'}),

    dbc.Row([
        dbc.Col(dbc.Card(data_for_doses("Total Vaccinations Administered",f'{total_vaccination_doses:,}' ), color = 'green',style = {'text-align':'center'}, inverse = True),xs = 12, sm = 12, md = 4, lg = 4, xl = 4, style = {'padding':'12px 12px 12px 12px'}),
        dbc.Col(dbc.Card(data_for_doses("Partially Vaccinated",f'{single_dose:,}' ), color = 'blue',style = {'text-align':'center'}, inverse = True),xs = 12, sm = 12, md = 4, lg = 4, xl = 4, style = {'padding':'12px 12px 12px 12px'}),
        dbc.Col(dbc.Card(data_for_doses("Fully Vaccinated",f'{fully_vaccinated:,}' ), color = 'brown',style = {'text-align':'center'}, inverse = True),xs = 12, sm = 12, md = 4, lg = 4, xl = 4, style = {'padding':'12px 12px 12px 12px'})


        ]),

    html.Br(),
    html.Br(),

    dbc.Row([html.Div(html.H4('Covid19 Global Vaccination Footprint'),
                      style = {'textAlign':'center','fontWeight':'bold','family':'georgia','width':'100%'})]),

    html.Br(),
    html.Br(),

    dbc.Row([dbc.Col(dcc.Graph(id = 'world-graph', figure = global_map(df_to_use)),style = {'height':'450px'},xs = 12, sm = 12, md = 6, lg = 6, xl = 6),

             dbc.Col([html.Div(id = 'dropdown-div', children =
             [dcc.Dropdown(id = 'country-dropdown',
                 options = [{'label':i, 'value':i} for i in np.append(['All'],df_to_use['COUNTRY'].unique()) ],
                 value = 'All',
                 placeholder = 'Select the country'
                 )], style = {'width':'100%', 'display':'inline-block'}),

                      html.Div(id = 'world-table-output')
                      ],style = {'height':'450px','text-align':'center'},xs = 12, sm = 12, md = 6, lg = 6, xl = 6)

             ])


    ],fluid = True)


############################## navigation bar ################################

header = dbc.Navbar( id = 'navbar', children = [


    html.A(
    dbc.Row([
        dbc.Col(html.Img(src = IMG, height = "70px")),
        dbc.Col(
            dbc.NavbarBrand("Covid-19 Vaccination Summary", style = {'color':'black', 'fontSize':'25px','fontFamily':'Times New Roman'}
                            )

            )


        ],align = "center",
        # no_gutters = True
        ),
    href = '/'
    ),
    
                dbc.Row(
            [
        dbc.Col(
        # dbc.Button(id = 'button', children = "Click Me!", color = "primary"), 
            dbc.Button(id = 'button', children = "Contact Us", color = "primary", className = 'ml-auto', href = '/')

            )        
    ],
            # add a top margin to make things look nice when the navbar
            # isn't expanded (mt-3) remove the margin on medium or
            # larger screens (mt-md-0) when the navbar is expanded.
            # keep button and search box on same row (flex-nowrap).
            # align everything on the right with left margin (ms-auto).
     className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
)
    # dbc.Button(id = 'button', children = "Support Us", color = "primary", className = 'ml-auto', href = '/')


    ])



app.layout = html.Div(id = 'parent', children = [ header,body_app])


#################################### Summary Table ####################### 

@app.callback(Output(component_id='world-table-output', component_property= 'children'),
              [Input(component_id='country-dropdown', component_property='value')])

def table_country(country):
    if country == 'All':
        df_final = df_to_use
    else:
        df_final = df_to_use.loc[df_to_use['COUNTRY'] == '{}'.format(country)]

    return dash_table.DataTable(
    data = df_final[['COUNTRY','TOTAL_VACCINATIONS','PERSONS_VACCINATED_1PLUS_DOSE','PERSONS_FULLY_VACCINATED']].to_dict('records'),
    columns = [{'id':c , 'name':c} for c in df_final[['COUNTRY','TOTAL_VACCINATIONS','PERSONS_VACCINATED_1PLUS_DOSE','PERSONS_FULLY_VACCINATED']].columns],
    fixed_rows = {'headers':True},

    sort_action = 'native',

    style_table = {
                   'maxHeight':'450px'
                   },

    style_header = {'backgroundColor':'rgb(224,224,224)',
                    'fontWeight':'bold',
                    'border':'4px solid white',
                    'fontSize':'12px'
                    },

    style_data_conditional = [

              {
                'if': {'row_index': 'odd',
                       # 'column_id': 'ratio',
                       },
                'backgroundColor': 'rgb(240,240,240)',
                'fontSize':'12px',
                },

            {
                  'if': {'row_index': 'even'},
                  'backgroundColor': 'rgb(255, 255, 255)',
                'fontSize':'12px',

            }

        ],

    style_cell = {
        'textAlign':'center',
        'fontFamily':'Times New Roman',
        'border':'4px solid white',
        'width' :'20%',
        # 'whiteSpace':'normal',
        # 'overflow':'hidden',
        'textOverflow': 'ellipsis',



        }

    # style_data

  )


if __name__ == "__main__":
    app.run_server()
