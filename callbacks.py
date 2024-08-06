import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Output, Input
from etl import get_data
from datetime import datetime as dtime

#genre=get_data('genres')
invoice=get_data('invoice')#.query("country in ('USA', 'Germany', 'France')")

min_date=invoice['invoice_date'].min()
max_date=invoice['invoice_date'].max()
years=invoice.sort_values(by='invoice_date')['invoice_date'].dt.year.unique().tolist()

slider_block=html.Div(
    children=[
        html.H2('Slider', style={'display':'inline-block'}),
        html.Div(
            dcc.RangeSlider(
                id='range_slider',
                min=years[0],
                max=years[-1],
                step=1,
                value=[2022,2024],
                marks={y:str(y) for y in years}
            ),
        )
    ]
)

date_picker_block=dcc.DatePickerRange(
    id='date_prange',
    min_date_allowed=min_date,
    max_date_allowed=max_date,
    #initial_visible_month=max_date,
)

dropdown_block=dcc.Dropdown(
    id='country_dd',
    options=[
        {'label':c, 'value':c} for c in invoice['country'].sort_values().unique().tolist()
    ],
    style={'margin-top':'20px', 'width':'50%'}
)

app=dash.Dash(__name__)
server=app.server

app.layout=html.Div([html.Div(
    children=[
        html.H1('Information on track sales', style={'text-align':'center'}),
        html.Div(
            children=[
                slider_block,
                date_picker_block,
                dropdown_block
            ],
            style={'width':'50%'}
        ),
        html.Div(
            children=[
                dcc.Graph(id='bar_fig', style={'width':'50%', 'display':'inline-block'}),
                dcc.Graph(id='tracks_fig', style={'width':'50%', 'display':'inline-block'})
            ]
        )
    ]
)]
)

@app.callback(
        Output(component_id='date_prange', component_property='start_date'),
        Output(component_id='date_prange', component_property='end_date'),
        Input(component_id='range_slider', component_property='value')
)
def update_drange(value):
    start_date=min_date.year
    end_date=min_date.year

    if value:
        start_date=dtime(value[0], 1, 1)
        end_date=dtime(value[1], 12, 31)
    return str(start_date), str(end_date)


@app.callback(
    Output(component_id='bar_fig', component_property='figure'),
    Output(component_id='tracks_fig', component_property='figure'),
    Input(component_id='date_prange', component_property='start_date'),
    Input(component_id='date_prange', component_property='end_date'),
    Input(component_id='country_dd', component_property='value')
)
def update_plot(start_date, end_date, selected_country):
    sdate=invoice['invoice_date'].min()
    edate=invoice['invoice_date'].max()
    country_filter='All Countries'
    sales=invoice.copy(deep=True)
    tracks=invoice.copy(deep=True)

    if selected_country:
        country_filter=selected_country
        sales=sales.query(f"country=='{country_filter}'")#.groupby('monthkey', as_index=False)['total'].sum()
        tracks=tracks.query(f"country=='{country_filter}'")#.groupby('monthkey', as_index=False)['tracks_cnt'].sum()
    if start_date and end_date:
        sdate=start_date
        edate=end_date
        sales=sales[(sales['invoice_date']>=sdate)&(sales['invoice_date']<=edate)]#.sort_values(by='monthkey', ascending=False)
    bar_fig=px.line(
        data_frame=sales,
        x='invoice_date',
        y='total',
        #hover_data='country',
        #color=sales['monthkey'].astype('str'),
        #color_discrete_map={f'{m}':'green' for m in sales['monthkey'].unique().tolist()}
    )
    tracks_fig=px.bar(
        data_frame=tracks.sort_values(by='invoice_date'),
        x='monthkey',
        y='tracks_cnt'
    )
    #bar_fig.update_layout({'xaxis':{'type':'category'}})
    bar_fig.update_layout(showlegend=False)
    tracks_fig.update_layout({'xaxis':{'type':'category'}})
    bar_fig.update_layout({'title':{'text':f'Sales for {country_filter}', 'font':{'weight':'bold'}}})
    tracks_fig.update_layout({'title':{'text':f'Sold tracks count for {country_filter}', 'font':{'weight':'bold'}}})
    return bar_fig, tracks_fig 


if __name__=='__main__':
    app.run_server(debug=True)
