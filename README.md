# 🤖 Gesture-Controlled Robotic Arm using Computer Vision

A real-time gesture-controlled robotic arm system that uses **MediaPipe** and **OpenCV** to track hand movements and control a servo motor via **ESP32**. The project enables intuitive, contactless human–robot interaction with low latency and visual feedback.

---

## 📌 Project Overview

Traditional robotic control relies on physical interfaces such as joysticks and buttons, which limit natural interaction. This project demonstrates an alternative approach using computer vision to interpret human hand gestures and convert them into robotic motion.

The system captures live video from a webcam, detects hand landmarks using MediaPipe, maps fingertip position to servo angles, and transmits commands to an ESP32 microcontroller for real-time actuation.

---

## ✨ Key Features

* 🎯 Real-time hand tracking (21 landmarks)
* ⚡ Low-latency gesture-to-servo control
* 🔌 Serial communication with ESP32
* 📺 OLED-based live angle feedback
* 🧠 Proportional mapping algorithm
* 🖥️ Interactive project website (GitHub Pages)

---

## 🛠️ Tech Stack

**Software**

* Python
* OpenCV
* MediaPipe
* NumPy
* PySerial

**Hardware**

* ESP32 Dev Board
* Servo Motor (SG90 or equivalent)
* OLED Display (0.96" I2C)
* Webcam

---

## 🏗️ System Architecture

```
Webcam → OpenCV → MediaPipe → Mapping Algorithm → ESP32 → Servo Motor → OLED
```

**Workflow:**

1. Webcam captures live video
2. MediaPipe detects hand landmarks
3. Index fingertip X-position is extracted
4. Position mapped to servo angle (0–180°)
5. Angle sent via serial to ESP32
6. ESP32 generates PWM for servo
7. OLED displays real-time angle

---

## 📂 Repository Structure

```
gesture-controlled-robotic-arm/
│
├── index.html          # Project website
├── requirements.txt    # Python dependencies
│
├── opencv_code/        # Computer vision scripts
│   ├── test_trace.py
│   ├── test_arm.py
│   ├── test_led.py
│   └── test_servo.py
│
├── esp32_code/         # ESP32 firmware
│   ├── cv_led.ino
│   ├── servo_count.ino
│   └── servo_trace.ino
│
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/vishy-ui/gesture-controlled-robotic-arm.git
cd gesture-controlled-robotic-arm
```

---

### 2️⃣ Create Virtual Environment (Recommended)

**Windows (PowerShell)**

```bash
python -m venv venv
venv\Scripts\activate
```

**Windows (CMD)**

```bash
python -m venv venv
venv\Scripts\activate.bat
```

### 3️⃣ Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 4️⃣ Run the Vision Module

```bash
python opencv_code/test_arm.py
```

---

### 5️⃣ Upload ESP32 Firmware

1. Open Arduino IDE
2. Navigate to `esp32_code/`
3. Select the required `.ino` file
4. Upload to ESP32

---

## 🌐 Live Project

🔗 **Website:**
https://vishy-ui.github.io/gesture-controlled-robotic-arm/

🔗 **Repository:**
https://github.com/vishy-ui/gesture-controlled-robotic-arm

---

## 🚧 Challenges Faced

* Maintaining stable hand detection under varying lighting
* Reducing serial communication latency
* Minimizing servo jitter
* Ensuring smooth proportional mapping

---

## 🔮 Future Work

* Multi-DOF robotic arm control
* ROS2 integration
* Gazebo simulation validation
* Advanced gesture recognition
* Collision detection and safety constraints

---

## 👨‍💻 Author

**Vishwas Patel**
B.Tech Computer Science & Engineering
Reg No: 2427030557

**Project Guide:**
Dr. Rishi Gupta

---

## 📜 License

This project is developed for academic and research purposes.
