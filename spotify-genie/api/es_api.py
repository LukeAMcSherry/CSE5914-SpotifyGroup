import requests
import json

url = "http://localhost:9200/song/_doc/1"


def enter_info(json_data):
    response = requests.post(url, json=json_data)

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
        print("Document posted to successfully.")
        return response.content
    else:
        print("Failed to post to document. Status code:", response.status_code)
        print("Response:", response.text)
        return 1



