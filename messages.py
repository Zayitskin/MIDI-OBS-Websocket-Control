from __future__ import annotations #for python3.8 or less


from collections.abc import Generator

from structures import OBS, Scene, Source, Filter

class Request:
    """Structure that represents a request to be sent to OBS."""

    def __init__(self, _id: Generator[str, None, None], data: dict, obs: OBS) -> None:
        """Initializes a request to be sent to OBS."""

        self.id: Generator[str, None, None] = _id
        self.data: dict = data
        self.obs: OBS = obs

    def format(self) -> list[dict]: #type: ignore
        """Returns a list of formatted messages to send to OBS."""

        msgs: list = []
        mtype: str = self.data["type"]

        #Requests from obs-websockets version 4.8.0

        #Configurable Interactions
        if mtype == "showSource":
            msg: dict = {"message-id": next(self.id)}
            msg["request-type"] = "SetSceneItemRender"
            msg["source"] = self.data["target"]
            msg["render"] = True
            msgs.append(msg)

        elif mtype == "hideSource":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = "SetSceneItemRender"
            msg["source"] = self.data["target"]
            msg["render"] = False
            msgs.append(msg)

        elif mtype == "toggleSource":
            source = self.obs.getSource(self.data["target"])
            if source != None:
                msg = {"message-id": next(self.id)}
                msg["request-type"] = "SetSceneItemRender"
                msg["source"] = self.data["target"]
                msg["render"] = not source.isVisible() #type: ignore
                msgs.append(msg)

        elif mtype == "showAllSources":
            if self.obs.currentScene != None:
                for source in self.obs.currentScene.sources: #type: ignore
                    msg = {"message-id": next(self.id)}
                    msg["request-type"] = "SetSceneItemRender"
                    msg["source"] = source.name
                    msg["render"] = True
                    msgs.append(msg)

        elif mtype == "hideAllSources":
            if self.obs.currentScene != None:
                for source in self.obs.currentScene.sources: #type: ignore
                    msg = {"message-id": next(self.id)}
                    msg["request-type"] = "SetSceneItemRender"
                    msg["source"] = source.name
                    msg["render"] = False
                    msgs.append(msg)

        elif mtype == "transitionToScene":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = "SetCurrentScene"
            msg["scene-name"] = self.data["target"]
            msgs.append(msg)

        elif mtype == "transitionToPreviousScene":
            if self.obs.previousScene != None:
                msg = {"message-id": next(self.id)}
                msg["request-type"] = "SetCurrentScene"
                msg["scene-name"] = self.obs.previousScene.name #type: ignore
                msgs.append(msg)

        elif mtype == "showFilter":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = "SetSourceFilterVisibility"
            msg["sourceName"] = self.data["targetSource"]
            msg["filterName"] = self.data["targetFilter"]
            msg["filterEnabled"] = True
            msgs.append(msg)

        elif mtype == "hideFilter":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = "SetSourceFilterVisibility"
            msg["sourceName"] = self.data["targetSource"]
            msg["filterName"] = self.data["targetFilter"]
            msg["filterEnabled"] = False
            msgs.append(msg)

        elif mtype == "toggleFilter":
            source = self.obs.getSource(self.data["targetSource"])
            if source != None:
                _filter = source.getFilter(self.data["targetFilter"]) #type: ignore
                if _filter != None:
                    msg = {"message-id": next(self.id)}
                    msg["request-type"] = "SetSourceFilterVisibility"
                    msg["sourceName"] = self.data["targetSource"]
                    msg["filterName"] = self.data["targetFilter"]
                    msg["filterEnabled"] = not _filter.isVisible() #type: ignore
                    msgs.append(msg)

        elif mtype == "editFilter":
            #TODO: Better arbitrary filter support
            msg = {"message-id": next(self.id)}
            msg["request-type"] = "SetSourceFilterSettings"
            msg["sourceName"] = self.data["targetSource"]
            msg["filterName"] = self.data["targetFilter"]
            value = self.data["data"]
            if self.data["targetSetting"] == "hue_shift":
                value = (((value - 0) * (180 - -180)) / (127 - 0)) + -180
            msg["filterSettings"] = {self.data["targetSetting"]: value}
            msgs.append(msg)

        #General Requests
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

        elif mtype == "OpenProjector":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "TriggerHotkeyByName":
            #Unreleased
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "TriggerHotkeyBySequence":
            #Unreleased
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        #Media Control
        elif mtype == "PlayPauseMedia":
            #Unreleased
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "RestartMedia":
            #Unreleased
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "StopMedia":
            #Unreleased
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "NextMedia":
            #Unreleased
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "PreviousMedia":
            #Unreleased
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "GetMediaDuration":
            #Unreleased
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "GetMediaTime":
            #Unreleased
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "SetMediaTime":
            #Unreleased
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "ScrubMedia":
            #Unreleased
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "GetMediaState":
            #Unreleased
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        #Sources
        elif mtype == "GetMediaSourcesList":
            #Unreleased
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

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

        elif mtype == "GetAudioActive":
            #Unreleased
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "SetSourceName":
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
            msg["sourceName"] = self.data["target"]
            msgs.append(msg)

        elif mtype == "GetSourceFilterInfo":
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

        elif mtype == "SetSourceFilterVisibility":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "GetAudioMonitorType":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "SetAudioMonitorType":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "TakeSourceScreenshot":
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
        elif mtype == "GetRecordingStatus":
            #Unreleased
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

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
        elif mtype == "GetReplayBufferStatus":
            #Unreleased
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

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

        #Scene Collections
        elif mtype == "SetCurrentSceneCollection":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
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
        elif mtype == "GetSceneItemList":
            #Unreleased
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "GetSceneItemProperties":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "SetSceneItemProperties":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
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

        elif mtype == "AddSceneItem":
            #Unreleased
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

        elif mtype == "CreateScene":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "ReorderSceneItems":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "SetSceneTransitionOverride":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "RemoveSceneTransitionOverride":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        elif mtype == "GetSceneTransitionOverride":
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

        elif mtype == "GetTransitionPosition":
            msg = {"message-id": next(self.id)}
            msg["request-type"] = mtype
            #msgs.append(msg)

        else:
            print(f"Unknown request with type {mtype}.")

        return msgs

class Response:
    """Structure that handles responses from OBS."""

    def __init__(self, data: dict, obs: OBS) -> None:
        """Initializes a response to handle a message from OBS."""

        self.data: dict = data
        self.obs: OBS = obs

    def handle(self) -> None:
        """Updates the state of the OBS container according to the response."""

        if self.data.get("message-id") != None:
            if self.data["status"] == "error":
                print(self.data["error"])
                return
            else:
                requestData = self.obs.pendingResponses.pop(self.data["message-id"])
                request = requestData["request-type"]
                #Requests as of version 4.8.0

                #General
                if request == "GetVersion":
                    pass

                elif request == "GetAuthRequired":
                    pass

                elif request == "Authenticate":
                    pass

                elif request == "SetHeartbeat":
                    #To be removed in 5.0.0
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

                elif request == "OpenProjector":
                    pass

                elif request == "TriggerHotkeyByName":
                    #Unreleased
                    pass

                elif request == "TriggerHotkeyBySequence":
                    #Unreleased
                    pass

                #Media Control
                elif request == "PlayPauseMedia":
                    #Unreleased
                    pass

                elif request == "RestartMedia":
                    #Unreleased
                    pass

                elif request == "StopMedia":
                    #Unreleased
                    pass

                elif request == "NextMedia":
                    #Unreleased
                    pass

                elif request == "PreviousMedia":
                    #Unreleased
                    pass

                elif request == "GetMediaDuration":
                    #Unreleased
                    pass

                elif request == "GetMediaTime":
                    #Unreleased
                    pass

                elif request == "SetMediaTime":
                    #Unreleased
                    pass

                elif request == "ScrubMedia":
                    #Unreleased
                    pass

                elif request == "GetMediaState":
                    #Unreleased
                    pass

                #Sources

                elif request == "GetMediaSourcesList":
                    #Unreleased
                    pass

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

                elif request == "GetAudioActive":
                    pass

                elif request == "SetSourceName":
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
                    source = self.obs.getSource(requestData["sourceName"])
                    if source != None:
                        for _filter in self.data["filters"]:
                            source.addFilter(_filter) #type: ignore

                elif request == "GetSourceFilterInfo":
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

                elif request == "SetSourceFilterVisibility":
                    pass
                
                elif request == "GetAudioMonitorType":
                    pass

                elif request == "SetAudioMonitorType":
                    pass

                elif request == "TakeSourceScreenshot":
                    pass

                #Outpute
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
                elif request == "GetRecordingStatus":
                    #Unreleased
                    pass

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
                elif request == "GetReplayBufferStatus":
                    #Unreleased
                    pass

                elif request == "StartStopReplayBuffer":
                    pass

                elif request == "StartReplayBuffer":
                    pass

                elif request == "StopReplayBuffer":
                    pass

                elif request == "SaveReplayBuffer":
                    pass

                #Scene Collections
                elif request == "SetCurrentSceneCollection":
                    pass

                elif request == "GetCurrentSceneCollection":
                    pass

                elif request == "ListSceneCollections":
                    pass

                #Scene Items
                elif request == "GetSceneItemList":
                    #Unreleased
                    pass

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

                elif request == "AddSceneItem":
                    #Unreleased
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

                elif request == "CreateScene":
                    pass

                elif request == "ReorderSceneItems":
                    pass

                elif request == "SetSceneTransitionOverride":
                    pass

                elif request == "RemoveSceneTransitionOverride":
                    pass

                elif request == "GetSceneTransitionOverride":
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

                elif request == "GetTransitionPosition":
                    pass

                else:
                    print(f"Unhandled response of type {request} and data {self.data}.")

                

        else:
            event: str = self.data["update-type"]
            #Events as of 4.8.0

            #Scenes
            if event == "SwitchScenes":
                self.obs.setCurrentScene(self.data["scene-name"])

            elif event == "ScenesChanged":
                #self.obs.purgeScenes()
                pass

            elif event == "SceneCollectionChanged":
                pass

            elif event == "SceneCollectionListChanged":
                pass

            #Transitions
            elif event == "SwitchTransition":
                pass

            elif event == "TransitionListChanged":
                pass

            elif event == "TransitionDurationChanged":
                pass

            elif event == "TransitionBegin":
                pass

            elif event == "TransitionEnd":
                pass

            elif event == "TransitionVideoEnd":
                pass

            #Profiles
            elif event == "ProfileChanged":
                pass

            elif event == "ProfileListChanged":
                pass

            #Streaming
            elif event == "StreamStarting":
                pass

            elif event == "StreamStarted":
                pass

            elif event == "StreamStopping":
                pass

            elif event == "StreamStopped":
                pass

            elif event == "StreamStatus":
                pass

            #Recording
            elif event == "RecordingStarting":
                pass

            elif event == "RecordingStarted":
                pass

            elif event == "RecordingStopping":
                pass

            elif event == "RecordingStopped":
                pass

            elif event == "RecordingPaused":
                pass

            elif event == "RecordingResumed":
                pass

            #Replay Buffer
            elif event == "ReplayStarting":
                pass

            elif event == "ReplayStarted":
                pass

            elif event == "ReplayStopping":
                pass

            elif event == "ReplayStopped":
                pass

            #Other
            elif event == "Exiting":
                pass

            #General
            elif event == "Heartbeat":
                pass

            elif event == "BroadcastCustomMessage":
                pass

            #Sources
            elif event == "SourceCreated":
                pass

            elif event == "SourceDestroyed":
                pass

            elif event == "SourceVolumeChanged":
                pass

            elif event == "SourceMuteStateChanged":
                pass

            elif event == "SourceAudioDeactivated":
                #Unreleased
                pass

            elif event == "SourceAudioActivated":
                #Unreleased
                pass

            elif event == "SourceAudioSyncOffsetChanged":
                pass

            elif event == "SourceAudioMixersChanged":
                pass

            elif event == "SourceRenamed":
                pass

            elif event == "SourceFilterAdded":
                pass

            elif event == "SourceFilterRemoved":
                pass

            elif event == "SourceFilterVisibilityChanged":
                source = self.obs.getSource(self.data["sourceName"])
                if source != None:
                    _filter = source.getFilter(self.data["filterName"]) #type: ignore
                    if _filter != None:
                        _filter.setVisible(self.data["filterEnabled"]) #type: ignore

            elif event == "SourceFiltersReordered":
                pass

            #Media
            elif event == "MediaPlaying":
                #Unreleased
                pass

            elif event == "MediaPaused":
                #Unreleased
                pass

            elif event == "MediaRestarted":
                #Unreleased
                pass

            elif event == "MediaStopped":
                #Unreleased
                pass

            elif event == "MediaNext":
                #Unreleased
                pass

            elif event == "MediaPrevious":
                #Unreleased
                pass

            elif event == "MediaStarted":
                #Unreleased
                pass

            elif event == "MediaEnded":
                #Unreleased
                pass

            #Scene Items
            elif event == "SceneItemOrderChanged":
                pass

            elif event == "SceneItemAdded":
                pass

            elif event == "SceneItemRemoved":
                pass

            elif event == "SceneItemVisibilityChanged":
                scene = self.obs.getScene(self.data["scene-name"])
                if scene != None:
                    source = scene.getSource(self.data["item-name"]) #type: ignore
                    if source != None:
                        source.setVisible(self.data["item-visible"]) #type: ignore
                        

            elif event == "SceneItemLockChanged":
                pass

            elif event == "SceneItemTransformChanged":
                pass

            elif event == "SceneItemSelected":
                pass

            elif event == "SceneItemDeselected":
                pass

            #Studio Mode
            elif event == "PreviewSceneChanged":
                pass

            elif event == "StudioModeSwitched":
                pass

            #Unhandled Events
            else:
                print("Unhandled event with data: " + str(self.data))
