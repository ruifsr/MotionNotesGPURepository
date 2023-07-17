import requests
import os
import re

BASE = 'http://127.0.0.1:5000/'

#teste post
def sendVideo(fileName):
    originPath = os.path.join('origin',fileName)
    file = {'file': open(originPath, 'rb')}
    response = requests.post(BASE + 'video/'+fileName, files=file)
    print(response.text)

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

def testingMenu():
    while True:
        print("""
            1- sendVideo
            2- getVideo
            3- getJson
            4- deleteJson
            5-deleteVideo
            0-sair""")
        value = input("Please enter something: ")
        if value == "1":
            sendVideo('teste.webm')
        elif value == "2":
            getVideo('teste.avi')
        elif value == "3":
            getJson('teste.webm','teste_keypoints.json')
        elif value == "4":
            deleteJson('teste.webm')
        elif value == "5":
            deleteVideo('teste.webm')
        elif value == "0":
            break
        else:
            print("values between 0 and 5")

testingMenu()