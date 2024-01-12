from flask import Flask, render_template, request, Response, redirect, url_for, session
import firebase_admin
from firebase_admin import credentials, db, credentials, storage
import numpy as np
import dlib
import cv2
from flask import jsonify
import time

app = Flask(__name__)
from datetime import datetime

# Firebase 관련 설정
cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "checkgym-322d2",
  "private_key_id": "36bf14196423b556d36527b1f7cc2d87cc986042",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDZFy/Wz8ess1Sw\nqd551y2S1s2z2Tm3Yit2EjhBxh6IGUHBdsBZrv2rD6HGfAxn1axUdRH85x+Cnwwb\n7HiAv9dS9O1RVoqXjy3etFxv+tzI3H9+lyShZDjT2k34nNzXAKKt4w7AV3qYV+qW\nGmTmQSm6IOT+41xHKLp69hQRd0eTIS/TI7YkEKO9IDLRO5F1I1Xw9xvNhYUWDaDO\nmoFOBsNcaRQRnjPDc/BuXdWm0OAc5gL9sdW/lNboP54+URjNnTaPhPC/MZKqXlHD\nm5YnhRIUOI6qIH0spYoEs8RYjbTvq23b7S+OmRaUWULSU3nx0QP7OaPqVhfH8ZQ5\n0tCnD5LrAgMBAAECggEAFQt+ybyh+lRc9QG8Q+RGOLvpSQwMrYH7/WaawyJcbb+O\np+osXDiIj5kX8VCvnmLdlK2crTJ10+9sxX0EP+1ZB5bsaQj4rbFlnJDjfSXwJupC\n02TKwKwhWvg775ciGX2oR5WBWPs7mTuJZ2+7l4Hg2t67FEwgjMCeabK9Rn9hSU16\nhMC4nk0YWm67Y6+QGHh6YchC/3lgpfsSSSw7ivCO4rGldow8loOO0bwV7ykquc04\nQuP5AnI7WvYtZYLnh4zyc6aiRZjOL4BGZFqdP1LcgTzoj1GCdUsMnrqMepYxzOSE\nE/Sla8mtEMqNmnAZQGueiDm+a8gUZXkOwEzJ7/n4sQKBgQD5qE+vB/q6OMyCYR4H\nc2CsmFKvDZckoAYvLlFrz6j60zzZscuKdOEfTF+3eD7T1CfLm4ZSv5zsHpIYuVhg\n2QCzuEHQHJoLYQiZPRFFKi2yxB7tY61wnh6cnf8Nq7A29Mgft79dgM3ZoaRbwEHc\nWEZwDNrUnfuN1iW7+kaWfNFJHQKBgQDemxJIv7GFFuQpKPcK1emuRJDThyH/VBR9\nE3meRVp4WO07rApNhIe9FBQl8uf6FI47Hk3pSHcDtM7Sn6quq15kjCQ3br7lpOoC\naq4plX1SF51SMRtHua2lXQEUZzmbMK008juYG9pSfrSlG8zFyvzxrcqD92RxtIWk\ndIeTYPeVpwKBgQC19tY1VdSKXJG6ybxQY+jng5JoYrhyCmzXgKP5t36LauFkLjGT\ndgMLg+gT2oG4dV6YCYBK2bwvYUzM1nKzDBd15muZmu8wMgZJYngu+EIclNOR5N/q\nQGVBc+sNdMDYHWurqorBRPtEj4szEJswVerpCoWJCKjrxVT1gMJoNwt3hQKBgQDX\nS9IGTGiMGRS4/mbYswWcx7Hu896czRw30FMrEVar2Q4xTXZ1fL2v0LCf92wHgkQB\nx5CBFNYO3pu+ODDjWNkllCke99xnzPWLOtSRYYTglfhRWy9QUrQwoF//9MpRX2XW\nNIYQ2rdwXB2pJtcJYgb8VCLvOaGLG5a59P5/OySaNwKBgGCmqUJSDbw/AXRgbJYY\n6a/3cjyZUMX9nuIrkZ1Ibmyf+54w3NO3t9ceK6eiS2+Acz5kXOt5OfAcUFjbtsUU\nDEhK6lwkdN8NNLBeSZ13LRE9gOnNoiJLjEvQaVbJG1kxnMQV9oLJCRegkoD8MzZs\nkXVaFvJlg4UrfZShoBa35eZe\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-bmi70@checkgym-322d2.iam.gserviceaccount.com",
  "client_id": "116016558862174674055",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-bmi70%40checkgym-322d2.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
})
cred2 = credentials.Certificate({
  "type": "service_account",
  "project_id": "checkgym-322d2",
  "private_key_id": "2fa2dd1f7820cfcb9eb443a4d256e23422c11325",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDHaQu+52gvsEDn\nwDAL2O9c5eQThRYkqG+GoJcdGZaVZYSpJX9L0bdoliwCqlVjPPUXcx7wHhvzonao\n4JqovhAARCbwHo5mrepmSH5xckVJM314QQY4f36Tzy0ZW1kTBb3GC+Bd15Gn5EEh\nyRZCKX1B0nOPC5W+Vi0HmNhGPKrXduMGlfCShrzM0965QmNURzGOes0XCjkKD6VU\n/MvMohW6dR8xQrfaR83vMlvCNeoPuCkJQUBY+5dovoDa/6+Mq8ODd6usL8C/vYUv\n40mKgu8SAsIsmku5MVvnTWYj7P6ZKutrayx/ZukocF1DSTESn56VGWS3XUYvwxN0\n6wr3hnbbAgMBAAECggEAQvf2z16UwUs+iPYkzJ3GyVqVba7I4HfGuJ5PEaFJzpOA\n6XNj3FkqcM/aKOz+by0GHKF3VumttnUtx4pitl/aLNS2hPamGTq4GTCocj4PocVO\nkme4CJpcrpQpz7W7ZOWNNalAaROf4ZQJAakwNfkMDWJ5l6Uq3XjAd6gvner67w/w\n6p1UTn4C9fXmz92dhduWwhlFi+GTxT49KPlaNIwPnskoA6kcyL7hy2/t7QfYi56t\nX41YoN6hiiCkRLYubanaf4N5PQ8goiofheN19TwE5f5hMPaoraGSuqqwuCJkiR1v\nf2DH8hcXv5FdkSLffPgdm6/dg0gSh8wso0J9z70pYQKBgQDklO1bMeODJoPK3Cph\njoVpqUCgklyBJ9XwMfpLkkTbFLUbvf3zMJeeEvMXD8X9/7il+zTiI4mulNfKXfpG\njhBZi0PPoleXcBM4lBdKuIYSsGR83S7JlVhpIDf6igoCGpsoDAZk4+EduyD3Erz4\npqQODNqb7rZW3uNQVhbNoBvs+wKBgQDfVFm60KZHamm6M0nmnpNS7DMrjpHRmkkU\nWrBYvaHkjFmMrFMfNuiBZG+Xo/znm6ujbxGPLhXKUlB41pDK7SseBjUAlXCBpdg8\nLGFj3v9mmK2C71XO9i+KHDnc1ZJTqNj/pID83nFvlAeRecSJtBWK0tHlKxrGBrLZ\nOIJye323oQKBgBAQn3XvVawcAts5Cgl9OMcqTA58+t9g61pMSOkSyKAVHn1qpvR2\nj9FeR5NxWlr1pAaWVyslkEGi2F+ypypaRa/lZ8iqAjn0eIVbcx+fRFz/5LAZ43Xr\ndyE8UHLdTMLFF+6CmdhxY5rxUenLeViIbbNHF/4pksscMyGsS0H8ZLoNAoGAR59r\nr4ge66RrB/ZO6xFMOjnaJ0vv5ALRESAMkkku1HdWeNEDT21yn5ywVTeYckbwgteq\nD/s9rcc8W6SkhxAM1fIzqV5D2LBxasro6PipfCPW8bkEEf3OPULUI8iyxvXNsh71\n5yMHyjr1OmiM6YTBq+X0vsRWL9ASJ6wB2elU5kECgYAranXHbi3JdVVppokoa35G\nk5OrfRhH87EVqLF8q+UyavF2Zsxd/I0lcU0fgtR0w23eZt2q6rx4nCeIKD3bm/ct\nxtxgvdG/GsqK/WuZbqa+my7bMoBjYNtN4lf+5l4ODQE7nCb8pd1iSYXZO1hfXIwg\nIMes/TRC6Gsz7K5AsgZgLg==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-bmi70@checkgym-322d2.iam.gserviceaccount.com",
  "client_id": "116016558862174674055",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-bmi70%40checkgym-322d2.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
})
firebase_admin.initialize_app(cred, {'databaseURL': 'https://checkgym-322d2-default-rtdb.asia-southeast1.firebasedatabase.app/','storageBucket': 'checkgym-322d2.appspot.com'})
ref = db.reference('users')  # 'users'는 사용자 데이터를 저장할 경로입니다.
bucket = storage.bucket()
# 세션 시크릿 키 설정
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pw']
        studentId = request.form['studentId']
        name = request.form['name']
        
        
        # Firebase Realtime Database에 사용자 정보 추가
        user_data = {'email': email, 'pw': password, 'studentId': studentId, 'name': name}
        ref.push(user_data)
        
        return redirect('/facepost')
    return render_template('signin.html')


# 사용자 정보 가져오기

@app.route('/facepost', methods=['GET', 'POST'])
def facepost():
    return render_template('facepost.html')

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
    ref.push(sysdate)

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
    
    


def generate_frames():
    cap = cv2.VideoCapture(0)
    capNum = 0

    while True:
        ret, frame = cap.read()

        key = cv2.waitKey(1)

        if key == ord('c'):
            firebase_path = f'captured_images/_captured_{capNum:}.png'
            blob = bucket.blob(firebase_path)
            capNum += 1

        elif key == ord('q'):
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        time.sleep(0.1)
@app.route('/facepost')
def face():
    return render_template('facepost.html')
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
