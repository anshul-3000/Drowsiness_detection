# Drowsiness Detection System

A real-time drowsiness detection app using OpenCV, Haar cascades, Tkinter GUI and pygame for alarm sound. This repository contains a simple, ready-to-run Python application that detects closed eyes/blinks and triggers an alarm when prolonged eye closure (drowsiness) is detected.

---

## Features

* Face and eye detection using Haar cascades (OpenCV)
* Calibration phase to measure user's average blink duration
* Real-time monitoring with visual feedback (green/red bounding box)
* Alarm sound using `pygame` when drowsiness is detected
* Simple Tkinter-based GUI for starting calibration, monitoring, and exiting

---

## Contents

* `app.py` — Main application (Tkinter GUI + OpenCV monitoring)
* `haarcascade_frontalface_alt.xml` — Haar cascade for face detection
* `haarcascade_eye_tree_eyeglasses.xml` — Haar cascade for eye detection
* `mmmut.png` — logo image used in the GUI
* `music.wav` — alarm sound (place your alarm tone here)
* `README.md` — (this file)

---

## Requirements

* Python 3.8+ recommended
* A webcam

Install dependencies (recommended to use a virtual environment):

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install --upgrade pip
pip install opencv-python pygame pillow
```

If you prefer a `requirements.txt`, create it with:

```
opencv-python
pygame
pillow
```

and install with:

```bash
pip install -r requirements.txt
```

---

## How to run

1. Make sure the following files are present in the project folder (same directory as `app.py`):

   * Haar cascade XML files
   * `mmmut.png` (or edit the path in `app.py`)
   * `music.wav` (or update the path in `app.py`)

2. Start the app:

```bash
python app.py
```

3. Use the GUI:

* Click **Start Calibration** and follow on-screen instructions to let the app measure your blink timings.
* Click **Start Monitoring** to begin real-time drowsiness detection.
* Click **Exit** to stop the app and close the window.

---

## Notes & Tips

* Calibration: If no blinks are detected during the default calibration duration, the code reduces the calibration time and uses a fallback threshold. Re-run calibration in a well-lit environment and face the camera.
* Alarm volume: Adjust `pygame.mixer.music.set_volume()` in `app.py` to set a comfortable alarm level.
* If face/eye detection is unreliable, try moving to better lighting, or tune the `detectMultiScale` parameters in `app.py`.

---

## Adding this README to your repo

If you haven't yet committed this file, run:

```bash
git add README.md
git commit -m "Add README"
git push
```

---

## License

This project is released under the MIT License. Add a `LICENSE` file if you want to make it explicit.

---

## Contact

If you want improvements (requirements.txt, GitHub Actions workflow, nicer README with badges and screenshots, or a cleaned code refactor), tell me and I will generate them for you.
