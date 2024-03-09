# me - this DAT
# scriptOp - the OP which is cooking

# Detecta la silueta de una persona

import numpy as np
import cv2
import mediapipe as mp


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

pose = mp_pose.Pose(
    # configura el modelo para detectar la silueta
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    # habilita la segmentación
    enable_segmentation=True
)

def SetupParameters(scriptOp):
    page = scriptOp.appendCustomPage('Custom')
    page.appendPulse('Buttona')
    page.appendPulse('Buttonb')
    return

# press 'Setup Parameters' in the OP to call this function to re-create the parameters.
def onSetupParameters(scriptOp):
    pose.reset()
    return

# called whenever custom pulse parameter is pushed
def onPulse(par):
    return

def onCook(scriptOp):
    # recibimos la imagen de la cámara o un video
    input = scriptOp.inputs[0].numpyArray(delayed=True)
    if input is not None:
        image = cv2.cvtColor(input, cv2.COLOR_RGBA2RGB)
        image *= 255
        image = image.astype('uint8')
        # procesamos la imagen com mediapipe
        results = pose.process(image)

        # dibujamos la silueta en el TOP
        if results.segmentation_mask is not None:
            rgb = cv2.cvtColor(results.segmentation_mask, cv2.COLOR_GRAY2RGB)
            rgb = rgb * 255
            rgb = rgb.astype(np.uint8)
            scriptOp.copyNumpyArray(rgb)
        else:
            # si no hay silueta, devolvemos una imagen negra
            black = np.zeros(image.shape, dtype=np.uint8)
            scriptOp.copyNumpyArray(black)
    return