from throwcolour import cthrow
import cv2
import boto3

ENDPOINT = "https://rekognition.us-west-2.amazonaws.com/detectlabels"
file_loc = "imgs/tmp.png"


def initCam():
    cthrow('Loaded OpenCV', type='INFO')

    cap = cv2.VideoCapture(0)
    return cap

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

def getCap(cap):
    ret, frame = cap.read()
    print(frame.shape)
    cap.release()
    return frame

cap = initCam()
frame = getCap(cap)
cv2.imwrite(file_loc, frame)

# BEGIN AWS SERVICES
client=boto3.client('rekognition')

with open(imageFile, 'rb') as image:
    response = client.detect_labels(Image={'Bytes': image.read()})

print('Detected labels in ' + file_loc)
for label in response['Labels']:
    print (label['Name'] + ' : ' + str(label['Confidence']))

print('Done...')
