import json
import csv 
import random
import threading
import time
import requests
import json

url = "https://localhost:9200/song/_doc/"
crt = "http_ca.crt"

running = 0

def run_thread(q, id):
    global running
    enter_info(q, id)
    running -= 1

def enter_info(json_data, id):
    url_to_use = url + str(id)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=json_data, verify=False, headers=headers, auth=("elastic", "4vlAqTiZw31UapG8IH8D") )

    if response.status_code == 201:
        print("Document posted to successfully.")
        return 0
    else:
        print("Failed to post to document. Status code:", response.status_code)
        print("Response:", response.text)
        return 1

with open('1M_unique_processed_data.csv') as file:
    random.seed('69420')
    heading = next(file) 

    reader_obj = csv.reader(file) 
    i = 1
    
    for row in reader_obj: 
        rnd = random.randint(0,100)
        query = { 
            "artist_name": row[0],
            "track_uri": row[1],
            "artist_uri": row[2],
            "track_name": row[3],
            "album_uri": row[4],
            "album_name": row[6],
            "sentiment": rnd,
        }
        x = threading.Thread(target=run_thread, args=(query, i))
        while running > 10:
            time.sleep(0.001)
        running += 1
        x.start()
        i += 1

