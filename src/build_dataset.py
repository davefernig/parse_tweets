from __future__ import division

# nltk imports
from nltk.tokenize import TweetTokenizer

# numpy, scipy, sklearn, and pandas imports
import pandas as pd
import numpy as np

# other imports
from collections import defaultdict
import json, re

"""Script to build a csv file of tweet counts by state from a collection
of tweets in JSON format
"""

"""
Params
"""

tables_path = '/home/dave/projects/twitter_data/tables' # Path to tables
output_path = '/home/dave/projects/twitter_data/output' # Path to output
tweet_file = 'example.json'
"""
Constants
"""

# Geographical Locations
places = pd.read_csv(tables_path + '/POP_PLACES_20151201.txt', delimiter='|')
cities = [city.lower() for city in list(places['FEATURE_NAME'])]
states = [state.lower() for state in list(places['STATE_ALPHA'])]
lats, lons = list(places['PRIM_LAT_DEC']), list(places['PRIM_LONG_DEC'])
places = dict(zip(zip(cities, states), zip(lats, lons)))

# Population Data
state_alpha, population = pd.read_csv('state_alpha.csv'), {}
state_alpha = dict( zip( [n.strip() for n in list(state_alpha.name)], 
                         [c.strip() for c in list(state_alpha.code)]))

pop_table = pd.read_csv(tables_path + '/NST-EST2014-01.csv', delimiter=',')
for row in pop_table.iterrows():
    if row[1][0] in state_alpha:
        population[state_alpha[row[1][0]]] = int(re.sub('[^0-9]','', row[1][1]))

# tweet tokenizer
tokenizer = TweetTokenizer(preserve_case=False)

"""
Functions
"""


def parse_tweet(data):

    tweet = json.loads(data)

    try:
        name = tweet['user']['name'].split()[0].lower()
    except:
        name = None

    loc = None
    try:
        loc = tuple([s.encode('ascii', 'ignore').strip()
                     for s in tweet['user']['location'].lower().split(',')])
    except:
        pass

    try:
        loc = tuple([s.encode('ascii', 'ignore').strip()
                     for s in tweet['place']['full_name'].lower().split(',')])
    except:
        pass

    try:
        state = loc[1]
        coords = places[loc]
    except:
        state = coords = None

    try:
        user_id = tweet['user']['id']
    except:
        user_id = None

    try:
        text = tokenizer.tokenize(tweet['text'])
    except:
        text = None

    retweeted = 'retweeted_status' in tweet

    return name, loc, state, coords, user_id, text, retweeted


if __name__ == '__main__':

    state_totals, geo_totals = defaultdict(set), defaultdict(set)
    fName = output_path + '/tweets/' + tweet_file

    with open(fName) as f:

        place_count, location_count = 0, 0

        for line in f:

            name, loc, state, coords, user_id, text, retweeted = parse_tweet(line)

            if state and state in population:
                state_totals[state].add(user_id)

            if coords:
                geo_totals[coords].add(user_id)

    with open(output_path + '/analysis/'+tweet_file.strip('.json')+'_states.csv', 'w') as f:
        for state in state_totals:
 
            line = state.upper() + ',' + \
                   str(len(state_totals[state]) / population[state]) + '\n'

            f.write(line)

    with open(output_path + '/analysis/'+tweet_file.strip('.json')+'_points.csv', 'w') as f:
        for point in geo_totals:
 
            line = str(point[0]) + ',' + str(point[1]) + ',' + \
                   str(len(geo_totals[point])) + '\n'

            f.write(line)
