let playerNum = 0;
let answered = false;
let pollInterval = null;


function startGame(){
    document.getElementById('intro').style.display = 'none';
    document.getElementById('quiz').style.display = 'block';
    loadQuestion();
}

function startPolling(){
    pollInterval = setInterval(async () => {
        try{
            const res = await fetch('/api/buttons');
            const data = await res.json();
            console.log('button3 value:', data.button3);

            if (!answered){
                if(data.button1) submitAnswer('a');
                else if(data.button2) submitAnswer('b');
            }
            if(data.button3){
                const intro = document.getElementById('intro');
                const quiz = document.getElementById('quiz');
                const result = document.getElementById('result');

                if (intro.style.display == 'block'){
                    startGame();
                }
                else if(answered && quiz.style.display == 'block'){
                    nextQuestion();
                }
                else if(result.style.display == 'block'){
                    resetGame();
                }
            }
        }
        catch(e){

        }
        
    }, 100);
}

async function loadQuestion(){
    answered = false;
    document.getElementById('feedback').textContent = '';
    document.getElementById('explanation').textContent = '';
    document.getElementById('next-btn').style.display = 'none';

    ['btn-a', 'btn-b'].forEach(id => {
        const  btn = document.getElementById(id);
        btn.className = 'option-btn';
        btn.disabled = false;
    });

    const res = await fetch('/api/question');
    const data = await res.json();

    if(data.finished){
        showResult();
        return;
    }

    document.getElementById('progress').textContent = `Question ${data.index + 1} of ${data.total}`;
    document.getElementById('question-text').textContent = data.question;
    document.getElementById('text-a').textContent = data.a;
    document.getElementById('text-b').textContent = data.b;
}

async function submitAnswer(selected){
    if(answered) return;
    answered = true;

    const res = await fetch('/api/answer', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({player: playerNum, answer: selected})
    });
    const data = await res.json();

    const correctBtn = document.getElementById(`btn-${data.correct_ans}`);
    const selectedBtn = document.getElementById(`btn-${selected}`);

    console.log('correct answer:', data.correct_ans);
    console.log('looking for:', `btn-${data.correct_ans}`);  
    correctBtn.classList.add('correct');
    if(!data.correct) selectedBtn.classList.add('wrong');

    document.getElementById('btn-a').disabled = true;
    document.getElementById('btn-b').disabled = true;

    const feedback = document.getElementById('feedback');
    feedback.textContent = data.correct ? 'Correct!' : 'Wrong!';
    feedback.className = `feedback ${data.correct ? 'feedback-correct' : 'feedback-wrong'}`;

    document.getElementById('explanation').textContent = data.explanation;
    document.getElementById('next-btn').style.display = 'block';
}

async function nextQuestion(){
    await fetch('/api/next', {method: 'POST'});
    loadQuestion();
}

async function resetGame(){
    await fetch('/api/reset', {method: 'POST'});
    document.getElementById('result').style.display = 'none';
    document.getElementById('intro').style.display = 'block';
    answered = false;
}

async function showResult(){
    document.getElementById('quiz').style.display = 'none';
    document.getElementById('result').style.display = 'block';

    const res = await fetch('/api/scores');
    const data = await res.json();
    const total = data.scores.length > 0 ? data.scores[data.scores.length - 1][1] : 0;
    document.getElementById('final-score').textContent = `Your score: ${total}`;
}

startPolling();