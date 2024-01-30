import cv2
import firebase_admin
from firebase_admin import credentials, storage
from flask import Flask, render_template, Response



app = Flask(__name__)
firebase_admin.initialize_app(cred, {'storageBucket': 'checkgym-322d2.appspot.com'})
bucket = storage.bucket()

capture = cv2.VideoCapture(0)
capNum = 0

def generate_frames():
    global capNum
    global capture

    while True:
        ret, frame = capture.read()

        cv2.imshow("ex01", frame)

        key = cv2.waitKey(1)

        if key == ord('c'):
            firebase_path = f'captured_images/_captured_{capNum}.png'
            capNum += 1

            cv2.imwrite(firebase_path, frame)

            blob = bucket.blob(firebase_path)
            blob.upload_from_filename(firebase_path)

        elif key == ord('q'):
            break

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def face():
    return render_template('facepost.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
