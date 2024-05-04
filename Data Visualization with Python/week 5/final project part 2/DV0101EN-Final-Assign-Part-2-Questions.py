import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Statistics Dashboard"

# Create the layout of the app
app.layout = html.Div(children=[
    # Add title to the dashboard
    html.H1('Automobile Statistics Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 26}),

    # Add dropdown menus
    html.Div([
        html.Label("Select Report Type:", style={'fontSize': 18}),
        dcc.Dropdown(
            id='dropdown-report-type',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            value='Yearly Statistics',
            style={'width': '50%', 'margin': '10px'}
        ),
    ], style={'columnCount': 2, 'textAlign': 'center'}),

    html.Div([
        html.Label("Select Year:", style={'fontSize': 18}),
        dcc.Dropdown(
            id='dropdown-year',
            options=[{'label': year, 'value': year} for year in data['Year'].unique()],
            value=data['Year'].min(),
            style={'width': '50%', 'margin': '10px'}
        ),
    ], style={'columnCount': 2, 'textAlign': 'center'}),

    # Add a division for output display
    html.Div(id='output-container', className='chart-grid', style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'center'})
])


# Define the callback function to update the output container based on the selected report type and year
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-report-type', component_property='value'),
     Input(component_id='dropdown-year', component_property='value')]
)
def update_output_container(selected_report_type, selected_year):
    if selected_report_type == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]

        # Plot 1: Average Automobile sales during the recession
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        chart1 = dcc.Graph(
            figure=px.line(yearly_rec, x='Year', y='Automobile_Sales',
                           title="Average Automobile Sales during Recession Period")
        )

        # Plot 2: Average number of vehicles sold by vehicle type during recession
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        chart2 = dcc.Graph(
            figure=px.bar(average_sales, x='Vehicle_Type', y='Automobile_Sales',
                          labels={'Automobile_Sales': 'Average Number of Vehicles Sold'},
                          title='Average Vehicles Sold by Vehicle Type during Recession')
        )

        # Plot 3: Total expenditure share by vehicle type during recession
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        chart3 = dcc.Graph(
            figure=px.pie(exp_rec, values='Advertising_Expenditure', names='Vehicle_Type',
                          title="Total Advertising Expenditure Share by Vehicle Type during Recession")
        )

        return [html.Div(chart1), html.Div(chart2), html.Div(chart3)]

    elif selected_report_type == 'Yearly Statistics':
        # Filter the data for the selected year
        yearly_data = data[data['Year'] == selected_year]

        # Plot 1: Yearly Average Automobile sales for the whole period
        chart1 = dcc.Graph(
            figure=px.line(yearly_data, x='Year', y='Automobile_Sales',
                           title="Yearly Average Automobile Sales")
        )

        # Plot 2: Total Monthly Automobile sales for the selected year
        chart2 = dcc.Graph(
            figure=px.line(yearly_data, x='Month', y='Automobile_Sales', color='Year',
                           title="Total Monthly Automobile Sales for {}".format(selected_year))
        )

        # Plot 3: Average Monthly Automobile sales of each vehicle type for the selected year
        avr_vdata = yearly_data.groupby(['Month', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        chart3 = dcc.Graph(
            figure=px.bar(avr_vdata, x='Month', y='Automobile_Sales', color='Vehicle_Type',
                          title='Average Monthly Automobile Sales by Vehicle Type for {}'.format(selected_year))
        )

        # Plot 4: Total Advertisement Expenditure for each vehicle for the selected year
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        chart4 = dcc.Graph(
            figure=px.pie(exp_data, values='Advertising_Expenditure', names='Vehicle_Type',
                          title="Total Advertising Expenditure for Each Vehicle in {}".format(selected_year))
        )

        return [html.Div(chart1), html.Div(chart2), html.Div(chart3), html.Div(chart4)]

    else:
        return None


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
