from flask import Flask, request, render_template
import requests
import json
import hello
import time

#-----------------------------------------------------------------------------------------------#
'''
app.py (originally named 'hello.py'

Purpose: Makes an API call to the Spotify API. Takes input based on a form (which prompts for
         an artist name), and returns a list of search results.
Boston University CS411 - Software Engineering

Originally written by: Jennifer Tsui (11-2-16)
'''
#-----------------------------------------------------------------------------------------------#


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/test', methods=['GET','POST'])
def test():
    if request.method == 'POST':
        response = request.form['artist'] #see sql injection comment
        # add secret key; call json file
        r = requests.get("https://api.spotify.com/v1/search?q=" + str(response) + "&type=artist")
        # keyword arg, query param, provide dict -- prevent against sql injection

        test_output = []
        has_more = True

        while has_more is not None:
            time.sleep(2)
            s = r.json() #converts body of json string to python dict

            artists = s['artists']['items']

            for i in range(len(artists)):
                test_output += [artists[i]['name']]

            has_more = s['artists']['next']
            if (has_more is not None):
                r = requests.get(s['artists']['next'])
            else:
                break

        #print("test output is:")
        #print(test_output)
        return render_template('test.html', x=test_output)
    else: # request.method == 'GET'
        return render_template('test.html')
    #x = 5
    #return render_template('test.html', x=x)


if __name__ == '__main__':
    app.run()