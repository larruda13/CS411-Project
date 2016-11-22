# CS411-Project

Project repository for the course project in the Fall 2016 iteration of the Software Engineering course at Boston University.

## Goal

The goal of this project is to create a Youtube to Spotify converter using Flask, SQLite, and AngularJS.

## Team members 
* [Chen Xu](https://github.com/chenyphg)
* [Jennifer Tsui](https://github.com/j-tsui)
* [Jiayuan Zheng](https://github.com/jiayuanz)
* [Lucas Arruda](https://github.com/larruda13)

## Running the software

Run `hello.py`. Note that we are developing with Python 3.5.2.
From there, the output should say something like this:

```
* Running on http://127.0.0.1:5000/
```

In this case, you would want to go to `http://localhost:5000/test` in your browser to see the resulting web app.
As of 11/01/16, all our app does is send an API request to Spotify. What it returns is a full list of the artist names that match with the search term that was input into the form. We plan to add authorization to the API calls.

## Authorization: Formatting the auth.json file

The auth.json file will remain empty, and will not be submitted to GitHub. When you are our code, you should use the `auth.json` file to store your credentials for any third-party data resources, APIs, services, or repositories that you use. An example of the contents you might store in your auth.json file is as follows:

{
    "services": {
        "cityofbostondataportal": {
            "service": "https://data.cityofboston.gov/",
            "username": "alice_bob@example.org",
            "token": "XxXXXXxXxXxXxxXXXXxxXxXxX",
            "key": "xxXxXXXXXXxxXXXxXXXXXXxxXxxxxXXxXxxX"
        },
        "mbtadeveloperportal": {
            "service": "http://realtime.mbta.com/",
            "username": "alice_bob",
            "token": "XxXX-XXxxXXxXxXXxXxX_x",
            "key": "XxXX-XXxxXXxXxXXxXxx_x"
        }
    }
}

[Idea based off of:](https://github.com/Data-Mechanics/course-2016-fal-proj)



First edit: Jennifer Tsui (11/01/16)

Most recent edit: Jennifer Tsui (11/22/16)
