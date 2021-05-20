import os
import json
import xml.etree.ElementTree as ET
import plistlib as PL

current_dir = os.path.dirname(os.path.realpath(__file__))
input_dir = os.path.join(current_dir, 'input')
output_dir = os.path.join(current_dir, 'input')

def doConvert(file):
    fileName = file[:-4]
    filePath = os.path.join(input_dir, file)
    newFilePath = os.path.join(output_dir, fileName + 'plist')
    f = open(filePath)
    contentJson = json.load(f)
    metaJson = contentJson["meta"]
    framesJson = contentJson["frames"]

    frameDict = dict()
    metaDict = dict()
    pl = dict()
    pl['frames'] = frameDict 
    pl['metadata'] = metaDict 

    metaDict["format"] = 3
    metaDict["premultiplyAlpha"] = False
    metaDict["pixelFormat"] = metaJson["format"]
    metaDict["smartupdate"] = metaJson["smartupdate"]
    metaDict["textureFileName"] = metaJson["image"]
    metaDict["realTextureFileName"] = metaJson["image"]
    texSize = metaJson["size"]
    metaDict["size"] = "{"+"{}, {}".format(texSize['w'],texSize['h'])+"}"

    for key in framesJson.keys():
        value = framesJson[key]
        frameSize = value["frame"]

        frameDict[key] = dict()
        subDict = frameDict[key]
        subDict["aliases"] = []
        subDict["spriteOffset"] = "{0, 0}"
        sizeStr = "{"+"{}, {}".format(frameSize['w'],frameSize['h'])+"}"
        subDict["spriteSize"] = sizeStr
        subDict["spriteSourceSize"] = sizeStr
        subDict["textureRect"] =  "{{"+"{}, {}".format(frameSize['x'],frameSize['y'])+"},"+sizeStr+"}"
        subDict["textureRotated"] = value["rotated"]

    with open(newFilePath, 'wb') as fp:
        PL.dump(pl, fp)
###############################################
for subdir, dirs, files in os.walk(input_dir):
    for file in files:
        if(file.endswith('.json')):
            doConvert(file)


