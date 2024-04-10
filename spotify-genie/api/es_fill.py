import json
import csv 
import random
import es_api


with open('1M_unique_processed_data.csv') as file:
    random.seed('69420')
    heading = next(file) 

    reader_obj = csv.reader(file) 

    for row in reader_obj: 
        rnd = random.randint(0,100)
        query = json.dumps({ 
            "artist_name": row[0],
            "track_uri": row[1],
            "artist_uri": row[2],
            "track_name": row[3],
            "album_uri": row[4],
            "album_name": row[6],
            "sentiment": rnd,
        })
        es_api.enter_info(query)

