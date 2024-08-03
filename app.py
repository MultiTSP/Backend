from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

from tsp import tsp
from mtsp import mtsp

app = Flask(__name__)
CORS(app)

@app.route('/docs')
def hello_world():
    return 'Releasing soon!'

@app.route('/solve')
def solve():
    data = request.json
    coordinates = np.array(data['coordinates'])
    time = data['time']
    speed = data['speed']
    
    path = tsp(coordinates)

    answer = mtsp(path, time, speed)

    result = {
        'vehicles': answer[0],
        'paths': answer[1],
        'TSPpath': path
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)