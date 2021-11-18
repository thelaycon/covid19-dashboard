import itertools
import bs4
import requests
import numpy as np
import pandas as pd



def get_covid_news():
    req = requests.get("https://covid19.ncdc.gov.ng/report/")
    soup = bs4.BeautifulSoup(req.text, "html.parser")
    feed_card = soup.find_all("div", "card feed-card")
    feed_card = feed_card[0]
    list_tags = feed_card.find_all("li")
    covid_news = [news.text for news in list_tags]
    covid_news = [news + "." for news in covid_news if not news.endswith(".")]
    return covid_news


def get_top_five_states(list_):
    
    def is_state(state):
        try:
            int(state)
        except:
            return True

    return list(filter(is_state, list_))[0:5]


def get_top_five_states_data(list_):

    def is_digit(raw):
        try:
            int(raw)
            return True
        except:
            return False

    #Split list into even parts with 5 elements
    splitted = np.split(np.array(list_), len(list_)/5)
    splitted = [list(arr) for arr in splitted][0:5]
    figures = [list(filter(is_digit, arr)) for arr in splitted]
    figures = [list(map(int, arr)) for arr in figures]
    confirmed = [x[0] for x in figures]
    admission = [x[1] for x in figures]
    discharged = [x[2] for x in figures]
    deaths = [x[3] for x in figures]
    cleaned_data = {"confirmed":confirmed, "admission":admission, "discharged":discharged, "deaths":deaths}
    return cleaned_data


def get_ncdc_data():
    req = requests.get("https://covid19.ncdc.gov.ng/report/")
    soup = bs4.BeautifulSoup(req.text, "html.parser")
    tbody = soup.find("tbody")
    tr = tbody.find_all("tr")
    td = itertools.chain.from_iterable([x.find_all("td") for x in tr])
    raw_data = [x.text.strip().replace(",","") for x in td]
    top_states = get_top_five_states(raw_data)
    figures = get_top_five_states_data(raw_data)
    return (top_states, figures)


def get_death_series(year=0):
    df = pd.read_csv("https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
    df = df[df["Country/Region"] == "Nigeria"]
    df = df.filter(regex="[012]$")
    if year != 0:
        df = df.filter(regex=f"[{year}]$")
    return df.columns, df.values[0]


def get_confirmed_series(year=0):
    df = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
    df = df[df["Country/Region"] == "Nigeria"]
    df = df.filter(regex="[012]$")
    if year != 0:
        df = df.filter(regex=f"[{year}]$")
    return df.columns, df.values[0]


def get_recovered_series(year=0):
    df = pd.read_csv("https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")
    df = df[df["Country/Region"] == "Nigeria"]
    df = df.filter(regex="[012]$")
    if year != 0:
        df = df.filter(regex=f"[{year}]$")
    return df.columns, df.values[0]


