import requests
import os
import re

BASE = 'http://127.0.0.1:5000/'

#teste post
def sendVideo(fileName):
    originPath = os.path.join('origin',fileName)
    file = {'file': open(originPath, 'rb')}
    response = requests.post(BASE + 'video/'+fileName, files=file)
    print(response)

#teste get Video processed
def getVideo(fileNameFinal):
    response = requests.get(BASE + "video/" + fileNameFinal, stream=True)
    dirVidToProc=os.path.join('origin', fileNameFinal)
    with open(dirVidToProc, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)
    print('video downloaded!')

#teste getJson with body parts location
def getJson(fileName,bodyFilesName):
    response = requests.get(BASE + "BodyPositionsFile/" + re.sub('\..+', '', fileName), stream=True)
    dirVidToProc=os.path.join('origin', bodyFilesName)
    with open(dirVidToProc, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)
    print('Json downloaded')

def deleteJson(fileName):
    response = requests.delete(BASE + "BodyPositionsFile/" + fileName)
    print (response)

def deleteVideo(fileName):
    response = requests.delete(BASE + "video/" + fileName)
    print (response)

#sendVideo('teste.webm')
#getVideo('teste.avi')
#getJson('teste.webm','teste_keypoints.json')
#deleteJson('teste.webm')
deleteVideo('teste.webm')
