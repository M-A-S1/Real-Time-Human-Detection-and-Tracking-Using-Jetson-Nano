Human detection and tracking are essential components in modern computer vision systems, powering applications such as intelligent surveillance, crowd monitoring, and autonomous navigation.

In this project, we first implement a state-of-the-art human tracking pipeline on a laptop, using:

YOLOv8 for high-accuracy human detection

BYTETracker for reliable multi-object tracking

This gives us strong baseline results and allows us to analyze performance on a powerful machine. The output videos (e.g., out.mp4) show smooth and accurate tracking using these SOTA models.

In the next stage of the project, we will deploy the system on a Jetson Nano, where we will use FastMOT, an optimized tracking framework designed specifically for edge devices with limited compute. This will allow us to compare:

SOTA results on a laptop (YOLOv8 + BYTETracker)

Real-time performance on Jetson Nano (FastMOT)

The goal is to evaluate both accuracy and efficiency across different hardware platforms.
