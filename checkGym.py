from flask import Flask, render_template, Response
import cv2
import numpy as np
import dlib
import firebase_admin
from firebase_admin import credentials, storage
import os

app = Flask(__name__)
predictor_file = 'C:/Users/Samsung/Desktop/CheckGym/shape_predictor_68_face_landmarks (1).dat'
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_file) 


firebase_admin.initialize_app(cred, {'storageBucket': 'checkgym-322d2.appspot.com'})
bucket = storage.bucket()

class FaceRecognition:
    detector = dlib.get_frontal_face_detector()
    cap = cv2.VideoCapture(0)

    def __init__(self):
        self.i = 0
        self.local_paths = []

    def download_image(self, remote_image_path, local_image_path):
            blob = bucket.blob(remote_image_path)
            blob.download_to_filename(local_image_path)
    def load_compare_image(self, local_image_path):
        global compare_image
        compare_image = cv2.imread(local_image_path)

    def generate_frames(self):
        while True:
            remote_image_path = f"captured_images/_captured_{self.i}.png"
            local_image_path = f"./downloaded_image_{self.i}.jpg"
            self.download_image(remote_image_path, local_image_path)
            self.local_paths.append(local_image_path)
            self.load_compare_image(local_image_path)

            success, frame = self.cap.read()

            max_size = 700
            if max(frame.shape) > max_size:
                scale_factor = max_size / max(frame.shape)
                frame = cv2.resize(frame, None, fx=scale_factor, fy=scale_factor)

            if compare_image is not None:
                compare_image_resized = cv2.resize(compare_image, (frame.shape[1], frame.shape[0]))

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rects = self.detector(gray, 1)

            for (i, rect) in enumerate(rects):
                points = np.matrix([[p.x, p.y] for p in predictor(gray, rect).parts()])

                x, y, w, h = rect.left(), rect.top(), rect.width(), rect.height()
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                match_result = False

                for (i, point) in enumerate(points):
                    x = point[0, 0]
                    y = point[0, 1]

                    difference = cv2.absdiff(frame, compare_image_resized)
                    mean_difference = np.mean(difference)

                    if mean_difference < 80:
                        match_result = True

                if match_result:
                    cv2.putText(frame, "true", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                else:
                    cv2.putText(frame, "false", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

            self.i += 1

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/video_feed')
def video_feed():
    return Response(FaceRecognition().generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
