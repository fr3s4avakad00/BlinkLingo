// const socket = io();
// const morseDisplay = document.getElementById('morse-display');
// const startChallengeBtn = document.getElementById('start-challenge');
// const challengeText = document.getElementById('challenge-text');
// const challengeMorse = document.getElementById('challenge-morse');
// let currentScore = 0;

// // Start the first challenge for the level
// startChallengeBtn.addEventListener('click', () => {
//     const params = new URLSearchParams(window.location.search);
//     const level = parseInt(params.get('level'), 10);
//     socket.emit('start_challenge', { level });
// });

// // Update Morse code display
// socket.on('morse_update', (data) => {
//     morseDisplay.textContent = `Morse Code: ${data.morse_code}`;
// });

// // Handle new challenges
// socket.on('new_challenge', (data) => {
//     challengeText.textContent = `Word: ${data.text}`;
//     challengeMorse.textContent = `Morse: ${data.morse}`;
// });

// // Handle challenge result
// socket.on('challenge_result', (data) => {
//     const { correct, score, user_input, correct_answer } = data;

//     if (correct === 1) {
//         currentScore += score; // Increment score by 1 if correct
//     }

//     // Display feedback popup
//     if (correct === 1) {
//         alert(`Correct! Well done!`);
//     } else {
//         alert(`Incorrect!\nYour Input: ${user_input}\nCorrect Answer: ${correct_answer}`);
//     }

//     // Update the score display
//     document.getElementById('score').textContent = `Score: ${currentScore}`;

//     // Automatically start the next challenge
//     const level = new URLSearchParams(window.location.search).get('level');
//     socket.emit('start_challenge', { level });
// });

// socket.on('redirect_to_score', () => {
//     const params = new URLSearchParams(window.location.search);
//     const level = parseInt(params.get('level'), 10);

//     if (currentScore >= 3) {
//         const unlockedLevels = JSON.parse(localStorage.getItem('unlockedLevels')) || [1];
//         if (!unlockedLevels.includes(level + 1)) {
//             unlockedLevels.push(level + 1);
//             localStorage.setItem('unlockedLevels', JSON.stringify(unlockedLevels));
//         }
//     }

//     window.location.href = `/score?score=${currentScore}`;
// });


// function updateLevelStatus() {
//     fetch('/get_unlocked_levels')
//         .then(response => response.json())
//         .then(data => {
//             const unlockedLevels = data.unlockedLevels || [1];
//             for (let i = 1; i <= 6; i++) {
//                 const button = document.getElementById(`level-${i}`);
//                 if (unlockedLevels.includes(i)) {
//                     button.disabled = false;
//                     button.classList.remove('locked');
//                 } else {
//                     button.disabled = true;
//                     button.classList.add('locked');
//                 }
//             }
//         });
// }

// // Initialize level status on the home page
// if (document.getElementById('levels')) {
//     updateLevelStatus();
// }

const socket = io(); // Establish a WebSocket connection
const morseDisplay = document.getElementById('morse-display'); // Element to display Morse code
const startChallengeBtn = document.getElementById('start-challenge'); // Button to start a new challenge
const challengeText = document.getElementById('challenge-text'); // Element to display the challenge text
const challengeMorse = document.getElementById('challenge-morse'); // Element to display the challenge Morse code
let currentScore = 0; // Track the user's current score

// Event listener for starting the first challenge of the level
startChallengeBtn.addEventListener('click', () => {
    const params = new URLSearchParams(window.location.search); // Get URL parameters
    const level = parseInt(params.get('level'), 10); // Parse the current level from the URL
    socket.emit('start_challenge', { level }); // Emit event to start a challenge for the selected level
});

// Update the Morse code display in real-time
socket.on('morse_update', (data) => {
    morseDisplay.textContent = `Morse Code: ${data.morse_code}`; // Display the updated Morse code
});

// Receive and display new challenges
socket.on('new_challenge', (data) => {
    challengeText.textContent = `Word: ${data.text}`; // Show the challenge word
    challengeMorse.textContent = `Morse: ${data.morse}`; // Show the corresponding Morse code
});

// Handle the result of a completed challenge
socket.on('challenge_result', (data) => {
    const { correct, score, user_input, correct_answer } = data; // Destructure challenge result data

    if (correct === 1) {
        currentScore += score; // Increment score by 1 if the challenge was correct
    }

    // Provide user feedback via an alert
    if (correct === 1) {
        alert(`Correct! Well done!`); // Positive feedback for correct answers
    } else {
        alert(`Incorrect!\nYour Input: ${user_input}\nCorrect Answer: ${correct_answer}`); // Show correct answer and user input for incorrect responses
    }

    // Update the score display in the UI
    document.getElementById('score').textContent = `Score: ${currentScore}`;

    // Automatically start the next challenge
    const level = new URLSearchParams(window.location.search).get('level'); // Get the current level
    socket.emit('start_challenge', { level }); // Request the next challenge
});

socket.on('redirect_to_score', () => {
    try {
        const params = new URLSearchParams(window.location.search); // Parse URL parameters
        const level = parseInt(params.get('level'), 10); // Get the current level number
        if (isNaN(level)) throw new Error("Invalid level parameter");

        // Determine the score threshold based on the current level
        const SCORE_THRESHOLD = (level % 3 === 0) ? 5 : 3; // 5 for every third level, 3 otherwise

        // Unlock the next level if the score threshold is met
        if (currentScore >= SCORE_THRESHOLD) {
            const unlockedLevels = JSON.parse(localStorage.getItem('unlockedLevels')) || [1]; // Default to level 1 unlocked
            if (!unlockedLevels.includes(level + 1)) { // Check if the next level is not already unlocked
                unlockedLevels.push(level + 1); // Unlock the next level
                localStorage.setItem('unlockedLevels', JSON.stringify(unlockedLevels)); // Update local storage
            }
        }

        // Redirect to the score page with the current score as a query parameter
        window.location.href = `/score?score=${currentScore}`;
    } catch (error) {
        console.error("Error during level unlock or redirection:", error);
        // Optionally redirect to a fallback page or show an error message
    }
}); 

// Function to update the status of level buttons based on unlocked levels
function updateLevelStatus() {
    fetch('/get_unlocked_levels') // Fetch the unlocked levels from the server
        .then(response => response.json()) // Parse the JSON response
        .then(data => {
            const unlockedLevels = data.unlockedLevels || [1]; // Default to level 1 if no data
            for (let i = 1; i <= 6; i++) { // Loop through all levels
                const button = document.getElementById(`level-${i}`); // Get the button for each level
                if (unlockedLevels.includes(i)) {
                    button.disabled = false; // Enable the button if the level is unlocked
                    button.classList.remove('locked'); // Remove the locked styling
                } else {
                    button.disabled = true; // Disable the button if the level is locked
                    button.classList.add('locked'); // Add the locked styling
                }
            }
        });
}

// Initialize level status on the home page
if (document.getElementById('levels')) { // Check if the levels container exists on the page
    updateLevelStatus(); // Update the status of level buttons
}
