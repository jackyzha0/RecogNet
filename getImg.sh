#!/bin/bash
HOST="pi@10.42.0.74"
LOCKDIR="/home/pi/recogNet/locks"
IMDIR="/home/pi/recogNet/imgs/tmp.jpg"

#SET IMAGE LOCK
#This lets the RPi know that we have requested a picture
sshpass -p 'raspberry' scp IM_LOCK $HOST:$LOCKDIR

#Begin checking to see if photo has been taken
while ! sshpass -p 'raspberry' scp $HOST:$IMDIR imgs/ &>/dev/null; do
    echo 'File not found, sleeping for 1 second.'
    sleep 1
done

echo 'File found and copied!'
echo 'Cleaning up...'

sshpass -p 'raspberry' ssh $HOST 'rm /home/pi/recogNet/locks/IM_LOCK /home/pi/recogNet/imgs/tmp.jpg'

#scp pi@10.42.0.74:/home/pi/recogNet/imgs
