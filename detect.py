from ultralytics import YOLO
import time
import threading
import win32com.client
import winsound


def speak(message):
    def _say():
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Rate = 2
        speaker.Speak(message)
    threading.Thread(target=_say, daemon=True).start()

def stop_speech():
    pass


def beep(pitch):
    threading.Thread(target=winsound.Beep, args=(pitch, 100), daemon=True).start()


model = YOLO('yolov8n.pt')

CLOSE_THRESHOLD = 0.15
BEEP_COOLDOWN   = 0.3

last_beeped      = {}
announced_labels = set()
close_labels     = set()

print("--- SAFETY PERIMETER ACTIVE ---")
results = model.predict(source='0', show=True, stream=True)

for r in results:
    current_time = time.time()

    close_objects = []

    for box in r.boxes:
        if float(box.conf) < 0.4:
            continue

        x1, y1, x2, y2 = box.xyxyn[0]
        area = float((x2 - x1) * (y2 - y1))

        if area < CLOSE_THRESHOLD:
            continue

        label    = model.names[int(box.cls)]
        x_center = float((x1 + x2) / 2)
        pitch    = max(37, min(int(500 + area * 2000), 32767))

        close_objects.append((x_center, label, area, pitch))

    close_objects.sort(key=lambda obj: obj[0])
    current_close_labels = {obj[1] for obj in close_objects}

    
    left_labels = close_labels - current_close_labels
    if left_labels:
        for label in left_labels:
            print(f"[{label}] left perimeter — reset")
        announced_labels -= left_labels

    close_labels = current_close_labels

    for x_center, label, area, pitch in close_objects:

        
        if current_time - last_beeped.get(label, 0) > BEEP_COOLDOWN:
            beep(pitch)
            last_beeped[label] = current_time

        # Announce once per visit / block repeat 
        if label in announced_labels:
            continue

        if x_center < 0.35:
            pos = "on your left"
        elif x_center > 0.65:
            pos = "on your right"
        else:
            pos = "straight ahead"

        if area > 0.4:
            zone = "very close"
        elif area > 0.25:
            zone = "close"
        else:
            zone = "nearby"

        message = f"{label} {zone}, {pos}"
        print(f"Assistant: {message}")
        speak(message)
        announced_labels.add(label)