import websockets, asyncio, json, yaml, sys, mido, argparse #type: ignore
from collections.abc import Generator
from multiprocessing import Process, SimpleQueue
from typing import Union, NoReturn, Optional

try:
    from gui import toolLoop
except ImportError:
    print("GUI mode unavailable.")

from messages import Request, Response
from structures import OBS, Scene, SceneItem

pairedCommands: dict[str, str] = {
    "showSource": "hideSource",
    "hideSource": "showSource",
    "showAllSources": "hideAllSources",
    "hideAllSources": "showAllSources",
    "showFilter": "hideFilter",
    "hideFilter": "showFilter",
    }

def Id() -> Generator[str, None, None]:
    """Unique id generator"""
    
    i: int = 0
    while True:
        yield str(i)
        i += 1
        
class WebsocketHandler:
    """Wrapper super-class for interacting with the OBS websocket control system."""
    
    def __init__(self, config: str) -> None:
        """Initializes base websocket handler with configuration from file at config."""
        
        
        self._id = Id()
        self.config = self.getConfig(config)
        
        self.obs = OBS()
        self.requests: list[Request] = []
        self.responses: list[Response] = []
        self.requests.append(Request(self._id, {"type": "GetSceneList"}, self.obs))
        
    def setDebugMode(self, boolean: bool) -> None:
        """Enables or disables debug mode."""

        self.debug = boolean
        
    def getConfig(self, path: str) -> dict:
        """Sets the config to the data in file at path."""
        
        with open(path, "r") as f:
            if path.endswith(".json"):
                data = json.load(f)
            elif path.endswith(".yaml"):
                data = yaml.safe_load(f)
            else:
                raise NotImplementedError("Not a valid configuration format.")
            config: dict = {}
            for obj in data:
                command, value = obj["command"], obj["value"]
                if "type" in obj:
                    _type = obj["type"]
                else:
                    _type = None
                if "target" in obj:
                    target = obj["target"]
                else:
                    target = None
                if "targetSource" in obj:
                    targetSource = obj["targetSource"]
                else:
                    targetSource = None
                if "targetFilter" in obj:
                    targetFilter = obj["targetFilter"]
                else:
                    targetFilter = None
                if "setting" in obj:
                    setting = obj["setting"]
                else:
                    setting = None

                if value not in config.keys():
                        config[value] = {"note_on": [], "note_off": [], "control_change": []}
                        
                if "Filter" not in command:
                    if _type == "open":
                        config[value]["note_on"].append({"type": command, "target": target})
                    elif _type == "close":
                        config[value]["note_off"].append({"type": command, "target": target})
                    elif _type == "latch":
                        config[value]["note_on"].append({"type": command, "target": target})
                        config[value]["note_off"].append({"type": command, "target": target})
                    elif _type == "mirror":
                        if command not in pairedCommands:
                            config[value]["note_on"].append({"type": command, "target": target})
                            config[value]["note_off"].append({"type": command, "target": target})
                        else:
                            config[value]["note_on"].append({"type": command, "target": target})
                            config[value]["note_off"].append({"type": pairedCommands[command], "target": target})
                else:
                    if setting == None:
                        config[value]["control_change"].append(
                            {"type": command, "targetSource": targetSource, "targetFilter": targetFilter})
                    else:
                        config[value]["control_change"].append(
                            {"type": command, "targetSource": targetSource, "targetFilter": targetFilter, "setting": setting})
                        
        return config
    
    async def read(self, websocket: websockets.WebSocketClientProtocol) -> None:
        """asynchronously reads responses from the OBS websocket."""
        
        try:
            while True:
                msg = await websocket.recv()
                data = json.loads(msg)
                if self.debug:
                    print(data)
                self.responses.append(Response(data, self.obs))
        except asyncio.CancelledError:
            return
        
    async def send(self, websocket: websockets.WebSocketClientProtocol, request: Union[list[dict], None]) -> None:
        """asynchronously sends a request to the OBS websocket."""
        
        if self.debug:
            print(request)
        if request == None:
            return
        
        #Assertion to make mypy happy
        assert isinstance(request, list)
        for msg in request:
            await websocket.send(json.dumps(msg))
            self.obs.requests[msg["message-id"]] = msg
            
class MIDIWebsocketHandler(WebsocketHandler):
    """Wrapper for interacting with the OBS websocket through a MIDI device."""
    
    def __init__(self, config, port):
        """Initalizes websocket handler with configuration at config controlling from MIDI device on port."""
        
        super().__init__(config)
        
        if port == None:
            self.port = mido.get_input_names()[0]
        else:
            for option in mido.get_input_names():
                if option.startswith(port):
                    self.port = option
                    break
        
    def parse(self, msg: mido.Message) -> None:
        """Parses MIDI message and creates requests based off of the config"""
        
        if self.debug == True:
            print(msg)
        key = msg.type
        if key == "note_on" or key == "note_off":
            _id = msg.note
            value: Optional[int] = None
        elif key == "control_change":
            _id = msg.control
            value = msg.value
        else:
            return
        _id = int(_id)
        try:
            for command in self.config[_id][key]:
                if command["type"] == "editFilter":
                    command["value"] = value
                self.requests.append(Request(self._id, command, self.obs))
        except KeyError:
            return        
    
    async def run(self) -> NoReturn:
        """Connects with the OBS websocket and endlessly parses MIDI messages and handles requests and responses."""
        
        with mido.open_input(self.port) as port:
            async with websockets.connect("ws://localhost:4444") as websocket:

                readTask = asyncio.create_task(self.read(websocket))

                while True:
                    await asyncio.sleep(0.1)
                    for msg in port.iter_pending():
                        self.parse(msg)

                    for update in self.obs.updates:
                        self.requests.append(Request(self._id, update, self.obs))
                        self.obs.updates.remove(update)

                    for request in self.requests:
                        await self.send(websocket, request.format())
                        self.requests.remove(request)

                    for response in self.responses:
                        response.handle()
                        self.responses.remove(response)

                await readTask        
    
class GUIWebsocketHandler(WebsocketHandler):
    """Wrapper for interacting with the OBS websocket through a bare-bones GUI."""

    def __init__(self, config: str) -> None:
        """Initalizes websocket handler with configuration at config controlling from the GUI."""

        super().__init__(config)

        self.queue: SimpleQueue = SimpleQueue()
        self.process = Process(target = toolLoop, args = (self.queue,))
        self.process.start()

    def __del__(self) -> None:
        """Properly ends the subprocess when the wrapper is removed."""

        self.process.join()

    def parse(self, msg: str) -> None:
        """Parses message from the GUI and creates requests based off of the config"""
        
        if self.debug:
            print(msg)
        value: Union[str, int] = ""
        key, value = msg.split(" ")
        value = int(value)
        try:
            for command in self.config[value][key]:
                self.requests.append(Request(self._id, command, self.obs))
        except KeyError:
            return

    async def run(self) -> None:
        """Connects with the OBS websocket and endlessly parses messages from the GUI and handles requests and responses."""
        
        async with websockets.connect("ws://localhost:4444") as websocket:

            readTask = asyncio.create_task(self.read(websocket))

            while True:
                await asyncio.sleep(0.1)
                if not self.queue.empty():
                    msg = self.queue.get()
                    if msg == "SHUTDOWN":
                        print("Attempting shutdown.")
                        readTask.cancel()
                        break
                    else:
                        self.parse(msg)

                for request in self.requests:
                    await self.send(websocket, request.format())
                    self.requests.remove(request)

                for response in self.responses:
                    response.handle()
                    self.responses.remove(response)

            await readTask
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", type = str, choices = ["midi", "gui", "scan"])
    parser.add_argument("--config", type = str, default = "settings.yaml")
    parser.add_argument("--port", type = str)
    parser.add_argument("--debug", type = bool, default = False)
                    
    args = parser.parse_args()
                
    if args.mode == "midi":
        websocketHandler: Union[MIDIWebsocketHandler, GUIWebsocketHandler] = MIDIWebsocketHandler(args.config, args.port)
    elif args.mode == "gui":
        websocketHandler = GUIWebsocketHandler(args.config)
    elif args.mode == "scan":
        print(mido.get_input_names())
        sys.exit()
    websocketHandler.setDebugMode(args.debug)
    asyncio.get_event_loop().run_until_complete(websocketHandler.run())
