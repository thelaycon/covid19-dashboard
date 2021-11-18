import base64
from webkage.application import App
from webkage.http_response import load, response
import plotly.graph_objects as go
import fetch 



#Fetch fetch from JHU CCSE
def get_covid_data(year=0):
    x_confirmed, y_confirmed = fetch.get_confirmed_series()
    x_death, y_death = fetch.get_death_series()
    x_recovered, y_recovered = fetch.get_recovered_series()

    covid_data = {
           "x_confirmed":x_confirmed,
           "y_confirmed":y_confirmed,
           "x_recovered":x_recovered,
           "y_recovered":y_recovered,
           "x_death":x_death,
           "y_death":y_death,
           }
    return covid_data


def home(ctx):
    current_data = get_covid_data()
    covid_news = fetch.get_covid_news()
    top_states, figures = fetch.get_ncdc_data()

    #Plot area plots
    fig = go.Figure()
    x_confirmed, y_confirmed = current_data["x_confirmed"], current_data["y_confirmed"]
    x_death, y_death = current_data["x_death"], current_data["y_death"]
    x_recovered, y_recovered = current_data["x_recovered"], current_data["y_recovered"]
    fig.add_trace(go.Scatter(name="Confirmed", x=x_confirmed, y=y_confirmed, fill="tonexty"))
    fig.add_trace(go.Scatter(name="Deaths", x=x_death, y=y_death, fill="tozeroy"))
    fig.add_trace(go.Scatter(name="Recovered", x=x_recovered, y=y_recovered, fill="tozeroy"))
    fig.update_layout(
            title={
        'text': "JHU Time Series",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
            xaxis_title = "Date",
            yaxis_title = "Count",
           showlegend = True,
           font=dict(
               family="Courier New, monospace",
               size=18,
               color="RebeccaPurple"
               )
           )
    area_plot = fig.to_html(full_html=False, include_plotlyjs=False)

    #Plot bar charts
    fig = go.Figure(
            data=[
                go.Bar(name="Confirmed", x=top_states, y=figures["confirmed"]),
                go.Bar(name="Admission", x=top_states, y=figures["admission"]),
                go.Bar(name="Discharged", x=top_states, y=figures["discharged"]),
                go.Bar(name="Deaths", x=top_states, y=figures["deaths"]),
                ]
            )
    fig.update_layout(
            title={
        'text': "NCDC Daily Updates",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
            xaxis_title = "Top Affected States",
            yaxis_title = "Count",
            showlegend=True,
            barmode="stack",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="RebeccaPurple"
                ),
            )
    bar_plot = fig.to_html(full_html=False, include_plotlyjs=False)
    data = {"area_plot":area_plot, "bar_plot":bar_plot, "covid_news":covid_news}
    data = load("home.html",data=data)
    return response(ctx, "200", data)


dash = App
dash.add_path("/",home)
dash.set_static("/static/", "assets")
wsgi = dash.wsgi
