const form = document.querySelector("form[name='word-submit']");
const wordInput = document.querySelector(".word_input");
const wordsList = document.querySelector(".words");
const scoreClass = document.querySelector(".score");
const timer = document.querySelector(".timer");
let score = 0;
let allowGuesses = true;
scoreClass.textContent = 'Score: 0';
timer.textContent = '60'; 

function updateTimer() {
    let currentTime = Number(timer.textContent) - 1;
    timer.textContent = currentTime; 

    if (currentTime <= 0) {
        clearInterval(timerInterval);
        timer.textContent = '0'; 
        allowGuesses = false;
        gameEnded(score); 
        score = 0;
        scoreClass.innerText = 'Score: ' + score; 
    }
}

let timerInterval;

function gameEnded(finalScore) {
    axios.post('/post-score', { score: finalScore })
        .then(function (response) {
            const brokeRecord = response.data.brokeRecord;
            
            if (brokeRecord) {
                alert("New high score!");
            }
            getGameStats();
        })
        .catch(function (error) {
            console.error("Error posting score", error);
        });
}

function getGameStats() {
    axios.get('/get-stats')
        .then(function (response) {
            document.getElementById('numPlays').textContent = response.data.num_plays;
            document.getElementById('highScore').textContent = response.data.highscore;
        })
        .catch(function (error) {
            console.error("Error fetching game stats", error);
        });
}

document.addEventListener("DOMContentLoaded", function() {
    getGameStats(); 
    timerInterval = setInterval(updateTimer, 1000); 
    form.addEventListener("submit", async function(event) {
        event.preventDefault();

        if (!allowGuesses) return; 

        const word = wordInput.value.trim(); 

        try {
            const response = await axios.get(`/checkword?word=${word}`);
            const result = response.data.result;
            if (result === 'ok') {
                score += word.length;
                scoreClass.innerText = `Score: ${score}`;
            }

            let li = document.createElement("li");
            li.textContent = `${word}: ${result}`;
            wordsList.appendChild(li);
            wordInput.value = "";
        } catch (error) {
            console.error("Error checking word", error);
            alert("There was an error checking the word. Please try again.");
        }
    });
});