# 🧍‍♂️ Real-Time Human Detection & Tracking  
### Using State-of-the-Art Models on Laptop & FastMOT Deployment on Jetson Nano

## 🚀 Overview
Human detection and tracking are essential tasks in computer vision, powering applications such as surveillance, robotics, autonomous navigation, and crowd analytics.

This project evaluates **real-time multi-object human tracking** across two environments:

1. **Laptop (RTX GPU):**  
   Running state-of-the-art **YOLOv8 + BYTETracker** for maximum accuracy and smooth tracking.

2. **Jetson Nano (Edge Device):**  
   Deploying the optimized **FastMOT** pipeline to achieve real-time performance under computational constraints.

The goal is to compare **accuracy, inference speed, and deployment feasibility** between high-end hardware and embedded systems.

---

## 🎥 State-of-the-Art MOT Results (Laptop)
The following demo shows YOLOv8 + BYTETracker running on a laptop GPU:

![State of the Art Demo](src/state_of_the_art/out.gif)

This pipeline provides:
- High-accuracy human detection  
- Stable multi-object ID tracking  
- Real-time performance on standard desktop hardware  

---

## 🧠 Laptop Pipeline (YOLOv8 + BYTETracker)

Components used:
- **YOLOv8 (Ultralytics):** Real-time deep-learning object detector  
- **BYTETracker:** Robust low-ID-switch multi-object tracker  
- **OpenCV:** Visualization and video processing  

This configuration is close to state-of-the-art and ideal for benchmarking accuracy.

---

## 🟩 Jetson Nano Deployment (FastMOT)

Since running YOLOv8 + BYTETracker directly on Jetson Nano is not practical, this project uses:

🔗 **FastMOT:** https://github.com/GeekAlexis/FastMOT

FastMOT is optimized for Jetson devices and provides:
- TensorRT-accelerated detectors  
- Lightweight tracking modules  
- Real-time FPS even on Jetson Nano  

The Jetson portion of this project will include:
- Setup & installation guide  
- TensorRT engine generation  
- Real-time tracking demo on Nano  
- Performance comparison against laptop results  

---

## 📊 Objective: Laptop vs Jetson Performance Comparison

| Hardware | Detector | Tracker | FPS | Notes |
|---------|----------|---------|-----|-------|
| **Laptop (RTX GPU)** | YOLOv8n/s | BYTETracker | High | State-of-the-art accuracy |
| **Jetson Nano** | FastMOT TensorRT model | DeepSORT / KLT / ReID | Moderate | Optimized for edge deployment |

This comparison highlights the trade-off between **accuracy** and **real-time performance** across platforms.

---

## 📂 Repository Structure

