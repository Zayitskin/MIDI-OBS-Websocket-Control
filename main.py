import websockets, asyncio, json, sys, mido, argparse
from multiprocessing import Process, SimpleQueue

try:
    from gui import toolLoop
except ImportError:
    print("GUI mode unavailable.")

from messages import Request, Response
from structures import OBS, Scene, SceneItem

pairedCommands = {
    "showSource": "hideSource",
    "hideSource": "showSource",
    "showAllSources": "hideAllSources",
    "hideAllSources": "showAllSources"
    }

def Id():
    #Unique id generator
    
    i = 0
    while True:
        yield str(i)
        i += 1
        
class WebsocketHandler:
    
    def __init__(self, config):
        
        self._id = Id()
        self.config = self.getConfig(config)
        
        self.obs = OBS()
        self.requests, self.responses = [], []
        self.requests.append(Request(self._id, {"type": "GetSceneList"}, self.obs))
        
    def setDebugMode(self, boolean):

        self.debug = boolean
        print(self.config)
        
    def getConfig(self, path):
        
        with open(path, "r") as f:
            data = json.load(f)
            config = {}
            for obj in data:
                command, value, _type = obj["command"], obj["value"], obj["type"]
                if "target" in obj:
                    target = obj["target"]
                else:
                    target = None
                if value not in config.keys():
                    config[value] = {"note_on": [], "note_off": []}
                
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
                        
        return config
    
    async def read(self, websocket):
        
        try:
            while True:
                msg = await websocket.recv()
                data = json.loads(msg)
                if self.debug:
                    print(data)
                self.responses.append(Response(data, self.obs))
        except asyncio.CancelledError:
            return
        
    async def send(self, websocket, request):
        
        if self.debug:
            print(request)
        if request == None:
            return
        for msg in request:
            await websocket.send(json.dumps(msg))
            self.obs.requests[msg["message-id"]] = msg["request-type"]
            
class MIDIWebsocketHandler(WebsocketHandler):
    
    def __init__(self, config, port):
        
        super().__init__(config)
        
        if port == None:
            self.port = mido.get_input_names()[0]
        else:
            for option in mido.get_input_names():
                if option.startswith(port):
                    self.port = option
                    break
        
    def parse(self, msg):
        
        if self.debug == True:
            print(msg)
        key = msg.type
        if key == "note_on" or key == "note_off":
            value = msg.note
        else:
            return
        value = int(value)
        try:
            for command in self.config[value][key]:
                self.requests.append(Request(self._id, command, self.obs))
        except KeyError:
            return        
    
    async def run(self):
        
        with mido.open_input(self.port) as port:
            async with websockets.connect("ws://localhost:4444") as websocket:

                readTask = asyncio.create_task(self.read(websocket))

                while True:
                    await asyncio.sleep(0.1)
                    for msg in port.iter_pending():
                        self.parse(msg)

                    for request in self.requests:
                        await self.send(websocket, request.format())
                        self.requests.remove(request)

                    for response in self.responses:
                        response.handle()
                        self.responses.remove(response)

                await readTask        
    
class GUIWebsocketHandler(WebsocketHandler):

    def __init__(self, config):

        super().__init__(config)

        self.queue = SimpleQueue()
        self.process = Process(target = toolLoop, args = (self.queue,))
        self.process.start()

    def __del__(self):

        self.process.join()

    def parse(self, msg):
        
        if self.debug:
            print(msg)
        key, value = msg.split(" ")
        value = int(value)
        try:
            for command in self.config[value][key]:
                self.requests.append(Request(self._id, command, self.obs))
        except KeyError:
            return

    async def run(self):
        
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
    parser.add_argument("--config", type = str, default = "settings.json")
    parser.add_argument("--port", type = str)
    parser.add_argument("--debug", type = bool, default = False)
                    
    args = parser.parse_args()
                
    if args.mode == "midi":
        websocketHandler = MIDIWebsocketHandler(args.config, args.port)
    elif args.mode == "gui":
        websocketHandler = GUIWebsocketHandler(args.config)
    elif args.mode == "scan":
        print(mido.get_input_names())
        sys.exit()
    websocketHandler.setDebugMode(args.debug)
    asyncio.get_event_loop().run_until_complete(websocketHandler.run())