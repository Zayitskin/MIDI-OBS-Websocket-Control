# MIDI-OBS-Websocket-Control
A python program for facilitating control of OBS via MIDI (or a bare-bones debug GUI) using the OBS Websocket library.
Currently requires python 3.9.x+, as well as several external libraries listed in the requirements.txt.

Important configuration information:
The script will not parse any messages with a velocity of 1 (as it is reserved for updating the midi device of changes).