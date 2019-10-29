import websockets, asyncio, json, sys, mido, argparse
from multiprocessing import Process, SimpleQueue

try:
    from gui import toolLoop
except ImportError:
    print("GUI mode unavailable.")

from messages import Request, Response
from structures import OBS, Scene, SceneItem

def Id():
    #Unique id generator
    
    i = 0
    while True:
        yield str(i)
        i += 1

class WebsocketHandler:

    def __init__(self, config):
        
        self.id = Id()
        self.config = self.getConfig(config)

        self.obs = OBS()
        self.requests, self.responses = [], []

        self.requests.append(Request(self.id, {"type": "GetSceneList"}, self.obs))

    def getConfig(self, path):
        #Aquires a config file for MIDI message parsing
        #A valid config is an array of objects with three parameters:
        #   key: the type of midi message
        #   value: the value associated with the message
        #   commands: an array of the commands to be run
        
        with open(path, "r") as f:
            data = json.load(f)
            config = {}
            for obj in data:
                if obj["key"] not in config.keys():
                    config[obj["key"]] = {obj["value"]: []}
                elif obj["value"] not in config[obj["key"]].keys():
                    config[obj["key"]][obj["value"]] = []
                config[obj["key"]][obj["value"]].extend(obj["commands"])
            return config

    async def read(self, websocket):
        try:
            while True:
                msg = await websocket.recv()
                data = json.loads(msg)
                self.responses.append(Response(data, self.obs))
                    
        except asyncio.CancelledError:
            return

    async def send(self, websocket, request):
        
        if msg == None:
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

        print(msg)
        key = msg.type
        if key == "note_on" or key == "note_off":
            value = msg.note
        elif key == "program_change":
            value = msg.channel
        value = int(value)
        try:
            for command in self.config[key][value]:
                self.requests.append(Request(self.id, command, self.obs))
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
        
        key, value = msg.split(" ")
        value = int(value)
        try:
            for command in self.config[key][value]:
                self.requests.append(Request(self.id, command, self.obs))
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
    parser.add_argument("-config", type = str, default = "settings.json")
    parser.add_argument("-port", type = str)
    args = parser.parse_args()

    if args.mode == "midi":
        websocketHandler = MIDIWebsocketHandler(args.config, args.port)
    elif args.mode == "gui":
        websocketHandler = GUIWebsocketHandler(args.config)
    elif args.mode == "scan":
        print(mido.get_input_names())
        sys.exit()
    asyncio.get_event_loop().run_until_complete(websocketHandler.run())
