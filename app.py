import os
import glob

# import numpy as np
# # Keras
# from keras.models import load_model
# from keras.preprocessing import image
# import keras.utils as image
# from PIL import Image
# import cv2

from flask import Flask, jsonify, request, render_template
from werkzeug.utils import secure_filename


app = Flask(__name__, static_url_path='/static')

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':         # รับไฟล์ของ post จาก index.html 
        # delete_image() 
        # f = request.files['file']        # เซฟรูปภาพไว้ที่ folder /uploads
        # basepath = os.path.dirname(__file__)
        # file_path = os.path.join(basepath, 'static/uploads', secure_filename(f.filename))
        # f.save(file_path) 

        # remove_background()

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

