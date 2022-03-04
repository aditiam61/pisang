import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, flash, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

img = cv2.imread('./data.matang.jpg')
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def getPercentage(objLow, objHigh, imgHsv):
    low = np.array(objLow, np.uint8)
    high = np.array(objHigh, np.uint8)
    mask = cv2.inRange(imgHsv, low, high)
    percentage = np.round((cv2.countNonZero(mask) / (img_hsv.size/3)) * 100, 2)

    return percentage

def getResult(img_hsv):
    res = {}
    # sangat matang
    res['s_matang'] = getPercentage([20, 100, 50], [24, 255, 255], img_hsv)
    # matang
    res['matang'] = getPercentage([25, 100, 50], [35, 255, 255], img_hsv)
    # mentah
    res['mentah'] = getPercentage([36, 100, 50], [60, 255, 255], img_hsv)
    return res

percentage = getResult(img_hsv)
# hasil = max(percentage, key=percentage.get)
print(percentage)


@app.route('/')
def upload():
    return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], 'data.jpg'))
      return redirect('/')
		
if __name__ == '__main__':
   app.run(debug = True)
