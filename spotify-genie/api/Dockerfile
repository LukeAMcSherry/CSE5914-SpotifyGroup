FROM python:3.11

WORKDIR /app

RUN pip install flask Flask python-dotenv requests pandas numpy json spotipy spotipy.oauth2 yaml re tqdm multiprocessing time random datetime sklearn matplotlib

COPY . .

EXPOSE 17490

CMD ["flask", "run", "--no-debugger", "-h", "0.0.0.0", "-p", "17490"]