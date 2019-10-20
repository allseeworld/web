from flask import Flask, jsonify,url_for

app1 = Flask(__name__)


@app1.route('/<name>/', methods=['POST'])
def index(name):
    return 'index' + name

@app1.route('/jsons/')
def jsons():
    dics = {}
    url =url_for()
    return jsonify(dics)



if __name__ == '__main__':
    app1.run(debug=True)
