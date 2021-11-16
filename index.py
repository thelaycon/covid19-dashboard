from webkage.application import App
from webkage.http_response import load, response
import plotly.express as px
import numpy as np
import data 



#Fetch data from JHU CCSE
def get_covid_data(year=0):
    x_confirmed, y_confirmed = data.get_confirmed_series()
    x_death, y_death = data.get_death_series()
    x_recovered, y_recovered = data.get_recovered_series()

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
    x_confirmed, y_confirmed = current_data["x_confirmed"], current_data()["y_confirmed"]
    x_death, y_death = current_data["x_death"], current_data()["y_death"]
    x_recovered, y_recovered = current_data["x_recovered"], current_data()["y_recovered"]
    if ctx.request["method"] == "POST":
        graph_type = ctx.form["type"]
        if graph_type == "bar":
            fig = px.bar(x=x_confirmed, y=y_confirmed)
    fig = px.scatter(x=x_confirmed, y=y_confirmed)
    graph1 = fig.to_html(full_html=False)
    fig = px.scatter(x=x_death, y=y_death)
    graph2 = fig.to_html(full_html=False)
    fig = px.scatter(x=x_recovered, y=y_recovered)
    graph3 = fig.to_html(full_html=False)
    d = {"graph1":graph1, "graph2":graph2, "graph3":graph3}
    graph = load("home.html",data=d)
    return response(ctx, "200 Success", graph)



dash = App
dash.add_path("/",home)
dash.set_static("/static/", "assets")
dash.serve()
