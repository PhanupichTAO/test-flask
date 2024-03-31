import os
import glob


# # Keras
from keras.models import load_model
# from keras.preprocessing import image
# import keras.utils as image
# from PIL import Image

import numpy as np
import cv2

from flask import Flask, jsonify, request, render_template
from werkzeug.utils import secure_filename


app = Flask(__name__, static_url_path='/static')

model = load_model('model/model__data_aug_BGR_RGB.h5') #ใช้อันนี้
model.make_predict_function()

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

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':         # รับไฟล์ของ post จาก index.html 
        delete_image() 
        f = request.files['file']        # เซฟรูปภาพไว้ที่ folder /uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'static/uploads', secure_filename(f.filename))
        f.save(file_path) 

        remove_background()

        # crop_image(file_path)
        # results, accuracies, accuracy_percentage = model_predict()  # Get predictions and accuracies
        # img = show_image()
        # data = [{'result': result, 'accuracy': accuracy, 'accuracy_average': accuracy_average, 'img_file': img_file}
        #         for result, accuracy, accuracy_average, img_file in zip(results, accuracies, accuracy_percentage, img)]

        # return jsonify(data)  # Return JSON response containing results and accuracies
        return None

    return None


@app.route('/', methods=['GET'])
def index():
    # หน้า page หลัก
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

