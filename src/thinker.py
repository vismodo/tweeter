
import time
from gradio_client import Client
from random import choice, randint
import sqlite3
from time import sleep
import datetime
import json
con = sqlite3.connect("tweets.db")
cur = con.cursor()
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
while True:
    print("\n\n")
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
    print("\n")
    time.sleep(settings['timeInterval'])