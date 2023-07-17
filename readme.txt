# MotionNotesGPU

This project's primary objective is to process videos through a deep learning model. The code
will be running in a cluster with powerfull graphics cards managed by David Semedo.
For this code to be able to run in that cluster, the project shoud be inside a docker container.
It is expected an API capable of receive a mp4 video, then execute the model to predict human pose 
coordinates (using OpenPose) or object coordinates (using YOLO) in each video frame. 
Ultimately, a file containing the output coordinates for each frame will be generated 
and made available for motionNotes annotator to get via HTTP request.

## Table of Contents

1. [Installation](#installation)
repository: https://github.com/ruifsr/MotionNotesGPURepository
Python Version: 3.9
Modules pip: flask, flask_restful

2. [Usage](#usage)
There are two important files with code in this solution:

The first one is the python http API "main.py". 
    This http API was developed using the flask framework
    The most important resource is the video:
        get - it returns processed video information from folder destination
        delete - delete the video file in order to free server disk space
        post - the most important function. It receives a new video, and starts by 
            saving the video in the server. The it creates all the necessary names
            and path for processing and saving the results in the right places. Next, 
            the code executes the openPose.exe model and waits for the results. The 
            final step is to merge the openpose output in a BodyPositionsFile
            and respond with 200 ok to the client.
    Resource BodyPositionsFile:
        get - verify if the requested BodyPositionsFile exist. If it exist, responds 
            with the file, if not, returns an error.
        delete - delete the file.

The second file "test.api" basically only exist to test the API and help in development
    sendVideo(fileName) : sends a testing video to the API
    getVideo(fileNameFinal): get a video from API
    getJson(fileName,bodyFilesName): Get an result file from API
    deleteJson(fileName): delete the result file
    deleteVideo(fileName): delete the video

There are two debug configurations and we need to start the API always first:
    1 - Python:main.py 
    2 - Python:test.py

3. [Contribution](#contribution)
4. [Tests](#tests)
5. [License](#license)
6. [Contact](#contact)

## Installation

Describe the installation process here. These are usually command line instructions.
