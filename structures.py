from __future__ import annotations #for python3.8 or less

from typing import Optional

class OBS:
    """Data container for information pertaining to the current state of OBS."""

    def __init__(self) -> None:
        """Initializes the OBS container"""

        self.scenes: list[Scene] = [] #type: ignore

        self.currentScene: Optional[Scene] = None
        self.previousScene: Optional[Scene] = None

        self.requests: list = []
        self.pendingResponses: dict = {}

    def addScene(self, data: dict) -> None:
        """Adds a scene to the container."""

        scene = Scene(data)

        for source in scene.sources:
            self.requests.append({
                "type": "GetSourceFilters",
                "target": source.name,
                })

        self.scenes.append(scene)

    def removeScene(self, name: str) -> None:
        """Remove a scene from the container."""

        for scene in self.scenes:
            if scene.name == name:
                self.scenes.remove(scene)
                return

    def purgeScenes(self) -> None:
        """Remove all scenes from the container"""


        print("\n\nPurging scenes!\n\n")

        self.scenes = []
        self.requests.append({"type": "GetSceneList"})

    def getScene(self, name: str) -> Optional["Scene"]:
        """Returns reference to scene called name, if it exists."""

        for scene in self.scenes:
            if scene.name == name:
                return scene
        return None

    def getSource(self, name: str) -> Optional["Source"]:
        """Returns reference to source in active, if it exists."""

        for source in self.currentScene.sources:
            if source.name == name:
                return source
        return None
        #TODO: Search in non-current scene

    def setCurrentScene(self, name: str) -> None:
        """Moves currentScene to previousScene and sets the named scene to current."""

        for scene in self.scenes:
            if scene.name == name:
                self.previousScene = self.currentScene
                self.currentScene = scene
                return

class Scene:
    """Data container for information pertaining to the current state of a scene."""

    def __init__(self, data: dict) -> None:
        """Initializes a scene."""

        self.name: str = data["name"]
        self.sources: list[Source] = [] #type: ignore

        for source in data["sources"]:
            self.addSource(source)

    def addSource(self, data: dict) -> None:
        """Adds a source to the source list."""

        self.sources.append(Source(data))

    def getSource(self, name: str) -> Optional["Source"]:
        """Returns reference to source called name, if it exists."""

        for source in self.sources:
            if source.name == name:
                return source
        return None

class Source:
    """Data container for information pertaining to the current state of a source."""

    def __init__(self, data: dict) -> None:
        """Initializes a source."""

        self.name: str = data["name"]
        self.data: dict = data
        self.filters: list[Filter] = [] #type: ignore

    def addFilter(self, data: dict) -> None:
        """Adds a filter to the source."""

        self.filters.append(Filter(data))

    def getFilter(self, name: str) -> Optional["Filter"]:
        """Returns the named filter if present in the source."""

        for _filter in self.filters:
            if _filter.name == name:
                return _filter
        return None

    def isVisible(self) -> bool:
        """Returns if the source is visible."""

        return self.data["render"]

    def setVisible(self, visible: bool) -> None:
        """Sets source visibility."""

        self.data["render"] = visible

class Filter:
    """Data container for information pertaining to the current state of a filter."""

    def __init__(self, data: dict) -> None:
        """Initializes a filter."""

        self.name: str = data["name"]
        self.settings: dict = data["settings"]
        self.type: str = data["type"]
        self.enabled: bool = data["enabled"]

    def isVisible(self) -> bool:
        """Returns if the filter is visible."""

        return self.enabled

    def setVisible(self, visible: bool) -> None:
        """Sets filter visibility."""

        self.enabled = visible

        

        
