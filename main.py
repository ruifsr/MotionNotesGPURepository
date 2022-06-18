from flask import Flask, render_template, request, send_from_directory
from flask_restful import Api, Resource, reqparse, abort
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
import subprocess
import os
import json
import re
import shutil

openPoseDirExe = 'openpose\\bin\\OpenPoseDemo.exe'
app =Flask(__name__)
api = Api(app)

class Video(Resource):
    def get(self, videoName):
        try: 
            return send_from_directory('destination', videoName)
        except FileNotFoundError: 
            abort(404)
    def delete(self, videoName):
        try: 
            videoNamePath = os.path.join('destination',re.sub('\..+', '',videoName))
            if os.path.isfile(videoNamePath+'.avi') : os.remove(videoNamePath+'.avi')
            if os.path.isfile(videoNamePath+'.webm') : os.remove(videoNamePath+'.webm')
            if os.path.isfile(videoNamePath+'.mp4') : os.remove(videoNamePath+'.mp4')
            return 'delete success!', 200
        except FileNotFoundError: 
            abort(404)
    def post(self,videoName):
        postedVideo = request.data if (len(request.files)==0) else request.files['file'].read()
        dirVidToProc=os.path.join('destination', videoName)
        with open(dirVidToProc, 'wb') as f:f.write(postedVideo)
        dirJson = os.path.join('destination', re.sub('\..+','', videoName))
        vidFinalName = re.sub('\..+', '.avi', videoName)
        dirVidFinal = os.path.join('destination',vidFinalName)
        finalCommand = '"'+openPoseDirExe+'" --video "'+dirVidToProc+'" --write_json "'+dirJson+'" --display "0" --write_video "'+dirVidFinal+'" --net_resolution "-1x160"'
        #openpose to process video, generating a new video and folder with all keypoints
        try:
            consoleContent = subprocess.run(finalCommand, check=True, capture_output=True, text=True).stdout.strip("\n")
        except Exception as e:
            return 'error',500
        print(dirVidToProc + ' successfully processed by openpose')
        #merger all position files
        mergeJsons={}
        files = os.listdir(dirJson)
        for l in files:
            filePath = os.path.join(dirJson,l)
            jsonFile = open(filePath, 'r').read()
            os.remove(filePath)
            index = int(re.findall('\d+(?=_key)',filePath)[0]) 
            mergeJsons[index] = jsonFile
        with open(os.path.join(dirJson,'keypoints.json'), 'x') as outfile:
            json.dump(mergeJsons, outfile)
        print(dirVidToProc + ' successfully merged!')
        return 'video successfully processed',200

api.add_resource(Video, '/video/<string:videoName>')

class BodyPositionsFile(Resource):
    def get(self,fileName):
        folder = os.path.join('destination',fileName)
        try: 
            return send_from_directory(folder, 'keypoints.json')
        except FileNotFoundError: 
            abort(404)
    def delete(self,fileName):
        try: 
            shutil.rmtree(os.path.join('destination', re.sub('\..+', '', fileName)))
            return '', 204
        except FileNotFoundError: 
            abort(404)

api.add_resource(BodyPositionsFile, '/BodyPositionsFile/<string:fileName>')


app.debug=True
#if __name__ == "__main__":
#    app.run(debug=True);
