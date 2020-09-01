from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/demo', methods=['GET', 'POST'])
def demo():
    if request.method=='GET':
        return render_template('demo.html')
    elif request.method=='POST':
        return render_template('demo.html')
    else:
        return 'illegal request encountered'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
