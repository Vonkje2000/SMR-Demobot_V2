from flask import Flask, send_file, render_template, request, jsonify
import io

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('RPS.html')

@app.route('/get_image')
def get_image():
    # Replace this with your actual image generation logic
    img_path = 'static/images/detected_frame_1736431751.5998628.jpg'
    return send_file(img_path, mimetype='image/jpg')

@app.route('/start_signal', methods=['POST'])
def start_signal():
    data = request.get_json()
    print('Start signal received:', data)
    return jsonify({'status': 'success', 'message': 'Start signal received'})

if __name__ == '__main__':
    app.run(debug=True)