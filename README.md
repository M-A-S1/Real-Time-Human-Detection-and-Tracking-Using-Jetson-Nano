# 🧍‍♂️ Real-Time Human Detection & Tracking

## 🚀 Overview
Human detection and tracking are fundamental problems in computer vision with applications in **surveillance, robotics, autonomous navigation, and crowd analytics**.

This project presents a **comparative evaluation of real-time multi-object human tracking** across two hardware environments:

1. **Laptop (RTX GPU)**  
   → High-accuracy pipeline using **YOLOv8 + BYTETracker**

2. **Jetson Nano (Edge Device)**  
   → Resource-efficient pipeline using **YOLOv4-tiny + FastMOT**

The objective is to analyze the **accuracy–speed trade-off**, evaluate **detector and tracker performance**, and study **deployment feasibility on edge devices**.

---

## 🧠 Pipelines Overview

### 💻 Laptop (RTX GPU)
- **Detector:** YOLOv8 (Ultralytics)
- **Tracker:** BYTETracker
- **Frameworks:** PyTorch, OpenCV
- **Goal:** State-of-the-art accuracy and stable multi-object tracking

### 🟩 Jetson Nano (Edge Device)
- **Detector:** YOLOv4 / YOLOv4-tiny
- **Tracker:** FastMOT (DeepSORT / KLT + ReID)
- **Acceleration:** TensorRT
- **Goal:** Real-time performance under constrained compute

---

## 🧠 Laptop Pipeline: YOLOv8 + BYTETracker
**Components:**
- **YOLOv8:** High-accuracy real-time object detector
- **BYTETracker:** Robust data association with minimal ID switches
- **OpenCV:** Visualization and video processing

### 🎥 State-of-the-Art MOT Demo
![State of the Art Demo](output/state_of_the_art.gif)

**Key Characteristics:**
- High detection accuracy  
- Stable identity preservation  
- ~30 FPS on RTX GPU  

---

## 🟩 Jetson Nano Deployment: FastMOT

Due to hardware constraints, YOLOv8 is not feasible on Jetson Nano. Instead, **FastMOT** is used as a lightweight MOT framework.

🔗 **FastMOT Repository:** https://github.com/GeekAlexis/FastMOT

### 🔧 FastMOT Features
- TensorRT-optimized inference  
- Hybrid tracking using **DeepSORT, KLT, and ReID**  
- Designed for embedded NVIDIA platforms  

---

### 📉 YOLOv4-tiny Training Curves
The following plot shows the **training and validation curves** for YOLOv4-tiny, including loss convergence and performance stabilization over epochs.

![YOLO Training Curves](output/yolo_train.png)

> **Observation:**  
> The curves indicate stable convergence with no severe overfitting, validating the effectiveness of training on the COCO human subset.

---

### 🎥 YOLOv4-tiny Standalone Testing (Colab)
![YOLOv4-tiny Demo](output/yolov4_tiny.gif)

---

### 🎥 FastMOT + YOLOv4-tiny on Jetson Nano
![FastMOT Jetson Demo](output/motwithyolov4tiny_on_jetson.gif)

---

## 🧪 Detector Evaluation (YOLOv4-tiny)

YOLOv4-tiny was trained on the **COCO human class subset (4299 images)** and evaluated using standard detection metrics.

### 📊 Detection Metrics

| Metric | Value |
|------|------|
| **AP (Class)** | 40.10 |
| **Precision** | 0.70 |
| **Recall** | 0.35 |
| **F1-score** | 0.46 |
| **mAP** | 0.4009 |

> **Observation:**  
> The detector favors **precision over recall**, which is desirable for tracking pipelines where false positives degrade ID consistency.

---

### 📈 Detector Comparison (AP@0.5)
Comparison of **YOLOv4-tiny**, **YOLOv7-tiny**, and **YOLOv7**:

![AP Comparison](output/AP_yolo.png)

---

### 🧩 Confusion Matrix (YOLOv4-tiny)
Illustrates true positives, false positives, and missed detections:

![Confusion Matrix](output/yolo_confusion.png)

---

## 📊 Multi-Object Tracking Evaluation (Jetson Nano)

### 🔹 Quantitative Tracking Results

| Dataset | MOTA (%) | IDF1 (%) | HOTA (%) | MOTP (%) | MT | ML |
|-------|----------|----------|----------|----------|----|----|
| **MOT17 (Pedestrian)** | 50.60 | 61.74 | 51.23 | 85.13 | 78 | 158 |
| **MOT20 (Pedestrian)** | 55.22 | 48.95 | 41.11 | 84.79 | 443 | 377 |

---

### 🔹 Reference: Original FastMOT Results (MOT20)

| Method | MOTA (%) | IDF1 (%) | HOTA (%) | MOTP (%) | MT | ML |
|------|----------|----------|----------|----------|----|----|
| **FastMOT (Original)** | 66.8 | 56.4 | 45.0 | 79.3 | 912 | 274 |

> **Note:**  
> Performance gap is expected due to **hardware constraints**, **custom-trained detector**, and **real-world deployment conditions**.

---

### 🎥 MOT17 Real-Time Tracking on Jetson Nano (~10 FPS)
The following GIF shows **FastMOT + YOLOv4-tiny** running on **MOT17** in real time on Jetson Nano:

![MOT17 Jetson GIF](output/mot_vid.gif)

---

### 🖼️ MOT20 Qualitative Results
Sample frames demonstrating tracking performance on **MOT20**, highlighting dense pedestrian scenes:

| Frame 1 | Frame 2 |
|--------|--------|
| ![](output/1.jpeg) | ![](output/2.jpeg) |
| ![](output/3.jpeg) | ![](output/4.jpeg) |


---


### 📈 MOT17 & MOT20 Tracking Curves
Tracking performance trends:

![MOT17 Results](output/mot1.jpeg)
![MOT20 Results](output/mot2.jpeg)

---

## ⚖️ Performance Comparison

| Hardware | Detector | Tracker | FPS | Notes |
|--------|----------|---------|-----|------|
| **Laptop (RTX GPU)** | YOLOv8 | BYTETracker | ~30 | State-of-the-art accuracy |
| **Jetson Nano** | YOLOv4 (Pre-trained) | FastMOT | 4–5 | Low accuracy |
| **Jetson Nano** | YOLOv4-tiny (600 imgs) | FastMOT | 12–15 | Improved FPS, unstable |
| **Jetson Nano** | YOLOv4-tiny (COCO – 4299 imgs) | FastMOT | 12–15 | Best balance |

---

## 🏁 Conclusion
- **YOLOv8 + BYTETracker** delivers superior accuracy but requires powerful GPUs.
- **YOLOv4-tiny + FastMOT** enables **real-time multi-object tracking on edge devices**.
- The project highlights the **accuracy–efficiency trade-off** crucial for embedded deployment.

This repository demonstrates an end-to-end **detector–tracker evaluation and deployment pipeline** suitable for both academic research and real-world edge applications.

---
