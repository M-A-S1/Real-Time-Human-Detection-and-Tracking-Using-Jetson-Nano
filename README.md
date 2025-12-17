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

## 🏗️ Model Architecture and Motivation

This project adopts a detector–tracker decoupled architecture tailored to hardware constraints.

- **YOLOv8 + BYTETracker** is used on the RTX laptop to maximize detection accuracy and identity stability, leveraging strong GPU compute.
- **YOLOv4-tiny + FastMOT** is used on Jetson Nano to enable real-time tracking under strict memory and power constraints.

The architectural choices reflect a deliberate **accuracy–efficiency trade-off**, demonstrating how model complexity must scale with available hardware.

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

## 📂 Dataset Used

- **Training dataset:** COCO human (person class) subset  
- **Training images:** 4,299  
- **Evaluation datasets:** MOT17 and MOT20 (pedestrian class)

The COCO subset provides diverse human appearances, while MOT17/MOT20 enable standardized multi-object tracking evaluation under real-world crowd conditions.

---

### 📉 YOLOv4-tiny Training Curves
The following plot shows the **training curve** for YOLOv4-tiny, depicting loss over epochs.

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

## 📐 Evaluation Metrics Explanation

- **Precision:** Fraction of detected humans that are correct. High precision reduces false positives, which is critical for stable tracking.
- **Recall:** Fraction of ground-truth humans that are detected. Lower recall indicates missed detections, common in lightweight models.
- **F1-score:** Harmonic mean of precision and recall.
- **Confusion Matrix:** Shows true positives, false positives, and false negatives. True negatives are not defined in object detection due to the vast background.

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

## 📚 Comparison with Related Work

- **BYTETrack (ECCV 2022):** Achieves high IDF1 by associating both high- and low-confidence detections, performing best with strong detectors such as YOLOv8.
- **DeepSORT:** Uses appearance embeddings to reduce ID switches but incurs higher computational cost.
- **FairMOT:** Jointly learns detection and ReID, achieving strong identity preservation but requiring more compute and complex training.

Compared to these methods, FastMOT prioritizes real-time embedded deployment, resulting in lower accuracy but significantly improved efficiency on edge devices.

---

## ⚖️ Performance Comparison

| Hardware | Detector | Tracker | FPS | Notes |
|--------|----------|---------|-----|------|
| **Laptop (RTX GPU)** | YOLOv8 | BYTETracker | ~30 | State-of-the-art accuracy |
| **Jetson Nano** | YOLOv4 (Pre-trained) | FastMOT | 4–5 | Low accuracy |
| **Jetson Nano** | YOLOv4-tiny (600 imgs) | FastMOT | 12–15 | Improved FPS, unstable |
| **Jetson Nano** | YOLOv4-tiny (COCO – 4299 imgs) | FastMOT | 12–15 | Best balance |

---

## ⚠️ Limitations

- Reduced recall due to lightweight detector architecture.
- Performance degradation in dense crowds and long occlusions (MOT20).
- Strong dependency on detector quality for tracking stability.
- High-accuracy pipeline requires GPU hardware and is not edge-deployable.

---


## 🏁 Conclusion
- **YOLOv8 + BYTETracker** delivers superior accuracy but requires powerful GPUs.
- **YOLOv4-tiny + FastMOT** enables **real-time multi-object tracking on edge devices**.
- The project highlights the **accuracy–efficiency trade-off** crucial for embedded deployment.

This repository demonstrates an end-to-end **detector–tracker evaluation and deployment pipeline** suitable for both academic research and real-world edge applications.

---

## 🤖 Use of AI Tools

AI tools such as ChatGPT were used as a **supportive aid** for:
- Understanding code and how to run it
- Evaluation metrics
- Jetson debugging 
- Structuring documentation

All model training, experiments, evaluations, and results were performed independently. No AI tools were used to generate datasets, train models, or produce experimental results.

