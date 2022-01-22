from __future__ import annotations #for python3.8 or less

import websockets, asyncio, yaml, json, sys, argparse
import mido #type: ignore

from collections import defaultdict as ddict
from collections.abc import Generator
from typing import Optional, NoReturn
from contextlib import contextmanager

from messages import Request, Response
from structures import OBS, Scene, Source

def Id() -> Generator[str, None, None]:
    """Unique id generator."""

    i: int = 0
    while True:
        yield str(i)
        i += 1

def getConfig(path: str) -> dict:
    """Loads config from file at path."""
    
    with open(path, "r") as file:
        if path.endswith(".json"):
            data = json.load(file)
        elif path.endswith(".yaml"):
            data = yaml.safe_load(file)
        else:
            raise RuntimeError("Not a supported config format.")

    config: dict = {"note_on": ddict(list),
                     "note_off": ddict(list),
                     "control_change": ddict(list)}

    for command in data:
        if command["trigger"] == "note":
            if command["style"] == "open" or command["style"] == "latch":
                config["note_on"][command["value"]].append(command)
            if command["style"] == "close" or command["style"] == "latch":
                config["note_off"][command["value"]].append(command)
            if command["style"] == "mirror" and command["type"] == "mirrorSource":
                config["note_on"][command["value"]].append({
                    "type": "showSource",
                    "target": command["target"],
                    "trigger": command["trigger"],
                    "style": "open",
                    "value": command["value"]})
                config["note_off"][command["value"]].append({
                    "type": "hideSource",
                    "target": command["target"],
                    "trigger": command["trigger"],
                    "style": "close",
                    "value": command["value"]})
        else:
            config[command["trigger"]][command["value"]].append(command)
            
    return config

@contextmanager
def openMidiPorts(name: str) -> mido.ports.BasePort:
    """Contextmanager that opens a ioport if possible, otherwise falling back to an input."""
    
    _in: mido.ports.BasePort
    _out: mido.ports.BasePort
    inames: list = [i for i in mido.get_input_names() if i.startswith(name)]
    onames: list = [o for o in mido.get_output_names() if o.startswith(name)]
    ionames: list = [io for io in mido.get_ioport_names() if io.startswith(name)]
    if len(inames) == len(onames) == len(ionames) == 0:
        raise OSError("No port found with name " + name + ".")
    if len(ionames) > 0:
        _in = _out = mido.open_ioport(ionames[0])
    else:
        _in = mido.open_input(inames[0])
        _out = mido.open_output(onames[0])
        
    try:
        yield (_in, _out)
    finally:
        _in.close()
        _out.close()
    

class WebsocketHandler:
    """Wrapper for interacting with the OBS websocket."""

    def __init__(self, path: str, port: str, debug: bool, password: str) -> None:
        """Initializes websocket handler with config from the path."""

        self.config: dict = getConfig(path)
        if debug == True:
            print(f"Config: {self.config}")
        self.port: str = port
        '''
        for option in mido.get_input_names():
            if option.startswith(port):
                self.port = option
                break
        if debug == True:
            print(f"Port: {self.port}")
        '''
        self.debug: bool = debug
        
        self.is_io: bool = False
        self.watches = self.getWatches()

        self._id: Generator[str, None, None] = Id()

        self.obs: OBS = OBS(password)
        self.requests: list[Request] = [] #type: ignore
        self.responses: list[Response] = [] #type: ignore

        self.requests.append(Request(
            self._id, {"type": "GetAuthRequired"}, self.obs))


    async def read(self, websocket: websockets.WebSocketClientProtocol) -> None:
        """Asynchronously reads responses from the OBS websocket."""

        try:
            while True:
                msg = await websocket.recv()
                data = json.loads(msg)
                if self.debug:
                    print(data)
                self.responses.append(Response(data, self.obs))
        except asyncio.CancelledError:
            return

    async def send(self, websocket: websockets.WebSocketClientProtocol, request: list[dict]) -> None: #type: ignore
        """Asynchronously sends a request to the OBS websocket."""

        if self.debug:
            print(request)

        for msg in request:
            await websocket.send(json.dumps(msg))
            self.obs.pendingResponses[msg["message-id"]] = msg

    async def run(self) -> NoReturn:
        """Connects to the OBS websocket and endlessly parses MIDI to handle requests and responses."""

        with openMidiPorts(self.port) as ports:
            iport, oport = ports
            if self.debug:
                print(f"Input: {iport}\nOutput: {oport}")
            async with websockets.connect("ws://localhost:4444") as websocket:

                readTask = asyncio.create_task(self.read(websocket))

                while True:
                    await asyncio.sleep(0.1)
                    for msg in iport.iter_pending():
                        self.parse(msg)

                    for request in self.obs.requests:
                        self.requests.append(Request(self._id, request, self.obs))
                        self.obs.requests.remove(request)

                    for request in self.requests:
                        await self.send(websocket, request.format())
                        self.requests.remove(request)

                    for response in self.responses:
                        response.handle()
                        self.responses.remove(response)

                    for update in self.obs.soundboardUpdates:
                        msgs: Optional[mido.Message] = self.unparse(update)
                        for msg in msgs:
                            oport.send(msg)

                await readTask

    def parse(self, msg: mido.Message) -> None:
        """Parses MIDI message and creates requests based off of the loaded configuration."""

        if self.debug:
            print(msg)

        trigger: str = msg.type
        value: int = -1
        data: int = -1

        if trigger == "note_on" or trigger == "note_off":
            value = msg.note
            data = msg.velocity
        elif trigger == "control_change":
            value = msg.control
            data = msg.value
        else:
            return

        for command in self.config[trigger][value]:
            request = command.copy()
            request["data"] = data
            self.requests.append(Request(self._id, request, self.obs))
            
    def unparse(self, data: dict) -> list[mido.Message]:
        """Preps MIDI messages from a dictionary if they are for any watched key values."""

        return []
        
    def getWatches(self) -> list:
        """Returns all of the values to be watched for updates"""
        
        ...
        
        

if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("--config", type = str, default = "settings.yaml")
    parser.add_argument("--port", type = str, default = "")
    parser.add_argument("--debug", action = "store_true")
    parser.add_argument("--password", type = str, default = "")

    args: argparse.Namespace = parser.parse_args()

    websocketHandler: WebsocketHandler = WebsocketHandler(args.config, args.port, args.debug, args.password)
    asyncio.get_event_loop().run_until_complete(websocketHandler.run())
