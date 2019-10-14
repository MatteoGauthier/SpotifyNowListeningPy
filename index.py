import inspect
import argparse
import os
from flask import Flask, jsonify
import spotipy
import json
from colorama import Back, Fore, Style, deinit, init
import spotipy.util as util
from flask_limiter.util import get_remote_address
from flask_limiter import Limiter
from datetime import datetime, timedelta
import sys
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address)
init()


parser = argparse.ArgumentParser()
parser.add_argument('-prod', action='store_true', default=False,
                    dest='boolean_switch',
                    help='Set a switch to true')
args = parser.parse_args()
timer = 0

client_id = os.getenv("client_id_spot")
client_secret = os.getenv("client_secret_spot")
redirect_uri = "http://localhost:8080/redirect"

scope = 'user-library-read user-read-currently-playing user-top-read playlist-modify-public user-follow-read'
print(sys.argv)
if len(sys.argv) >= 1:
    username = '5biqzzeq4srnrc8cohnlfw0t1'
    # mood = float('5biqzzeq4srnrc8cohnlfw0t1')
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()

if (args.boolean_switch):
    token = os.environ['SP_TOKEN']
else:
    token = util.prompt_for_user_token(
        username, scope, client_id, client_secret, redirect_uri)


nowTime = datetime.now()
print(nowTime)
progress = datetime.now()
period = datetime.now()


goal = nowTime - timedelta(days=10)
lastdata = 'None'


def fetchSpot():
    global goal
    global lastdata
    print('52', goal)
    if token:
        print(Fore.GREEN, 'Token Trouvé\n')
        sp = spotipy.Spotify(auth=token)
        data = sp.currently_playing()
        lastdata = data
        # if (goal <= datetime.now()):
        #     print(Fore.BLUE, 'goal est supérieur à la date dauj')
        #     print('Hey 57')
        #     goal = timedelta(milliseconds=data['item']['duration_ms']) - timedelta(
        #         milliseconds=data['progress_ms']) + datetime.now()
        #     print('60 le goal me',goal)
        #     print('61 date timle', datetime.now())
        #     lastdata = data
        #     return data
    return lastdata
    # region
    # duration = data.item.duration_ms
    # print(data['progress_ms'])
    # print(data['item']['duration_ms'])
    # progress = datetime.now() + timedelta(milliseconds=data['progress_ms'])
    # print(progress)
    # finish = datetime.now() + timedelta(milliseconds=data['item']['duration_ms'])
    # print(finish)

    # progressms = data.progress_ms
    # print(progress)
    # next_time = datetime.now() + period

    # if (progress >= finish):
    #     print('fini')
    # endregion


@app.route('/', methods=['GET'])
@limiter.limit("1 per minute", error_message='cc')
def index():
    return fetchSpot()


@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify(lastdata), 429


if __name__ == '__main__':
    app.run(host='localhost', port=8080)
