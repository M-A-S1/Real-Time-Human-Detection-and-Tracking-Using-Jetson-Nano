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

- **YOLOv8 + BYTETracker** is used on the RTX laptop to maximize detection accuracy and identity stability.
- **YOLOv4-tiny + FastMOT** is used on Jetson Nano to enable real-time tracking under strict memory and power constraints.

These choices reflect a deliberate **accuracy–efficiency trade-off** required for edge deployment.

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

The COCO subset provides diverse human appearances and scales, while MOT17/MOT20 enable standardized tracking evaluation in crowded scenes.

---

## 📉 YOLOv4-tiny Training Curves
![YOLO Training Curves](output/yolo_train.png)

> **Observation:**  
> Stable convergence with no severe overfitting, validating training effectiveness on the COCO human subset.

---

## 🎥 YOLOv4-tiny Standalone Testing (Colab)
![YOLOv4-tiny Demo](output/yolov4_tiny.gif)

---

## 🎥 FastMOT + YOLOv4-tiny on Jetson Nano
![FastMOT Jetson Demo](output/motwithyolov4tiny_on_jetson.gif)

---

## 🧪 Detector Evaluation (YOLOv4-tiny — **Updated Results**)

YOLOv4-tiny was trained on the **COCO human class subset (4,299 images)** and evaluated using standard detection metrics.

### 📊 Updated Detection Metrics

| Metric | Value |
|------|------|
| **AP (Class)** | **83.06** |
| **Precision** | **0.84** |
| **Recall** | **0.72** |
| **F1-score** | **0.78** |
| **mAP** | **0.8306** |

> **Key Observation:**  
> The detector achieves **high precision and strong recall**, indicating a well-balanced model that significantly improves tracking stability compared to earlier results.

---

## 📐 Detection Metrics Explanation (Updated)

- **Precision (0.84):**  
  84% of detected humans are correct, reducing false positives that cause ID switches.
- **Recall (0.72):**  
  Detects most ground-truth humans, improving track continuity.
- **F1-score (0.78):**  
  Strong balance between precision and recall.
- **AP / mAP (~83%):**  
  Robust localization and classification while remaining lightweight.

> **Note:**  
> True negatives are not defined in object detection due to the vast background; confusion matrices focus on TP, FP, and FN.

---

## 📈 Detector Comparison (AP@0.5)
![AP Comparison](output/AP_yolo.png)

> **Insight:**  
> With AP above 83%, the custom-trained YOLOv4-tiny narrows the gap with heavier YOLO models while remaining edge-deployable.

---

## 🧩 Confusion Matrix (YOLOv4-tiny)
![Confusion Matrix](output/yolo_confusion.png)

---

## 📊 Impact on Multi-Object Tracking
Improved detector quality leads to:
- Fewer missed detections → **higher track continuity**
- Reduced false positives → **fewer ID switches**
- More stable trajectories in crowded scenes (MOT17/MOT20)

This confirms that **detector quality is the dominant factor** in overall tracking performance.

---

## 🎥 MOT17 Real-Time Tracking on Jetson Nano (~10 FPS)
![MOT17 Jetson GIF](output/mot_vid.gif)

---

## 🖼️ MOT20 Qualitative Results

| Frame 1 | Frame 2 |
|--------|--------|
| ![](output/1.jpeg) | ![](output/2.jpeg) |
| ![](output/3.jpeg) | ![](output/4.jpeg) |

---

## 📈 MOT17 & MOT20 Tracking Curves
![MOT17 Results](output/mot1.jpeg)  
![MOT20 Results](output/mot2.jpeg)

---

## 📊 Multi-Object Tracking Evaluation (Jetson Nano)

| Dataset | MOTA (%) | IDF1 (%) | HOTA (%) | MOTP (%) | MT | ML |
|-------|----------|----------|----------|----------|----|----|
| **MOT17** | 50.60 | 61.74 | 51.23 | 85.13 | 78 | 158 |
| **MOT20** | 55.22 | 48.95 | 41.11 | 84.79 | 443 | 377 |

---

## ⚖️ Performance Comparison

| Hardware | Detector | Tracker | FPS | Notes |
|--------|----------|---------|-----|------|
| **Laptop (RTX GPU)** | YOLOv8 | BYTETracker | ~30 | Best accuracy |
| **Jetson Nano** | YOLOv4 (pre-trained) | FastMOT | 4–5 | Low recall |
| **Jetson Nano** | YOLOv4-tiny (small dataset) | FastMOT | 12–15 | Unstable |
| **Jetson Nano** | **YOLOv4-tiny (COCO – 4,299 imgs)** | **FastMOT** | **12–15** | **Best accuracy–speed balance** |

---

## ⚠️ Limitations
- Recall remains lower than heavyweight detectors (YOLOv8).
- Performance degrades in extreme occlusions and dense crowds.
- Tracking stability strongly depends on detector confidence thresholds.
- High-accuracy pipeline requires powerful GPUs.

---

## 🏁 Conclusion
- **YOLOv8 + BYTETracker** delivers state-of-the-art tracking on high-end GPUs.
- **YOLOv4-tiny + FastMOT**, when properly trained, achieves **83% mAP** and real-time tracking on Jetson Nano.
- The project demonstrates the **accuracy–efficiency trade-off** critical for embedded AI systems.

---

## 🤖 Use of AI Tools
AI tools (e.g., ChatGPT) were used only for:
- Understanding code and workflows  
- Evaluation metric clarification  
- Jetson debugging  
- Documentation structuring  

All datasets, training, experiments, and results were produced independently.
