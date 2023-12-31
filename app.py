import base64

import numpy as np
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import cv2

from skimage.metrics import structural_similarity as ssim

app = Flask(__name__)
cors = CORS(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


# 文件上传
@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']
        if file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], 'photo_left.jpg')
            file.save(filename)
            return jsonify({'message': 'Upload successful', 'file_path': filename}), 200
        else:
            return jsonify({'message': 'No file uploaded'}), 400
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error uploading file'}), 500


# 文件上传右边
@app.route('/upload-right', methods=['POST'])
def upload_file_right():
    try:
        file = request.files['file']
        if file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], 'photo_right.jpg')
            file.save(filename)
            return jsonify({'message': 'Upload successful', 'file_path': filename}), 200
        else:
            return jsonify({'message': 'No file uploaded'}), 400
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error uploading file'}), 500


# 图像对比
@app.route('/image_matching', methods=['GET'])
def matching():
    image1_path = 'static/photo_left.jpg'
    image2_path = 'static/photo_right.jpg'
    # 读取两张图片
    image1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
    image2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)

    # 调整图片大小，确保两张图片具有相同的尺寸
    image1 = cv2.resize(image1, (image2.shape[1], image2.shape[0]))

    # 计算结构相似性指数
    similarity_score = ssim(image1, image2)
    print(similarity_score)
    return jsonify({'Similarity': similarity_score, 'message': 'success'}), 200


@app.route('/image_matching_2', methods=['GET'])
def matching_2():
    image1_path = 'static/photo_left.jpg'
    image2_path = 'static/photo_right.jpg'

    # 读取两张图片
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)

    # 调整图片大小，确保两张图片具有相同的尺寸
    image1 = cv2.resize(image1, (image2.shape[1], image2.shape[0]))

    # 计算均方误差
    mse = np.sum((image1 - image2) ** 2) / float(image1.shape[0] * image1.shape[1])

    # 均方误差越小，表示图像越相似
    similarity_score = 1 / (1 + mse)

    print(similarity_score)
    return jsonify({'Similarity': similarity_score, 'message': 'success'}), 200


ALLOWED_EXTENSIONS = {'png', 'jpg', 'JPG', 'PNG'}
UPLOAD_FOLDER = './static'  # 存储上传图片的文件夹
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# 保存图片
@app.route('/save-photo', methods=['POST'])
def save_photo():
    try:
        # 获取前端发送的照片数据
        data_url = request.json.get('photoDataUrl')
        # 解码base64数据
        _, img_data = data_url.split(',')
        img_bytes = base64.b64decode(img_data)

        # 保存照片到指定文件夹
        file_path = './static/photo_left.jpg'
        with open(file_path, 'wb') as f:
            f.write(img_bytes)

        return jsonify({'message': 'Photo saved successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error saving photo'}), 500


# 保存右边图片
@app.route('/save-photo-right', methods=['POST'])
def save_photo_right():
    try:
        # 获取前端发送的照片数据
        data_url = request.json.get('photoDataUrl')
        # 解码base64数据
        _, img_data = data_url.split(',')
        img_bytes = base64.b64decode(img_data)

        # 保存照片到指定文件夹
        file_path = './static/photo_right.jpg'
        with open(file_path, 'wb') as f:
            f.write(img_bytes)

        return jsonify({'message': 'Photo saved successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error saving photo'}), 500


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run()
