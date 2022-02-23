from __future__ import annotations #for python3.9 and less

def handleEvent(obs: "OBS", msg: dict) -> None:
    
    mtype: str = msg["eventType"]
    data: dict = msg["eventData"]
    
    #General
    
    if mtype == "ExitStarted":
        pass
    
    elif mtype == "VendorEvent":
        pass
    
    #Config
    
    elif mtype == "CurrentSceneCollectionChanging":
        self.obs.locked = True
    
    elif mtype == "CurrentSceneCollectionChanged":
        self.obs.locked = False
    
    elif mtype == "SceneCollectionListChanged":
        pass
    
    elif mtype == "CurrentProfileChanging":
        self.obs.locked = True #May be unnecessary
    
    elif mtype == "CurrentProfileChanged":
        self.obs.locked = False #May be unnecessary
    
    elif mtype == "ProfileListChanged":
        pass
    
    #Scenes
    
    elif mtype == "SceneCreated":
        pass
    
    elif mtype == "SceneRemoved":
        pass
    
    elif mtype == "SceneNameChanged":
        pass
    
    elif mtype == "CurrentProgramSceneChanged":
        obs.setCurrentScene(data["sceneName"])
        for source in obs.currentScene.sources:
            for watch in obs.watches:
                if source.name == watch.name:
                    watch.triggered = True
                    watch.data = "1" if source.enabled else "0"
                    
    
    elif mtype == "CurrentPreviewSceneChanged":
        pass
    
    elif mtype == "SceneListChanged":
        pass
    
    #Inputs
    
    elif mtype == "InputCreated":
        pass
    
    elif mtype == "InputRemoved":
        pass
    
    elif mtype == "InputNameChanged":
        pass
    
    elif mtype == "InputActiveStateChanged":
        pass
    
    elif mtype == "InputShowStateChanged":
        pass
    
    elif mtype == "InputMuteStateChanged":
        pass
    
    elif mtype == "InputVolumeChanged":
        pass
    
    elif mtype == "InputAudioBalanceChanged":
        pass
    
    elif mtype == "InputAudioSyncOffsetChanged":
        pass
    
    elif mtype == "InputAudioTracksChanged":
        pass
    
    elif mtype == "InputAudioMonitorTypeChanged":
        pass
    
    elif mtype == "InputVolumeMeters":
        pass
    
    #Scene Items
    
    elif mtype == "SceneItemCreated":
        pass
    
    elif mtype == "SceneItemRemoved":
        pass
    
    elif mtype == "SceneItemListReindexed":
        pass
    
    elif mtype == "SceneItemEnableStateChanged":
        pass
    
    elif mtype == "SceneItemLockStateChanged":
        pass
    
    elif mtype == "SceneItemTransformChanged":
        pass
    
    #Outputs
    
    elif mtype == "StreamStateChanged":
        pass
    
    elif mtype == "RecordStateChanged":
        pass
    
    elif mtype == "ReplayBufferStateChanged":
        pass    
    
    elif mtype == "VirtualcamStateChanged":
        pass    
    
    elif mtype == "ReplayBufferSaved":
        pass    
    
    #Media Inputs
    
    elif mtype == "MediaInputPlaybackStarted":
        pass    
    
    elif mtype == "MediaInputPlaybackEnded":
        pass
    
    elif mtype == "MediaInputActionTriggered":
        pass
    
    #UI
    
    elif mtype == "StudioModeStateChanged":
        pass
    
    else:
        print(f"Unknown event of type {mtype}.")
        
    
def handleResponse(obs: "OBS", msg: dict) -> None:
    
    mtype: str = msg["requestType"]
    try:
        data: Optional[dict] = msg["responseData"]
    except KeyError:
        data = None
    rid: str = msg["requestId"]
    
    #General
    
    if mtype == "GetVersion":
        pass
    
    elif mtype == "GetStats":
        pass
    
    elif mtype == "BroadcastCustomEvent":
        pass
    
    elif mtype == "CallVendorRequest":
        pass
    
    elif mtype == "GetHotkeyList":
        pass
    
    elif mtype == "TriggerHotkeyByName":
        pass
    
    elif mtype == "TriggerHotkeyByKeySequence":
        pass
    
    elif mtype == "Sleep":
        pass
    
    #Config
    
    elif mtype == "GetPersistentData":
        pass
    
    elif mtype == "SetPersistentData":
        pass
    
    elif mtype == "GetSceneCollectionList":
        pass
    
    elif mtype == "SetCurrentSceneCollection":
        pass
    
    elif mtype == "CreateSceneCollection":
        pass
    
    elif mtype == "GetProfileList":
        pass
    
    elif mtype == "SetCurrentProfile":
        pass
    
    elif mtype == "CreateProfile":
        pass
    
    elif mtype == "RemoveProfile":
        pass
    
    elif mtype == "GetProfileParameter":
        pass
    
    elif mtype == "SetProfileParameter":
        pass
    
    elif mtype == "GetVideoSettings":
        pass
    
    elif mtype == "SetVideoSettings":
        pass
    
    elif mtype == "GetStreamServiceSettings":
        pass
    
    elif mtype == "SetStreamServiceSettings":
        pass
    
    #Sources
    
    elif mtype == "GetSourceActive":
        pass
    
    elif mtype == "GetSourceScreenshot":
        pass
    
    elif mtype == "SaveSourceScreenshot":
        pass
    
    #Scenes
    
    elif mtype == "GetSceneList":
        for scene in data["scenes"]:
            obs.addScene(scene)
        obs.setCurrentScene(data["currentProgramSceneName"])
        
    elif mtype == "GetGroupList":
        pass
    
    elif mtype == "GetCurrentProgramScene":
        pass
    
    elif mtype == "SetCurrentProgramScene":
        pass 
    
    elif mtype == "GetCurrentPreviewScene":
        pass
    
    elif mtype == "SetCurrentPreviewScene":
        pass
    
    elif mtype == "CreateScene":
        pass
    
    elif mtype == "RemoveScene":
        pass
    
    elif mtype == "SetSceneName":
        pass
    
    #Inputs
    
    elif mtype == "GetInputList":
        pass
    
    elif mtype == "GetInputKindList":
        pass
    
    elif mtype == "GetSpecialInputs":
        pass
    
    elif mtype == "CreateInput":
        pass
    
    elif mtype == "RemoveInput":
        pass
    
    elif mtype == "SetInputName":
        pass
    
    elif mtype == "GetInputDefaultSettings":
        pass
    
    elif mtype == "GetInputSettings":
        pass
    
    elif mtype == "SetInputSettings":
        pass
    
    elif mtype == "GetInputMute":
        pass
    
    elif mtype == "SetInputMute":
        pass
    
    elif mtype == "ToggleInputMute":
        pass
    
    elif mtype == "GetInputVolume":
        pass
    
    elif mtype == "SetInputVolume":
        pass
    
    elif mtype == "GetInputAudioBalance":
        pass
    
    elif mtype == "SetInputAudioBalance":
        pass
    
    elif mtype == "GetInputAudioSyncOffset":
        pass
    
    elif mtype == "SetInputAudioSyncOffset":
        pass
    
    elif mtype == "GetInputAudioMonitorType":
        pass
    
    elif mtype == "SetInputAudioMonitorType":
        pass
    
    elif mtype == "GetInputAudioTracks":
        pass
    
    elif mtype == "SetInputAudioTracks":
        pass
    
    elif mtype == "GetInputPropertiesListPropertyItems":
        pass
    
    elif mtype == "PressInputPropertiesButton":
        pass
    
    #Transitions
    
    elif mtype == "GetTransitionKindList":
        pass
    
    elif mtype == "GetSceneTransitionList":
        pass
    
    elif mtype == "GetCurrentSceneTransition":
        pass
    
    elif mtype == "SetCurrentSceneTransition":
        pass
    
    elif mtype == "SetCurrentSceneTransitionDuration":
        pass
    
    elif mtype == "SetCurrentSceneTransitionSettings":
        pass
    
    elif mtype == "TriggerStudioModeTransition":
        pass
    
    #Filters
    
    elif mtype == "GetSourceFilter":
        pass
    
    #Scene Items
    
    elif mtype == "GetSceneItemList":
        scene = obs.getScene(rid.split("_")[0])
        for sceneitem in data["sceneItems"]:
            scene.addSource(sceneitem)
    
    elif mtype == "GetGroupItemList":
        pass
    
    elif mtype == "GetSceneItemId":
        pass
    
    elif mtype == "CreateSceneItem":
        pass
    
    elif mtype == "RemoveSceneItem":
        pass
    
    elif mtype == "DuplicateSceneItem":
        pass
    
    elif mtype == "GetSceneItemTransform":
        pass
    
    elif mtype == "SetSceneItemTransform":
        pass
    
    elif mtype == "GetSceneItemEnabled":
        scene, source, _ = rid.split("_")
        obs.getScene(scene).getSource(source).setVisible(data["sceneItemEnabled"])
        if obs.getScene(scene) == obs.currentScene:
            for watch in obs.watches:
                if source == watch.name:
                    watch.triggered = True
                    watch.data = "1" if obs.currentScene.getSource(source).enabled else "0"                    
    
    elif mtype == "SetSceneItemEnabled":
        pass
    
    elif mtype == "GetSceneItemLocked":
        pass
    
    elif mtype == "SetSceneItemLocked":
        pass
    
    elif mtype == "GetSceneItemIndex":
        pass
    
    elif mtype == "SetSceneItemIndex":
        pass
    
    elif mtype == "GetSceneItemBlendMode":
        pass
    
    elif mtype == "SetSceneItemBlendMode":
        pass
    
    #Outputs
    
    elif mtype == "GetVirtualCamStatus":
        pass
    
    elif mtype == "ToggleVirtualCam":
        pass
    
    elif mtype == "StartVirtualCam":
        pass
    
    elif mtype == "StopVirtualCam":
        pass
    
    #Stream
    
    elif mtype == "GetStreamStatus":
        pass
    
    elif mtype == "ToggleStream":
        pass
    
    elif mtype == "StartStream":
        pass
    
    elif mtype == "StopStream":
        pass
    
    #Record
    
    elif mtype == "GetRecordStatus":
        pass
    
    elif mtype == "ToggleRecord":
        pass
    
    elif mtype == "StartRecord":
        pass
    
    elif mtype == "StopRecord":
        pass
    
    elif mtype == "ToggleRecordPause":
        pass
    
    elif mtype == "PauseRecord":
        pass
    
    elif mtype == "ResumeRecord":
        pass
    
    elif mtype == "GetRecordDirectory":
        pass
    
    #Media Inputs
    
    elif mtype == "GetMediaInputStatus":
        pass
    
    elif mtype == "SetMediaInputCursor":
        pass
    
    elif mtype == "OffsetMediaInputCursor":
        pass
    
    elif mtype == "TriggerMediaInputAction":
        pass
    
    #UI
    
    elif mtype == "GetStudioModeEnabled":
        pass
    
    elif mtype == "SetStudioModeEnabled":
        pass
    
    elif mtype == "OpenInputPropertiesDialog":
        pass
    
    elif mtype == "OpenInputFiltersDialog":
        pass
    
    elif mtype == "OpenInputInteractDialog":
        pass
    
    else:
        print(f"Unknown response with type {mtype}.")