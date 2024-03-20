import os
import pandas as pd
import numpy as np
import json
import spotipy
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyOAuth,SpotifyClientCredentials
import yaml
import re
from tqdm import tqdm
import multiprocessing as mp
import datetime
import csv as csv
import random
import time
from datetime import datetime

def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if isinstance(x, dict):
            for a in x:
                flatten(x[a], name + a + '_')
        elif isinstance(x, list):
            for i, a in enumerate(x):
                flatten(a, name + str(i) + '_')
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


# function to divide a list of uris (or ids) into chuncks of 50.
chunker = lambda y, x: [y[i : i + x] for i in range(0, len(y), x)]

list_of_ids = []

with open('/Users/alex/Documents/CSE-5914/CSE5914-SpotifyGroup/output.csv', 'r') as file:
        
    csv_reader = csv.reader(file)
    
    # Iterate over each row in the CSV file
    for row in csv_reader:
        list_of_ids.append(row[0])


# using the function
uri_chunks = chunker(list_of_ids, 50)

# initialize connection to spotify to pull data
stream= open("spotify.yaml")
spotify_details = yaml.safe_load(stream)
auth_manager = SpotifyClientCredentials(client_id=spotify_details['Client_id'],
                                        client_secret=spotify_details['client_secret'])
sp = spotipy.client.Spotify(auth_manager=auth_manager)

with open('album_output'+str(datetime.now())+'.json', 'w', newline='') as writing_file:

    print("Set up everything prior to actually attempting to run chunks.")       
        
    chunk_counter = 0   
    for chunk in uri_chunks:
        
        # counter_format = {)}
        # json.dump(counter_format, writing_file, indent = 4)
        
        # attempt to pull and dump the information into the file
        # otherwise logs the error
        try:
            track_info = sp.tracks(chunk)
            track_info["iteration number"] = chunk_counter
            json.dump(track_info, writing_file, indent = 4)
            print('Completed round '+str(chunk_counter))
        except Exception as e:
            json.dump("Error:"+str(e), writing_file)    
            json.dump(track_info, writing_file)
            json.dump("Died on "+str(chunk_counter), writing_file)
            print('ERROR on round '+str(chunk_counter))

        # sleep for random "unpredictable" amount of time, hopefully prevents api being blocked by spotify
        time.sleep(random.randint(15, 30))
        
        chunk_counter += 1
        
# This was redundant. The million playlist dataset already contains all the album names we'll need. Just need to parse through it. f##k
