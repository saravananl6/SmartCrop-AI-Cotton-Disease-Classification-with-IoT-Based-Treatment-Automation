# # app.py
# import os
# import csv
# import numpy as np
# import json
# from flask import Flask, render_template, request, redirect, url_for, session, flash
# from werkzeug.utils import secure_filename
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing import image
# from PIL import Image
# import io
# import base64
# import serial
# import time

# # Change 'COM3' to your Arduino port (e.g., 'COM4' or '/dev/ttyACM0')
# arduino = serial.Serial('COM3', 9600, timeout=1)
# time.sleep(2) 

# app = Flask(__name__)
# app.secret_key = 'cotton_disease_prediction_app'

# # Configuration
# UPLOAD_FOLDER = 'static/uploads'
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
# MODEL_PATH = 'model/final_saved_model.h5'
# PESTICIDE_CSV = 'cotton_pesticides.csv'
# USERS_FILE = 'users.json'
# # SERIAL_PORT = 'COM3'  # Change to your Arduino port
# # BAUD_RATE = 9600

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Load model and pesticide data
# model = load_model(MODEL_PATH)
# pesticide_data = {}

# # Load pesticide recommendations from CSV
# with open(PESTICIDE_CSV, mode='r') as infile:
#     reader = csv.reader(infile)
#     next(reader)  # Skip header
#     for row in reader:
#         pesticide_data[row[0]] = {
#             'pesticide': row[1],
#             'description': row[2],
#             'spray_rule': row[3]
#         }

# # Class mapping
# class_mapping = {
#     0: 'Aphids',
#     1: 'Army worm',
#     2: 'Bacterial blight',
#     3: 'Cotton Boll Rot',
#     4: 'Green Cotton Boll',
#     5: 'Healthy',
#     6: 'Powdery mildew',
#     7: 'Target spot'
# }

# # IoT device groups
# group_a = ['Aphids', 'Army worm', 'Bacterial blight', 'Cotton Boll Rot']
# group_b = ['Green Cotton Boll', 'Powdery mildew', 'Target spot']

# # User management functions
# def load_users():
#     if os.path.exists(USERS_FILE):
#         with open(USERS_FILE, 'r') as f:
#             return json.load(f)
#     return {}

# def save_users(users):
#     with open(USERS_FILE, 'w') as f:
#         json.dump(users, f)

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def preprocess_image(img_path):
#     img = image.load_img(img_path, target_size=(224, 224))
#     img_array = image.img_to_array(img)
#     img_array = np.expand_dims(img_array, axis=0)
#     img_array /= 255.0
#     return img_array

# @app.route('/')
# def index():
#     if 'username' in session:
#         return render_template('index.html')
#     return redirect(url_for('login'))

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
        
#         # Load users from JSON file
#         users = load_users()
        
#         # Check if user exists and password matches
#         if username in users and users[username] == password:
#             session['username'] = username
#             flash('Login successful!', 'success')
#             return redirect(url_for('index'))
#         else:
#             flash('Invalid credentials', 'danger')
#     return render_template('login.html')

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
        
#         # Load existing users
#         users = load_users()
        
#         # Check if username already exists
#         if username in users:
#             flash('Username already exists!', 'danger')
#         else:
#             # Add new user
#             users[username] = password
#             save_users(users)
#             flash('Registration successful! Please login.', 'success')
#             return redirect(url_for('login'))
#     return render_template('register.html')

# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     flash('You have been logged out', 'info')
#     return redirect(url_for('login'))

# @app.route('/predict', methods=['POST'])
# def predict():
#     if 'username' not in session:
#         return redirect(url_for('login'))
    
#     if 'file' not in request.files:
#         flash('No file part', 'danger')
#         return redirect(request.url)
    
#     file = request.files['file']
#     if file.filename == '':
#         flash('No image selected', 'danger')
#         return redirect(request.url)
    
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(filepath)
        
#         # Preprocess and predict
#         processed_image = preprocess_image(filepath)
#         predictions = model.predict(processed_image)
#         predicted_class_idx = np.argmax(predictions[0])
#         confidence = np.max(predictions[0]) * 100
#         predicted_class = class_mapping[predicted_class_idx]
        
#         # Get pesticide recommendations
#         if predicted_class in pesticide_data:
#             pesticide_info = pesticide_data[predicted_class]
#             pesticide = pesticide_info['pesticide']
#             description = pesticide_info['description']
#             spray_rule = pesticide_info['spray_rule']
#         else:
#             pesticide = "No specific recommendation"
#             description = "No specific description"
#             spray_rule = "No specific spray recommendation"
        
#         # IoT command logic
#         iot_command = None
#         if predicted_class in group_a:
#             arduino.write(b'A')
#         elif predicted_class in group_b:
#             arduino.write(b'B')
#         arduino.close()

#         # Convert image to base64 for display
#         img = Image.open(filepath)
#         buffered = io.BytesIO()
#         img.save(buffered, format="JPEG")
#         img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
#         return render_template('dashboard.html', 
#                               image=img_str,
#                               prediction=predicted_class,
#                               confidence=f"{confidence:.2f}%",
#                               pesticide=pesticide,
#                               description=description,
#                               spray_rule=spray_rule,
#                               iot_command=iot_command)
    
#     flash('Invalid file format', 'danger')
#     return redirect(url_for('index'))

# if __name__ == '__main__':
#     if not os.path.exists(UPLOAD_FOLDER):
#         os.makedirs(UPLOAD_FOLDER)
#     app.run(debug=True)

# app.py
import os
import csv
import numpy as np
import json
import io
import base64
import time
import serial
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image

app = Flask(__name__)
app.secret_key = 'cotton_disease_prediction_app'

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MODEL_PATH = 'model/final_saved_model.h5'
PESTICIDE_CSV = 'cotton_pesticides.csv'
USERS_FILE = 'users.json'
SERIAL_PORT = 'COM3'   # ✅ Change if needed
BAUD_RATE = 9600

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load model and pesticide data
model = load_model(MODEL_PATH)
pesticide_data = {}

# Load pesticide recommendations from CSV
with open(PESTICIDE_CSV, mode='r') as infile:
    reader = csv.reader(infile)
    next(reader)  # Skip header
    for row in reader:
        pesticide_data[row[0]] = {
            'pesticide': row[1],
            'description': row[2],
            'spray_rule': row[3]
        }

# Class mapping
class_mapping = {
    0: 'Aphids',
    1: 'Army worm',
    2: 'Bacterial blight',
    3: 'Cotton Boll Rot',
    4: 'Green Cotton Boll',
    5: 'Healthy',
    6: 'Powdery mildew',
    7: 'Target spot'
}

# IoT device groups
group_a = ['Aphids', 'Army worm', 'Bacterial blight', 'Cotton Boll Rot']
group_b = ['Green Cotton Boll', 'Powdery mildew', 'Target spot']

# ---------- User management ----------
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    return img_array

# ---------- Routes ----------
@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    return redirect(url_for('login'))




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()

        if username in users and users[username] == password:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()

        if username in users:
            flash('Username already exists!', 'danger')
        else:
            users[username] = password
            save_users(users)
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

# ---------- Prediction + Arduino ----------
@app.route('/predict', methods=['POST'])
def predict():
    if 'username' not in session:
        return redirect(url_for('login'))

    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('No image selected', 'danger')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Preprocess + Predict
        processed_image = preprocess_image(filepath)
        predictions = model.predict(processed_image)
        predicted_class_idx = np.argmax(predictions[0])
        confidence = np.max(predictions[0]) * 100
        predicted_class = class_mapping[predicted_class_idx]

        # Get pesticide info
        pesticide_info = pesticide_data.get(predicted_class, {
            'pesticide': "No specific recommendation",
            'description': "No specific description",
            'spray_rule': "No specific spray recommendation"
        })

        # ---------- Safe Arduino Communication ----------
        iot_command = None
        try:
            with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as arduino:
                time.sleep(2)
                if predicted_class in group_a:
                    arduino.write(b'A')
                    iot_command = 'A'
                elif predicted_class in group_b:
                    arduino.write(b'B')
                    iot_command = 'B'
                elif predicted_class == 'Healthy':
                    arduino.write(b'H')
                    iot_command = 'H'
                print(f"✅ Sent '{iot_command}' to Arduino")
        except serial.SerialException as e:
            print(f"⚠️ Serial communication error: {e}")
            flash('Arduino not connected or port busy.', 'danger')

        # ---------- Convert image to Base64 for dashboard ----------
        img = Image.open(filepath)
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

        return render_template(
            'dashboard.html',
            image=img_str,
            prediction=predicted_class,
            confidence=f"{confidence:.2f}%",
            pesticide=pesticide_info['pesticide'],
            description=pesticide_info['description'],
            spray_rule=pesticide_info['spray_rule'],
            iot_command=iot_command
        )

    flash('Invalid file format', 'danger')
    return redirect(url_for('index'))

# ---------- Main ----------
if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
