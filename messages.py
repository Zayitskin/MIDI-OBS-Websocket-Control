from typing import Union
from collections.abc import Generator

from structures import OBS, Scene

class Request:
    """Structure that represents a request to be sent to OBS."""

    def __init__(self, _id: Generator[str, None, None], data: dict, obs: OBS) -> None:
        """
        Initializes a request to be sent to OBS.

        id: generator for producing unique integers for each request
        data: dict containing the type of request and all necessary information
        obs: the OBS container for ensuring parity between script and OBS
        """
        
        self.id = _id
        self.data = data
        self.obs = obs

    def format(self) -> Union[list[dict], None]:
        """
        Returns a series of messages formatted to be sent to OBS
        via the websocket. All custom requests begin with a
        lower-case letter, while the websocket library requests
        begin with an upper-case letter.
        """
        
        msgs = []
        mtype = self.data["type"]

        #Custom Requests
        #Common requests to be used in the settings file
        
        #SceneCollection

        #Scene

        if mtype == "transitionToScene":
            msg: dict = {"message-id": next(self.id)}
            msg["request-type"] = "SetCurrentScene"
            msg["scene-name"] = self.data["target"]
            msgs.append(msg)

        elif mtype == "transitionToPreviousScene":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = "SetCurrentScene"
            if self.obs.previousScene != None:
                #Assertion to make mypy happy
                assert isinstance(self.obs.previousScene, Scene)
                msg["scene-name"] = self.obs.previousScene.name
            else:
                print("No previous scene to transition to.")
                return None
            msgs.append(msg)

        elif mtype == "hideAllSources":
            if self.obs.currentScene != None:
                #Assertion to make mypy happy
                assert isinstance(self.obs.currentScene, Scene)
                for target in self.obs.currentScene.getAllSceneItems():
                    msg = {"message-id": next(self.id)}
                    msg["request-type"] = "SetSceneItemProperties"
                    msg["item"] = target.name
                    msg["visible"] = False
                    msgs.append(msg)

        elif mtype == "showAllSources":
            if self.obs.currentScene != None:
                #Assertion to make mypy happy
                assert isinstance(self.obs.currentScene, Scene)
                for target in self.obs.currentScene.getAllSceneItems():
                    msg = {"message-id": next(self.id)}
                    msg["request-type"] = "SetSceneItemProperties"
                    msg["item"] = target.name
                    msg["visible"] = True
                    msgs.append(msg)

        #Source

        elif mtype == "hideSource":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = "SetSceneItemProperties"
            msg["item"] = self.data["target"]
            msg["visible"] = False
            msgs.append(msg)

        elif mtype == "showSource":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = "SetSceneItemProperties"
            msg["item"] = self.data["target"]
            msg["visible"] = True
            msgs.append(msg)

        elif mtype == "toggleSource":
            if self.obs.currentScene != None:
                #Assertion to make mypy happy
                assert isinstance(self.obs.currentScene, Scene)
                msg = {"message-id": next(self.id)}
                msg["request-type"] = "SetSceneItemProperties"
                msg["item"] = self.data["target"]
                msg["visible"] = not self.obs.currentScene.sceneItems[self.data["target"]].isVisible()
                msgs.append(msg)

        #Filter

        #Transition

        #OBS Websocket Requests
        #Full request list for the OBS Websocket library
        #DO NOT INVOKE IN THE SETTINGS UNLESS YOU KNOW WHAT YOU ARE DOING!
        #Requests with commented out msgs.append are not yet implemented

        #General
        elif mtype == "GetVersion":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "GetAuthRequired":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "Authenticate":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "SetHeartbeat":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "SetFilenameFormatting":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "GetFilenameFormatting":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "GetStats":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "BroadcastCustomMessage":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "GetVideoInfo":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        #Outputs
        elif mtype == "ListOutputs":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "GetOutputInfo":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "StartOutput":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "StopOutput":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        #Profiles
        elif mtype == "SetCurrentProfile":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "GetCurrentProfile":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "ListProfiles":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        #Recording
        elif mtype == "StartStopRecording":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "StartRecording":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "StopRecording":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "PauseRecording":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "ResumeRecording":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "SetRecordingFolder":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "GetRecordingFolder":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        #Replay Buffer
        elif mtype == "StartStopReplayBuffer":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "StartReplayBuffer":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "StopReplayBuffer":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "SaveReplayBuffer":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        #SceneCollections
        elif mtype == "SetCurrentSceneCollection":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            msg["sc-name"] = self.data["sc-name"]
            #msgs.append(msg)

        elif mtype == "GetCurrentSceneCollection":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "ListSceneCollections":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        #Scene Items
        elif mtype == "GetSceneItemProperties":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            msg["item"] = self.data["item"]
            #msgs.append(msg)

        elif mtype == "SetSceneItemProperties":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            msg.update(self.data["updates"])
            #msgs.append(msg)

        elif mtype == "ResetSceneItem":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "SetSceneItemRender":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "SetSceneItemPosition":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "SetSceneItemTransform":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "SetSceneItemCrop":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "DeleteSceneItem":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "DuplicateSceneItem":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        #Scenes
        elif mtype == "SetCurrentScene":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "GetCurrentScene":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            msgs.append(msg)

        elif mtype == "GetSceneList":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            msgs.append(msg)

        elif mtype == "ReorderSceneItems":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        #Sources
        elif mtype == "GetSourcesList":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "GetSourceTypesList":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "GetVolume":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "SetVolume":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "GetMute":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "SetMute":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "ToggleMute":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "SetSyncOffset":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "GetSyncOffset":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "GetSourceSettings":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "SetSourceSettings":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "GetTextGDIPlusProperties":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "SetTextGDIPlusProperties":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "GetTextFreetype2Properties":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "SetTextFreetype2Properties":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "GetBrowserSourceProperties":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "SetBrowserSourceProperties":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "GetSpecialSources":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "GetSourceFilters":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "AddFilterToSource":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "RemoveFilterFromSource":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "ReorderSourceFilter":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "MoveSourceFilter":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "SetSourceFilterSettings":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "TakeSourceScreenshot":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        #Streaming
        elif mtype == "GetStreamingStatus":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "StartStopStreaming":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "StartStreaming":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "StopStreaming":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "SetStreamSettings":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "GetStreamSettings":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "SaveStreamSettings":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "SendCaptions":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        #Studio Mode
        elif mtype == "GetStudioModeStatus":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "GetPreviewScene":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "SetPreviewScene":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "TransitionToProgram":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "EnableStudioMode":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "DisableStudioMode":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "ToggleStudioMode":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        #Transitions
        elif mtype == "GetTransitionList":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "GetCurrentTransition":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "SetCurrentTransition":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "SetTransitionDuration":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "GetTransitionDuration":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)


        else:
            print("Malformed request data: " + str(self.data))
            return None

        return msgs

class Response:
    """Structure that handles repsonses from OBS"""

    def __init__(self, data: dict, obs: OBS) -> None:
        """
        Initializes a response to handle a message from OBS.

        data: dict of the information received from OBS
        obs: the OBS container for ensuring parity between script and OBS
        """
        
        self.data = data
        self.obs = obs

    def handle(self) -> None:
        """Updates the state of the OBS container according to the response."""

        if self.data.get("message-id") != None:
            if self.data["status"] == "error":
                print(self.data["error"])
                return
            else:
                request = self.obs.requests.pop(self.data["message-id"])
                #Responses
                #General
                if request == "GetVersion":
                    pass

                elif request == "GetAuthRequired":
                    pass

                elif request == "Authenticate":
                    pass

                elif request == "SetHeartbeat":
                    pass

                elif request == "SetFilenameFormatting":
                    pass

                elif request == "GetFilenameFormatting":
                    pass

                elif request == "GetStats":
                    pass

                elif request == "BroadcastCustomMessage":
                    pass

                elif request == "GetVideoInfo":
                    pass

                #Outputs
                elif request == "ListOutputs":
                    pass

                elif request == "GetOutputInfo":
                    pass

                elif request == "StartOutput":
                    pass

                elif request == "StopOutput":
                    pass

                #Profiles
                elif request == "SetCurrentProfile":
                    pass

                elif request == "GetCurrentProfile":
                    pass

                elif request == "ListProfiles":
                    pass

                #Recording
                elif request == "StartStopRecording":
                    pass

                elif request == "StartRecording":
                    pass

                elif request == "StopRecording":
                    pass

                elif request == "PauseRecording":
                    pass

                elif request == "ResumeRecording":
                    pass

                elif request == "SetRecordingFolder":
                    pass

                elif request == "GetRecordingFolder":
                    pass

                #Replay Buffer
                elif request == "StartStopReplayBuffer":
                    pass

                elif request == "StartReplayBuffer":
                    pass

                elif request == "StopReplayBuffer":
                    pass

                elif request == "SaveReplayBuffer":
                    pass

                #SceneCollections
                elif request == "SetCurrentSceneCollection":
                    pass

                elif request == "GetCurrentSceneCollection":
                    pass

                elif request == "ListSceneCollections":
                    pass

                #SceneItems
                elif request == "GetSceneItemProperties":
                    pass

                elif request == "SetSceneItemProperties":
                    pass

                elif request == "ResetSceneItem":
                    pass

                elif request == "SetSceneItemRender":
                    pass

                elif request == "SetSceneItemPosition":
                    pass

                elif request == "SetSceneItemTransform":
                    pass

                elif request == "SetSceneItemCrop":
                    pass

                elif request == "DeleteSceneItem":
                    pass

                elif request == "DuplicateSceneItem":
                    pass

                #Scenes
                elif request == "SetCurrentScene":
                    pass

                elif request == "GetCurrentScene":
                    self.obs.setCurrentScene(self.data["name"])

                elif request == "GetSceneList":
                    for scene in self.data["scenes"]:
                        self.obs.addScene(scene)
                    self.obs.setCurrentScene(self.data["current-scene"])

                elif request == "ReorderSceneItems":
                    pass

                #Sources
                elif request == "GetSourcesList":
                    pass

                elif request == "GetSourceTypesList":
                    pass

                elif request == "GetVolume":
                    pass

                elif request == "SetVolume":
                    pass

                elif request == "GetMute":
                    pass

                elif request == "SetMute":
                    pass

                elif request == "ToggleMute":
                    pass

                elif request == "SetSyncOffset":
                    pass

                elif request == "GetSyncOffset":
                    pass

                elif request == "GetSourceSettings":
                    pass

                elif request == "SetSourceSettings":
                    pass

                elif request == "GetTextGDIPlusProperties":
                    pass

                elif request == "SetTextGDIPlusProperties":
                    pass

                elif request == "GetTextFreetype2Properties":
                    pass

                elif request == "SetTextFreetype2Properties":
                    pass

                elif request == "GetBrowserSourceProperties":
                    pass

                elif request == "SetBrowserSourceProperties":
                    pass

                elif request == "GetSpecialSources":
                    pass

                elif request == "GetSourceFilters":
                    pass

                elif request == "AddFilterToSource":
                    pass

                elif request == "RemoveFilterFromSource":
                    pass

                elif request == "ReorderSourceFilter":
                    pass

                elif request == "MoveSourceFilter":
                    pass

                elif request == "SetSourceFilterSettings":
                    pass

                elif request == "TakeSourceScreenshot":
                    pass

                #Streaming
                elif request == "GetStreamingStatus":
                    pass

                elif request == "StartStopStreaming":
                    pass

                elif request == "StartStreaming":
                    pass

                elif request == "StopStreaming":
                    pass

                elif request == "SetStreamSettings":
                    pass

                elif request == "GetStreamSettings":
                    pass

                elif request == "SaveStreamSettings":
                    pass

                elif request == "SendCaptions":
                    pass

                #Studio Mode
                elif request == "GetStudioModeStatus":
                    pass

                elif request == "GetPreviewScene":
                    pass

                elif request == "SetPreviewScene":
                    pass

                elif request == "TransitionToProgram":
                    pass

                elif request == "EnableStudioMode":
                    pass

                elif request == "DisableStudioMode":
                    pass

                elif request == "ToggleStudioMode":
                    pass

                #Transitions
                elif request == "GetTransitionList":
                    pass

                elif request == "GetCurrentTransition":
                    pass

                elif request == "SetCurrentTransition":
                    pass

                elif request == "SetTransitionDuration":
                    pass

                elif request == "GetTransitionDuration":
                    pass

                else:
                    print("Malformed response data:\ntype: " + str(request) + "\ndata: " + str(self.data))
            
        else:
            #Events
            #Scenes
            if self.data["update-type"] == "SwitchScenes":
                self.obs.setCurrentScene(self.data["scene-name"])
            
            elif self.data["update-type"] == "ScenesChanged":
                pass

            elif self.data["update-type"] == "SceneCollectionChanged":
                pass

            elif self.data["update-type"] == "SceneCollectionListChanged":
                pass

            #Transitions
            elif self.data["update-type"] == "SwitchTransition":
                pass

            elif self.data["update-type"] == "TransitionListedChanged":
                pass

            elif self.data["update-type"] == "TransitionDurationChanged":
                pass

            elif self.data["update-type"] == "TransitionBegin":
                pass

            #Profiles
            elif self.data["update-type"] == "ProfileChanged":
                pass

            elif self.data["update-type"] == "ProfileListChanged":
                pass

            #Streaming
            elif self.data["update-type"] == "StreamStarting":
                pass

            elif self.data["update-type"] == "StreamStarted":
                pass

            elif self.data["update-type"] == "StreamStopping":
                pass

            elif self.data["update-type"] == "StreamStopped":
                pass

            elif self.data["update-type"] == "StreamStatus":
                pass

            #Recording
            elif self.data["update-type"] == "RecordingStarting":
                pass

            elif self.data["update-type"] == "RecordingStarted":
                pass

            elif self.data["update-type"] == "RecordingStopping":
                pass

            elif self.data["update-type"] == "RecordingStopped":
                pass

            elif self.data["update-type"] == "RecordingPaused":
                pass

            elif self.data["update-type"] == "RecordingResumed":
                pass

            #Replay Buffer
            elif self.data["update-type"] == "ReplayStarting":
                pass

            elif self.data["update-type"] == "ReplayStarted":
                pass

            elif self.data["update-type"] == "ReplayStopping":
                pass

            elif self.data["update-type"] == "ReplayStopped":
                pass

            #Other
            elif self.data["update-type"] == "Exiting":
                pass

            #General
            elif self.data["update-type"] == "Heartbeat":
                pass

            elif self.data["update-type"] == "BroadcastCustomMessage":
                pass

            #Sources
            elif self.data["update-type"] == "SourceCreated":
                pass

            elif self.data["update-type"] == "SourceDestroyed":
                pass

            elif self.data["update-type"] == "SourceVolumeChanged":
                pass

            elif self.data["update-type"] == "SourceMuteStateChanged":
                pass

            elif self.data["update-type"] == "SourceAudioSyncOffsetChanged":
                pass

            elif self.data["update-type"] == "SourceAudioMixersChanged":
                pass

            elif self.data["update-type"] == "SourceRenamed":
                pass

            elif self.data["update-type"] == "SourceFilterAdded":
                pass

            elif self.data["update-type"] == "SourceFilterRemoved":
                pass

            elif self.data["update-type"] == "SourceFiltersReordered":
                pass

            elif self.data["update-type"] == "SourceOrderChanged":
                pass

            elif self.data["update-type"] == "SceneItemAdded":
                pass

            elif self.data["update-type"] == "SceneItemRemoved":
                pass

            elif self.data["update-type"] == "SceneItemVisibilityChanged":
                self.obs.scenes[self.data["scene-name"]].sceneItems[self.data["item-name"]].data["render"] = self.data["item-visible"]

            elif self.data["update-type"] == "SceneItemTransformChanged":
                pass

            elif self.data["update-type"] == "SceneItemSelected":
                pass

            elif self.data["update-type"] == "SceneItemDeselected":
                pass

            #Studio Mode
            elif self.data["update-type"] == "PreviewSceneChange":
                pass

            elif self.data["update-type"] == "StudioModeSwitched":
                pass

            #Unhandled Events
            else:
                print("Unhandled event with data: " + str(self.data))
