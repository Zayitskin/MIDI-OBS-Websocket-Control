from typing import Union, Optional

class OBS:
    """Container that holds information regarding the current state of OBS."""

    def __init__(self) -> None:
        """Initializes an OBS container."""

        self.scenes: dict = {}
        self.currentScene: Union[Scene, None] = None
        self.previousScene: Union[Scene, None] = None

        self.requests: dict = {}
        self.updates: list = []

    def clearScenes(self) -> None:
        """Removes all scenes and resets current and previous scene to None."""
        
        self.scenes = {}
        self.currentScene = None
        self.previousScene = None

    def addScene(self, scene: dict) -> None:
        """
        Adds new Scene with all SceneItems.

        scene: a dict that contains a:
            name - str
            sources - list of dicts that define SceneItems
        """

        name = scene["name"]
        self.scenes[name] = Scene(name)
        for sceneItem in scene["sources"]:
            self.scenes[name].addSceneItem(sceneItem)
            self.updates.append({"type": "GetSourceFilters", "target": sceneItem["name"]})
        

    def setCurrentScene(self, scene: str) -> None:
        """Updates previousScene to currentScene and sets currentScene to Scene."""

        if self.scenes.get(scene) == None:
            print("No Scene with name: " + scene)
        else:
            self.previousScene = self.currentScene
            self.currentScene = self.scenes[scene]

    def getSceneItem(self, name: str) -> Optional["SceneItem"]:
        """Returns the SceneItem with the requested name."""

        for scene in self.scenes:
            for sceneItem in self.scenes[scene].sceneItems:
                if sceneItem == name:
                    return self.scenes[scene].sceneItems[sceneItem]
        return None

class SceneCollection:
    """Container that holds information regarding a Scene Collection."""

    def __init__(self, name: str) -> None:
        """
        Initializes a SceneCollection.

        name - str name of Scene Collection
        """

        self.name = name  

class Scene:
    """Container that holds information regarding a Scene."""

    def __init__(self, name: str) -> None:
        """
        Initializes a Scene.

        name - str name of Scene
        """
        

        self.name = name
        self.sceneItems: dict = {}

    def addSceneItem(self, sceneItem: dict) -> None:
        """
        Adds a new SceneItem with all data.

        sceneItem: a dict that contains a name str and other sceneItem data
        """

        self.sceneItems[sceneItem["name"]] = SceneItem(sceneItem)

    def getAllSceneItems(self) -> list["SceneItem"]:
        """Returns list of all SceneItems in Scene."""

        sceneItems = []
        for key in self.sceneItems.keys():
            sceneItems.append(self.sceneItems[key])
        return sceneItems

class SceneItem:
    """Container that hold information regarding a SceneItem."""

    def __init__(self, data: dict) -> None:
        """Initializes a SceneItem from a dict."""

        self.name = data["name"]
        self.data = data
        self.filters: list = []

    def isVisible(self) -> bool:
        """Returns if the SceneItem is visible in OBS."""

        return self.data["render"]

    def addFilter(self, _filter: dict) -> None:
        """Adds a filter to the list of filters."""

        self.filters.append(Filter(_filter))

    def getFilter(self, filterName: str) -> Optional["Filter"]:
        """Returns the filter with name filterName."""

        for _filter in self.filters:
            if _filter.name == filterName:
                return _filter
        return None

class Filter:
    """Container that holds information regarding a Filter."""

    def __init__(self, data:dict) -> None:

        self.name = data["name"]
        self.settings = data["settings"]
        self.type = data["type"]
        self.enabled = data["enabled"]
