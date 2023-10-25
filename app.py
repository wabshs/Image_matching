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


@app.route('/image_matching')
def matching():
    image1_path = 'assets/e.jpg'
    image2_path = 'assets/e.jpg'
    # 读取两张图片
    image1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
    image2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)

    # 调整图片大小，确保两张图片具有相同的尺寸
    image1 = cv2.resize(image1, (image2.shape[1], image2.shape[0]))

    # 计算结构相似性指数
    similarity_score = ssim(image1, image2)
    print(similarity_score)
    return '请返回控制台查看相似度'


ALLOWED_EXTENSIONS = {'png', 'jpg', 'JPG', 'PNG'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run()
