FROM python:3.11

WORKDIR /app

RUN pip install flask Flask python-dotenv requests flask_cors pandas spotipy pyyaml regex tqdm scikit-learn 

COPY . .

EXPOSE 17490

CMD ["flask", "run", "--no-debugger", "-h", "0.0.0.0", "-p", "17490"]