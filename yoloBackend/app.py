from importlib import import_module
import os, cv2
from flask import Flask, render_template, Response, request, redirect, url_for, jsonify, send_file

from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import random
from datetime import datetime
from ultralytics import YOLO
import gc
# Load the YOLOv8 model
model = YOLO('yolov5su.pt')
app = Flask(__name__)
CORS(app, resources=r'/*')  # 注册CORS, "/*" 允许访问所有api

# 定义全局变量
rtmp_url = ''
isPause = False


def release_camera(cap):
    # 释放摄像头资源
    cap.release()


def get_rtmp_camera(url):
    cap = cv2.VideoCapture(url)
    return cap


def process_frame(frame):
    # 在这里对视频帧进行处理
    # 这里只是一个示例，你可以根据需要自定义处理逻辑
    # 例如这里就返回yolo检测的结果
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if isPause:
        return frame  # 如果暂停，则直接返回原始帧
    res = model(frame)  # predict on an image
    res_plotted = res[0].plot()
    return res_plotted


def generate_rtmp_frames(url):
    # 创建VideoCapture对象
    cap = get_rtmp_camera(url)
    global isPause
    while True:
        ret, frame = cap.read()

        if not ret:
            print("break now")
            break

        processed_frame = process_frame(frame)
        # 将处理后的帧转换为JPEG格式
        ret, buffer = cv2.imencode('.jpg', processed_frame)
        frame_data = buffer.tobytes()

        if isPause:
            # 如果暂停，释放摄像头资源并等待重新获取
            release_camera(cap)
            del cap
            gc.collect()
            break
        # 使用生成器生成视频帧
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')
    return 200


@app.route('/rtmp', methods=['GET'])
@cross_origin(supports_credentials=True)
def rtmp():
    global isPause
    isPause = False
    global rtmp_url
    rtmp_url = request.args.get('url')
    print(str(rtmp_url))
    print("-----------")
    return Response(generate_rtmp_frames(rtmp_url),
                         mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/stop', methods=['POST'])
@cross_origin(supports_credentials=True)
def stopyolo():
    "Stop yolo"
    global isPause
    global cap  # 从全局变量获取摄像头资源
    if isPause:
        release_camera(cap)  # 如果已暂停，释放摄像头资源
        cap = None
        isPause = False
        return jsonify(message="YOLO detection resumed")
    else:
        if cap is None:
            cap = get_rtmp_camera(rtmp_url)  # 重新打开摄像头资源
        isPause = True
        return jsonify(message="YOLO detection paused")


if __name__ == '__main__':
    cap = None
    app.run(host='0.0.0.0', port=5002)