import argparse, os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import folium

#
# USAGE: `python3 render.py -i input.csv -o [output.html]`
#

parser = argparse.ArgumentParser(description='Processes an election result CSV file and outputs a HTML proportional bubble map of candidate victory margins.')
parser.add_argument('-i', '--infile', type=argparse.FileType('r'), help='input file, in CSV format', required=True)
parser.add_argument('-o', '--outfile', type=argparse.FileType('w'), help='output file, in HTML format')
#parser.add_argument("input_csv", ..., required=True)

args = parser.parse_args()

input_csv = args.infile.name

if not args.outfile:
    output_html = 'out.html'
else:
    output_html = args.outfile.name


def gen_color_dict(candidates, colors):
    color_dict = {}

    i=0
    for cand in candidates:
        color_dict[cand] = colors[i]
        i = i + 1
    return color_dict

def pre_process_map_data(raw_df):
    map_data = pd.DataFrame({
    'label':[],
    'lat':[],
    'lon':[],
    'cand_name':[],
    'margin':[],
    'popup_html': []
    })


    i=0
    for index, row in df.iterrows(): #Populates map_data row by row
        i = i + 1
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

        popup_text = """
            <h6>%s</h6>
            %s"""

        popup_text = popup_text %(metadata[0], votes_sorted.to_string().replace('\n', '<br>'))

        new_row = {'label': metadata[0],
                    'lat': float(location[0]),
                    'lon': float(location[1]),
                    'cand_name': win_candidate_name,
                    'margin': candidate_margin,
                    'popup_html': popup_text}

        map_data = map_data.append(new_row, ignore_index=1)
    return map_data

#plots points from map_data on the candidate map
#cand_map is a folium map initialized at the mean value of points to be plotted
def plot_points(cand_map, map_data):
    for i in range(0,len(map_data)):
        circle_color = color_dict[map_data.iloc[i]['cand_name']]

        folium.CircleMarker(
        location=[map_data.iloc[i]['lat'], map_data.iloc[i]['lon']],
        popup=map_data.iloc[i]['popup_html'],
        radius=map_data.iloc[i]['margin'] / 4,
        color=circle_color,
        fill_color=circle_color,
        fill=True,
        fill_opacity = .4,
        weight = 0).add_to(cand_map)

    return cand_map

#set up read file TODO file integrity/format check
df=pd.read_csv(input_csv, sep=',')

#assign each candidate a color
num_candidates = len(df.columns)
candidates = df.columns[2:].values
colors = ['red', 'dodgerblue', 'limegreen', "darkorange", 'm', "slategray"]

color_dict = gen_color_dict(candidates, colors)

map_data = pre_process_map_data(df)

#TODO generate coordinates and zoom. Die Hardcoded stuff!!
m = folium.Map([44.976217, -93.263540], zoom_start=12.3)
f = folium.map.FeatureGroup()


map = plot_points(m, map_data)

m.save(output_html)
