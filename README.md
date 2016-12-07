# SpotifYT

Project repository for the course project in the Fall 2016 iteration of the Software Engineering course at Boston University.

## Purpose

This web app seeks to automate the process of converting a playlist of songs held in Spotify into a playlist of YouTube videos, which would be saved to your YouTube user account. The motivation of this is to save time from having to manually search for videos on and assembled a playlist based on that. 

## Team members 
* [Chen Xu](https://github.com/chenyphg)
* [Jennifer Tsui](https://github.com/j-tsui)
* [Jiayuan Zheng](https://github.com/jiayuanz)
* [Lucas Arruda](https://github.com/larruda13)

## Development

* [Pycharm Professional Edition](https://www.jetbrains.com/pycharm/download/)
* [Python 3.5.2](https://www.python.org/downloads/release/python-350/)

## Dependences

### Frontend

* [Bootstrap v3.3.7](http://getbootstrap.com/)

### Backend

* [Flask v0.11.1](https://pypi.python.org/pypi/Flask)
* [Google APIs Client Library for Python](https://developers.google.com/api-client-library/python/start/installation)

### Database

* [Dataset (with SQLite3)](https://dataset.readthedocs.io/en/latest/)

### External APIs

* [Spotify](https://developer.spotify.com/web-api/)
* [YouTube Data API v3](https://developers.google.com/youtube/v3/)

## Running the app in SpotifYT - Final

Run `app.py`. In terminal, you could do this by typing the following command:
 
```
$ python app.py
```

After doing that, you would see something like this:


```
 * Running on http://127.0.0.1:8080/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!

```

From there, go to `http://127.0.0.1:8080/` in your preferred web browser!


## Running the app in Prototype Code (Part 3)/flask

Run `app.py` (which was formerly called `hello.py`). 

```
* Running on http://127.0.0.1:5000/
```

In this case, you would go to `http://localhost:5000/test` in your browser to see the resulting web app.
As of 11/01/16, all our app does is send an API request to Spotify. What it returns is a full list of the artist names that match with the search term that was input into the form. We plan to add authorization to the API calls.

---

First edit: Jennifer Tsui (11/01/16)

Most recent edit: Jennifer Tsui (12/02/16)
