import tkinter as tk
import cv2
import numpy as np
import mediapipe as mp


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


    # Function to calculate the angle between three points by finding the difference between bc and ab
def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return round(angle)



    # Function to determine if the form is correct based on the selected exercise 
def is_form_correct(selected_exercise, left_elbow_angle, right_elbow_angle, left_shoulder_angle, right_shoulder_angle):
    if selected_exercise == "Bicep Curl":
        return (0 <= left_shoulder_angle <= 20) and (right_shoulder_angle <= 20)
    elif selected_exercise == "Skull Crusher":
        return (left_elbow_angle >= 20) and (left_shoulder_angle >= 120) and (right_elbow_angle >= 20) and (right_shoulder_angle >= 120)
    elif selected_exercise == "Overhead Press":
        return left_elbow_angle >= 45 and right_elbow_angle >= 45
    elif selected_exercise == "Lateral Raise":
        return left_shoulder_angle <= 90 and right_shoulder_angle <= 90
    elif selected_exercise == "Chest Press":
        return 75 >= left_shoulder_angle >= 20 and 75 >= right_shoulder_angle >= 20
    elif selected_exercise == "Pull-up":
        return left_elbow_angle <= 180 and right_elbow_angle <= 180
    elif selected_exercise == "Push-up":
        return left_shoulder_angle <= 10 and right_shoulder_angle <= 10
    elif selected_exercise == "Dips":
        return 45 >= left_shoulder_angle >= 30 and 45 >= right_shoulder_angle >= 30
    return False

def start_camera(selected_exercise, window_name):

    left_counter = 0
    left_stage = None
    right_counter = 0
    right_stage = None
    show_lines = True



    cap = cv2.VideoCapture(0)
    
    
    left_elbow_angle = right_elbow_angle = left_shoulder_angle = right_shoulder_angle = left_wrist_angle = right_wrist_angle = 0
        

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


            try:
                landmarks = results.pose_landmarks.landmark

                # Extracting the x and y coordinates of body landmarks to find the angle
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]



                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                # Calculating the elbow angles
                left_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                right_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
                # Calculatig the shoulder angles
                left_shoulder_angle = calculate_angle(left_hip,left_shoulder, left_elbow)
                right_shoulder_angle = calculate_angle(right_hip, right_shoulder, right_elbow)

                if is_form_correct(selected_exercise, left_elbow_angle, right_elbow_angle, left_shoulder_angle, right_shoulder_angle):
                    color = (0, 255, 0)  # Correct form
                else:
                    color = (0, 0, 255)  # Incorrect form


                if results.pose_landmarks and show_lines:  # Only draw lines if show_lines is True
                    mp_drawing.draw_landmarks(
                        image, 
                        results.pose_landmarks, 
                        mp_pose.POSE_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=color, thickness=2, circle_radius=4),  # Joint circles
                        mp_drawing.DrawingSpec(color=color, thickness=2, circle_radius=2)   # Joint connections
                    )




                # counter logic for the exercises
                if selected_exercise == "Bicep Curl":
                    if left_elbow_angle > 160:
                        left_stage = "down"
                    if left_elbow_angle < 30 and left_stage == 'down':
                        left_stage = "up"
                        left_counter += 1
                        print(left_counter)


                    if right_elbow_angle > 160:
                        right_stage = "down"
                    if right_elbow_angle < 30 and right_stage == 'down':
                        right_stage = "up"
                        right_counter += 1
                        print(right_counter)

                if selected_exercise == "Skull Crusher":
                    if left_elbow_angle <= 70:
                        left_stage = "down"
                    if left_elbow_angle >= 160 and left_stage == 'down':
                        left_stage = "up"
                        left_counter += 1
                        print(left_counter)

                    if right_elbow_angle <= 70:
                        right_stage = "down"
                    if right_elbow_angle >= 160 and right_stage == 'down':
                        right_stage = "up"
                        right_counter += 1
                        print(right_counter)
                    
                if selected_exercise == "Overhead Press":
                    if left_elbow_angle <= 70:
                        left_stage = "down"
                    if left_elbow_angle >= 160 and left_stage == 'down':
                        left_stage = "up"
                        left_counter += 1
                        print(left_counter)

                    if right_elbow_angle <= 70:
                        right_stage = "down"
                    if right_elbow_angle >= 160 and right_stage == 'down':
                        right_stage = "up"
                        right_counter += 1
                        print(right_counter)

                if selected_exercise == "Lateral Raise":
                    if left_shoulder_angle <= 50:
                        left_stage = "down"
                    if left_shoulder_angle >= 50 and left_stage == 'down':
                        left_stage = "up"
                        left_counter += 1
                        print(left_counter)

                    if right_shoulder_angle <= 50:
                        right_stage = "down"
                    if right_shoulder_angle >= 50 and right_stage == 'down':
                        right_stage = "up"
                        right_counter += 1
                        print(right_counter)


                if selected_exercise == "Chest Press":
                    if left_elbow_angle > 140 and right_elbow_angle > 140:
                        left_stage = "up"
                        right_stage = "up"

                    if (left_elbow_angle < 90 and left_stage == 'up') or (right_elbow_angle < 90 and right_stage == 'up'):
                        left_stage = "down"
                        right_stage = "down"
                        
                        left_counter += 1
                        right_counter += 1
                        
                        print(left_counter)
                        print(right_counter)

                if selected_exercise == "Pull-up":
                    if left_elbow_angle <= 70 or right_elbow_angle <= 70:
                        left_stage = "up"
                        right_stage = "up"

                    if (left_elbow_angle >= 160 and left_stage == 'up') and (right_elbow_angle >= 160 and right_stage == 'up'):
                        left_stage = "down"
                        right_stage = "down"
                        
                        left_counter += 1
                        right_counter += 1
                        
                        print(left_counter)
                        print(right_counter)


                if selected_exercise == "Push-up":
                    if left_elbow_angle > 140 and right_elbow_angle > 140:
                        left_stage = "up"
                        right_stage = "up"

                    if (left_elbow_angle < 90 and left_stage == 'up') or (right_elbow_angle < 90 and right_stage == 'up'):
                        left_stage = "down"
                        right_stage = "down"
                        
                        left_counter += 1
                        right_counter += 1
                        
                        print(left_counter)
                        print(right_counter)


                if selected_exercise == "Dips":
                    if left_shoulder_angle <= 20 or right_shoulder_angle <= 20:
                        left_stage = "up"
                        right_stage = "up"

                    if (left_shoulder_angle >= 30 and left_stage == 'up') and (right_shoulder_angle >= 30 and right_stage == 'up'):
                        left_stage = "down"
                        right_stage = "down"
                        
                        left_counter += 1
                        right_counter += 1
                        
                        print(left_counter)
                        print(right_counter)


            except Exception as e:
                print(f"An error occurred: {e}")

            cv2.rectangle(image, (0, 0), (700, 100), (245, 117, 16), -1)
            cv2.rectangle(image, (1230, 0), (1920, 100), (245, 117, 16), -1)
            cv2.rectangle(image, (640, 0), (1340, 100), (245, 117, 16), -1)
            cv2.rectangle(image, (0, 950), (400, 1100), (245, 117, 16), -1)
            cv2.rectangle(image, (1530, 950), (1920, 1100), (245, 117, 16), -1)

            # Angle data
            cv2.putText(image, "Left Elbow Angle: " + str(left_elbow_angle), (0, 1000), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(image, "Left Shoulder Angle: " + str(left_shoulder_angle), (0, 1050), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(image, "Right Elbow Angle: " + str(right_elbow_angle), (1530, 1000), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(image, "Right Shoulder Angle: " + str(right_shoulder_angle), (1530, 1050), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)

            # Exercise data
            cv2.putText(image, f"Exercise: {selected_exercise}", (625, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

            # Rep data
            cv2.putText(image, 'REPS', (15, 25), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, str(right_counter), 
                        (10, 80), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

            cv2.putText(image, 'REPS', (1775, 25), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, str(left_counter), 
                        (1810, 80), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

            # Stage data
            cv2.putText(image, 'STAGE', (165, 25), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, right_stage if right_stage else "N/A", 
                        (160, 80), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

            cv2.putText(image, 'STAGE', (1625, 25), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, left_stage if left_stage else "N/A", 
                        (1560, 80), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

            cv2.imshow(window_name, image)


            cv2.imshow('RILA V2', image)

            key = cv2.waitKey(10)
            
            # Make feedback lines disappear/reappear
            if key == ord('t'):
                show_lines = not show_lines
            # Reset counter
            if key == ord('r'):
                left_counter = 0
                right_counter = 0
            # Exit exercise screen
            if key == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

def open_rep_detector(selected_exercise):
    window_name = 'RILA V2'
    cv2.namedWindow(window_name)
    start_camera(selected_exercise, window_name)

def exercise_selection_screen():
    root = tk.Tk()
    root.title("Exercise Library")

    # It's possible to add additional exercises
    freeweights = ["Bicep Curl", "Skull Crusher", "Overhead Press", "Lateral Raise", "Chest Press"]
    calisthenics = ["Pull-up", "Push-up", "Dips"]
     

    calisthenics_frame = tk.Frame(root)
    calisthenics_frame.pack(pady=10, padx=10)

    freeweights_frame = tk.Frame(root)
    freeweights_frame.pack(pady=10, padx=10)

    tk.Label(calisthenics_frame, text="Calisthenics", font=('Helvetica', 16, 'bold')).grid(row=0, column=0, columnspan=2, pady=5)
    tk.Label(freeweights_frame, text="Free Weights", font=('Helvetica', 16, 'bold')).grid(row=0, column=0, columnspan=2, pady=5)

    for i, cal in enumerate(calisthenics):
        button = tk.Button(calisthenics_frame, text=cal, command=lambda e=cal: open_rep_detector(e))
        button.grid(row=i+1, column=0, padx=10, pady=5)  # Start from row 1 to leave space for the label

    
    for i, fr in enumerate(freeweights):
        button = tk.Button(freeweights_frame, text=fr, command=lambda e=fr: open_rep_detector(e))
        button.grid(row=i+1, column=0, padx=10, pady=5)  # Start from row 1 to leave space for the label

    root.mainloop()

if __name__ == "__main__":
    exercise_selection_screen()
