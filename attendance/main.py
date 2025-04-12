from flask import Flask, render_template, Response
from camera import VideoCamera
# import create_data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/exec2')
def parse1():
#     response_data_collection = 
    print("Here")
    VideoCamera().save_to_dataset()
#     if response_data_collection != None:
#         print("Done with Collecting Data")
#     else:    
#         response_data_collection = "Couldn't able to create data files"
#     return render_template('index.html', alert='Done with Collecting Data')

@app.route('/training')
def training():
    return render_template('training.html', alert='Not Yet Trained')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
Need help correcting parse1() class.

VideoCamera.py:- (Where all face detection related py code lies)

import cv2
import os
import time
face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
ds_factor=0.6
datasets = 'datasets'

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        image=cv2.resize(image,None,fx=ds_factor,fy=ds_factor,interpolation=cv2.INTER_AREA)
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        face_rects=face_cascade.detectMultiScale(gray,1.3,5)
        for (x,y,w,h) in face_rects:
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
            break
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def save_to_dataset(self):
        return_data = ''
        sub_data = 'Tapan_1'
        (width, height) = (130, 100) 


        count = 1
        path = os.path.join(datasets, sub_data)
        if not os.path.isdir(path):
            os.mkdir(path)
            while count < 20: 
                success, image = self.video.read()
                image=cv2.resize(image,None,fx=ds_factor,fy=ds_factor,interpolation=cv2.INTER_AREA)
                gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
                face_rects=face_cascade.detectMultiScale(gray,1.3,5)
                for (x,y,w,h) in face_rects:
                    cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
                    face = gray[y:y + h, x:x + w]
                    face_resize = cv2.resize(face, (width, height))
                    cv2.imwrite('%s/%s.png' % (path,count), face_resize)
                count += 1

                if count == 20:
                    return_data = '20 image captured.'
                    # cv2.waitKey(1)
                    # self.video.release()
                    # cv2.destroyAllWindow()
                    # time.sleep(1)

                    break
        else:
            return_data = "Data already Thr"

        return return_data
