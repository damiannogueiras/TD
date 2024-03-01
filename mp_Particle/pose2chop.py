# script utilizado dentro del contenedor base pose2chop
# para la extracción de datos de pose de la librería mediapipe
# by Bryan Chung https://github.com/chungbwc


# me - this DAT
# scriptOp - the OP which is cooking

import numpy as np
import cv2
import mediapipe as mp


mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    smooth_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# press 'Setup Parameters' in the OP to call this function to re-create the parameters.
def onSetupParameters(scriptOp):
    # add a parameter page
    page = scriptOp.appendCustomPage('Custom')
    # add Image param called 'Video image'
    p = page.appendTOP('Image', label='Video image')
    return

# called whenever custom pulse parameter is pushed
def onPulse(par):
    return

def onCook(scriptOp):
    # clear channels
    scriptOp.clear()
    # get image from in TOP (defined in param 'Video image' of Custom)
    img_par = scriptOp.par.Image.eval()
    # convert to numpy array
    input = img_par.numpyArray(delayed=True)
    if input is not None:
        # convert RGBA to RGB
        image = cv2.cvtColor(input, cv2.COLOR_RGBA2RGB)
        # convert to grayscale
        image *= 255
        # convert to uint8
        image = image.astype('uint8')
        # procesa la pose de cada frame
        results = pose.process(image)

        xpos = []
        ypos = []
        zpos = []
        visb = []

        if results.pose_landmarks:
            for p in results.pose_landmarks.landmark:
                xpos.append(p.x)
                ypos.append(p.y)
                zpos.append(p.z)
                visb.append(p.visibility)
            # append channels to chop
            tx = scriptOp.appendChan('pose:x')
            ty = scriptOp.appendChan('pose:y')
            tz = scriptOp.appendChan('pose:z')
            tv = scriptOp.appendChan('pose:visibility')
            # set values
            tx.vals = xpos
            ty.vals = ypos
            tz.vals = zpos
            tv.vals = visb

            # set rate and number of samples
            scriptOp.rate = me.time.rate
            scriptOp.numSamples = len(xpos)

    return
