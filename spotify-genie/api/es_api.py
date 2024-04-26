import requests
import json
import es_fill

url = "https://localhost:9200/song/_doc/"
crt = "http_ca.crt"


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
    
def get_info(json_query):
    response = requests.get(url, params=json_query)

    if response.status_code == 201:
        print("Document gotten successfully.")
        return response.content
    else:
        print("Failed to get to document. Status code:", response.status_code)
        print("Response:", response.text)
        return 1


def find_best_25(thousand_songs, goal_sentiment):
    resulting_songs = []
    print(thousand_songs)
    for song in thousand_songs:
        json_query = {"query": {
            "match": {"track_uri": song.uri}
        }}
        str_query = json.dump(json_query)
        response = get_info(str_query)

        if (len(resulting_songs) < 25):
            resulting_songs.append(response)
        else:
            min_ind = -1
            min = 101
            for s in range(len(resulting_songs)):
                if abs(resulting_songs[s].sentiment - goal_sentiment) < min:
                    min_ind = s
                    min = abs(resulting_songs[s].sentiment - goal_sentiment)
            if abs(response.sentiment - goal_sentiment) < min:
                resulting_songs[min_ind] = response
    return resulting_songs
