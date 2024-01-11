from flask import Flask, render_template, Response
import cv2
import numpy as np
import dlib

app = Flask(__name__)

ALL = list(range(0, 68))  # 점을 표시
RIGHT_EYEBROW = list(range(17, 22))
LEFT_EYEBROW = list(range(22, 27))
RIGHT_EYE = list(range(36, 42))
LEFT_EYE = list(range(42, 48))
NOSE = list(range(27, 36))
MOUTH_OUTLINE = list(range(48, 61))
MOUTH_INNER = list(range(61, 68))
JAWLINE = list(range(0, 17))

index = ALL
predictor_file = 'C:/Users/Samsung/Desktop/CheckGym/shape_predictor_68_face_landmarks (1).dat'
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_file)

cap = cv2.VideoCapture(0)

image_file = 'C:/Users/Samsung/Desktop/CheckGym/static/img/20240101_230333.jpg'
compare_image = cv2.imread(image_file)

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break

        max_size = 700
        if max(frame.shape) > max_size:
            scale_factor = max_size / max(frame.shape)
            frame = cv2.resize(frame, None, fx=scale_factor, fy=scale_factor)

        compare_image_resized = cv2.resize(compare_image, (frame.shape[1], frame.shape[0]))

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 1)

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

                if mean_difference < 72:
                    match_result = True

            if match_result:
                cv2.putText(frame, "true", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "false", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
