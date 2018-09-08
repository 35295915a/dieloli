import os
from script.Core import GameConfig,RichText,GameData,EraPrint,PyCmd,CacheContorl,TextHandle,ValueHandle,GamePathConfig

language = GameConfig.language
gamepath = GamePathConfig.gamepath
mapDataDir = os.path.join(gamepath, 'data',language, 'map')

# 输出地图
def printMap(mapId):
    mapText = CacheContorl.mapData['MapTextData'][mapId]
    playerNowSceneId = CacheContorl.playObject['object']['0']['Position']
    playerNowSceneId = getMapSceneIdForSceneId(mapId,playerNowSceneId)
    playerNowSceneId = str(playerNowSceneId)
    sceneList = getSceneListForMap(mapId)
    inputS = []
    inputCmd = ''
    passList = []
    mapYList = mapText.split('\n')
    for mapXList in mapYList:
        mapXListStyle = RichText.setRichTextPrint(mapXList,'standard')
        mapXList = RichText.removeRichCache(mapXList)
        mapXFix = TextHandle.align(mapXList,'center',True)
        EraPrint.p(mapXFix)
        for i in range(0, len(mapXList)):
            if str(i) not in passList:
                if mapXListStyle[i] == 'mapbutton':
                    inputCmd = inputCmd + mapXList[i]
                    for n in range(i + 1,len(mapXList)):
                        if mapXListStyle[n] == 'mapbutton':
                            inputCmd = inputCmd + mapXList[n]
                            passList.append(str(n))
                        else:
                            break
                    if inputCmd in sceneList:
                        if inputCmd == playerNowSceneId:
                            EraPrint.p(inputCmd,'nowmap')
                            inputS.append(None)
                        else:
                            PyCmd.pcmd(inputCmd, inputCmd, None)
                            inputS.append(inputCmd)
                    else:
                        EraPrint.p(inputCmd,'standard')
                    inputCmd = ''
                else:
                    EraPrint.p(mapXList[i], mapXListStyle[i])
        EraPrint.p('\n')
    return inputS

# 获取场景所在地图
def getMapForScene(sceneId):
    sceneId = int(sceneId)
    scenePath = CacheContorl.sceneData['ScenePathData'][sceneId]
    mapPath = getMapForPath(scenePath)
    return mapPath

# 查找场景所在地图
def getMapForPath(scenePath):
    mapPath = os.path.abspath(os.path.join(scenePath, '..'))
    if 'Map' in os.listdir(mapPath):
        pass
    else:
        mapPath = getMapForPath(mapPath)
    return mapPath

# 查找场景所在地图ID
def getMapIdForScene(sceneId):
    mapPath = getMapForScene(sceneId)
    mapData = CacheContorl.mapData['MapPathData']
    mapId = mapData.index(mapPath)
    return mapId

# 从场景路径获取所在地图ID
def getMapIdForScenePath(scenePath):
    mapPath = getMapForPath(scenePath)
    mapData = CacheContorl.mapData['MapPathData']
    mapId = mapData.index(mapPath)
    return mapId

# 获取地图下所有场景
def getSceneListForMap(mapId):
    mapId = int(mapId)
    mapPath = CacheContorl.mapData['MapPathData'][mapId]
    sceneList = GameData.getPathList(mapPath)
    return sceneList

# 从场景ID获取场景路径
def getScenePathForSceneId(sceneId):
    sceneId = int(sceneId)
    sceneData = CacheContorl.sceneData['ScenePathData']
    scenePath = sceneData[sceneId]
    return scenePath

# 场景移动
def playerMoveScene(oldSceneId,newSceneId,characterId):
    scenePlayerData = CacheContorl.sceneData['ScenePlayerData']
    characterId = str(characterId)
    oldSceneId = int(oldSceneId)
    newSceneId = int(newSceneId)
    if characterId in scenePlayerData[oldSceneId]:
        scenePlayerData[oldSceneId].remove(characterId)
    if characterId in scenePlayerData[newSceneId]:
        pass
    else:
        CacheContorl.playObject['object'][characterId]['Position'] = newSceneId
        scenePlayerData[newSceneId].append(characterId)
    CacheContorl.sceneData['ScenePlayerData'] = scenePlayerData

# 计算寻路路径
def getPathfinding(mapId,nowNode,targetNode,pathNodeList = [],pathTimeList = []):
    pathList = CacheContorl.pathList
    timeList = CacheContorl.pathTimeList
    mapId = int(mapId)
    nowNode = str(nowNode)
    targetNode = str(targetNode)
    mapData = CacheContorl.mapData['MapData'][mapId].copy()
    pathEdge = mapData['PathEdge'].copy()
    targetListDict = pathEdge[nowNode].copy()
    targetList = ValueHandle.dictKeysToList(targetListDict)
    if nowNode == targetNode:
        return 'End'
    else:
        for i in range(0,len(targetList)):
            target = targetList[i]
            if target in pathNodeList:
                pass
            else:
                targetTime = targetListDict[target]
                findPath = pathNodeList.copy()
                if findPath == []:
                    findPath = [nowNode]
                    findTime = [-1]
                else:
                    findTime = pathTimeList.copy()
                findPath.append(target)
                findTime.append(targetTime)
                if target == targetNode:
                    pathList.append(findPath)
                    timeList.append(findTime)
                else:
                    pathEdgeNow = pathEdge[target].copy()
                    pathEdgeNow.pop(nowNode)
                    targetNodeInTargetList = pathEdgeNow.copy()
                    targetNodeInTargetToList = ValueHandle.dictKeysToList(targetNodeInTargetList)
                    for i in range(0,len(targetNodeInTargetToList)):
                        targetNodeInTarget = targetNodeInTargetToList[i]
                        findPath.append(targetNodeInTarget)
                        findTime.append(targetNodeInTargetList[targetNodeInTarget])
                        pathData = getPathfinding(mapId,targetNodeInTarget,targetNode,findPath,findTime)
                        if pathData == 'Null':
                            pass
                        elif pathData == 'End':
                            pathList.append(findPath)
                            timeList.append(findTime)
                        else:
                            pathList.append(pathData['Path'])
                            timeList.append(pathData['Time'])
        CacheContorl.pathTimeList = []
        CacheContorl.pathList = []
        return getMinimumPath(pathList,timeList)

# 获取最短路径
def getMinimumPath(pathList,timeList):
    if len(pathList) > 0:
        needTimeList = []
        for i in range(0,len(timeList)):
            needTimeList.append(getNeedTime(timeList[i]))
        pathId = needTimeList.index(min(needTimeList))
        return {'Path': pathList[pathId], 'Time': timeList[pathId]}
    else:
        return 'Null'

# 获取路径所需时间
def getNeedTime(timeGroup):
    needTime = 0
    for i in timeGroup:
        needTime = needTime + i
    return needTime

# 获取地图路径列表
def getSceneToSceneMapList(nowScenePath,targetScenePath):
    sceneAffiliation = judgeSceneAffiliation(nowScenePath,targetScenePath)
    if sceneAffiliation == '0':
        return '0'
    elif sceneAffiliation == '1':
        return getMapHierarchyListForScenePath(nowScenePath,targetScenePath)
    elif sceneAffiliation == '2':
        commonMap = getCommonMapForScenePath(nowScenePath,targetScenePath)
        nowSceneToCommonMap = getMapHierarchyListForScenePath(nowScenePath,commonMap)
        targetSceneToCommonMap = getMapHierarchyListForScenePath(targetScenePath,commonMap)
        commonMapToTargetScene = ValueHandle.reverseArrayList(targetSceneToCommonMap)
        return nowSceneToCommonMap + commonMapToTargetScene[1:]

# 查找节点共同所属地图
def getCommonMapForScenePath(sceneAPath,sceneBPath):
    sceneAPathHierarchyList = getMapHierarchyListForScenePath(sceneAPath,mapDataDir)
    sceneAPathHierarchyList = ValueHandle.reverseArrayList(sceneAPathHierarchyList)
    sceneBPathHierarchyList = getMapHierarchyListForScenePath(sceneBPath,mapDataDir)
    sceneBPathHierarchyList = ValueHandle.reverseArrayList(sceneBPathHierarchyList)
    hierarchy = mapDataDir
    try:
        for i in range(0,len(sceneAPathHierarchyList)):
            if sceneAPathHierarchyList[i] == sceneBPathHierarchyList[i]:
                hierarchy = sceneAPathHierarchyList[i]
    except IndexError:
        pass
    return hierarchy

# 获取节点所属层级列表
def getMapHierarchyListForScenePath(nowScenePath,targetScenePath):
    hierarchyList = []
    nowPath = None
    while(True):
        if nowPath == None:
            nowPath = os.path.abspath(os.path.join(nowScenePath,'..'))
        if nowPath != targetScenePath:
            hierarchyList.append(nowPath)
            nowPath = os.path.abspath(os.path.join(nowPath,'..'))
        else:
            break
    return hierarchyList

# 判断场景有无所属关系
def judgeSceneIsAffiliation(nowScenePath,targetScenePath):
    if judgeSceneAffiliation(nowScenePath,targetScenePath) == '1':
        return '0'
    elif judgeSceneAffiliation(targetScenePath,nowScenePath) == '1':
        return '1'
    else:
        return '2'

# 判断场景所属关系
def judgeSceneAffiliation(nowScenePath,targetScenePath):
    nowScenePathFile = os.path.join(nowScenePath)
    targetScenePathFile = os.path.join(targetScenePath)
    # 判断nowScene是否和targetScene在同一层级
    if os.path.abspath(os.path.join(nowScenePathFile,'..')) != os.path.abspath(os.path.join(targetScenePathFile,'..')):
        # 判断nowScene是否是targetScene的下属节点
        if os.path.abspath(os.path.join(nowScenePathFile,'..')) != targetScenePathFile:
            # 如果上级节点不是公共节点则递归
            if os.path.abspath(os.path.join(nowScenePathFile,'..')) != mapDataDir:
                return judgeSceneAffiliation(os.path.abspath(os.path.join(nowScenePath,'..')),targetScenePathFile)
            else:
                return '2'
        else:
            return '1'
    else:
        return '0'

# 获取场景所在所有直接地图位置
def getRelationMapListForScenePath(scenePath):
    nowPath = scenePath
    nowMapPath = getMapPathForScenePath(nowPath)
    nowMapId = getMapIdForPath(nowMapPath)
    mapList = []
    if os.path.abspath(os.path.join(nowMapPath,'..')) != mapDataDir:
        nowPathId = getMapSceneIdForScenePath(nowMapId,scenePath)
        mapList.append(nowMapPath)
        if nowPathId == '0':
            return mapList + getRelationMapListForScenePath(nowMapPath)
        else:
            return mapList
    else:
        mapList.append(nowMapPath)
        return mapList

# 载入地图下对应场景数据
def getSceneDataForMap(mapId,mapSceneId):
    mapId = int(mapId)
    mapSceneId = str(mapSceneId)
    mapPath = CacheContorl.mapData['MapPathData'][mapId]
    scenePath = os.path.join(mapPath,mapSceneId)
    sceneData = getSceneDataForPath(scenePath)
    return sceneData

# 获取全局场景id对应的地图场景id
def getMapSceneIdForSceneId(mapId,sceneId):
    sceneId = int(sceneId)
    scenePath = getScenePathForSceneId(sceneId)
    mapId = int(mapId)
    sceneInPath = getMapScenePathForScenePath(mapId,scenePath)
    mapPath = getPathForMapId(mapId)
    mapSceneId = judgeSonMapInMap(mapPath, sceneInPath)
    return mapSceneId

# 获取从场景路径获取对应地图下路径
def getMapScenePathForScenePath(mapId,scenePath):
    mapPath = CacheContorl.mapData['MapPathData'][mapId]
    sceneInPath = os.path.abspath(os.path.join(scenePath, '..'))
    if mapPath == sceneInPath:
        nowPath = scenePath
    else:
        nowPath = getMapScenePathForScenePath(mapId,sceneInPath)
    return nowPath

# 获取地图场景id对应的全局场景id
def getSceneIdForMapSceneId(mapId,mapSceneId):
    scenePath = getScenePathForMapSceneId(mapId,mapSceneId)
    sceneId = getSceneIdForPath(scenePath)
    return sceneId

# 从场景路径获取所在地图路径
def getMapPathForScenePath(scenePath):
    mapId = getMapIdForScenePath(scenePath)
    mapPath = CacheContorl.mapData['MapPathData'][mapId]
    return mapPath

# 判断地图在指定地图中的位置
def judgeSonMapInMap(mapPath,sonMapPath):
    mapDirList = os.listdir(mapPath)
    mapPathList = []
    for i in mapDirList:
        loadPath = os.path.join(mapPath,i)
        if os.path.isfile(loadPath):
            pass
        else:
            mapPathList.append(loadPath)
    if sonMapPath in mapPathList:
        for i in mapDirList:
            if os.path.join(mapPath,i) == sonMapPath:
                return i
    else:
        loadSonMapPath = os.path.abspath(os.path.join(sonMapPath, '..'))
        sonMapId = judgeSonMapInMap(mapPath,loadSonMapPath)
        return sonMapId

# 从对应地图场景id查找场景路径
def getScenePathForMapSceneId(mapId,mapSceneId):
    mapId = int(mapId)
    mapSceneId = str(mapSceneId)
    mapPath = CacheContorl.mapData['MapPathData'][mapId]
    scenePath = os.path.join(mapPath,mapSceneId)
    scenePath = getScenePathForTrue(scenePath)
    return scenePath

# 从场景路径查找地图场景id
def getMapSceneIdForScenePath(mapId,scenePath):
    mapId = int(mapId)
    mapPath = CacheContorl.mapData['MapPathData'][mapId]
    sceneId = judgeSonMapInMap(mapPath,scenePath)
    return sceneId

# 获取有效场景路径
def getScenePathForTrue(scenePath):
    if 'Scene.json' in os.listdir(scenePath):
        pass
    else:
        scenePath = os.path.join(scenePath,'0')
        scenePath = getScenePathForTrue(scenePath)
    return scenePath

# 从对应路径查找场景数据
def getSceneDataForPath(scenePath):
    if 'Scene.json' in os.listdir(scenePath):
        scenePath = os.path.join(scenePath,'Scene.json')
        sceneData = GameData._loadjson(scenePath)
    else:
        scenePath = os.path.join(scenePath,'0')
        sceneData = getSceneDataForPath(scenePath)
    return sceneData

# 载入所有场景数据
def initSceneData():
    sceneData = []
    scenePathData = []
    scenePlayerData = []
    for dirpath, dirnames, filenames in os.walk(mapDataDir):
        for i in range(0,len(filenames)):
            filename = filenames[i]
            if filename == 'Scene.json':
                scenePath = os.path.join(dirpath,filename)
                scene = GameData._loadjson(scenePath)
                sceneData.append(scene)
                scenePathData.append(dirpath)
                scenePlayerData.append([])
    CacheContorl.sceneData = {"SceneData":sceneData,"ScenePathData":scenePathData,"ScenePlayerData":scenePlayerData}

# 载入所有地图数据
def initMapData():
    mapData = []
    mapPathData = []
    mapTextData = []
    for dirpath, dirnames, filenames in os.walk(mapDataDir):
        for filename in filenames:
            if filename == 'Map':
                mapPath = os.path.join(dirpath,'Map')
                mapDataPath = os.path.join(dirpath,'Map.json')
                openMap = open(mapPath)
                mapText = openMap.read()
                mapJsonData = GameData._loadjson(mapDataPath)
                mapData.append(mapJsonData)
                mapTextData.append(mapText)
                mapPathData.append(dirpath)
    CacheContorl.mapData = {"MapData":mapData,"MapPathData":mapPathData,"MapTextData":mapTextData}

# 初始化场景上的角色
def initScanePlayerData():
    scenePlayerData = CacheContorl.sceneData['ScenePlayerData']
    for i in range(0,len(scenePlayerData)):
        scenePlayerData[i] = []
    CacheContorl.sceneData['ScenePlayerData'] = scenePlayerData

# 获取场景上所有角色的数据
def getScenePlayerData(sceneId):
    playerData = CacheContorl.playObject['object']
    scenePlayerData = []
    scenePlayerDataList = CacheContorl.sceneData['ScenePlayerData'][sceneId]
    for i in scenePlayerDataList:
        scenePlayerData.append(playerData[i])
    return scenePlayerData

# 获取场景上所有角色的姓名列表
def getScenePlayerNameList(sceneId):
    scenePlayerData = getScenePlayerData(sceneId)
    scenePlayerNameList = []
    for i in scenePlayerData:
        scenePlayerNameList.append(i['Name'])
    return scenePlayerNameList

# 获取场景上角色姓名对应角色id
def getPlayerIdByPlayerName(playerName,sceneId):
    playerNameList = getScenePlayerNameList(sceneId)
    playerNameIndex = playerNameList.index(playerName)
    playerIdList = getScenePlayerIdList(sceneId)
    playerId = playerIdList[playerNameIndex]
    return playerId

# 获取场景上所有角色的id列表
def getScenePlayerIdList(sceneId):
    scenePlayerDataList = CacheContorl.sceneData['ScenePlayerData'][sceneId]
    scenePlayerIdList = []
    for i in scenePlayerDataList:
        scenePlayerIdList.append(i)
    return scenePlayerIdList

# 从路径获取取场景ID
def getSceneIdForPath(path):
    sceneData = CacheContorl.sceneData.copy()
    scenePathData = sceneData['ScenePathData']
    sceneId = scenePathData.index(path)
    return sceneId

# 从路径获取地图ID
def getMapIdForPath(path):
    mapData = CacheContorl.mapData.copy()
    mapPathData = mapData['MapPathData']
    mapId = mapPathData.index(path)
    return mapId

# 从地图ID获取地图路径
def getPathForMapId(mapId):
    mapData = CacheContorl.mapData.copy()
    mapPathData = mapData['MapPathData']
    return mapPathData[int(mapId)]

# 从目录列表获取场景ID
def getSceneIdForDirList(dirList):
    scenePath = os.path.join(mapDataDir)
    for i in dirList:
        scenePath = os.path.join(scenePath,i)
    sceneId = getSceneIdForPath(scenePath)
    return sceneId
