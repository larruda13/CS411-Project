import json
from flask import Flask, request, redirect, session, render_template, url_for, make_response, flash
import requests
import base64
import urllib.parse
import uuid
from apiclient import discovery
from oauth2client import client
import httplib2
import os
import sys
from apiclient.errors import HttpError
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

#-----------------------------------------------------------------------------------------------#
"""
app.py
Purpose: This is the guts of our web app. In particular, this is the backend of the project.
Boston University CS411 - Software Engineering
Originally written by: Jiayuan Zheng
Edited by: Jennifer Tsui (12-1-16; added '/oauth2callback' and '/youtube' approutes, added
                          authentication json files)
           Jiayuan Zheng (12-2-16; added '/spotifyplaylist' updated '/youtube' approutes)
"""
#-----------------------------------------------------------------------------------------------#
app = Flask(__name__)



# Client side
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 8080

with open('auth.json') as data_file:
    auth = json.load(data_file)

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the {{ Google Cloud Console }} at
# {{ https://cloud.google.com/console }}.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secrets.json"
with open(CLIENT_SECRETS_FILE) as data_file:
    client_secr = json.load(data_file)

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0
To make this sample run you will need to populate the client_secrets.json file
found at:
   %s
with information from the {{ Cloud Console }}
{{ https://cloud.google.com/console }}
For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

#  Client Keys
SP_CLIENT_ID = auth['services']['spotify']['client_id']
SP_CLIENT_SECRET = auth['services']['spotify']['client_secret']

YT_CLIENT_ID = client_secr['web']['client_id']
YT_CLIENT_SECRET = client_secr['web']['client_secret']


# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
SP_API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, SP_API_VERSION)

#YouTube URLS
#YOUTUBE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_TOKEN_URL = ""
YOUTUBE_API_BASE_URL = "GET https://www.googleapis.com/youtube"
#YOUTUBE_API_URL = "{}/{}".format(YOUTUBE_API_BASE_URL,YT_API_VERSION)
YOUTUBE_CALLBACK = "callback"


# Spotify Server-side Parameters

SP_REDIRECT_URI = "{}:{}/spotify/callback/q".format(CLIENT_SIDE_URL, PORT)
SP_SCOPE = "playlist-modify-public playlist-modify-private"
SP_STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

#YouTube Server-side Parameters
YT_REDIRECT_URI = "{}:{}/youtube/callback".format(CLIENT_SIDE_URL,PORT,YOUTUBE_CALLBACK)




sp_auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": SP_REDIRECT_URI,
    "scope": SP_SCOPE,
    "client_id": SP_CLIENT_ID
}

yt_auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": YT_REDIRECT_URI,
    "scope": YOUTUBE_READ_WRITE_SCOPE,
    "client_id": YT_CLIENT_ID
}

@app.route("/spotify")
def spotify():
    # Authorization
    url_args = "&".join(["{}={}".format(key,urllib.parse.quote(val)) for key,val in sp_auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)


@app.route("/spotify/callback/q", methods=['POST', 'GET'])
def callback():

    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": SP_REDIRECT_URI
    }
    b = ("{}:{}".format(SP_CLIENT_ID, SP_CLIENT_SECRET))
    base64encoded = base64.b64encode(b.encode('utf-8'))
    #print(base64encoded)
    new_encode= str(base64encoded)[2:-1]
    #print(new_encode)
    headers = {"Authorization": "Basic {}".format(new_encode)}
    #print(headers)
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    # Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    #Use the access token to access Spotify API
    authorization_header = {"Authorization":"Bearer {}".format(access_token)}



    # Get profile data
    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    profile_data = profile_response.json()

    user_id = profile_data["id"]

    #print(profile_data)

    # Get user playlist data
    playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
    playlists_response = requests.get(playlist_api_endpoint, headers=authorization_header)
    playlists = playlists_response.json()


    p = {}
    p_names = []

    for i in range(len(playlists["items"])):
        p[playlists["items"][i]["name"]] = playlists["items"][i]["id"]
    print(p)

    for item in p.keys():
        name = item
        p_names +=[item]




    session["playlist_names"] = p_names

    session["playlist"] = p
    session["user"] = profile_data["href"]
    session["auth_header"] =  authorization_header
    session["user_id"] = user_id



    return (redirect(url_for("spotifyplaylist")))


@app.route("/spotifyplaylist", methods=['POST', 'GET'])
def spotifyplaylist():
    playlist_names = session.get("playlist_names")
    playlist = session.get("playlist")
    if request.method == 'GET':
        return render_template("spotify_playlist.html", playlist_names=playlist_names)
    elif request.method =='POST':
        p_name = str(request.form["user_choice"])
        session["playlist_name"]=p_name
        playlist_id = playlist.get(p_name)
        user = session.get("user", None)
        auth_header = session.get("auth_header", None)
        user_playlist_api_endpoint = "{}/playlists/{}/tracks".format(user, playlist_id)
        user_playlist_response = requests.get(user_playlist_api_endpoint, headers=auth_header)
        user_playlist = user_playlist_response.json()


        song = {}
        for j in range(len(user_playlist["items"])):
            song[user_playlist["items"][j]["track"]["name"]] = user_playlist["items"][j]["track"]["artists"][0]["name"]

        song_information= []
        for m in range(len(user_playlist["items"])):

            song_information += [user_playlist["items"][m]["track"]["name"] + " " + user_playlist["items"][m]["track"]["artists"][0]["name"] ]

            song_information += [user_playlist["items"][m]["track"]["name"] + " " + user_playlist["items"][m]["track"]["artists"][0]["name"] + " " +user_playlist["items"][m]["track"]["album"]["name"]]

        print(song_information)
        session["song_options"] = song_information

        return (redirect("/youtube"))


DEVELOPER_KEY = "" #add the google api key

@app.route("/youtube", methods = ['GET','POST'])
def youtube():
    if 'credentials' not in session:
        return redirect(url_for('oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    if credentials.access_token_expired:
        return redirect(url_for('oauth2callback'))
    else:
        playlist_name = session.get("playlist_name")
        http_auth = credentials.authorize(httplib2.Http())
        yt_service = discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,http=credentials.authorize(httplib2.Http()))#,http_auth
        playlists_insert_response = yt_service.playlists().insert(
            part="snippet,status",
            body=dict(
                snippet=dict(
                    title=playlist_name,
                    description="Playlist created by SpotifYT from my Spotify Playlist" + " " + "(" + playlist_name + ")"
                ),
                status=dict(
                    privacyStatus="public"
                )
            )
        ).execute()

        ytplaylist_id = playlists_insert_response["id"]

        yt_playlist_url = "https://www.youtube.com/playlist?list=" + ytplaylist_id

        song_options = session.get("song_options")

        youtube = discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                                  developerKey=DEVELOPER_KEY)
        # search for the most viewed video of songs in the playlist
        video_ids = []
        for n in range(len(song_options)):

            search_response = youtube.search().list(
                q=song_options[n],
                part="id,snippet",
                maxResults=10).execute()



            for search_result in search_response.get("items",[]):

                if search_result["id"]["kind"] == "youtube#video":
                    v_id = search_result["id"]["videoId"]
                    video_ids += [v_id]
                    break


        for x in video_ids:
            add_video_request = yt_service.playlistItems().insert(
                part="snippet",
                body={
                    'snippet': {
                        'playlistId': ytplaylist_id,
                        'resourceId': {
                            'kind': 'youtube#video',
                            'videoId': x
                        }


                    }
                }).execute()


    return (render_template("youtubeplaylist.html", youtube_url= yt_playlist_url))



@app.route("/oauth2callback")
def oauth2callback():
    flow = client.flow_from_clientsecrets(
      'client_secrets.json',
      message=MISSING_CLIENT_SECRETS_MESSAGE,
      scope=YOUTUBE_READ_WRITE_SCOPE,
      redirect_uri=url_for('oauth2callback', _external=True))
    if 'code' not in request.args:
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)
    else:
        auth_code = request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        session['credentials'] = credentials.to_json()
        return redirect(url_for('youtube'))

'''


storage = Storage("%s-oauth2.json" % sys.argv[0])
credentials = storage.get()

if credentials is None or credentials.invalid:
  flags = argparser.parse_args()
  credentials = run_flow(flow, storage, flags)

'''
if __name__ == "__main__":
    app.secret_key = str(uuid.uuid4())
    app.run(debug=True,port=PORT)

