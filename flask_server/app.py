from flask import Flask, render_template, request, redirect, url_for
import json

graphs = None


def initialize():
    try:
        bss_file = open('/project/flask_server/graphs.json', 'r')
    except FileNotFoundError:
        from utility.process_bss import process_bss
        print("Cached graphs not found. Processing graphs. This could take a while")
        # This line is slow in debug... Don't run this line in debug lol
        process_bss('/project/Graph-Hashing/data/FULL_ALCHEMY/train/graphs.bss', '/project/flask_server/graphs.json')
        bss_file = open('/project/flask_server/graphs.json', 'r')
    global graphs
    graphs = json.load(bss_file)
    bss_file.close()
initialize()
app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')


@app.route('/about_us')
def about_us():
    return render_template('about_us.html')


@app.route('/about_demo')
def about_demo():
    return render_template('about_demo.html')


@app.route('/demo')
def demo():
    show_result = False
    return render_template('demo.html', show_result=show_result)


@app.route('/query', methods=['POST'])
def query():
    show_result = True
    num_results = 13
    results_type_list = list()
    idx = 0
    while (idx < num_results) or (idx % 3 != 0):
        append_dict = dict()
        if 0 == idx % 3:
            append_dict['start_div'] = True
            append_dict['end_div'] = False
        elif 2 == idx % 3:
            append_dict['start_div'] = False
            append_dict['end_div'] = True
        else:
            pass
        if idx < num_results:
            append_dict['dummy_div'] = False
        else:
            append_dict['dummy_div'] = True
        results_type_list.append(append_dict)
        append_dict['idx'] = idx
        idx += 1

    return render_template('demo.html', show_result=show_result, num_results=num_results,
                           results_type_list=results_type_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
