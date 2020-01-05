#!/usr/bin/env python
# coding: utf-8


#Importing my modules necessary for this analysis: Requests to get the data from the SMK API, 
# Pandas for dataframe analysis and Json formatting, numpy for potential mathematical methods 
import requests

import pandas as pd

from pandas.io.json import json_normalize

#My Url key for search: "jesus" with 200rows under the "response variabel"
api_search_url = 'https://api.smk.dk/api/v1/art/search/?keys=jesus&filters=&offset=0&rows=200&lang=en'

response = requests.get(api_search_url)

json = response.json()

#Cookie cutter Json flatter code. 
def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


dic_flattened = [flatten_json(d) for d in json['items']]
df= json_normalize(dic_flattened)

#Printing the shape and size of my dataframe
print("The shape of my Dataframe is: "+ str(df.shape))
print("The size of my Dataframe is: "+ str(df.size))


#Different attributes of my data
df.dtypes

#Dropping irrelevant rows. If each row doesn't have more than 150 non NaN elements it's not included
df.dropna(axis = 1, thresh = 150, inplace = True)


#Making a new dataframe consisting of my chosen topics
reformed_data = df[["acquisition_date_precision","dimensions_0_value","dimensions_1_value", "number_of_parts"]]

#Cutting off the first four indexes of "acquisition_date_precision" since im only interested in the specfic year. 
reformed_data.loc[:,"acquisition_date_precision"] = reformed_data["acquisition_date_precision"].str[:4]

#Logging my current Dataframe
reformed_data

#Printing out my findings
date_count = reformed_data.acquisition_date_precision.value_counts(normalize=True);
n_of_parts_count = reformed_data.number_of_parts.value_counts(normalize=True);
height_count = reformed_data.dimensions_0_value.value_counts(normalize=True);
width_count = reformed_data.dimensions_1_value.value_counts(normalize=True);

print("Most frequent year for the acquirement of 'Jesus' related artworks:\n", date_count)
print("\n\n")
print("The most frequent amount of parts for 'Jesus' related artworks:\n", n_of_parts_count)
print("\n\n")
print("The most frequent height of painting for 'Jesus' related artworks in milimeters:\n", height_count)
print("\n\n")
print("The most frequent width of painting for 'Jesus' related artworks in milimeters:\n", width_count)

#Creating Dataframes suitable for the graph module. 
graph_suitable_1 = pd.DataFrame(reformed_data['acquisition_date_precision'].value_counts().reset_index().values, columns=['Acquisition_Date', "N"])
graph_suitable_2 = pd.DataFrame(reformed_data['dimensions_0_value'].value_counts().reset_index().values, columns=['Average Height', "N"])

import altair as alt

#Creating a bar graph inserting Acquisition_Date as the x axis, and N (count) as the y axis. Width and height are set aswell. 
alt.Chart(graph_suitable_1).mark_bar().encode(
    x = alt.X("Acquisition_Date", axis=alt.Axis(format = "c", title="Acquisition_Date")),
    y = alt.Y("N", axis=alt.Axis(format = "c", title="Number of acquiered Jesus related artworks")),
).properties(width = 900, height = 300)