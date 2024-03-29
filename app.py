from __future__ import division, print_function
# coding=utf-8
import os

import glob
import numpy as np
# Keras
from keras.models import load_model
from keras.preprocessing import image
import keras.utils as image
from PIL import Image

from flask import Flask, jsonify, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename

import cv2


app = Flask(__name__, static_url_path='/static')


model = load_model('model/model__data_aug_BGR_RGB.h5') #ใช้อันนี้
model.make_predict_function()



#funtion ทำนายระดับความสุกของมะม่วง
def model_predict():
    image_path = 'static/uploads'
    results = [] 
    accuracies = []  # List to store accuracy values as percentages
    total_samples = 0  # Variable to count total samples for accuracy calculation

    for images in glob.iglob(f'{image_path}/*'):
        img_predict = cv2.imread(images , cv2.COLOR_BGR2RGB)
        img_predict = cv2.resize(img_predict ,(128,128))
        img_predict = np.array(img_predict).astype('float32')
        img_predict /= 255
        img_predict = np.expand_dims(img_predict, axis=0)
        class_name = ['สุก','ห่าม','ดิบ']
        prediction = model.predict(img_predict)[0]
        result = class_name[np.argmax(prediction)]
        accuracy = float(np.max(prediction)) * 100  # Convert accuracy to percentage
        results.append(result)
        accuracies.append(f"{accuracy:.2f}%")  # Format accuracy as percentage with two decimal places
        total_samples += 1

    # Calculate overall accuracy based on predictions
    accuracy_percentage = [0, 0, 0]
    for result in results:
        if result == 'สุก':
            accuracy_percentage[0] += 1
        elif result == 'ห่าม':
            accuracy_percentage[1] += 1
        elif result == 'ดิบ':
            accuracy_percentage[2] += 1

    accuracy_percentage = [f"{(count / total_samples) * 100:.2f}%" for count in accuracy_percentage]

    print('Predictions:', results)
    print('Accuracies:', accuracies)
    print('Overall Accuracy:', accuracy_percentage)

    return results, accuracies, accuracy_percentage

def crop_image(img_path):
    # Reading an image in default mode:
    inputImage = cv2.imread(img_path)
    # Grayscale conversion:
    grayscaleImage = cv2.cvtColor(inputImage, cv2.COLOR_BGR2GRAY)
    # Thresholding:
    threshValue, binaryImage = cv2.threshold(grayscaleImage, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # Find the contours on the binary image:
    contours, hierarchy = cv2.findContours(binaryImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Loop through the contours:
    for i, c in enumerate(contours):
        # Get contour area:
        contourArea = cv2.contourArea(c)
        # Set minimum area threshold:
        minArea = 1000
        # Check if contour area is greater than minimum area:
        if contourArea > minArea:
            # Approximate the contour to a polygon:
            contoursPoly = cv2.approxPolyDP(c, 3, True)
            # Convert the polygon to a bounding rectangle:
            boundRect = cv2.boundingRect(contoursPoly)
            # Get the rectangle dimensions:
            rectangleX, rectangleY, rectangleWidth, rectangleHeight = boundRect
            # Crop the ROI:
            croppedImg = inputImage[rectangleY:rectangleY + rectangleHeight, rectangleX:rectangleX + rectangleWidth]
            # Save the cropped image:
            cv2.imwrite(f'static/uploads/image_{i}.png', croppedImg)
    os.remove(img_path)


#ลบพื้นหลังของภาพ
def remove_background():
        files = glob.glob(os.path.join('static/uploads/*'))
        for file in files:
            imgInput = cv2.imread(file)
            imgInput = cv2.resize(imgInput, (300, 300))
            height, width = imgInput.shape[:2]
            mask = np.zeros(imgInput.shape[:2], np.uint8)
            backgroundModel = np.zeros((1, 65), np.float64)
            forgroundModel = np.zeros((1, 65), np.float64)
            rect = (10, 10, width-30, height-30)
            cv2.grabCut(imgInput, mask, rect, backgroundModel,
                        forgroundModel, 5, cv2.GC_INIT_WITH_RECT)
            mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
            image_1 = imgInput*mask[:, :, np.newaxis]
            background = imgInput - image_1
            background[np.where((background > [0, 0, 0]).all(axis=2))] = [0, 0, 0]
            imgFinal = background + image_1
            cv2.imwrite(file,imgFinal)     

#ลบไฟล์รูปภาพจากโฟลเดอร์ uploads  
def delete_image():
    files = glob.glob(os.path.join('static/uploads/*'))
    for file in files:
        os.remove(file)

def show_image():
    img = []
    image_folder = 'static/uploads/'
    # Get a list of all image files in the folder
    image_files = glob.glob(os.path.join(image_folder, '*.png'))
    # Loop through the image files and process each one
    for image_file in image_files:
        # print(str(image_file))  # This will print the full path of each image file
        img.append(image_file)
    print(str(img))
    return img

@app.route('/', methods=['GET'])
def index():
    # หน้า page หลัก
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':         # รับไฟล์ของ post จาก index.html 
        delete_image() 
        f = request.files['file']        # เซฟรูปภาพไว้ที่ folder /uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'static/uploads', secure_filename(f.filename))
        f.save(file_path) 

        remove_background()

        crop_image(file_path)
        results, accuracies, accuracy_percentage = model_predict()  # Get predictions and accuracies
        img = show_image()
        data = [{'result': result, 'accuracy': accuracy, 'accuracy_average': accuracy_average, 'img_file': img_file}
                for result, accuracy, accuracy_average, img_file in zip(results, accuracies, accuracy_percentage, img)]

        return jsonify(data)  # Return JSON response containing results and accuracies

    # delete_image()  #ลบไฟล์รูปภาพจากโฟลเดอร์ uploads   
    return None

if __name__ == '__main__':
    app.run(debug=True)


