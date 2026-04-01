from flask import Flask, jsonify, render_template, request
import serial_handler

app = Flask(__name__)

game_state = {
    "current_question": 0,
    "scores": {},
}

questions = [
    {
        "question": "Question 1",
        "options": "options",
        "answer": "answers",
    },
    {
        "question": "Question 2",
        "options": "options",
        "answer": "answers",
    },
    {
        "question": "Question 3",
        "options": "options",
        "answer": "answers",
    },
    {
        "question": "Question 4",   
        "options": "options",
        "answer": "answers",
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_buttons')
def check_buttons():
    pressed1 = serial_handler.button1_pressed

    if pressed1:
        serial_handler.button1_pressed = False
        serial_handler.send_led1_status("red")
    
    return jsonify({'pressed1': pressed1})


if __name__ == '__main__':
    app.run(debug=True, port=5000)