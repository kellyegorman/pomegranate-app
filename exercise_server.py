from flask import Flask, send_file, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_file(os.path.join('front', 'exercise.html'))

@app.route('/exercise')
def exercise():
    return send_file(os.path.join('front', 'exercise.html'))

@app.route('/api/fitness/llm_recommend', methods=['POST'])
def llm_recommend():
    data = request.get_json() or {}
    customs = data.get('custom_exercises') or []
    # simple heuristic: echo customs then a couple of canned exercises
    exercises = []
    for c in customs:
        exercises.append({
            'name': c.get('name','Custom Exercise'),
            'description': c.get('targets',''),
            'prescription': {'freq_per_week':1, 'duration_min':20}
        })
    exercises.extend([
        {'name':'Brisk Walk','description':'Cardio, low impact','prescription':{'freq_per_week':3,'duration_min':30}},
        {'name':'Bodyweight Squats','description':'Lower body strength','prescription':{'freq_per_week':2,'duration_min':15}}
    ])
    return jsonify({'status':'success','recommendations':exercises})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
