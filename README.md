# AI Based Signature Verification for Forensic Document Analysis

An AI-powered web application for verifying handwritten signatures using **Computer Vision and Deep Learning**. The system compares a reference signature with a questioned signature and determines whether the signature is **Genuine or Forged** based on their similarity.

## 🚀 Project Overview

Signature verification is an important process in forensic document analysis. Manual verification can be time-consuming and may depend on human expertise. This project uses **Convolutional Neural Networks (CNN)** and image-processing techniques to automate the verification process.

The application allows users to upload two signatures:

* **Reference Signature** – Known genuine signature
* **Verification Signature** – Signature to be tested

The system preprocesses both images, extracts important features, calculates their similarity, and displays the verification result.

## ✨ Features

* Reference and verification signature upload
* Image preprocessing using OpenCV
* Deep Learning-based feature extraction
* Similarity score calculation
* Genuine / Forged classification
* Signature image preview
* Verification history
* User login and session management
* Forensic-themed web interface

## 🛠️ Technologies Used

**Frontend:** HTML, CSS, Bootstrap, JavaScript

**Backend:** Python, Flask

**AI / Machine Learning:** TensorFlow, Keras, OpenCV, NumPy, Scikit-learn

**Database:** MySQL

## ⚙️ System Workflow

```text
Upload Signatures
       ↓
Image Preprocessing
       ↓
Feature Extraction
       ↓
Similarity Calculation
       ↓
Threshold Comparison
       ↓
Genuine / Forged Result
```

## 📁 Project Structure

```text
Signature-Verification/
│
├── app.py
├── train.py
├── model/
├── templates/
├── static/
├── uploads/
├── data/
├── requirements.txt
└── README.md
```

## 🎯 Applications

* Forensic document analysis
* Bank signature verification
* Financial document verification
* Identity verification
* Document fraud detection

## 👩‍💻 Author

**Nandhini Palaniselvam**

M.Sc. Computer Science 
Python & AI Enthusiast
