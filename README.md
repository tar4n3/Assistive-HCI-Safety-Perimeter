# AuraVision: Assistive Spatial Audio Prototype

## Concept
AuraVision is an experimental interaction design project that explores how computer vision can be used to create a "Safety Perimeter" for visually impaired individuals. Instead of overwhelming the user with continuous speech, it uses **dynamic sonification**—mapping the distance of an object to audio pitch and frequency.

## Key Features
- **Multithreaded Feedback:** Uses parallel processing to provide non-blocking audio alerts (voice + beeps) without lagging the camera feed.
- **Dynamic Sonification:** Translates object proximity into pitch ($Hz$), providing an intuitive sense of "distance" without verbal instructions.
- **State-Aware Logic:** Avoids "audio spam" by only announcing labels when an object first enters the safety zone or changes its relative position significantly.

## Technical Implementation
- **Core Engine:** YOLOv8 (Nano) for high-frequency object detection.
- **Interface:** Windows SAPI (Speech API) for low-latency voice feedback.
- **Spatial Logic:** Normalized bounding box area ($A$) used as a proxy for physical proximity.

- ## How to Run:
1. Clone the repository:
git clone https://github.com/tar4n3/Assistive-HCI-Safety-Perimeter.git
cd Assistive-HCI-Safety-Perimeter

2. Install dependencies:
pip install -r requirements.txt

3. Run the detector:
python detect.py
   The YOLOv8 model weights will download automatically on first run.

**Note**: This project uses Windows SAPI for voice feedback, so it currently runs on Windows only.

requirements.txt:
ultralytics
opencv-python
pywin32
