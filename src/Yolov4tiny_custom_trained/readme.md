# YOLOv4-tiny Person Detection on Jetson Nano

This repository contains the implementation of **YOLOv4-tiny** trained on a custom **person detection dataset** from [Roboflow](https://universe.roboflow.com/cvproject-hd43l/people-mpod5-i1urw). The model is optimized for deployment on **NVIDIA Jetson Nano**, following the tutorial by [Code with Arohi](https://www.youtube.com/watch?v=XaYRY4EM6is&t=1s).

---

## 📌 Overview
- **Model**: YOLOv4-tiny (lightweight version of YOLOv4)
- **Dataset**: Custom "people" dataset from Roboflow
- **Target Device**: NVIDIA Jetson Nano
- **Use Case**: Real-time person detection

---

## 📂 Dataset
The dataset used for training is the **[People Dataset](https://universe.roboflow.com/cvproject-hd43l/people-mpod5-i1urw)** by CVProject, hosted on Roboflow Universe. It contains annotated images for a single class: **person**.

### Citation
```bibtex
@misc{
    people-mpod5-i1urw_dataset,
    title = { people Dataset },
    type = { Open Source Dataset },
    author = { CVProject },
    howpublished = { \url{ https://universe.roboflow.com/cvproject-hd43l/people-mpod5-i1urw } },
    url = { https://universe.roboflow.com/cvproject-hd43l/people-mpod5-i1urw },
    journal = { Roboflow Universe },
    publisher = { Roboflow },
    year = { 2025 },
    month = { dec },
    note = { visited on 2025-12-06 },
}

