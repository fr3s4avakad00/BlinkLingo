# import cv2
# import mediapipe as mp
# import time


# class BlinkMorseCode:
#     def __init__(self, socketio, blink_threshold=0.03):
#         self.socketio = socketio
#         self.mp_face_mesh = mp.solutions.face_mesh
#         self.face_mesh = self.mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=False)
#         self.blink_threshold = blink_threshold
#         self.blink_start_time = 0
#         self.last_blink_end = time.time()
#         self.morse_code = ""
#         self.morse_code_map = {
#             ".-": "A", "-...": "B", "-.-.": "C", "-..": "D", ".": "E", "..-.": "F",
#             "--.": "G", "....": "H", "..": "I", ".---": "J", "-.-": "K", ".-..": "L",
#             "--": "M", "-.": "N", "---": "O", ".--.": "P", "--.-": "Q", ".-.": "R",
#             "...": "S", "-": "T", "..-": "U", "...-": "V", ".--": "W", "-..-": "X",
#             "-.--": "Y", "--..": "Z"
#         }

#     @staticmethod
#     def eye_aspect_ratio(landmarks, eye_indices):
#         top = landmarks[eye_indices[0]]
#         bottom = landmarks[eye_indices[1]]
#         return abs(top.y - bottom.y)

#     def process_frame(self, frame, results, current_challenge):
#         left_eye = [159, 145]
#         right_eye = [386, 374]
#         left_ear, right_ear = 0.0, 0.0

#         if results.multi_face_landmarks:
#             for face_landmarks in results.multi_face_landmarks:
#                 left_ear = self.eye_aspect_ratio(face_landmarks.landmark, left_eye)
#                 right_ear = self.eye_aspect_ratio(face_landmarks.landmark, right_eye)

#                 # Detect blinking
#                 if left_ear < self.blink_threshold and right_ear < self.blink_threshold:
#                     if self.blink_start_time == 0:
#                         self.blink_start_time = time.time()
#                 else:
#                     if self.blink_start_time > 0:
#                         # Calculate blink duration
#                         blink_duration = time.time() - self.blink_start_time
#                         self.blink_start_time = 0

#                         # Add to Morse code
#                         if blink_duration < 0.4:
#                             self.morse_code += "."
#                         elif blink_duration < 0.8:
#                             self.morse_code += "-"
#                         self.last_blink_end = time.time()
#                         self.socketio.emit('morse_update', {'morse_code': self.morse_code})

#                     # Stop processing input once the Morse code length matches the challenge length (including letter spaces)
#                     if current_challenge:
#                         challenge_morse = current_challenge['morse']
#                         expected_length = len(challenge_morse) + challenge_morse.count(' ')  # Add letter spaces

#                         if len(self.morse_code.strip()) >= expected_length:
#                             is_correct = self.morse_code.strip() == challenge_morse

#                             # Only increment score by 1 for a correct answer
#                             if is_correct:
#                                 self.socketio.emit('challenge_result', {
#                                     'correct': 1,
#                                     'score': 1,
#                                     'user_input': self.morse_code.strip(),
#                                     'correct_answer': challenge_morse
#                                 })
#                             else:
#                                 self.socketio.emit('challenge_result', {
#                                     'correct': 0,
#                                     'score': 0,  # No change in score for wrong answers
#                                     'user_input': self.morse_code.strip(),
#                                     'correct_answer': challenge_morse
#                                 })

#                             # Reset Morse code for the next challenge
#                             self.morse_code = ""
#                             return frame

#                     # Handle spaces for letters (include in length) and words (ignore in length)
#                     current_time = time.time()
#                     if current_time - self.last_blink_end > 1.1:  # Word space (2 seconds pause)
#                         if not self.morse_code.endswith("   "):  # Avoid duplicate spaces
#                             self.morse_code += "   "
#                             self.socketio.emit('morse_update', {'morse_code': self.morse_code})
#                     elif current_time - self.last_blink_end > 0.9:  # Letter space (1 second pause)
#                         if not self.morse_code.endswith(" "):  # Avoid duplicate spaces
#                             self.morse_code += " "
#                             self.socketio.emit('morse_update', {'morse_code': self.morse_code})

#         return frame

import cv2
import mediapipe as mp
import time

class BlinkMorseCode:
    def __init__(self, socketio, blink_threshold=0.03):
        """
        Initialize the BlinkMorseCode class with socketio for real-time communication 
        and a blink threshold for detecting blinks.

        Args:
            socketio: A SocketIO instance for emitting real-time events.
            blink_threshold (float): Threshold for detecting blinks based on eye aspect ratio.
        """
        self.socketio = socketio
        self.mp_face_mesh = mp.solutions.face_mesh  # Mediapipe FaceMesh utility
        self.face_mesh = self.mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=False)
        self.blink_threshold = blink_threshold  # Eye aspect ratio threshold for detecting a blink
        self.blink_start_time = 0  # Time when a blink starts
        self.last_blink_end = time.time()  # Time when the last blink ended
        self.morse_code = ""  # String to accumulate detected Morse code
        self.morse_code_map = {  # Map of Morse code to characters
            ".-": "A", "-...": "B", "-.-.": "C", "-..": "D", ".": "E", "..-.": "F",
            "--.": "G", "....": "H", "..": "I", ".---": "J", "-.-": "K", ".-..": "L",
            "--": "M", "-.": "N", "---": "O", ".--.": "P", "--.-": "Q", ".-.": "R",
            "...": "S", "-": "T", "..-": "U", "...-": "V", ".--": "W", "-..-": "X",
            "-.--": "Y", "--..": "Z"
        }

    @staticmethod
    def eye_aspect_ratio(landmarks, eye_indices):
        """
        Calculate the Eye Aspect Ratio (EAR) to determine if the eye is closed.

        Args:
            landmarks: Facial landmarks detected by Mediapipe.
            eye_indices (list): Indices for the top and bottom points of the eye.

        Returns:
            float: Absolute difference between the top and bottom landmark y-coordinates.
        """
        top = landmarks[eye_indices[0]]
        bottom = landmarks[eye_indices[1]]
        return abs(top.y - bottom.y)

    def process_frame(self, frame, results, current_challenge):
        """
        Process each video frame to detect blinking patterns and decode Morse code.

        Args:
            frame: Current video frame captured from the webcam.
            results: Mediapipe FaceMesh results for the current frame.
            current_challenge: The Morse code challenge (dictionary with 'text' and 'morse').

        Returns:
            frame: Processed video frame with annotations (if any).
        """
        # Indices of key landmarks for the eyes
        left_eye = [159, 145]
        right_eye = [386, 374]

        # Initialize eye aspect ratios
        left_ear, right_ear = 0.0, 0.0

        if results.multi_face_landmarks:  # Check if face landmarks are detected
            for face_landmarks in results.multi_face_landmarks:
                # Calculate EAR for both eyes
                left_ear = self.eye_aspect_ratio(face_landmarks.landmark, left_eye)
                right_ear = self.eye_aspect_ratio(face_landmarks.landmark, right_eye)

                # Detect blinking
                if left_ear < self.blink_threshold and right_ear < self.blink_threshold:
                    if self.blink_start_time == 0:  # Start timing the blink
                        self.blink_start_time = time.time()
                else:
                    if self.blink_start_time > 0:  # If a blink ended
                        # Calculate the duration of the blink
                        blink_duration = time.time() - self.blink_start_time
                        self.blink_start_time = 0  # Reset blink start time

                        # Classify the blink as a dot or dash based on duration
                        if blink_duration < 0.4:  # Short blink (dot)
                            self.morse_code += "."
                        elif blink_duration < 0.8:  # Long blink (dash)
                            self.morse_code += "-"
                        self.last_blink_end = time.time()  # Update the last blink end time

                        # Emit the updated Morse code to the client
                        self.socketio.emit('morse_update', {'morse_code': self.morse_code})

                    # Check if Morse code matches the current challenge
                    if current_challenge:
                        challenge_morse = current_challenge['morse']
                        expected_length = len(challenge_morse) + challenge_morse.count(' ')  # Account for spaces

                        if len(self.morse_code.strip()) >= expected_length:
                            is_correct = self.morse_code.strip() == challenge_morse

                            # Emit challenge result to the client
                            self.socketio.emit('challenge_result', {
                                'correct': int(is_correct),
                                'score': int(is_correct),  # Increment score only for correct answers
                                'user_input': self.morse_code.strip(),
                                'correct_answer': challenge_morse
                            })

                            # Reset Morse code for the next challenge
                            self.morse_code = ""
                            return frame

                    # Handle inter-character and inter-word spacing
                    current_time = time.time()
                    if current_time - self.last_blink_end > 1.1:  # Word space (2 seconds pause)
                        if not self.morse_code.endswith("   "):  # Avoid duplicate spaces
                            self.morse_code += "   "
                            self.socketio.emit('morse_update', {'morse_code': self.morse_code})
                    elif current_time - self.last_blink_end > 0.9:  # Letter space (1 second pause)
                        if not self.morse_code.endswith(" "):  # Avoid duplicate spaces
                            self.morse_code += " "
                            self.socketio.emit('morse_update', {'morse_code': self.morse_code})

        return frame  # Return the processed frame
