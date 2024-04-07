# Installation Instructions

To install and run Spotify Genie, ensure you have npm (https://docs.npmjs.com/downloading-and-installing-node-js-and-npm), Python (https://www.python.org/downloads/), and Docker Desktop (https://www.docker.com/products/docker-desktop/) installed.

Once installed, follow the below steps using exact order.

### Initial Setup
First, install the required packages for this project using npm. Yarn needs to be installed globally, but the rest can be installed automatically using our package definitions. 
From the repository's root folder, run the commands
```
cd spotify-genie
npm install -g yarn
npm install
```

Additionally, receive the processed dataset contained in the file `1M_unique_processed_data.csv`, sentiment model `sentiment_model.h5` and tokenizer `tokenizer.pickle`, from either the group's google drive or from a group member. Place that in the `api` folder. Then, replace the `acoustic` column name (in the top row) with the word `acousticness` in the dataset. Next, we can move onto spotify setup.

### Spotify Setup
To setup Spotify integration, you first need a Spotify for Developers (https://developer.spotify.com/) account. Create one, and then navigate to your dashboard (click on your SfD username to navigate to this). On your dashbord, click the "Create app" button. Edit your app to have a name and a description, as well as ensuring it is marked as a "Web API".

Next, on your Spotify for Developers app's dashboard, set your `Redirect URIs` to include the uri `http://localhost:3000/callback`. 

Finally, create a new file named `.env` in your `api` folder. Your `.env` file should include:
```
CLIENT_ID=[Your Spotify app's client ID (encase in single parentheses to make it a string literal)]
CLIENT_SECRET=[Your Spotify app's client secret (encase in single parentheses to make it a string literal)]
```

The required values should be in your Spotify for Developers app's page.

### Docker Setup

Run these commands in this order to setup Elasticsearch. When actually running Elasticsearch the first time, make sure to save the passwords and enrollment tokens it gives you.

```
docker network create elastic
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.12.2
docker run --name es01 --net elastic -p 9200:9200 -it -m 1GB docker.elastic.co/elasticsearch/elasticsearch:8.12.2
docker cp es01:/usr/share/elasticsearch/config/certs/http_ca.crt .
```

After saving your passwords and enrollment tokens, setup Kibana. Follow the link given by running Kibana and input your enrollment token, and then your elasticsearch password with username `elastic`.

```
docker pull docker.elastic.co/kibana/kibana:8.12.2
docker run --name kib01 --net elastic -p 5601:5601 docker.elastic.co/kibana/kibana:8.12.2
```

Next, add a new file named `.env` to your `spotify-genie` folder. Here are its contents- make sure to set your Elasticsearch and Kibana passwords to your given Elasticsearch password!

```
ELASTIC_PASSWORD=[Your given password]
KIBANA_PASSWORD=[Your given password]
STACK_VERSION=8.12.2
ES_PORT=127.0.0.1:9200
# Set the cluster name
CLUSTER_NAME=docker-cluster

# Set to 'basic' or 'trial' to automatically start the 30-day trial
LICENSE=basic
#LICENSE=trial

# Port to expose Elasticsearch HTTP API to the host
ES_PORT=9200
#ES_PORT=127.0.0.1:9200

# Port to expose Kibana to the host
KIBANA_PORT=5601
#KIBANA_PORT=80

# Increase or decrease based on the available host memory (in bytes)
MEM_LIMIT=1073741824
```

### Run Spotify Genie

Upon setup, running `docker-compose up -d`, and then `yarn run` should start Spotify Genie!
