from __future__ import annotations #for python3.9 and less

import argparse
import asyncio
import json
import mido
import websockets

from base64 import b64encode
from contextlib import contextmanager
from hashlib import sha256

from collections.abc import Generator
from typing import NoReturn
from typing import Optional

from structures import OBS
from structures import Watch


def Id() -> Generator[str, None, None]:
    """Unique ID generator."""

    i: int = 0
    while True:
        yield str(i)
        i += 1

def authenticate(hello: str, password: str) -> str:
    """Does the necessary steps to generate a valid authentication message."""
    #First, turn the string into a json object so it can be parsed
    data: dict = json.loads(hello)["d"]["authentication"]
    
    #Then, create the secret using the password and salt
    secret_string: str = password + data["salt"]
    secret_hash: sha256 = sha256(secret_string.encode("utf-8"))
    secret: bytes = b64encode(secret_hash.digest())
    
    #Next, create the response string using the secret and the challenge
    response_string: str = secret.decode("utf-8") + data["challenge"]
    response_hash: sha256 = sha256(response_string.encode("utf-8"))
    response: bytes = b64encode(response_hash.digest())

    #Finally, package it all into a dictionary and stringify it to be sent back to the websocket server
    return json.dumps({"op": 1,
                       "d": {
                           "rpcVersion": 1,
                           "authentication": response.decode("utf-8")
                           }
                       })
    

def getConfig(path: str) -> dict:
    """Loads the configuration file for determining what MIDI messages do what actions."""
    #Load using the proper library depending on extension
    data: list
    with open(path) as file:
        if path.endswith(".json"):
            data = json.load(file)
        elif path.endswith(".yaml"):
            data = yaml.safe_load(file)
        else:
            raise RuntimeError("Not a supported config format.")
    
    #Divide the different types of midi messages into different buckets.
    config: dict = {"note": [], "control": []}
    for obj in data:
        if obj["type"] == "note":
            config["note"].append(obj)
        elif obj["type"] == "control":
            config["control"].append(obj)
        else:
            raise RuntimeError(f"Invalid object type {obj['type']}.")
        
    return config

def generateWatches(config: dict) -> list[Watch]:
    
    watches: list[Watch] = []
    for cfg in config["note"]:
        for action in cfg["actions"]:
            watches.append(Watch(action["target"], cfg["value"], action["type"]))
            
    return watches

@contextmanager
def openMidiPorts(name: str) -> Generator[tuple[mido.ports.BasePort, mido.ports.BasePort], None, None]:
    """Opens input and output midi ports from the first port found based on the given name hint."""
    #Type hints for returned values
    ip: mido.ports.BasePort
    op: mido.ports.BasePort
    
    #List of all valid ports that start with the name hint
    inames: list = [i for i in mido.get_input_names() if i.startswith(name)]
    onames: list = [o for o in mido.get_output_names() if o.startswith(name)]
    ionames: list = [io for io in mido.get_ioport_names() if io.startswith(name)]
    
    #If the hint results in no valid ports being found, raise an error
    if len(inames) == len(onames) == len(ionames) == 0:
        raise OSError("No port found from name hint " + name + ".")
    
    #If an ioport exists, it should be used
    if len(ionames) > 0:
        ip = op = mido.open_ioport(ionames[0])
    #Otherwise, fall back on a input and output port
    #TODO: handle missing output
    else:
        ip = mido.open_input(inames[0])
        op = mido.open_output(onames[0])

    #Yield the ports, and close them on cleanup
    try:
        yield (ip, op)
    finally:
        ip.close()
        op.close()

class WebsocketHandler:
    """Wrapper for interacting with the OBS websocket."""

    def __init__(self, port: str, password: str, path: str, debug: bool, nolatch: bool) -> None:
        """Initializes websocket handler with config from the path."""
        #Store values from arguments (and generate config dictionary)
        self.port: str = port
        self.password: str = password
        self.config: dict = getConfig(path)
        self.debug: bool = debug
        self.nolatch = nolatch
        self.latchState: bool = False
        
        if self.debug:
            print(self.config)
        
        #Instantiate unique ID generator
        self.uid: Generator[str, None, None] = Id()
        
        #Create data structures for the OBS and websocket message instance data
        self.obs: OBS = OBS(self.uid)
        self.obs.watches = generateWatches(self.config)
        self.ignores: list = []
        self.events: list = []
        self.requests: list = [{"op": 6, "d": {"requestType": "GetSceneList", "requestId": next(self.uid)}}]
        self.requestResponses: list = []
        self.requestBatches: list = [] #TODO: Implement request batching
        self.requestBatchResponses: list = []

    async def read(self, websocket: websockets.WebSocketClientProtocol) -> None:
        """Asynchronously reads responses from the OBS websocket."""

        try:
            while True:
                #Whenever a message is received, add it to the list of server responses
                msg: str = await websocket.recv()
                data: dict = json.loads(msg)
                if self.debug:
                    print(f"Received {data}")
                if data["op"] == 2:
                    self.obs.locked = False #Unlock the OBS object on authentication verification
                elif data["op"] == 5:
                    self.events.append(data)
                elif data["op"] == 7:
                    self.requestResponses.append(data)
                elif data["op"] == 9:
                    self.requestBatchResponses.append(data)
                else:
                    print(f"Unexpected message with opcode {data['op']}.")
        except asyncio.CancelledError:
            return
        
    async def send(self, websocket: websockets.WebSocketClientProtocol, msg: dict) -> None:
        """Asynchronously sends a request to the OBS websocket."""

        if self.debug:
            print(f"Sending {msg}")       

        await websocket.send(json.dumps(msg))

    async def run(self) -> NoReturn:
        """Connects to the OBS websocket and endlessly parses MIDI to handle requests and responses."""
        #Aquire the bundled ports from the context manager...
        with openMidiPorts(self.port) as ports:
            iport: mido.ports.BasePort
            oport: mido.ports.BasePort
            #...and split them into their two respective port objects
            iport, oport = ports
            if self.debug:
                print(f"Opened input {iport}.")
                print(f"Opened output {oport}.")
                
            #Connect to the OBS websocket...
            async with websockets.connect("ws://localhost:4444") as websocket:
                #...and handle the initial authentication handshake...
                await websocket.send(authenticate(await websocket.recv(), self.password))
                #...and create a task to check for new messages during downtime
                readTask = asyncio.create_task(self.read(websocket))
                #Oh, and since we shouldn't need the password anymore, lets ditch it
                self.password = "" #TODO: proper password management system

                while True:
                    #Downtime so that reads can occur
                    await asyncio.sleep(0.1)
                    
                    #Check for and parse any messages from the MIDI input port
                    for msg in iport.iter_pending():
                        self.parse(msg)
                        
                    #Update the OBS object based on incoming events
                    for msg in self.events:
                        self.obs.handle(msg)
                        self.events.remove(msg)
                    
                    #Send out solo requests to the server (as long as the OBS object is not locked)
                    if not self.obs.locked:
                        for msg in self.requests:
                            await self.send(websocket, msg)
                            self.requests.remove(msg)
                    
                    #Update the OBS object based on responses to solo requests
                    for msg in self.requestResponses:
                        self.obs.handle(msg)
                        self.requestResponses.remove(msg)
                    
                    #Send out batch requests to the server (as long as the OBS object is not locked)
                    if not self.obs.locked:
                        for msg in self.requestBatches:
                            await self.send(websocket, msg)
                            self.requestBatches.remove(msg)
                    
                    #Update the OBS object based on responses to batch requests
                    for msg in self.requestBatchResponses:
                        self.obs.handle(msg)
                        self.requestBatchResponses.remove(msg)
                        
                    #Move all OBS object requests into the regular requests list (and add the unique id)...
                    for msg in self.obs.requests:
                        self.requests.append(msg)
                        self.obs.requests.remove(msg)
                    #and also for requests that any scenes have generated
                    for scene in self.obs.scenes:
                        for msg in scene.requests:
                            self.requests.append(msg)
                            scene.requests.remove(msg)
                            
                    #Run any necessary actions for triggered Watches
                    for watch in self.obs.watches:
                        if watch.triggered:
                            if self.debug:
                                print(f"{watch} triggered.")
                            watch.triggered = False
                            if watch.mtype == "SetSceneItemEnabled":
                                msg = mido.Message("note_on", note = watch.value, velocity = 127 if watch.data == "1" else 0)
                                if self.debug:
                                    print(f"Sending {msg}")
                                oport.send(msg)
                                if msg.type == "note_on":
                                    self.ignores.append(msg)

                #This might not be necessary? (unreachable code?)
                await readTask
            

    def parse(self, msg: mido.Message) -> None:
        """Parses MIDI message and creates requests based off of the loaded configuration."""

        if self.debug:
            print(msg)
        
        #Simplify the message type from the MIDI message...
        mtype: str
        if msg.type == "note_on" or msg.type == "note_off":
            #If nolatch is active, do nothing if the type is note_off
            if self.nolatch and msg.type == "note_off":
                return
            #If the message matches one in the ignore list, ignore it (and remove it from the list)
            if msg in self.ignores:
                if self.debug:
                    print(f"Skipping echo of sent message: {msg}.")
                self.ignores.remove(msg)
                return
            mtype = "note"
        elif msg.type == "control_change":
            mtype = "control"
        else:
            if self.debug:
                print(f"Unhandled MIDI message with type {msg.type}.")
            return
        
        #...aquire the channel...
        channel: int = msg.channel
        #...the value (which may have unique names in the MIDI message)...
        value: int
        if mtype == "note":
            value = msg.note
        elif mtype == "control":
            value = msg.control
        #...and any extra data (on/off for note, value for control, etc)
        data: int
        if mtype == "note":
            data = 0 if msg.type == "note_off" or msg.velocity == 0 else 1
            if self.nolatch:
                data = 1 if self.latchState else 0
                self.latchState = not self.latchState
        elif mtype == "control":
            data = msg.value
            
        #Check the config for any actions associated with the MIDI message and add them to the requests list
        for obj in self.config[mtype]:
            if obj["channel"] == channel and obj["value"] == value:
                for action in self.obs.generateRequests(obj["actions"], data):
                    self.requests.append({"op": 6,
                                          "d": action})
                
    def pack(self, msg: dict) -> dict:
        """Packages a message into a proper opcode with unique id."""
        ...

if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type = str, default = "")
    parser.add_argument("-P", "--password", type = str, default = "")
    parser.add_argument("-c", "--config", type = str, default = "settings.yaml")
    parser.add_argument("-d", "--debug", action = "store_true")
    parser.add_argument("-n", "--nolatch", action = "store_true")

    args: argparse.Namespace = parser.parse_args()

    websocketHandler: WebsocketHandler = WebsocketHandler(args.port, args.password, args.config, args.debug, args.nolatch)
    asyncio.get_event_loop().run_until_complete(websocketHandler.run())
