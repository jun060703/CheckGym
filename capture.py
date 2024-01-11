import cv2
import firebase_admin
from firebase_admin import credentials, storage
from flask import Flask, render_template, Response
from checkGym import generate_frames
cred = credentials.Certificate({
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
app = Flask(__name__)
firebase_admin.initialize_app(cred, {'storageBucket': 'checkgym-322d2.appspot.com'})
bucket = storage.bucket()

capture = cv2.VideoCapture(0)

capNum = 0

while True:
    ret, frame = capture.read()

    cv2.imshow("ex01", frame)

    key = cv2.waitKey(1)

    if key == ord('c'):
        firebase_path = f'captured_images/_captured_{capNum:}.png'
        blob = bucket.blob(firebase_path)
        capNum += 1

    elif key == ord('q'):
        break
    
@app.route('/')
def face():
    return render_template('facepost.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
capture.release()
if __name__ == "__main__":
    app.run(debug=True)