# SpotifyServer
A Spotify Server to control spotify remotely.

It uses the *D-BUS* interface to control spotify and retrieve the current track
information.
It also has a simple support to control volume on systems using *PulseAudio*.

## Modes
Currently, SpotifyServer supports *two* modes. One is a **HTTP Server**
that allows you to control Spotify using a *simple* bundled web interface
and the other is as a **Socket Server**. Currently the socket version is used
as the backend for [SpotifyRemote](https://github.com/WasserX/SpotifyRemote)

## Dependencies
If you want to use the **HTTP Server** mode, you will need `cherrypy`.
In Ubuntu you can install it with:

```
#apt-get install python-cherrypy
```

For the **Socket Server** there are no known dependencies.

## How to Use it

### HTTP Server
Once installed the dependencies, run the server with `./http_server.py`.

That's all! Now you can go to your favorite browser and access
http://localhost:8080/ and start controlling your Spotify!

### Socket Server
Just run `./socket_server.py` and connect from [SpotifyRemote](https://github.com/WasserX/SpotifyRemote)

## Future Plans
The current setup of socket/HTTP Server is a workaround because I'm facing some
issues with *WS*. Once I get it to work, the server will be unified and it will
be possible to access from your *browser* or from the native *Android Client*.
