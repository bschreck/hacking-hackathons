import os
import pickle as pck
def mergeDicts(*dictArgs):
    '''
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    '''
    result = {}
    for dictionary in dictArgs:
        result.update(dictionary)
    return result

def checkPickleFileExistsAndCreate(pf):
    if not os.path.isfile(pf):
        with open(pf, 'a') as f:
            pck.dump({'placeholder':None},f)
def loadObjectsFromPickleFile(objectNameList, pf):
    with open(pf) as f:
        try:
            allData = pck.load(f)
        except:
            return [None]* len(objectNameList)
    objectList = []
    for o in objectNameList:
        if o in allData:
            objectList.append(allData[o])
        else:
            objectList.append(None)
    return objectList

def saveObjectsToPickleFile(objectDict, pf):
    with open(pf) as f:
        allData = pck.load(f)
    with open(pf, 'w') as f:
        allData = mergeDicts(allData, objectDict)
        pck.dump(allData,f)
def overwritePickleFile(objects,pf):
    with open(pf, 'w') as f:
        pck.dump(objects,f)


