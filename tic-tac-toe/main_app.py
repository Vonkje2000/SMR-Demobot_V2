from flask import Flask, render_template, redirect, url_for

main_app = Flask(__name__)

@main_app.route('/')
def welcome():
    return render_template('welcome.html')

@main_app.route('/app1')
def redirect_to_app1():
    return redirect('http://127.0.0.1:5001')  # Redirects to App 1 (running on port 5001)

@main_app.route('/app2')
def redirect_to_app2():
    return redirect('http://127.0.0.1:5002')  # Redirects to App 2 (running on port 5002)

if __name__ == '__main__':
    main_app.run(port=5000)  # The master app runs on port 5000
