from throwcolour import cthrow
import cv2
import boto3

ENDPOINT = "https://rekognition.us-west-2.amazonaws.com/detectlabels"
file_loc = "imgs/tmp.png"

minconf = 75

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

def getCap(cap):
    cthrow('Capture Start', type='INFO')
    ret, frame = cap.read()
    print(frame.shape)
    cap.release()
    return frame

cap = initCam()
frame = getCap(cap)
cthrow('Frame retrieved', type='OK')
cv2.imwrite(file_loc, frame)
cthrow('Write file', type='OK')

# BEGIN AWS SERVICES
client=boto3.client('rekognition')

with open(file_loc, 'rb') as image:
    response = client.detect_labels(Image={'Bytes': image.read()}, MinConfidence=minconf)

for label in response['Labels']:
    if label['Name'] == 'Person':
        print(label['Instances'])
        print(label['Name'])

print('Done...')
