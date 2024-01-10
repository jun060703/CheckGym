import cv2
import time
import face_recognition
import numpy as np
from flask import Flask, render_template, Response
from fileinput import close


app = Flask(__name__)
face_cascade = cv2.CascadeClassifier('C:/Users/Samsung/Desktop/CheckGym/ddd.xml')

img_check = face_recognition.load_image_file('C:/Users/Samsung/Desktop/CheckGym/static/img/20240101_230333.jpg')
img_check = cv2.cvtColor(img_check, cv2.COLOR_BGR2RGB)
encodeElon = face_recognition.face_encodings(img_check)[0]

cam = cv2.VideoCapture(0)
capNum = 0

def generate_frames():
    while True:
        ret, frame = cam.read()
        if not ret:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        
        face_locations = face_recognition.face_locations(frame)

        if face_locations:
        
            faceLocTest = face_locations[0]

        
            cv2.rectangle(frame, (faceLocTest[3], faceLocTest[0]), (faceLocTest[1], faceLocTest[2]), (255, 0, 255), 2)

        
            encodeTest = face_recognition.face_encodings(frame)[0]

            if encodeElon is not None:
                results = face_recognition.compare_faces([encodeElon], encodeTest)
                faceDis = face_recognition.face_distance([encodeElon], encodeTest)

                cv2.putText(frame, f'{results} {round(faceDis[0], 2)}', (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

        ret, jpeg = cv2.imencode('.jpg', frame)
        data = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n\r\n')
        
        if cv2.waitKey(1) == ord('c'): # c를 누르면 화면 캡쳐 후 파일경로에 저장
            cam = cv2.imwrite('C:/Users/Samsung/Desktop/CheckGym/static/img' % capNum, frame)
        capNum += 1
        time.sleep(0)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=5050, debug=True)
    finally:
        if cam.isOpened():
            cam.release()
        cv2.destroyAllWindows()
