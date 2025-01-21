# from flask import Flask, render_template, request, Response, redirect, url_for, session
# from flask_socketio import SocketIO
# from Blink import BlinkMorseCode
# import cv2
# import random

# app = Flask(__name__)
# socketio = SocketIO(app)
# app.secret_key = 'secretKey'

# # Initialize the BlinkMorseCode detector
# blink_morse_code = BlinkMorseCode(socketio)
# current_challenge = None

# current_challenge_indices = {}
# user_score = 0

# # Challenges for each level
# levels = {
#     "1": [{"text": "A", "morse": ".-"}, {"text": "B", "morse": "-..."}, {"text": "C", "morse": "-.-."}, {"text": "D", "morse": "-.."}],
#     "2": [{"text": "E", "morse": "."}, {"text": "F", "morse": "..-."}, {"text": "G", "morse": "--."}, {"text": "H", "morse": "...."}],
#     "3": [{"text": "I", "morse": ".."}, {"text": "J", "morse": ".---"}, {"text": "K", "morse": "-.-"}, {"text": "L", "morse": ".-.."}],
#     "4": [{"text": "M", "morse": "--"}, {"text": "N", "morse": "-."}, {"text": "O", "morse": "---"}, {"text": "P", "morse": ".--."}],
#     "5": [{"text": "Q", "morse": "--.-"}, {"text": "R", "morse": ".-."}, {"text": "S", "morse": "..."}, {"text": "T", "morse": "-"}],
#     "6": [{"text": "U", "morse": "..-"}, {"text": "V", "morse": "...-"}, {"text": "W", "morse": ".--"}, {"text": "X", "morse": "-..-"}],
# }

# @app.route('/')
# def menu():
#     return render_template('menu.html')

# @app.route('/home')
# def home():
#     return render_template('home.html')

# @app.route('/level')
# def level():
#     level_number = int(request.args.get('level', 1))
#     return render_template('index.html', level=level_number)

# @app.route('/score')
# def score():
#     print("[DEBUG] Entered score route.")
#     global user_score
#     return render_template('score.html', score=user_score)

# def generate_frames():
#     cap = cv2.VideoCapture(0)
#     if not cap.isOpened():
#         print("Error: Could not access the camera.")
#         return
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#         frame = cv2.flip(frame, 1)
#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         results = blink_morse_code.face_mesh.process(rgb_frame)
#         processed_frame = blink_morse_code.process_frame(frame, results, current_challenge)
#         _, buffer = cv2.imencode('.jpg', processed_frame)
#         frame_bytes = buffer.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
#     cap.release()

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# @socketio.on('start_challenge')
# def start_challenge(data):
#     print("[DEBUG] Received start_challenge event.")
#     global current_challenge, user_score
#     level = str(data.get('level', 1))
#     print(f"[DEBUG] Starting challenge for Level {level}.")
#     challenges = levels.get(str(level), [])
#     current_index = current_challenge_indices.get(str(level), 0)

#     if current_challenge_indices.get(level, 0) >= len(levels.get(level, [])):
#         print(f"[DEBUG] Restarting Level {level}.")
#         current_challenge_indices[level] = 0  # Reset challenge index
#         user_score = 0  # Reset the score

#     if current_index >= len(challenges):
#         print(f"[DEBUG] All challenges completed for Level {level}. Redirecting to score.")
#         socketio.emit('redirect_to_score')
#         return

#     current_challenge = challenges[current_index]
#     current_challenge_indices[str(level)] = current_index + 1
#     print(f"[DEBUG] Sending challenge: {current_challenge}.")
#     socketio.emit('new_challenge', current_challenge)
  
# if __name__ == "__main__":
#     print("[DEBUG] Starting Flask app...")
#     socketio.run(app, host="127.0.0.1", port=8000, debug=True)
from flask import Flask, render_template, request, Response, redirect, url_for, session
from flask_socketio import SocketIO
from Blink import BlinkMorseCode
import cv2
import random

# Initialize the Flask app
app = Flask(__name__)
# Enable WebSocket support using Flask-SocketIO
socketio = SocketIO(app)
# Set a secret key for session management
app.secret_key = 'BA8MUPCs6n5cfuhPGXFfy3QWLlFKwGmW'

# Create an instance of the BlinkMorseCode detector, which processes Morse code from blinking patterns
blink_morse_code = BlinkMorseCode(socketio)

# Global variables to store the current challenge and user score
current_challenge = None
current_challenge_indices = {}  # Tracks the progress of challenges for each level
user_score = 0

# Define Morse code challenges for each level
levels = {
    "1": [{"text": "A", "morse": ".-"}, {"text": "B", "morse": "-..."}, {"text": "C", "morse": "-.-."}, {"text": "D", "morse": "-.."}],
    "2": [{"text": "E", "morse": "."}, {"text": "F", "morse": "..-."}, {"text": "G", "morse": "--."}, {"text": "H", "morse": "...."}],
    "3": [{"text": "AC", "morse": ".- -.-."}, {"text": "BED", "morse": "-... . -.."}, {"text": "HA", "morse": ".... .-"}, {"text": "AE", "morse": ".- ."}, {"text": "AB", "morse": ".- -..."}, {"text": "ABCD", "morse": ".- -... -.-. -.."}, {"text": "EFGH", "morse": "..-.. --.. ...."}],
    "4": [{"text": "OK", "morse": "..."}, {"text": "NO", "morse": "-"}, {"text": "SOS", "morse": "... --- ..."}, {"text": "HI", "morse": ".... .-"}],
    "5": [{"text": "DOWN", "morse": "-.. --- .-- -."}, {"text": "YES", "morse": "-.-- . ..."}, {"text": "LEFT", "morse": ".-.. . ..-. -"}, {"text": "UP", "morse": "..- .--."}],
    "6": [{"text": "OK DOWN", "morse": "--- -.- -.. --- .-- -."}, {"text": "HI YES", "morse": "...-"}, {"text": "WLEFT UP", "morse": ".--"}, {"text": "SOS DOWN LEFT", "morse": "-..-"}, {"text": "HI YES UP", "morse": "..-"}, {"text": "OK DOWN LEFT", "morse": "...-"}],
}

# Route for the main menu
@app.route('/')
def menu():
    return render_template('menu.html')

# Route for the home page
@app.route('/home')
def home():
    return render_template('home.html')

# Route to display the level selection or game interface
@app.route('/level')
def level():
    level_number = int(request.args.get('level', 1))  # Default to level 1 if not provided
    return render_template('index.html', level=level_number)

# Route to display the user's score
@app.route('/score')
def score():
    print("[DEBUG] Entered score route.")
    global user_score
    return render_template('score.html', score=user_score)

# Generator function to process video frames and detect Morse code from blinking
def generate_frames():
    cap = cv2.VideoCapture(0)  # Open the webcam
    if not cap.isOpened():
        print("Error: Could not access the camera.")
        return

    while True:
        ret, frame = cap.read()  # Capture a frame from the webcam
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # Flip the frame horizontally for a mirrored effect
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert frame to RGB
        results = blink_morse_code.face_mesh.process(rgb_frame)  # Process the frame with BlinkMorseCode
        processed_frame = blink_morse_code.process_frame(frame, results, current_challenge)  # Annotate frame with Morse code feedback

        _, buffer = cv2.imencode('.jpg', processed_frame)  # Encode the frame as JPEG
        frame_bytes = buffer.tobytes()  # Convert to bytes for streaming

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()  # Release the webcam resource

# Route to provide video feed for the game
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Event handler for starting a new challenge via WebSocket
@socketio.on('start_challenge')
def start_challenge(data):
    print("[DEBUG] Received start_challenge event.")
    global current_challenge, user_score

    level = str(data.get('level', 1))  # Get the selected level from the event data
    print(f"[DEBUG] Starting challenge for Level {level}.")
    challenges = levels.get(level, [])  # Retrieve challenges for the specified level
    current_index = current_challenge_indices.get(level, 0)  # Get the current challenge index for the level

    # Reset level progress and score if all challenges are completed
    if current_challenge_indices.get(level, 0) >= len(challenges):
        print(f"[DEBUG] Restarting Level {level}.")
        current_challenge_indices[level] = 0  # Reset challenge index
        user_score = 0  # Reset the score

    if current_index >= len(challenges):
        print(f"[DEBUG] All challenges completed for Level {level}. Redirecting to score.")
        socketio.emit('redirect_to_score')  # Notify the client to redirect to the score page
        return

    current_challenge = challenges[current_index]  # Set the current challenge
    current_challenge_indices[level] = current_index + 1  # Increment the challenge index
    print(f"[DEBUG] Sending challenge: {current_challenge}.")
    socketio.emit('new_challenge', current_challenge)  # Send the new challenge to the client

# Main entry point of the application
if __name__ == "__main__":
    print("[DEBUG] Starting Flask app...")
    socketio.run(app, host="127.0.0.1", port=8000, debug=True)
