let currentQuestion = 0;
let score = 0;
let time = 15;
let timer;
let carPosition = 10;

const car = document.getElementById("car");
const question = document.getElementById("question");
const optionButtons = document.querySelectorAll(".option-btn");
const progressBar = document.getElementById("progressBar");
const timeSpan = document.getElementById("time");

function startTimer() {

    clearInterval(timer);

    time = 15;
    timeSpan.innerHTML = time;

    timer = setInterval(() => {

        time--;

        timeSpan.innerHTML = time;

        if (time <= 0) {

            clearInterval(timer);

            nextQuestion();

        }

    }, 1000);

}

function loadQuestion() {

    let q = questions[currentQuestion];

    question.innerHTML = q.question;

    optionButtons[0].innerHTML = q.option1;
    optionButtons[1].innerHTML = q.option2;
    optionButtons[2].innerHTML = q.option3;
    optionButtons[3].innerHTML = q.option4;

    progressBar.style.width = ((currentQuestion + 1) / questions.length) * 100 + "%";

    progressBar.innerHTML =
        "Question " +
        (currentQuestion + 1) +
        " / " +
        questions.length;

    startTimer();

}

optionButtons.forEach(btn => {

    btn.addEventListener("click", function () {

        clearInterval(timer);

        let answer = this.innerHTML.trim();

        if (answer === questions[currentQuestion].correct_answer) {

            score++;

            carPosition += 80;

            car.style.left = carPosition + "px";

        }

        nextQuestion();

    });

});

function nextQuestion() {

    currentQuestion++;

    if (currentQuestion >= questions.length) {

        clearInterval(timer);

        alert(
            "🏆 Race Finished\n\nScore : " +
            score +
            " / " +
            questions.length
        );

        location.reload();

        return;

    }

    loadQuestion();

}

loadQuestion();

fetch("/save_race_score",{

    method:"POST",

    headers:{
        "Content-Type":"application/json"
    },

    body:JSON.stringify({

        score:score

    })

})
.then(r=>r.json())
.then(data=>{

    alert("🏆 Score Saved Successfully!");

});