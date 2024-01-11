import cv2
import time
import face_recognition
from flask import Flask, render_template, Response
from pathlib import Path

app = Flask(__name__)

# Load the reference image for face recognition
imgElon = face_recognition.load_image_file('C:/Users/Samsung/Desktop/CheckGym/static/img/20240101_230333.jpg')
imgElon = cv2.cvtColor(imgElon, cv2.COLOR_BGR2RGB)
encodeElon = face_recognition.face_encodings(imgElon)

# Try to open the camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Camera not opened. Check camera index or connection.")
    exit()

capNum = 0 

def generate_frames():
    global capNum  # Use the global variable

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Couldn't read frame from the camera.")
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(frame)

        if face_locations:
            faceLocTest = face_locations[0]
            cv2.rectangle(frame, (faceLocTest[3], faceLocTest[0]), (faceLocTest[1], faceLocTest[2]), (255, 0, 255), 2)

            encodeTest = face_recognition.face_encodings(frame)
            if encodeTest:
                encodeTest = encodeTest[0]

                if encodeElon is not None:
                    results = face_recognition.compare_faces([encodeElon], encodeTest)
                    faceDis = face_recognition.face_distance([encodeElon], encodeTest)

                    cv2.putText(frame, f'{results} {round(float(faceDis[0][0]), 2)}', (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

        ret, jpeg = cv2.imencode('.jpg', frame)
        data = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n\r\n')

        # if cv2.waitKey(1) == ord('c'):
        #     file_path = f'path/to/save/captured_{capNum}.jpg'
        #     cv2.imwrite(file_path, frame)
        #     capNum += 1
        #     print(f"Captured frame saved at: {file_path}")

        time.sleep(0.01)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)
    cap.release()
    cv2.destroyAllWindows()
