from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/demo')
def demo():
    show_result = False
    return render_template('demo.html', show_result=show_result)


@app.route('/query', methods=['POST'])
def query():
    show_result = True
    return render_template('demo.html', show_result=show_result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
