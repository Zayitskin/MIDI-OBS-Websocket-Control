from __future__ import annotations #for python3.9 and less

from collections.abc import Generator
from typing import Optional

from messages import handleEvent, handleResponse

class OBS:
    """Data container for information pertaining to the current state of OBS."""

    def __init__(self, uid: Generator[str, None, None]) -> None:
        
        self.uid: Generator[str, None, None] = uid

        self.scenes: list[Scene] = []

        self.currentScene: Optional[Scene] = None
        self.previousScene: Optional[Scene] = None

        self.locked = True
        
        self.requests: list[dict] = []
        
    def handle(self, msg: dict) -> None:
        """Update data based on incoming messages."""
        if msg["op"] == 5:
            handleEvent(self, msg["d"])
        elif msg["op"] == 7:
            handleResponse(self, msg["d"])
        elif msg["op"] == 9:
            for response in msg["d"]["results"]:
                handleResponse(self, response)
                
    def generateRequests(self, msgs: dict, data: int) -> list[dict]:
        """Creates request messages to be sent to the OBS server."""
        reqs: list[dict] = []
        for msg in msgs:
            if msg["type"] == "SetSceneItemEnabled":
                for scene in self.scenes:
                    for source in scene.sources:
                        if source.name == msg["target"]:
                            reqs.append({"requestType": msg["type"],
                                         "requestId": next(self.uid),
                                         "requestData": {
                                             "sceneName": scene.name,
                                             "sceneItemId": source.siid,
                                             "sceneItemEnabled": True if data == 1 else False}
                                         })
                            
            elif msg["type"] == "SetCurrentProgramScene":
                target: str = msg["target"]
                if target == "PreviousScene":
                    if self.previousScene != None:
                        target = self.previousScene.name
                    else:
                        print("No previous scene to return to.")
                        continue
                reqs.append({"requestType": msg["type"],
                                         "requestId": next(self.uid),
                                         "requestData": {
                                             "sceneName": target}
                                         })
        return reqs

    def addScene(self, data: dict) -> None:
        """Adds a scene to the container."""
        self.scenes.append(Scene(self.uid, data["sceneName"], data["sceneIndex"]))
        self.requests.append({"op": 6,
                              "d":{
            "requestType": "GetSceneItemList",
            "requestId": data["sceneName"] + "_" + next(self.uid),
            "requestData": {"sceneName": data["sceneName"]}}
                              })

    def removeScene(self, name: str) -> None:
        """Remove a scene from the container."""
        scene: Optional[Scene] = self.getScene(name)
        if scene == None:
            return
        
        self.scenes.remove(scene)

    def getScene(self, name: str) -> Optional["Scene"]:
        """Returns reference to scene called name, if it exists."""
        for scene in self.scenes:
            if scene.name == name:
                return scene
        return None

    def setCurrentScene(self, name: str) -> None:
        """Moves currentScene to previousScene and sets the named scene to current."""
        scene: Optional[Scene] = self.getScene(name)
        if scene == None:
            return
        
        self.previousScene: Optional[Scene] = self.currentScene
        self.currentScene: Optional[Scene] = scene

class Scene:
    """Data container for information pertaining to the current state of a scene."""

    def __init__(self, uid: Generator[str, None, None], name: str, siid: int) -> None:
        """Initializes a scene."""
        self.uid: Generator[str, None, None] = uid
        self.name: str = name
        self.siid: int = siid

        self.sources: list[Source] = []
        
        self.requests: list[dict] = []

    def addSource(self, data: dict) -> None:
        """Adds a source to the source list."""
        self.sources.append(Source(self.uid, data["sourceName"], data["sceneItemId"], data["sceneItemIndex"]))
        self.requests.append({"op": 6,
                              "d":{
            "requestType": "GetSceneItemEnabled",
            "requestId": self.name + "_" + data["sourceName"] + "_" + next(self.uid),
            "requestData": {"sceneName": self.name,
                            "sceneItemId": data["sceneItemId"]}}
                              })
        

    def getSource(self, name: str) -> Optional["Source"]:
        """Returns reference to source called name, if it exists."""
        for source in self.sources:
            if source.name == name:
                return source
        return None


class Source:
    """Data container for information pertaining to the current state of a source."""

    def __init__(self, uid: Generator[str, None, None], name: str, ssid: int, ssin: int) -> None:
        """Initializes a source."""
        self.uid: Generator[str, None, None] = uid
        self.name: str = name
        self.siid: int = ssid
        self.ssin: int = ssin
        
        self.enabled: bool = True #Unknown at instantiation and should be confirmed before reference, but better safe than sorry
        
        self.filters: list[Filter] = []

    def addFilter(self, data: dict) -> None:
        """Adds a filter to the source."""
        ...

    def getFilter(self, name: str) -> Optional["Filter"]:
        """Returns the named filter if present in the source."""
        ...

    def isVisible(self):
        """Returns if the source is visible."""
        return self.enabled

    def setVisible(self, visible: bool) -> None:
        """Sets source visibility."""
        self.enabled = visible


class Filter:
    """Data container for information pertaining to the current state of a filter."""

    def __init__(self, data: dict) -> None:
        """Initializes a filter."""

        self.name: str #TODO: this
        self.settings: dict #TODO: this
        self.type: str #TODO: this
        self.enabled: bool #TODO: this

    def isVisible(self) -> bool:
        """Returns if the filter is visible."""
        ...

    def setVisible(self, visible: bool) -> None:
        """Sets filter visibility."""
        ...
