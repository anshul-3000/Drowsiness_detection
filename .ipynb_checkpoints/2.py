import cv2
import pygame
import threading
import time
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sys
import numpy as np

# Initialize pygame mixer for sound
pygame.mixer.init()

def play_alarm():
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load("D:/Drowiness/music.wav")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

def stop_alarm():
    if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
eyeCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')

if faceCascade.empty() or eyeCascade.empty():
    messagebox.showerror("Error", "Failed to load Haar cascades. Check file paths.")
    sys.exit()

start_time = None
blink_durations = []
DROWSINESS_THRESHOLD = 1.5
calibration_complete = False
alarm_active = False
monitoring_active = False

def load_logo():
    try:
        logo = Image.open("ddu.jpg").resize((175, 175))
        logo = ImageTk.PhotoImage(logo)
        logo_label.config(image=logo)
        logo_label.image = logo
    except Exception as e:
        messagebox.showerror("Error", f"Logo not found: {e}")

def calibrate():
    global start_time, calibration_complete, blink_durations, DROWSINESS_THRESHOLD
    cap = cv2.VideoCapture(0)
    calibration_start = time.time()
    calibration_duration = 15
    no_blinks_detected = True

    while True:
        ret, img = cap.read()
        if not ret:
            break
        
        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
        
        for (x, y, w, h) in faces:
            face_region = gray[y:y + h, x:x + w]
            eyes = eyeCascade.detectMultiScale(face_region, 1.1, 5, minSize=(10, 10))
            
            if len(eyes) == 0:
                if start_time is None:
                    start_time = time.time()
                no_blinks_detected = False
            else:
                if start_time is not None:
                    blink_durations.append(time.time() - start_time)
                    start_time = None

        elapsed_time = time.time() - calibration_start
        if elapsed_time > calibration_duration:
            break
    
    cap.release()
    if no_blinks_detected:
        messagebox.showwarning("No Blinks Detected", "Using default threshold.")
    else:
        avg_blink_duration = np.mean(blink_durations)
        DROWSINESS_THRESHOLD = avg_blink_duration * 2
        messagebox.showinfo("Calibration Complete", f"Avg Blink Duration: {avg_blink_duration:.2f} sec")
    calibration_complete = True

def monitor():
    global start_time, alarm_active, monitoring_active
    if not calibration_complete:
        messagebox.showerror("Error", "Calibration not completed yet!")
        return
    monitoring_active = True
    cap = cv2.VideoCapture(0)

    while monitoring_active:
        ret, img = cap.read()
        if not ret:
            break
        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
        
        for (x, y, w, h) in faces:
            face_region = gray[y:y + h, x:x + w]
            eyes = eyeCascade.detectMultiScale(face_region, 1.1, 5, minSize=(10, 10))
            
            if len(eyes) == 0:
                if start_time is None:
                    start_time = time.time()
                else:
                    elapsed_time = time.time() - start_time
                    if elapsed_time > DROWSINESS_THRESHOLD and not alarm_active:
                        alarm_active = True
                        threading.Thread(target=play_alarm).start()
            else:
                start_time = None
                if alarm_active:
                    stop_alarm()
                    alarm_active = False
    
        cv2.imshow('Drowsiness Monitoring', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    stop_alarm()
    monitoring_active = False

def exit_app():
    global monitoring_active
    monitoring_active = False
    stop_alarm()
    window.quit()
    window.destroy()
    sys.exit()

def create_interface():
    global window, logo_label
    window = tk.Tk()
    window.title("Drowsiness Detection System")
    window.geometry("800x600")
    window.config(bg="#f4f4f9")
    
    logo_label = tk.Label(window, bg="#f4f4f9")
    logo_label.pack(pady=10)
    load_logo()
    
    tk.Button(window, text="Start Calibration", font=("Arial", 16), bg="#4caf50", fg="white", command=calibrate).pack(pady=10)
    tk.Button(window, text="Start Monitoring", font=("Arial", 16), bg="#2196f3", fg="white", command=monitor).pack(pady=10)
    tk.Button(window, text="Exit", font=("Arial", 16), bg="#f44336", fg="white", command=exit_app).pack(pady=10)
    
    window.mainloop()

create_interface()
