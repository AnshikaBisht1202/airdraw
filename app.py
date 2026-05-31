from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64
import mediapipe as mp
from mediapipe.tasks import python 
from mediapipe.tasks.python import vision

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

base_options = python.BaseOptions(
    model_asset_path="hand_landmarker.task"
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
    min_hand_detection_confidence=0.6,
    min_hand_presence_confidence=0.6,
    min_tracking_confidence=0.6
)

detector = vision.HandLandmarker.create_from_options(options)


@app.route("/process", methods=["POST"])
def process():

    data = request.json["image"]

    img_data = base64.b64decode(data.split(",")[1])

    np_img = np.frombuffer(img_data, np.uint8)

    frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    print(frame.shape)
    
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

    result = detector.detect(mp_image)

    if result.hand_landmarks:

        hand = result.hand_landmarks[0]

        index_tip = hand[8]

        h, w, _ = frame.shape

        x = int(index_tip.x * w)
        y = int(index_tip.y * h)

        return jsonify({
            "found": True,
            "x": x,
            "y": y
        })

    return jsonify({
            "found": False
        })
if __name__ == "__main__":
    app.run(debug=True)