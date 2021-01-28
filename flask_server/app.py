from flask import Flask, render_template, request, redirect, url_for
import json
import os
import socket
graphs = None


def initialize():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    try:
        bss_file = open(os.path.join(script_dir, 'graphs.json'), 'r')
    except FileNotFoundError:
        from utility.process_bss import process_bss
        print("Cached graphs not found. Processing graphs. This could take a while")
        # This line is slow in debug... Don't run this line in debug lol

        process_bss(os.path.join(os.path.dirname(script_dir), 'Graph-Hashing/data/FULL_ALCHEMY/train/graphs.bss'), os.path.join(script_dir, 'graphs.json'))
        bss_file = open(os.path.join(script_dir, 'graphs.json'), 'r')
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
    query_result = backend_query(request.form.get('query', ''))
    query_result = query_result.decode("utf-8").split(';')
    query_result = [q for q in query_result if q]
    num_results = len(query_result)
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
            append_dict['graph'] = json.dumps(graphs[query_result[idx]])
        else:
            append_dict['dummy_div'] = True
        results_type_list.append(append_dict)
        append_dict['idx'] = idx
        idx += 1

    return render_template('demo.html', show_result=show_result, num_results=num_results,
                           results_type_list=results_type_list)


def backend_query(string):
    port_1 = 7000
    string = string.replace(';', '\n')
    s = socket.socket()
    host = socket.gethostname()
    s.connect((host, port_1))
    s.send(string.encode(encoding="utf-8"))
    s.send(bytes("done\n", 'utf-8'))
    ret = s.recv(102400)
    return ret

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
