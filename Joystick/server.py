from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('joystick.html')

@app.route('/joystick', methods=['POST'])
def joystick():
    data = request.json
    x = data.get('x')
    y = data.get('y')
    print(f"Received joystick data: x={x}, y={y}")
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)