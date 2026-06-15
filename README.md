Overview

SmartCotton AI is an intelligent agricultural decision-support platform designed to assist farmers in identifying cotton plant diseases and receiving immediate treatment recommendations.

The system utilizes Deep Learning image classification models trained on cotton crop disease datasets to analyze uploaded leaf images and detect disease conditions with confidence scoring.

Based on the detected disease, the platform recommends suitable pesticides, provides treatment guidelines, and communicates with IoT-enabled Arduino devices to automate farming actions.

The application is deployed as a Flask web platform with secure user authentication and interactive dashboards for agricultural monitoring.

Key Features
Farmer Module
User Registration
Secure Login System
Disease Image Upload
Disease Detection Dashboard
Confidence Score Display
Treatment Recommendation
Spray Guidance Instructions
AI Disease Detection
Deep Learning Image Classification
TensorFlow/Keras Model
Automated Disease Recognition
Confidence Score Calculation
Multi-Class Disease Prediction
Smart Agriculture Features
Automated Arduino Communication
IoT Device Integration
Disease-Based Action Triggering
Smart Farm Automation
Real-Time Control Signals
Crop Health Monitoring
Cotton Disease Analysis
Healthy Crop Detection
Pest Identification
Treatment Advisory System
Diseases Detected

The AI model can classify:

Disease Class
Aphids
Army Worm
Bacterial Blight
Cotton Boll Rot
Green Cotton Boll
Powdery Mildew
Target Spot
Healthy Plant
Technologies Used
Backend
Python
Flask
TensorFlow
Keras
Computer Vision
Image Processing
CNN-Based Classification
Data Processing
NumPy
CSV Processing
IoT Integration
Arduino
Serial Communication (PySerial)
Frontend
HTML5
CSS3
JavaScript
Jinja2 Templates
Database & Storage
JSON User Storage
CSV Knowledge Base
AI Workflow
Step 1: Image Upload

Farmer uploads a cotton leaf image.

Leaf Image
↓
Flask Application

Step 2: Image Preprocessing

System resizes image to:

224 × 224

and normalizes pixel values.

Image
↓
Preprocessing
↓
Normalized Tensor

Step 3: Deep Learning Prediction

Preprocessed image is passed into a trained TensorFlow CNN model.

Image Tensor
↓
CNN Model (.h5)
↓
Disease Prediction

Step 4: Confidence Scoring

Prediction probabilities are generated.

Prediction Probabilities
↓
Highest Probability
↓
Confidence Score

Step 5: Disease Identification

Model classifies disease as:

Aphids
Army Worm
Bacterial Blight
Cotton Boll Rot
Green Cotton Boll
Powdery Mildew
Target Spot
Healthy
Step 6: Recommendation Engine

The system retrieves:

Recommended pesticide
Disease description
Spray instructions

from the pesticide database.

Disease
↓
Recommendation Engine
↓
Treatment Plan

Step 7: IoT Automation

Arduino receives commands:

Disease Group	Command
Aphids / Army Worm / Bacterial Blight / Cotton Boll Rot	A
Green Cotton Boll / Powdery Mildew / Target Spot	B
Healthy Plant	H

AI Prediction
↓
Arduino Signal
↓
Smart Farm Device

Step 8: Result Dashboard

Farmer receives:

Disease Name
Confidence Percentage
Pesticide Recommendation
Disease Description
Spray Rules
IoT Status
