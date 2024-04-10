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
        print("Document posted to successfully.")
        return response.content
    else:
        print("Failed to post to document. Status code:", response.status_code)
        print("Response:", response.text)
        return 1



