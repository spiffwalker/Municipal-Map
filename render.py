import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import folium

#TODO support file input/output on command line

#set up read file
df=pd.read_csv('examples/MPLS Mayor.csv', sep=',')
coordinates_dataframe = df['Location']
coord_array = coordinates_dataframe.str.split(',', expand=True)

#TODO file integrity/format check

#assign each candidate a color
num_candidates = len(df.columns)

candidates = df.columns[2:].values
colors = ['red', 'dodgerblue', 'limegreen', "darkorange", 'm', "slategray"]

f = folium.map.FeatureGroup()

#TODO generate coordinates and zoom. Die Hardcoded stuff!!
m = folium.Map([44.976217, -93.263540], zoom_start=12.3)

i=0
for index, row in df.iterrows():
    i = i + 1
    print(row[2])
    metadata = row[0:2]
    votes_sorted = row[2:].sort_values(ascending = False)
    total_votes = sum(votes_sorted)

    #check if location NULL
    if type(metadata[1]) is not str:
        continue
    try:
        location = str.split(metadata[1], ',')
    except TypeError as e:
        continue

    #candidate w/ most votes
    # TODO account for ties

    area_winner = votes_sorted[0:1]
    win_candidate_name = area_winner.index[0]
    win_candidate_votes = area_winner[0]
    second_place_votes = votes_sorted[1]

    if win_candidate_votes is 0:
        continue

    candidate_margin = win_candidate_votes - second_place_votes


    x0 = float(location[1])
    y0 = float(location[0])

    print("x=" + str(x0) + ", y=" + str(y0))

    candidate_index = np.where(candidates == win_candidate_name)[0][0]

    popup_text = """
        <h6>%s</h6>
        %s"""

    popup_text = popup_text %(metadata[0], votes_sorted.to_string().replace('\n', '<br>'))

    folium.CircleMarker(
    location = [y0, x0],
    radius = candidate_margin / 4,
    popup = popup_text,
    color = colors[candidate_index],
    fill_color = colors[candidate_index],
    fill_opacity = .4,
    fill = True,
    weight = 0
).add_to(m)

m.save('examples/folium.html')
