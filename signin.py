from flask import Flask, render_template, request, Response, redirect, url_for, session
import firebase_admin
from firebase_admin import credentials, db, credentials, storage
import numpy as np
import dlib
import cv2
from flask import jsonify
import time
<<<<<<< HEAD
import os
=======
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

>>>>>>> 1b671cfdc9d6ab5e88802ab1df52688d9be8f439
app = Flask(__name__)
from datetime import datetime
from werkzeug.utils import secure_filename

# Firebase 관련 설정

firebase_admin.initialize_app(cred, {'databaseURL': 'https://checkgym-322d2-default-rtdb.asia-southeast1.firebasedatabase.app/','storageBucket': 'checkgym-322d2.appspot.com'})
ref = db.reference('users')  # 'users'는 사용자 데이터를 저장할 경로입니다.
bucket = storage.bucket()
# 세션 시크릿 키 설정
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form.get('pw')
        hashed_password = hash_password(password)
        studentId = request.form['studentId']
        name = request.form['name']
        
        # Firebase Realtime Database에 사용자 정보 추가
<<<<<<< HEAD
        user_data = {'email': email, 'pw': password, 'studentId': studentId, 'name': name}
        # 'users' 경로에 사용자 정보 추가
        ref_users = db.reference('users')
        ref_users.push(user_data)
=======
        user_data = {'email': email, 'pw': hashed_password, 'studentId': studentId, 'name': name}
        ref.push(user_data)
>>>>>>> 1b671cfdc9d6ab5e88802ab1df52688d9be8f439
        
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                # 파일 이름에 studentId를 반영하여 안전하게 저장
                filename = secure_filename(f'{studentId}_{file.filename}')
                file_path = f'./static/images/{filename}'
                file.save(file_path)
                

                blob = bucket.blob(f'captured_images/{filename}')
                blob.upload_from_filename(file_path)
                
        return redirect('/facepost')
    return render_template('signin.html')
def hash_password(password):
    # 솔트 생성
    salt = os.urandom(16)

    # PBKDF2 알고리즘을 사용하여 비밀번호 해싱
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))

    # 해시된 비밀번호와 솔트를 조합하여 저장
    hashed_password = f'{base64.urlsafe_b64encode(salt).decode()}${key.decode()}'
    return hashed_password

# 사용자 정보 가져오기

@app.route('/facepost', methods=['GET', 'POST'])
def facepost():
    return render_template('facepost.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/admin_log', methods=['GET', 'POST'])
def get_user():
    users_data = ref.get()
    
    return render_template('admin_log.html', users_data=users_data)

@app.route('/admin_users', methods=['GET', 'POST'])
def get_users():
    users_data = ref.get()
    
    return render_template('admin_users.html', users_data=users_data)


@app.route('/main_login', methods=['GET', 'POST'])
def get_email():
    # Firebase Realtime Database에서 email 가져오기
    student_id = '20401'
    email = ref.get()
    studentId = ref.get()
    sysdate = datetime.now().strftime("%Y-%m-%d %H:%M")
    sysdate = {'sysdate': sysdate}
    # ref.push(sysdate)

    # 가져온 email을 JSON 형태로 반환
    users_data = ref.order_by_child('studentId').equal_to(student_id).get()
    user_info = None
    for key, value in users_data.items():
        if 'studentId' in value and value['studentId'] == student_id:
            user_info = {
                'name': value['name'],
                'studentId': value['studentId']
            }
            break
   
    return render_template('main_login.html', user_info=user_info)    


@app.route('/main_logout', methods=['GET', 'POST'])
def main_logout():
    return render_template('main_logout.html')


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
predictor_file = 'shape_predictor_68_face_landmarks (1).dat'
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_file)

cap = cv2.VideoCapture(0)

image_file = './static/imges/Con1.jpg'
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
    
capture = cv2.VideoCapture(0)
capNum = 0
def generate_frames():
    while True:
        success, frame = capture.read()
        if not success:
            break

        # Convert the frame to JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # Yield the frame as bytes
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# Route to display the facepost.html template
@app.route('/facepost')
def face():
    return render_template('facepost.html')

# Route to capture a frame
@app.route('/capture_frame', methods=['POST'])
def capture_frame():
    global capNum

    if request.method == 'POST':
        # Read a frame from the webcam
        ret, frame = capture.read()

        # Save the frame to a file
        filename = f'captured_frame_{capNum}.png'
        cv2.imwrite(filename, frame)

        # Upload the frame to Firebase Storage
        blob = bucket.blob(f'/captured_images/{filename}')
        blob.upload_from_filename(filename)

        
        capNum += 1

        return '캡쳐성공'

    return '실패'

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
