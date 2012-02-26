# SpotifyController
A web based remote control for spotify running on Linux-based systems.
It uses the D-BUS interface to control spotify and retrieve the current track
information.

## How to Use it
SpotifyController depends on `cherrypy` so you need to install it first.
in Ubuntu:

```
#apt-get install python-cherrypy
```

Once installed you can launch the server by executying
`./spotify_controller` By default it will listen on port 8080.

That's all! Now you can go to your favorite browser and access
http://localhost:8080/ and start controlling your Spotify!
