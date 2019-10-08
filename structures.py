

class OBS:

    def __init__(self):

        self.scenes = {}
        self.currentScene = None
        self.previousScene = None

        self.requests = {}

    def clearScenes(self):
        
        self.scenes = {}
        self.currentScene = None
        self.previousScene = None

    def addScene(self, scene):

        name = scene["name"]
        self.scenes[name] = Scene(name)
        for sceneItem in scene["sources"]:
            self.scenes[name].addSceneItem(sceneItem)
        

    def setCurrentScene(self, scene):

        if self.scenes.get(scene) == None:
            print("No Scene with name: " + scene)
        else:
            self.previousScene = self.currentScene
            self.currentScene = self.scenes[scene]

class SceneCollection:

    def __init__(self, name):

        self.name = name  

class Scene:

    def __init__(self, name):

        self.name = name
        self.sceneItems = {}

    def addSceneItem(self, sceneItem):

        self.sceneItems[sceneItem["name"]] = SceneItem(sceneItem)

    def getAllSceneItems(self):

        sceneItems = []
        for key in self.sceneItems.keys():
            sceneItems.append(self.sceneItems[key])
        return sceneItems

class SceneItem:

    def __init__(self, data):

        self.name = data["name"]
        self.data = data

    def isVisible(self):

        return self.data["render"]
