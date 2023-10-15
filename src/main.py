import datetime
import json
from flask import Flask
from flask import send_file
from flask import render_template
import sqlite3
from gradio_client import Client
from random import choice, randint

settings = json.load(open("settings.json"))
def extract(input_string):
    first_quote = input_string.find('"')
    last_quote = input_string.rfind('"')

    if first_quote != -1 and last_quote != -1:
        extracted_text = input_string[first_quote + 1:last_quote]
        return extracted_text
    else:
        return input_string
client = Client("https://ysharma-explore-llamav2-with-tgi.hf.space/--replicas/xwjz8/")

import os
from dotenv import load_dotenv
load_dotenv()
# Replace these with your own API keys and tokens
consumer_key = os.environ['api_key']
consumer_secret = os.environ['api_key_secret']
access_token = os.environ['access_token']
access_token_secret = os.environ['access_token_secret']
import requests
import json

# URL for making a tweet
url = "https://api.twitter.com/2/tweets"

# Data for the request body

# Create OAuth1a authorization header
from requests_oauthlib import OAuth1

auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)




app = Flask(__name__)

@app.route("/")
def index():
    con = sqlite3.connect("tweets.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM tweet")
    data = cur.fetchall()
    con.close()
    return render_template('index.html', tweets=data)


@app.route("/media/<filename>")
def media(filename=None):
    if filename!=None:
        return send_file('media/'+filename)
    else:
        return 'No file specified'
    
@app.route("/delete/<date>")
def delete(date=None):
    connection = sqlite3.connect('tweets.db')
    cursor = connection.cursor() # Replace with the value you're searching for
    cursor.execute("SELECT * FROM tweet WHERE date=?", (date,))
    item = cursor.fetchone()
    if item:
        item_id = item[0]  # Assuming the first column is the unique identifier (e.g., primary key)
        cursor.execute("DELETE FROM tweet WHERE date=?", (item_id,))
    connection.commit()
    connection.close()
    return 'Done!'

@app.route("/tweet/<date>")
def tweet(date=None):
    connection = sqlite3.connect('tweets.db')
    cursor = connection.cursor() # Replace with the value you're searching for
    cursor.execute("SELECT * FROM tweet WHERE date=?", (date,))
    item = cursor.fetchone()
    if item:
        item_id = item[0]  # Assuming the first column is the unique identifier (e.g., primary key)
        cursor.execute("DELETE FROM tweet WHERE date=?", (item_id,))
    connection.commit()
    connection.close()


    data = {
            "text": item[1]
        }
    response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(data), auth=auth)

    # Check the response
    if response.status_code == 201:  # HTTP status code 201 indicates a successful tweet
        print("Tweeted!")
        return "Tweet posted successfully!"
    else:
        print(f"No Tweet! {response.status_code}")
        return f"Failed to post tweet. Status code: {response.status_code}"


@app.route("/new")
def new():
    con = sqlite3.connect("tweets.db")
    cur = con.cursor()
    the_choice = choice(settings['prompts'])
    print(the_choice)
    result = client.predict(
            the_choice,	# str  in 'parameter_7' Textbox component
            settings["backstory"],	# str  in 'Optional system prompt' Textbox component
            randint(1,8)/10,	# int | float (numeric value between 0.0 and 1.0) in 'Temperature' Slider component
            280,	# int | float (numeric value between 0 and 4096) in 'Max new tokens' Slider component
            randint(3,8)/10,	# int | float (numeric value between 0.0 and 1) in 'Top-p (nucleus sampling)' Slider component
            1.2,	# int | float (numeric value between 1.0 and 2.0) in 'Repetition penalty' Slider component
            api_name="/chat"
    )
    print(extract(result))
    cur.execute(f"""
    INSERT INTO tweet VALUES
        ('{datetime.datetime.now().isoformat()}',"{extract(result).replace('"', "'")}")
""")
    con.commit()
    con.close()
    return 'Created!'

app.run(debug=True)