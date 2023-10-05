#base image
FROM python:3.9.18

#copy all files in dir to app folder
COPY . /app

#change working dir
WORKDIR /app

#install dependencies in requirements.txt
CMD pip install -r requirements.txt

#launch the app
streamlit run tweet_app.py

