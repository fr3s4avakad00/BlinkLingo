### README.md

# BlinkLingo - The Morse Code Game

BlinkLingo is an interactive web-based game designed to teach and test your Morse code skills through engaging challenges. Using your webcam, BlinkLingo tracks your eye blinks to input Morse code. Progress through multiple levels, unlock challenges, and master Morse code in a fun and gamified way.

---

## Features
- **Webcam-Based Input**: Detect eye blinks to input dots (`.`) and dashes (`-`) for Morse code.
- **Progressive Levels**: Unlock new levels by completing challenges and scoring points.
- **Real-Time Feedback**: View live updates of your Morse code as you blink.
- **Responsive Design**: Play the game seamlessly across various devices.
- **Local Progress Tracking**: Track your progress and unlocked levels locally.

---

## How It Works
1. Navigate through the menu and select a level to start.
2. Blink your eyes to input Morse code:
   - Short blinks (`< 0.4 seconds`) are interpreted as dots (`.`).
   - Longer blinks (`0.4 - 0.8 seconds`) are interpreted as dashes (`-`).
3. Match the displayed Morse code challenge to score points.
4. Complete challenges to unlock higher levels.

---

## Project Structure
```
.
├── app.py              # Flask application backend
├── Blink.py            # Eye blink detection and Morse code processing
├── templates/          # HTML files for the game interface
│   ├── home.html       # Home page with level selection
│   ├── index.html      # Level page with challenges
│   ├── menu.html       # Main menu page
│   ├── score.html      # Level completion page
├── static/             # Static files (CSS, JS, images)
│   ├── css/
│   │   └── style.css   # Styling for the game
│   ├── js/
│   │   └── script.js   # Frontend logic and real-time communication
├── README.md           # Project documentation
├── requirements.txt    # List of Python dependencies
```

---

## Prerequisites
1. **Python 3.8+** installed on your system.
2. Webcam for blink detection.

---

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/BlinkLingo.git
   cd BlinkLingo
   ```

2. **Install Dependencies**
   Use the provided `requirements.txt` file to install the necessary Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Server**
   Run the Flask application:
   ```bash
   python app.py
   ```

4. **Access the Application**
   Open your browser and navigate to:
   ```
   http://127.0.0.1:8000
   ```

---

## Usage

### Navigating the Game
1. **Start the Game**: Open the game in your browser and click on "Let's GO!!!" to begin.
2. **Select a Level**: Choose a level from the home page. Unlocked levels will be clickable.
3. **Play the Challenge**: Match the Morse code displayed on the screen by blinking.
4. **Complete Levels**: Accumulate points to unlock higher levels.

---

## Technical Details

### Backend
- Built with **Flask**.
- Handles real-time communication using **Socket.IO**.
- Blink detection implemented with **Mediapipe**.

### Frontend
- Interactive UI created with HTML, CSS, and JavaScript.
- Real-time feedback and level management powered by **Socket.IO**.

---

## Key Components

1. **Blink.py**:
   - Detects blinks and translates them into Morse code.
   - Handles timing thresholds to differentiate between dots and dashes.

2. **script.js**:
   - Handles real-time communication with the backend.
   - Updates the UI with the current Morse code and challenge progress.

3. **style.css**:
   - Provides a clean and responsive design for the game.

---

## Future Enhancements
- Add support for multiplayer mode.
- Include more levels and challenges.
- Integrate audio feedback for Morse code.

---

## License
This project is licensed under the [MIT License](LICENSE).

---

## Contributing
Feel free to contribute to BlinkLingo! Fork the repository and submit a pull request with your improvements.

---

Enjoy the journey of mastering Morse code with BlinkLingo! 🚀