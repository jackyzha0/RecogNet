from throwcolour import cthrow
import cv2
import boto3
import subprocess
import os
import time

ENDPOINT = "https://rekognition.us-west-2.amazonaws.com/detectlabels"
file_loc = "imgs/tmp.jpg"

minconf = 75
DIM = [480, 640]

def initCam():
    cthrow('Loaded OpenCV', type='OK')
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        cthrow('Camera cannot be initialized', type="ERR")
        raise IOError("Cannot open webcam")
    else:
        cthrow('Camera', type='OK')
    return cap

def getCap(usePi = False):
    cap = initCam()
    if usePi:
        cthrow('Using Raspberry Pi Camera')
        subprocess.call(["./getImg.sh"])
        cthrow('Image received!', type='OK')
        frame = cv2.imread('/media/jacky/jzhao_cs/CS/RecogNet/imgs/tmp.jpg')
    else:
        cthrow('Capture Start', type='INFO')
        ret, frame = cap.read()
        print(frame.shape)
        cap.release()
    return frame

def decodeInstance(arr):
    decode_arr = []
    for inst in arr:
        _ = inst['BoundingBox']
        left = float(_['Left'])
        top = float(_['Top'])
        width = float(_['Width'])
        height = float(_['Height'])
        inst_tmp = [left*DIM[1], top*DIM[0], (left+width)*DIM[1], (height+top)*DIM[0], float(inst['Confidence'])] # Format [x1, y1, x2, y2, conf]
        decode_arr.append(inst_tmp)
    return decode_arr

def dispImage(frame,preds):
    for inst in preds:
        if inst[4] > 85:
            cv2.rectangle(frame, (int(inst[0]), int(inst[1])), (int(inst[2]), int(inst[3])), (0, 0, 255), 1)#inst[4]/100)
            cv2.putText(frame, str(inst[4]), (int(inst[0]), int(inst[1])-5), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 255))

    cv2.imshow("frame.jpg", frame)
    while(cv2.waitKey(25) & 0xFF != ord('q')):
        pass

# BEGIN AWS SERVICES
client=boto3.client('rekognition')

def getDect():
    frame = getCap(usePi = True)
    # frame = getCap()
    cthrow('Frame retrieved', type='OK')
    cv2.imwrite(file_loc, frame)
    cthrow('Write file', type='OK')

    with open(file_loc, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()}, MinConfidence=minconf)

    print(response)

    for label in response['Labels']:
        if label['Name'] == 'Person':
            arr = decodeInstance(label['Instances'])
            dispImage(frame, arr)

getDect()
