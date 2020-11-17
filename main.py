import websockets, asyncio, yaml, json, sys, argparse
import mido #type: ignore

from collections import defaultdict as ddict
from collections.abc import Generator
from typing import Optional, NoReturn

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
        else:
            config[command["trigger"]][command["value"]].append(command)
            
    return config

class WebsocketHandler:
    """Wrapper for interacting with the OBS websocket."""

    def __init__(self, path: str, port: str, debug: bool) -> None:
        """Initializes websocket handler with config from the path."""

        self.config: dict = getConfig(path)
        if debug == True:
            print(f"Config: {self.config}")
        self.port: str = ""
        for option in mido.get_input_names():
            if option.startswith(port):
                self.port = option
                break
        if debug == True:
            print(f"Port: {self.port}")
        self.debug: bool = debug

        self._id: Generator[str, None, None] = Id()

        self.obs: OBS = OBS()
        self.requests: list[Request] = [] #type: ignore
        self.responses: list[Response] = [] #type: ignore

        self.requests.append(Request(
            self._id, {"type": "GetSceneList"}, self.obs))


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

        with mido.open_input(self.port) as port:
            async with websockets.connect("ws://localhost:4444") as websocket:

                readTask = asyncio.create_task(self.read(websocket))

                while True:
                    await asyncio.sleep(0.1)
                    for msg in port.iter_pending():
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
        
        

if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("--config", type = str, default = "settings.yaml")
    parser.add_argument("--port", type = str, default = "")
    parser.add_argument("--debug", type = bool, default = False)

    args: argparse.Namespace = parser.parse_args()

    websocketHandler: WebsocketHandler = WebsocketHandler(args.config, args.port, args.debug)
    asyncio.get_event_loop().run_until_complete(websocketHandler.run())
