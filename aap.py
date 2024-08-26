from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import pandas as pd
import numpy as np
import joblib
import cv2
import os

app = Flask(__name__)
model = joblib.load('model.pkl')  # Load your pre-trained model

# Path to save processed images
IMAGE_PATH = "static/images/output.jpg"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_dataset():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))

    # Process the dataset
    data = pd.read_csv(file)
    data.fillna(data.mean(), inplace=True)
    data.to_csv('processed_dataset.csv', index=False)
    
    return render_template('process.html', data_preview=data.head().to_html())

@app.route('/predict', methods=['POST'])
def predict():
    features = request.form.getlist('features')
    features = [float(x) for x in features]
    prediction = model.predict([features])
    
    return render_template('predict.html', prediction=prediction[0])

@app.route('/image', methods=['POST'])
def image_processing():
    action = request.form['action']
    if action == 'capture_crop':
        capture_and_crop_face()
    elif action == 'apply_filters':
        apply_filters()
    
    return render_template('image_processing.html', image_url=IMAGE_PATH)

def capture_and_crop_face():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        face = frame[y:y+h, x:x+w]
        cv2.imwrite(IMAGE_PATH, face)
        break
    cap.release()

def apply_filters():
    image = cv2.imread(IMAGE_PATH)
    if image is None:
        return

    blur = cv2.GaussianBlur(image, (15, 15), 0)
    cv2.imwrite(IMAGE_PATH, blur)

@app.route('/download')
def download_file():
    return send_from_directory(directory='.', path='processed_dataset.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
