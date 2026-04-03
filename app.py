from flask import Flask, jsonify, render_template, request
import serial_handler

app = Flask(__name__)

game_state = {
    "current_question": 0,
    "scores": {},
}

player_count = 0

questions = [
    {
        "id": 1,
        "question": "You just woke up and your room feels chilly. What do you do?",
        "a": "Turn up the thermostat",
        "b": "Put on a sweater",
        "answer": "b",
        "explanation": "ex"
    },
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/question')
def get_question():
    qId = game_state["current_question"]
    if qId >= len(questions):
        return jsonify({"finished": True})
    
    q = questions[qId].copy()
    q.pop("answer")
    q.pop("explanation")
    q["index"] = qId
    q["total"] = len(questions)
    return jsonify(q)

@app.route('/api/answer', methods=['POST'])
def submit_answer():
    global player_count

    data = request.get_json()
    player = data.get("player")
    if player not in game_state["scores"]:
        player_count += 1
        player = f"Player {player_count}"
        game_state["scores"][player] = 0
    selected = data.get("answer")
    qId = game_state["current_question"]

    if qId >= len(questions):
        return({"error": "No active questions"}), 400
    
    correct_ans = questions[qId]["answer"]
    explanation = questions[qId]["explanation"]

    is_correct = selected == correct_ans

    if is_correct:
        game_state["scores"][player] = game_state["scores"].get(player, 0) + 1
        serial_handler.send_led1_status("green")
    else:
        serial_handler.send_led1_status("red")

    return jsonify({
        "correct": is_correct,
        "correct_ans": correct_ans,
        "explanation": explanation,
        "scores": game_state["scores"]
    })

@app.route('/api/next', methods=['POST'])
def next_question():
    game_state["current_question"] += 1
    return jsonify({"current question": game_state["current_question"]})

@app.route('/api/reset', methods=['POST'])
def reset_game():
    game_state["current_question"] = 0
    game_state["scores"] = {}
    #set leds off
    return jsonify({"status": "reset"})

@app.route('/api/scores')
def get_scores():
    sorted_scores = sorted(
        game_state["scores"].items(),
        key=lambda x: x[1],
        reverse=True,
    )
    return jsonify({"scores": sorted_scores})

@app.route('/api/buttons')
def check_buttons():
    print(f"button1: {serial_handler.button1_pressed}, button2: {serial_handler.button2_pressed}, button3: {serial_handler.button3_pressed}")

    state = {
        "button1": serial_handler.button1_pressed,
        "button2": serial_handler.button2_pressed,
        "button3": serial_handler.button3_pressed,
    }

    serial_handler.button1_pressed = False
    serial_handler.button2_pressed = False
    serial_handler.button3_pressed = False

    return jsonify(state)


if __name__ == '__main__':
    app.run(debug=True, port=4000, use_reloader=False)