# -*- encoding: utf-8 -*-



import importlib
import argparse
import StringIO
import io
import picamera
import subprocess
import os
import time
import configparser
from datetime import datetime
from PIL import Image




#
# static settings
#

PATH_TO_CONFIG_FILE = "./config.ini"




#
# get command line arguments
#

def parse_arguments():

    parser = argparse.ArgumentParser(
            description='Record short clip or image after motion detection',
            usage='start process using fitting CLI settings and wait for images / videos to be dropped',
            )

    parser.add_argument(
            '--filepath',
            type=str,
            default='',
            help='basic path name for export of images / videos',
            )
    parser.add_argument(
            '--mondel',
            type=int,
            default=0,
            help='time delay until motion detection starts (in seconds)',
            )
    parser.add_argument(
            '--mondur',
            type=int,
            default=0,
            help='duration of motion detection until give up (in seconds)',
            )
    parser.add_argument(
            '--recdur',
            type=int,
            default=10,
            help='duration of single recording when in video mode (in seconds)',
            )
    parser.add_argument(
            '--motsens',
            type=int,
            default=20,
            help='sensitivity in number of pixels for motion to be detected',
            )
    parser.add_argument(
            '--thres',
            type=int,
            default=20,
            help='color threshold value to identify a dot as different',
            )
    parser.add_argument(
            '--video',
            action='store_true',
            default=False,
            help='use in order to record moving images (video)',
            )
    parser.add_argument(
            '--image',
            action='store_true',
            default=False,
            help='use in order to record still images',
            )
    parser.add_argument(
            '--forcecap',
            action='store_true',
            default=False,
            help='additionally force capture every hour',
            )
    parser.add_argument(
            '--debug',
            action='store_true',
            default=False,
            help='store debug information (e.g. detection images)',
            )
    parser.add_argument(
            '--txdel',
            action='store_true',
            default=False,
            help='immediately transmit captured media and delete it locally',
            )

    return parser.parse_args()




#
# capture a small test image (for motion detection)
#

def captureTestImage(camera):

    # get buffer
    imageData = io.BytesIO()

    # get picture
    camera.resolution = (100, 75)
    camera.capture(imageData, format='jpeg')

    imageData.seek(0)
    im = Image.open(imageData)
    buffer = im.load()
    imageData.close()
    return im, buffer




#
# save a full size image to disk
#

def saveImage(camera, width, height, diskSpaceToReserve):

    keepDiskSpaceFree(diskSpaceToReserve)
    time = datetime.now()
    filename = "capture-%04d%02d%02d-%02d%02d%02d.jpg" % (time.year, time.month, time.day, time.hour, time.minute, time.second)

    # get image
    camera.resolution = (width, height)
    camera.capture(filename)

    print "Captured %s" % filename




#
# save a video
#

def saveVideo(camera, width, height, diskSpaceToReserve):

    keepDiskSpaceFree(diskSpaceToReserve)
    time = datetime.now()
    filename = "capture-%04d%02d%02d-%02d%02d%02d" % (time.year, time.month, time.day, time.hour, time.minute, time.second)

    # record video
    camera.resolution = (width, height)
    camera.rotation = 180
    camera.start_recording(filename + '.h264')
    camera.wait_recording(10)
    camera.stop_recording()




#
# keep free space above given level
#

def keepDiskSpaceFree(bytesToReserve):

    if (getFreeSpace() < bytesToReserve):
        for filename in sorted(os.listdir(".")):
            if filename.startswith("capture") and filename.endswith(".jpg"):
                os.remove(filename)
                print "Deleted %s to avoid filling disk" % filename
                if (getFreeSpace() > bytesToReserve):
                    return




#
# get available disk space
#

def getFreeSpace():

    st = os.statvfs(".")
    du = st.f_bavail * st.f_frsize
    return du




#
# create local configuration file
#

def createSecretFile():

    # very simple implementation of configuration file
    # to avoid re-entering of access credentials each
    # program start

    # list of questions to be answered
    lstQuestionsAndVariables = [
            ['account name',          'EMAIL',     'test@gmx.de', ],
            ['account password',      'PASSWORD',  'GEHEIMMMM', ],
            ['from email',            'FROM',      'sender@email.de', ],
            ['to email',              'TO',        'target@email.de', ],
            ]

    # output welcome message
    print('[ INFO   : in order to create a configuration file, ]')
    print('[ INFO   : please answer the following questions:   ]')
    print('[ INFO   :                                          ]')

    # loop over each question
    for question in lstQuestions:

        print(question[0] + ' [ ' + question[2] + ' ]:')
        raw_input()




#
# MAIN
#

if __name__ == '__main__':




    # example

    # start this application as follows:
    # python surveil.py --video --txdel




    #
    # handle configuration files
    #

    # read general configuration file
    config = configparser.ConfigParser()
    config.read(PATH_TO_CONFIG_INI_FILE)

    # create secret file if not already present
    secretpath = config.get('general', 'PATH_TO_SECRET_FILE')
    if not os.path.isfile(secretpath):
        createSecretFile()

    # read and decode secret file
    _spec = importlib.util.spec_from_file_location('myconfig', secretpath)
    _module = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_module)




    #
    # init camera
    #

    camera = picamera.PiCamera()




    #
    # get user's command line arguments
    #

    arguments = parse_arguments()




    #
    # fix settings
    #

    # Threshold (how much a pixel has to change by to be marked as "changed")
    threshold = arguments.thres
    bRecordImage = arguments.image
    bRecordVideo = arguments.video

    # organizationals
    bSendAndDelete = arguments.txdel

    # Sensitivity (how many changed pixels before capturing an image)
    sensitivity = arguments.motsens

    # ForceCapture (whether to force an image to be captured every forceCaptureTime seconds)
    forceCapture = arguments.forcecap
    forceCaptureTime = 60 * 60 # Once an hour

    # image file settings
    saveWidth = 1280
    saveHeight = 960
    diskSpaceToReserve = 40 * 1024 * 1024 # Keep 40 mb free on disk

    # delay motion detection
    delay = arguments.mondel

    # debug mode
    debug = arguments.debug




    #
    # delay motion detection
    #

    if delay != 0:
        time.sleep(delay)




    #
    # get first image
    #

    image1, buffer1 = captureTestImage(camera)




    #
    # check changes of 2nd image
    #

    # Reset last capture time
    lastCapture = time.time()
    doloop = True
    while doloop:




        #
        # EXPERIMENTAL: find, read, process and delete command.txt
        #

        datafile="/home/pi/APP__surveillance/command.txt"




        #
        # check for existence of command.txt file
        #

        if os.path.isfile(datafile):





            #
            # check, read, process and delete command.txt file
            #

            with open(datafile,"r") as f:   # open datafile
                command = f.read()          # read data into variable
                if command == "quit":       # if quit code received
                    doloop = False          # then init end of loop
                    os.remove(datafile)     # del datafile only if code executed




        #
        # this method works, but it seems to take some time to end the surveil program
        #

        #
        # END EXPERIMENTAL
        #

        #
        # get comparison image
        #

        image2, buffer2 = captureTestImage(camera)




        #
        # count changed pixels
        #

        changedPixels = 0
        for x in xrange(0, 100):
            for y in xrange(0, 75):

                # Just check green channel as it's the highest quality channel
                pixdiff = abs(buffer1[x,y][1] - buffer2[x,y][1])
                if pixdiff > threshold:
                    changedPixels += 1




        #
        # process debugging
        #

        if debug:

            if changedPixels > sensitivity:




                #
                # save comparison pictures
                #

                pass




        #
        # check for force capture
        #

        if forceCapture:
            if time.time() - lastCapture > forceCaptureTime:

                # set number of changed pixels above threshold
                changedPixels = sensitivity + 1




        #
        # save an image if pixels changed
        #

        if bRecordImage:
            if changedPixels > sensitivity:
                lastCapture = time.time()
                saveImage(camera, saveWidth, saveHeight, diskSpaceToReserve)




        #
        # record 10s sequence
        #

        if bRecordVideo:
            if changedPixels > sensitivity:
                lastCapture = time.time()
                saveVideo(camera, 640, 480, diskSpaceToReserve)




        #
        # send email and delete media
        #

        if bSendAndDelete:

            # check for media present
            lstFiles = os.listdir('/home/pi/APP__surveillance/')
            for _file in lstFiles:
                if 'capture' in _file:

                    # send email
                    _cmd = 'echo \'siehe Aufzeichnung...\' | sendemail' \
                            + ' -f '+myconfig.FROM \
                            + ' -t '+myconfig.TO \
                            + ' -u "Bewegung in Werkstatt"' \
                            + ' -s smtp.gmx.de:587' \
                            + ' -xu '+myconfig.EMAIL \
                            + ' -xp '+myconfig.PASSWORD \
                            + ' -o tls=yes' \
                            + ' -a /home/pi/APP__surveillance/capture*'
                    subprocess.call([ _cmd ], shell=True)

                    # delete files
                    _cmd = 'rm /home/pi/APP__surveillance/capture*'
                    subprocess.call([ _cmd ], shell=True)




        #
        # set new 1st comparison picture
        #

        image1 = image2
        buffer1 = buffer2
